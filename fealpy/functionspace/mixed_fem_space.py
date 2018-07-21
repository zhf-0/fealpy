import numpy as np
from .function import FiniteElementFunction
from .lagrange_fem_space import LagrangeFiniteElementSpace

class HuZhangFiniteElementSpace():
    """
    Hu-Zhang Mixed Finite Element Space.
    """
    def __init__(self, mesh, p):
        self.space = LagrangeFiniteElementSpace(mesh, p) # the scalar space
        self.mesh = mesh
        self.p = p
        self.dof = self.space.dof
        self.dim = self.space.dim
        self.init_orth_matrices()
        self.init_cell_to_dof()

    def init_orth_matrices(self):
        """
        Initialize the othogonal symetric matrix basis.
        """
        mesh = self.mesh

        NE = mesh.number_of_edges()
        if self.dim == 2:
            idx = np.array([(0, 0), (0, 1), (1, 1)])
            self.T = np.array([[(1, 0), (0, 0)], [(0, 1), (1, 0)], [(0, 0), (0, 1)]])
            self.TE = np.zeros((NE, 3, 3), dtype=np.float)
        elif self.dim == 3:
            idx = np.array([(0, 0), (0, 1), (0, 2), (1, 1), (1, 2), (2, 2)])
            self.T = np.array([
                [(1, 0, 0), (0, 0, 0), (0, 0, 0)], 
                [(0, 1, 0), (1, 0, 0), (0, 0, 0)],
                [(0, 0, 1), (0, 0, 0), (1, 0, 0)],
                [(0, 0, 0), (0, 1, 0), (0, 0, 0)],
                [(0, 0, 0), (0, 0, 1), (0, 1, 0)],
                [(0, 0, 0), (0, 0, 0), (0, 0, 1)]])

            self.TE = np.zeros((NE, 6, 6), dtype=np.float)

        t = mesh.edge_unit_tagent() 
        _, _, frame = np.linalg.svd(t[:, np.newaxis, :]) # get the axis frame on the edge by svd
        frame[:, 0] = t
        for i, (j, k) in enumerate(idx):
            self.TE[:, i] = (frame[:, j, idx[:, 0]]*frame[:, k, idx[:, 1]] + frame[:, j, idx[:, 1]]*frame[:, k, idx[:, 0]])/2

        self.TE[:, 1] *= np.sqrt(2) # normalize

        if self.dim == 3:
            NF = mesh.number_of_faces()
            n = mesh.face_unit_normal()
            face2edge = mesh.ds.face_to_edge()
            ft = t[face2edge]
            self.TF = np.zeros((NF, 6, 6), dtype=np.float)
            self.TF[:, 0:3, :] = self.TE[face2edge, 0, :] # 
            self.TF[:, 3:, :] = np.sqrt(2)*(n[:, np.newaxis, idx[:, 0]]*ft[:, :, idx[:, 1]] + n[:, np.newaxis, idx[:, 1]]*ft[:, :, idx[:, 0]])/2

    def __str__(self):
        return "Hu-Zhang mixed finite element space!"

    def number_of_global_dofs(self):
        p = self.p
        dim = self.dim
        tdim = self.tensor_dimension() 

        mesh = self.mesh

        NC = mesh.number_of_cells()
        N = mesh.number_of_nodes()
        gdof = tdim*N
        if p > 1:
            edof = p - 1
            NE = mesh.number_of_edges()
            gdof += (tdim-1)*edof*NE 
            E = mesh.number_of_edges_of_cells()
            gdof += NC*E*edof

        if p > 2:
            fdof = (p+1)*(p+2)//2 - 3*p
            if dim == 2:
                gdof += tdim*fdof*NC
            elif dim == 3:
                NF = mesh.number_of_faces()
                gdof += 3*fdof*NF + 3*4*fdof*NC

        if (p > 3) and (dim == 3):
            ldof = self.dof.number_of_local_dofs()
            cdof = ldof - 6*edof - 4*fdof - 4
            gdof += tdim*cdof*NC
        return gdof 

    def number_of_local_dofs(self):
        tdim = self.tensor_dimension() 
        return tdim*self.dof.number_of_local_dofs()

    def cell_to_dof(self):
        return self.cell2dof

    def init_cell_to_dof(self):
        """
        构建局部自由度到全局自由度的映射矩阵

        Returns
        -------
        cell2dof : ndarray with shape (NC, ldof*tdim)
            NC: 单元个数
            ldof: p 次标量空间局部自由度的个数
            tdim: 对称张量的维数
        """
        mesh = self.mesh
        N = mesh.number_of_nodes()
        NE = mesh.number_of_edges()
        NC = mesh.number_of_cells()

        dim = self.geo_dimension()
        tdim = self.tensor_dimension()
        p = self.p
        dof = self.dof # 标量空间自由度对象 
       
        c2d = dof.cell2dof[..., np.newaxis]
        ldof = dof.number_of_local_dofs() 
        # ldof : 标量空间单元上自由度个数
        # tdim : 张量维数
        cell2dof = np.zeros((NC, ldof, tdim), dtype=np.int)

        dofFlags = self.dof_flags_1() # 把不同类型的自由度区分开来
        idx, = np.nonzero(dofFlags[0]) # 局部顶点自由度的编号
        cell2dof[:, idx, :] = tdim*c2d[:, idx] + np.arange(tdim)

        base0 = 0
        base1 = 0
        idx, = np.nonzero(dofFlags[1]) # 边内部自由度的编号
        if len(idx) > 0:
            base0 += N # 这是标量编号的新起点
            base1 += tdim*N # 这是张量自由度编号的新起点
            #  0号局部自由度对应的是切向不连续的自由度, 留到后面重新编号
            cell2dof[:, idx, 1:] = base1 + (tdim-1)*(c2d[:, idx] - base0) + np.arange(tdim - 1)

        idx, = np.nonzero(dofFlags[2])
        if len(idx) > 0:
            edof = p - 1
            base0 += edof*NE
            base1 += (tdim-1)*edof*NE
            if dim == 2:
                cell2dof[:, idx, :] = base1 + tdim*(c2d[:, idx] - base0) + np.arange(tdim)
            elif dim == 3:
                # 0, 1, 2号局部自由度对应切向不连续的张量自由度, 留到后面重新编号
                cell2dof[:, idx, 3:]= base1 + (tdim - 3)*(c2d[:, idx] - base0) + np.arange(tdim - 3)

        fdof = (p+1)*(p+2)//2 - 3*p
        if dim == 3:
            idx, = np.nonzero(dofFlags[3])
            if len(idx) > 0:
                NF = mesh.number_of_faces()
                base0 += fdof*NF 
                base1 += (tdim - 3)*fdof*NF
                cell2dof[:, idx, :] = base1 + tdim*(c2d[:, idx] - base0) + np.arange(tdim)
            cdof = ldof - 4*fdof - 6*edof - 4
        else:
            cdof = fdof

        idx, = np.nonzero(dofFlags[1])
        if len(idx) > 0:
            base1 += tdim*cdof*NC 
            cell2dof[:, idx, 0] = base1 + np.arange(NC*len(idx)).reshape(NC, len(idx)) 

        if dim == 3:
            base1 += NC*len(idx)
            idx, = np.nonzero(dofFlags[2])
            if len(idx) > 0:
                cell2dof[:, idx, 0:3] = base1 + np.arange(NC*len(idx)*3).reshape(NC, len(idx), 3)

        self.cell2dof = cell2dof.reshape(NC, -1)

    def geo_dimension(self):
        return self.dim

    def tensor_dimension(self):
        dim = self.dim
        return dim*(dim - 1)//2 + dim

    def interpolation_points(self):
        return self.dof.interpolation_points()

    def dof_flags(self):
        """ 对标量空间中的自由度进行分类, 分为边内部自由度, 面内部自由度(如果是三维空间的话)及其它自由度 

        Returns
        -------

        isOtherDof : ndarray, (ldof,)
            除了边内部和面内部自由度的其它自由度
        isEdgeDof : ndarray, (ldof, 3) or (ldof, 6) 
            每个边内部的自由度
        isFaceDof : ndarray, (ldof, 4)
            每个面内部的自由度
        -------

        """
        dim = self.geo_dimension()
        dof = self.dof 
        
        isPointDof = dof.is_on_node_local_dof()
        isEdgeDof = dof.is_on_edge_local_dof()
        isEdgeDof[isPointDof] = False
        
        isEdgeDof0 = np.sum(isEdgeDof, axis=-1) > 0 # 
        isOtherDof = (~isEdgeDof0) # 除了边内部自由度之外的其它自由度
                                   # dim = 2: 包括点和面内部自由度
                                   # dim = 3: 包括点, 面内部和体内部自由度
        if dim == 2:
            return isOtherDof, isEdgeDof
        elif dim == 3:
            isFaceDof = dof.is_on_face_local_dof()
            isFaceDof[isPointDof, :] = False
            isFaceDof[isEdgeDof0, :] = False

            isFaceDof0 = np.sum(isFaceDof, axis=-1) > 0
            isOtherDof = isOtherDof & (~isFaceDof0) # 三维情形下, 从其它自由度中除去面内部自由度

            return isOtherDof, isEdgeDof, isFaceDof
        else:
            raise ValueError('`dim` should be 2 or 3!')

    def dof_flags_1(self):
        """ 
        对标量空间中的自由度进行分类, 分为:
            点上的自由由度
            边内部的自由度
            面内部的自由度
            体内部的自由度

        Returns
        -------

        isOtherDof : ndarray, (ldof,)
            除了边内部和面内部自由度的其它自由度
        isEdgeDof : ndarray, (ldof, 3) or (ldof, 6) 
            每个边内部的自由度
        isFaceDof : ndarray, (ldof, 4)
            每个面内部的自由度
        -------

        """
        dim = self.dim # the geometry space dimension
        dof = self.dof 
        isPointDof = dof.is_on_node_local_dof()
        isEdgeDof = dof.is_on_edge_local_dof()
        isEdgeDof[isPointDof] = False
        isEdgeDof0 = np.sum(isEdgeDof, axis=-1) > 0
        if dim == 2:
            return isPointDof, isEdgeDof0, ~(isPointDof | isEdgeDof0)
        elif dim == 3:
            isFaceDof = dof.is_on_face_local_dof()
            isFaceDof[isPointDof, :] = False
            isFaceDof[isEdgeDof0, :] = False

            isFaceDof0 = np.sum(isFaceDof, axis=-1) > 0
            return isPointDof, isEdgeDof0, isFaceDof0, ~(isPointDof | isEdgeDof0 | isFaceDof0)
        else:
            raise ValueError('`dim` should be 2 or 3!')

    def basis(self, bc, cellidx=None):
        """

        Parameters
        ----------
        bc : ndarray with shape (NQ, dim+1)
            bc[i, :] is i-th quad point
        cellidx : ndarray
            有时我我们只需要计算部分单元上的基函数
        Returns
        -------
        phi : ndarray with shape (NQ, NC, ldof*tdim, 3 or 6)
            NQ: 积分点个数
            NC: 单元个数
            ldof: 标量空间的单元自由度个数
            tdim: 对称张量的维数

            (NQ, NC, ldof*tdim, dim, dim) 这样的存储有点浪费空间?
        """
        dim = self.geo_dimension() 
        tdim = self.tensor_dimension()

        mesh = self.mesh

        if cellidx is None:
            NC = mesh.number_of_cells()
            cell2edge = mesh.ds.cell_to_edge()
        else:
            NC = len(cellidx)
            cell2edge = mesh.ds.cell_to_edge()[cellidx]

        phi0 = self.space.basis(bc) # the shape of phi0 is (NQ, ldof)
        shape = list(phi0.shape)
        shape.insert(-1, NC)
        shape += [tdim, tdim]
        # The shape of `phi` is (NQ, NC, ldof, tdim, tdim), where
        #   NQ : the number of quadrature points 
        #   NC : the number of cells
        #   ldof : the number of dofs in each cell
        #   tdim : the dimension of symmetric tensor matrix
        phi = np.zeros(shape, dtype=np.float) 

        dofFlag = self.dof_flags()
        # the dof on the vertex and the interior of the cell
        isOtherDof = dofFlag[0]
        idx, = np.nonzero(isOtherDof)
        if len(idx) > 0:
            phi[..., idx[..., np.newaxis], range(tdim), range(tdim)] = phi0[..., np.newaxis, idx, np.newaxis]
  
        isEdgeDof = dofFlag[1]
        for i, isDof in enumerate(isEdgeDof.T):
            phi[..., isDof, :, :] = np.einsum('...j, imn->...ijmn', phi0[..., isDof], self.TE[cell2edge[:, i]]) 

        if dim == 3:
            if cellidx is None:
                cell2face = mesh.ds.cell_to_face()
            else:
                cell2face = mesh.ds.cell_to_face()[cellidx]
            isFaceDof = dofFlag[2]
            for i, isDof in enumerate(isFaceDof.T):
                phi[..., isDof, :, :] = np.einsum('...j, imn->...ijmn', phi0[..., isDof], self.TF[cell2face[:, i]])

        # The new shape of `phi` is `(NQ, NC, ldof*tdim, dim, dim)`, where
        #   dim : the geometry space dimension
        phi = np.einsum('...jk, kmn->...jmn', phi, self.T)
        shape = phi.shape[:-4] + (-1, dim, dim)
        return phi.reshape(shape) 

    def div_basis(self, bc, cellidx=None):
        dim = self.dim
        tdim = self.tensor_dimension() 
        mesh = self.mesh

        # the shape of `gphi` is (NQ, NC, ldof, dim)
        gphi = self.space.grad_basis(bc, cellidx=cellidx) 
        shape = list(gphi.shape)
        shape.insert(-1, tdim)
        # the shape of `dphi` is (NQ, NC, ldof, tdim, dim)
        dphi = np.zeros(shape, dtype=np.float)

        dofFlag = self.dof_flags()
        # the dof on the vertex and the interior of the cell
        isOtherDof = dofFlag[0]
        dphi[..., isOtherDof, :, :] = np.einsum('...ijm, kmn->...ijkn', gphi[..., isOtherDof, :], self.T)

        if cellidx is None:
            cell2edge = mesh.ds.cell_to_edge()
        else:
            cell2edge = mesh.ds.cell_to_edge()[cellidx]
        isEdgeDof = dofFlag[1]
        for i, isDof in enumerate(isEdgeDof.T):
            VAL = np.einsum('ijk, kmn->ijmn', self.TE[cell2edge[:, i]], self.T)
            dphi[..., isDof, :, :] = np.einsum('...ikm, ijmn->...ikjn', gphi[..., isDof, :], VAL) 

        if dim == 3:
            if cellidx is None:
                cell2face = mesh.ds.cell_to_face()
            else:
                cell2face = mesh.ds.cell_to_face()[cellidx]
            isFaceDof = dofFlag[2]
            for i, isDof in enumerate(isFaceDof.T):
                VAL = np.einsum('ijk, kmn->ijmn', self.TF[cell2face[:, i]], self.T)
                dphi[..., isDof, :, :] = np.einsum('...ikm, ijmn->...ikjn', gphi[..., isDof, :], VAL) 


        # The new shape of `dphi` is `(NQ, NC, ldof*tdim, dim)`, where
        shape = dphi.shape[:-3] + (-1, dim)
        return dphi.reshape(shape)

    def value(self, uh, bc, cellidx=None):
        phi = self.basis(bc, cellidx=cellidx)
        cell2dof = self.cell_to_dof()
        tdim = self.tensor_dimension()
        if cellidx is None:
            uh = uh[cell2dof]
        else:
            uh = uh[cell2dof[cellidx]]
        val = np.einsum('...ijmn, ij->...imn', phi, uh) 
        return val 

    def div_value(self, uh, bc, cellidx=None):
        dphi = self.div_basis(bc, cellidx=cellidx)
        cell2dof = self.cell_to_dof()
        tdim = self.tensor_dimension()
        if cellidx is None:
            uh = uh[cell2dof]
        else:
            uh = uh[cell2dof[cellidx]]
        val = np.einsum('...ijm, ij->...im', dphi, uh)
        return val

    def interpolation(self, u):

        mesh = self.mesh;
        dim = self.geo_dimension()
        tdim = self.tensor_dimension()

        if dim == 2:
            idx = np.array([(0, 0), (0, 1), (1, 1)])
        elif dim == 3:
            idx = np.array([(0, 0), (0, 1), (0, 2), (1, 1), (1, 2), (2, 2)])

        ipoint = self.dof.interpolation_points()
        c2d = self.dof.cell2dof
        val = u(ipoint)[c2d]

        ldof = self.dof.number_of_local_dofs()
        cell2dof = self.cell_to_dof().reshape(-1, ldof, tdim)

        uI = FiniteElementFunction(self)
        dofFlag = self.dof_flags()
        isOtherDof = dofFlag[0]
        idx0, = np.nonzero(isOtherDof)
        uI[cell2dof[:, idx0, :]] = val[:, idx0][..., idx[:, 0], idx[:, 1]]

        isEdgeDof = dofFlag[1]
        cell2edge = self.mesh.ds.cell_to_edge()
        for i, isDof in enumerate(isEdgeDof.T):
            TE = np.einsum('ijk, kmn->ijmn', self.TE[cell2edge[:, i]], self.T)
            uI[cell2dof[:, isDof, :]] = np.einsum('ikmn, ijmn->ikj', val[:, isDof, :, :], TE)

        if dim == 3:
            cell2face = mesh.ds.cell_to_face()
            isFaceDof = dofFlag[2]
            for i, isDof in enumerate(isFaceDof.T):
                TF = np.einsum('ijk, kmn->ijmn', self.TF[cell2face[:, i]], self.T)
                uI[cell2dof[:, isDof, :]] = np.einsum('ikmn, ijmn->ikj', val[..., isDof, :, :], TF) 
        return uI

    def function(self, dim=None):
        f = FiniteElementFunction(self)
        return f

    def array(self, dim=None):
        gdof = self.number_of_global_dofs()
        return np.zeros(gdof, dtype=np.float)


class RTFiniteElementSpace2d:
    def __init__(self, mesh, p=0):
        self.mesh = mesh
        self.p = p

    def cell_to_edge_sign(self):
        mesh = self.mesh
        NC = mesh.number_of_cells()
        edge2cell = mesh.ds.edge2cell
        cell2edgeSign = -np.ones((NC, 3), dtype=np.int)
        cell2edgeSign[edge2cell[:, 0], edge2cell[:, 2]] = 1
        return cell2edgeSign

    def basis(self, bc):
        mesh = self.mesh
        p = self.p
        ldof = self.number_of_local_dofs()
        NC = mesh.number_of_cells()
        Rlambda = mesh.rot_lambda()
        cell2edgeSign = self.cell_to_edge_sign()
        shape = bc.shape[:-1] + (NC, ldof, 2)
        phi = np.zeros(shape, dtype=np.float)
        if p == 0:
            phi[..., 0, :] = bc[..., 1, np.newaxis, np.newaxis]*Rlambda[:, 2, :] - bc[..., 2, np.newaxis, np.newaxis]*Rlambda[:, 1, :]
            phi[..., 1, :] = bc[..., 2, np.newaxis, np.newaxis]*Rlambda[:, 0, :] - bc[..., 0, np.newaxis, np.newaxis]*Rlambda[:, 2, :]
            phi[..., 2, :] = bc[..., 0, np.newaxis, np.newaxis]*Rlambda[:, 1, :] - bc[..., 1, np.newaxis, np.newaxis]*Rlambda[:, 0, :]
            phi *= cell2edgeSign.reshape(-1, 3, 1)
        else:
            raise ValueError('p')

        return phi

    def grad_basis(self, bc):
        mesh = self.mesh
        p = self.p

        ldof = self.number_of_local_dofs()
        NC = mesh.number_of_cells()
        shape = (NC, ldof, 2, 2)
        gradPhi = np.zeros(shape, dtype=np.float)

        cell2edgeSign = self.cell_to_edge_sign()
        W = np.array([[0, 1], [-1, 0]], dtype=np.float)
        Rlambda= mesh.rot_lambda()
        Dlambda = Rlambda@W
        if p == 0:
            A = np.einsum('...i, ...j->...ij', Rlambda[:, 2, :], Dlambda[:, 1, :])
            B = np.einsum('...i, ...j->...ij', Rlambda[:, 1, :], Dlambda[:, 2, :]) 
            gradPhi[:, 0, :, :] = A - B 

            A = np.einsum('...i, ...j->...ij', Rlambda[:, 0, :], Dlambda[:, 2, :])
            B = np.einsum('...i, ...j->...ij', Rlambda[:, 2, :], Dlambda[:, 0, :])
            gradPhi[:, 1, :, :] = A - B 

            A = np.einsum('...i, ...j->...ij', Rlambda[:, 1, :], Dlambda[:, 0, :])
            B = np.einsum('...i, ...j->...ij', Rlambda[:, 0, :], Dlambda[:, 1, :])
            gradPhi[:, 2, :, :] = A - B 

            gradPhi *= cell2edgeSign.reshape(-1, 3, 1, 1) 
        else:
            #TODO:raise a error
            print("error")

        return gradPhi 

    def div_basis(self, bc):
        mesh = self.mesh
        p = self.p

        ldof = self.number_of_local_dofs()
        NC = mesh.number_of_cells()
        divPhi = np.zeors((NC, ldof), dtype=np.float)
        cell2edgeSign = self.cell_to_edge_sign()
        W = np.array([[0, 1], [-1, 0]], dtype=np.float)

        Rlambda = mesh.rot_lambda()
        Dlambda = Rlambda@W
        if p == 1:
            divPhi[:, 0] = np.sum(Dlambda[:, 1, :]*Rlambda[:, 2, :], axis=1) - np.sum(Dlambda[:, 2, :]*Rlambda[:, 1, :], axis=1)
            divPhi[:, 1] = np.sum(Dlambda[:, 2, :]*Rlambda[:, 0, :], axis=1) - np.sum(Dlambda[:, 0, :]*Rlambda[:, 2, :], axis=1)
            divPhi[:, 2] = np.sum(Dlambda[:, 0, :]*Rlambda[:, 1, :], axis=1) - np.sum(Dlambda[:, 1, :]*Rlambda[:, 0, :], axis=1)
            divPhi *= cell2edgeSign
        else:
            #TODO:raise a error
            print("error")

        return divPhi 

    def cell_to_dof(self):
        p = self.p
        mesh = self.mesh
        cell = mesh.ds.cell

        N = mesh.number_of_nodes()
        NC = mesh.number_of_cells()

        ldof = self.number_of_local_dofs()
        if p == 0:
            cell2dof = mesh.ds.cell2edge
        else:
            #TODO: raise a error 
            print('error!')

        return cell2dof

    def number_of_global_dofs(self):
        p = self.p
        mesh = self.mesh
        NE = mesh.number_of_edges()
        if p == 0:
            return NE
        else:
            #TODO: raise a error
            print("error!")


    def number_of_local_dofs(self):
        p = self.p
        if p==0:
            return 3
        else:
            #TODO: raise a error
            print("error!")

class BDMFiniteElementSpace2d:
    def __init__(self, mesh, p=1, dtype=np.float):
        self.mesh = mesh
        self.p = p
        self.dtype= dtype

    def cell_to_edge_sign(self):
        mesh = self.mesh
        edge2cell = mesh.ds.edge2cell
        NC = mesh.number_of_cells()
        cell2edgeSign = -np.ones((NC, 3), dtype=np.int)
        cell2edgeSign[edge2cell[:, 0], edge2cell[:, 2]] = 1
        return cell2edgeSign

    def basis(self, bc):
        mesh = self.mesh
        dim = mesh.geom_dimension()

        ldof = self.number_of_local_dofs()

        NC = mesh.number_of_cells()
        p = self.p
        phi = np.zeros((NC, ldof, dim), dtype=self.dtype)

        cell2edgeSign = self.cell_to_edge_sign()
        Rlambda, _ = mesh.rot_lambda()
        if p == 1:
            phi[:, 0, :] = bc[1]*Rlambda[:, 2, :] - bc[2]*Rlambda[:, 1, :]
            phi[:, 1, :] = bc[1]*Rlambda[:, 2, :] + bc[2]*Rlambda[:, 1, :]

            phi[:, 2, :] = bc[2]*Rlambda[:, 0, :] - bc[0]*Rlambda[:, 2, :]
            phi[:, 3, :] = bc[2]*Rlambda[:, 0, :] + bc[0]*Rlambda[:, 2, :]

            phi[:, 4, :] = bc[0]*Rlambda[:, 1, :] - bc[1]*Rlambda[:, 0, :]
            phi[:, 5, :] = bc[0]*Rlambda[:, 1, :] + bc[1]*Rlambda[:, 0, :]

            phi[:, 0:6:2, :] *=cell2edgeSign.reshape(-1, 3, 1)
        else:
            #TODO:raise a error
            print("error")

        return phi

    def grad_basis(self, bc):
        mesh = self.mesh
        dim = mesh.geom_dimension()
        p = self.p

        gradPhi = np.zeros((NC, ldof, dim, dim), dtype=self.dtype)

        cell2edgeSign = self.cell_to_edge_sign()
        W = np.array([[0, 1], [-1, 0]], dtype=self.dtype)
        Rlambda, _ = mesh.rot_lambda()
        Dlambda = Rlambda@W
        if p == 1:
            A = np.einsum('...i, ...j->...ij', Rlambda[:, 2, :], Dlambda[:, 1, :])
            B = np.einsum('...i, ...j->...ij', Rlambda[:, 1, :], Dlambda[:, 2, :]) 
            gradPhi[:, 0, :, :] = A - B 
            gradPhi[:, 1, :, :] = A + B

            A = np.einsum('...i, ...j->...ij', Rlambda[:, 0, :], Dlambda[:, 2, :])
            B = np.einsum('...i, ...j->...ij', Rlambda[:, 2, :], Dlambda[:, 0, :])
            gradPhi[:, 2, :, :] = A - B
            gradPhi[:, 3, :, :] = A + B

            A = np.einsum('...i, ...j->...ij', Rlambda[:, 1, :], Dlambda[:, 0, :])
            B = np.einsum('...i, ...j->...ij', Rlambda[:, 0, :], Dlambda[:, 1, :])
            gradPhi[:, 4, :, :] = A - B
            gradPhi[:, 5, :, :] = A + B

            gradPhi[:, 0:6:2, :, :] *= cell2edgeSign.reshape(-1, 3, 1, 1) 
            gradPhi[:, 1:6:2, :, :] *= cell2edgeSign.reshape(-1, 3, 1, 1) 
        else:
            #TODO:raise a error
            print("error")

        return gradPhi 

    def div_basis(self, bc):
        mesh = self.mesh
        p = self.p

        divPhi = np.zeors((NC, ldof), dtype=self.dtype)

        Dlambda, _ = mesh.grad_lambda()
        Rlambda, _ = mesh.rot_lambda()
        if p == 1:
            divPhi[:, 0] = np.sum(Dlambda[:, 1, :]*Rlambda[:, 2, :] - Dlambda[:, 2, :]*Rlambda[:, 1, :], axia=1)
            divPhi[:, 1] = np.sum(Dlambda[:, 1, :]*Rlambda[:, 2, :] + Dlambda[:, 2, :]*Rlambda[:, 1, :], axia=1)
            divPhi[:, 2] = np.sum(Dlambda[:, 2, :]*Rlambda[:, 0, :] - Dlambda[:, 0, :]*Rlambda[:, 2, :], axis=1)
            divPhi[:, 3] = np.sum(Dlambda[:, 2, :]*Rlambda[:, 0, :] + Dlambda[:, 0, :]*Rlambda[:, 2, :], axis=1)
            divPhi[:, 4] = np.sum(Dlambda[:, 0, :]*Rlambda[:, 1, :] - Dlambda[:, 1, :]*Rlambda[:, 0, :], axis=1)
            divPhi[:, 5] = np.sum(Dlambda[:, 0, :]*Rlambda[:, 1, :] + Dlambda[:, 1, :]*Rlambda[:, 0, :], axis=1)
            divPhi[:, 0:6:2] *= cell2edgeSign
            divPhi[:, 1:6:2] *= cell2edgeSign
        else:
            #TODO:raise a error
            print("error")

        return divPhi 

    def edge_to_dof(self):
        p = self.p
        mesh = self.mesh

        NE = mesh.number_of_edges()

        if p == 1:
            edge2dof = np.arange(2*NE).reshape(NE, 2)
        else:
            #TODO: raise error
            print('error!')

        return edge2dof

    def cell_to_dof(self):
        p = self.p
        mesh = self.mesh
        cell = mesh.ds.cell

        N = mesh.number_of_nodes()
        NC = mesh.number_of_cells()

        ldof = self.number_of_local_dofs()
        edge2dof = self.edge_to_dof()

        cell2edgeSign = mesh.ds.cell_to_edge_sign()
        cell2edge = mesh.ds.cell_to_edge()

        if p == 1:
            cell2dof = np.zeros((NC, ldof), dtype=np.int)
            cell2dof[cell2edgeSign[:, 0], 0:2]= edge2dof[cell2edge[cell2edgeSign[:, 0], 0], :]  
            cell2dof[~cell2edgeSign[:, 0], 0:2]= edge2dof[cell2edge[~cell2edgeSign[:, 0], 0], -1::-1]  

            cell2dof[cell2edgeSign[:, 1], 2:4]= edge2dof[cell2edge[cell2edgeSign[:, 1], 1], :]  
            cell2dof[~cell2edgeSign[:, 1], 2:4]= edge2dof[cell2edge[~cell2edgeSign[:, 1], 1], -1::-1]  

            cell2dof[cell2edgeSign[:, 2], 4:6]= edge2dof[cell2edge[cell2edgeSign[:, 2], 2], :]  
            cell2dof[~cell2edgeSign[:, 2], 4:6]= edge2dof[cell2edge[~cell2edgeSign[:, 2], 2], -1::-1]  

        return cell2dof

    def number_of_global_dofs(self):
        p = self.p
        mesh = self.mesh
        NE = mesh.number_of_edges()
        if p == 1:
            return 2*NE
        else:
            #TODO: raise a error
            print("error!")

    def number_of_local_dofs(self):
        p = self.p
        if p == 1:
            return 6
        else:
            #TODO: raise a error
            print("error!")


class RaviartThomasFiniteElementSpace3d:
    def __init__(self, mesh, p=0, dtype=np.float):
        self.mesh = mesh
        self.p = p
        self.dtype= dtype

    def basis(self, bc):
        mesh = self.mesh
        dim = mesh.geom_dimension()

        ldof = self.number_of_local_dofs()

        p = self.p
        phi = np.zeors((NC, ldof, dim), dtype=self.dtype)


        return phi

    def grad_basis(self, bc):
        mesh = self.mesh
        dim = mesh.geom_dimension()
        p = self.p

        gradPhi = np.zeros((NC, ldof, dim, dim), dtype=self.dtype)

        return gradPhi 

    def div_basis(self, bc):
        mesh = self.mesh
        p = self.p

        divPhi = np.zeors((NC, ldof), dtype=self.dtype)

        return divPhi 

    def cell_to_dof(self):
        p = self.p
        mesh = self.mesh
        cell = mesh.ds.cell

        N = mesh.number_of_nodes()
        NC = mesh.number_of_cells()

        ldof = self.number_of_local_dofs()

        return cell2dof

    def number_of_global_dofs(self):
        p = self.p
        mesh = self.mesh
        NE = mesh.number_of_edges()
        if p == 0:
            return NE
        elif p==1:
            return 2*NE
        else:
            #TODO: raise a error
            print("error!")


    def number_of_local_dofs(self):
        p = self.p
        if p==0:
            return 3
        elif p==1:
            return 6
        else:
            #TODO: raise a error
            print("error!")


class FirstNedelecFiniteElement2d():
    def __init__(self, mesh, p=0, dtype=np.float):
        self.mesh=mesh
        self.p = p
        self.dtype=dtype
    
    def cell_to_edge_sign(self):
        mesh = self.mesh
        NC = mesh.number_of_cells()
        edge2cell = mesh.ds.edge2cell
        cell2edgeSign = -np.ones((NC, 3), dtype=np.int)
        cell2edgeSign[edge2cell[:, 0], edge2cell[:, 2]] = 1
        return cell2edgeSign

    def basis(self, bc):
        mesh = self.mesh
        NC = mesh.number_of_cells()
        dim = mesh.geom_dimension()
        p = self.p
        ldof = self.number_of_local_dofs()
        phi = np.zeros((NC, ldof, dim), dtype=self.dtype)
        Dlambda, _ = mesh.grad_lambda() 
        cell2edgeSign = self.cell_to_edge_sign()
        if p == 0:
            phi[:, 0, :] = bc[1]*Dlambda[:, 2, :] - bc[2]*Dlambda[:, 1, :]
            phi[:, 1, :] = bc[2]*Dlambda[:, 0, :] - bc[0]*Dlambda[:, 2, :]
            phi[:, 2, :] = bc[0]*Dlambda[:, 1, :] - bc[1]*Dlambda[:, 0, :]
            phi *= cell2edgeSign.reshape(-1, 3, 1)
        else:
            #TODO: raise a error
            print("error!")

        return phi

    def grad_basis(self, bc):
        mesh = self.mesh

        NC = mesh.number_of_cells()
        dim = mesh.geom_dimension()

        ldof = self.number_of_local_dofs()

        gradPhi = np.zeros((NC, ldof, dim, dim), dtype=self.dtype)

        cell2edgeSign = self.cell_to_edge_sign()
        Dlambda, _ = mesh.grad_lambda(bc)
        if p == 0:
            A = np.einsum('...i, ...j->...ij', Dlambda[:, 2, :], Dlambda[:, 1, :])
            B = np.einsum('...i, ...j->...ij', Dlambda[:, 1, :], Dlambda[:, 2, :]) 
            gradPhi[:, 0, :, :] = A - B 

            A = np.einsum('...i, ...j->...ij', Dlambda[:, 0, :], Dlambda[:, 2, :])
            B = np.einsum('...i, ...j->...ij', Dlambda[:, 2, :], Dlambda[:, 0, :])
            gradPhi[:, 1, :, :] = A - B 

            A = np.einsum('...i, ...j->...ij', Dlambda[:, 1, :], Dlambda[:, 0, :])
            B = np.einsum('...i, ...j->...ij', Dlambda[:, 0, :], Dlambda[:, 1, :])
            gradPhi[:, 2, :, :] = A - B 

            gradPhi *= cell2edgeSign.reshape(-1, 3, 1, 1) 
        else:
            #TODO:raise a error
            print("error")

        return gradPhi 

    def div_basis(self, bc):
        mesh = self.mesh
        p = self.p

        divPhi = np.zeors((NC, ldof), dtype=self.dtype)

        cell2edgeSign = self.cell_to_edge_sign()
        Dlambda, _ = mesh.grad_lambda()
        if p == 0:
            divPhi[:, 0] = np.sum(Dlambda[:, 1, :]*Dlambda[:, 2, :] - Dlambda[:, 2, :]*Dlambda[:, 1, :], axia=1)
            divPhi[:, 1] = np.sum(Dlambda[:, 2, :]*Dlambda[:, 0, :] - Dlambda[:, 0, :]*Dlambda[:, 2, :], axis=1)
            divPhi[:, 2] = np.sum(Dlambda[:, 0, :]*Dlambda[:, 1, :] - Dlambda[:, 1, :]*Dlambda[:, 0, :], axis=1)
            divPhi *= cell2edgeSign 
        else:
            #TODO:raise a error
            print("error")

        return divPhi 

    def dual_basis(self, u):
        pass

    def array(self):
        pass

    def value(self, uh, bc):
        pass

    def grad_value(self, uh, bc):
        pass

    def number_of_global_dofs(self):
        p = self.p
        mesh = self.mesh
        NE = mesh.number_of_edges()
        if p == 0:
            return NE
        else:
            #TODO: raise a error
            print("error!")

    def number_of_local_dofs(self):
        p = self.p
        if p==0:
            return 3
        else:
            #TODO: raise a error
            print("error!")

    def cell_to_dof(self):
        p = self.p
        mesh = self.mesh
        cell = mesh.ds.cell

        N = mesh.number_of_nodes()
        NC = mesh.number_of_cells()

        ldof = self.number_of_local_dofs()
        if p == 0:
            cell2dof = mesh.ds.cell2edge
        else:
            #TODO: raise a error 
            print('error!')

        return cell2dof

class SecondNedelecFiniteElementTwo2d():
    def __init__(self, mesh, p=1, dtype=np.float):
        self.mesh=mesh
        self.p = p
    
    def cell_to_edge_sign(self):
        mesh = self.mesh
        NC = mesh.number_of_cells()
        edge2cell = mesh.ds.edge2cell
        cell2edgeSign = -np.ones((NC, 3), dtype=np.int)
        cell2edgeSign[edge2cell[:, 0], edge2cell[:, 2]] = 1
        return cell2edgeSign

    def basis(self, bc):
        mesh = self.mesh
        NC = mesh.number_of_cells()
        dim = mesh.geom_dimentsion()
        p = self.p
        ldofs = mesh.number_of_local_dofs()
        phi = np.zeros((NC, ldofs, dim), dtype=self.dtype)
        Dlambda, _ = mesh.grad_lambda() 
        cell2edgeSign = self.cell_to_edge_sign()
        if p == 1:
            phi[:, 0, :] = bc[1]*Dlambda[:, 2, :] - bc[2]*Dlambda[:, 1, :]
            phi[:, 1, :] = bc[1]*Dlambda[:, 2, :] + bc[2]*Dlambda[:, 1, :]
            phi[:, 2, :] = bc[2]*Dlambda[:, 0, :] - bc[0]*Dlambda[:, 2, :]
            phi[:, 3, :] = bc[2]*Dlambda[:, 0, :] + bc[0]*Dlambda[:, 2, :]
            phi[:, 4, :] = bc[0]*Dlambda[:, 1, :] - bc[1]*Dlambda[:, 0, :]
            phi[:, 5, :] = bc[0]*Dlambda[:, 1, :] + bc[1]*Dlambda[:, 0, :]
            phi[:, 0:6:2] *=cell2edgeSign
            phi[:, 1:6:2] *=cell2edgeSign
        else:
            #TODO: raise a error
            print("error!")

        return phi

    def grad_basis(self, bc):
        mesh = self.mesh

        NC = mesh.number_of_cells()
        dim = mesh.geom_dimension()

        ldof = self.number_of_local_dofs()

        gradPhi = np.zeros((NC, ldof, dim, dim), dtype=self.dtype)

        cell2edgeSign = self.cell_to_edge_sign()
        Dlambda, _ = mesh.grad_lambda()
        if p == 1:
            A = np.einsum('...i, ...j->...ij', Dlambda[:, 2, :], Dlambda[:, 1, :])
            B = np.einsum('...i, ...j->...ij', Dlambda[:, 1, :], Dlambda[:, 2, :]) 
            gradPhi[:, 0, :, :] = A - B 
            gradPhi[:, 1, :, :] = A + B 

            A = np.einsum('...i, ...j->...ij', Dlambda[:, 0, :], Dlambda[:, 2, :])
            B = np.einsum('...i, ...j->...ij', Dlambda[:, 2, :], Dlambda[:, 0, :])
            gradPhi[:, 2, :, :] = A - B 
            gradPhi[:, 3, :, :] = A + B 

            A = np.einsum('...i, ...j->...ij', Dlambda[:, 1, :], Dlambda[:, 0, :])
            B = np.einsum('...i, ...j->...ij', Dlambda[:, 0, :], Dlambda[:, 1, :])
            gradPhi[:, 4, :, :] = A - B 
            gradPhi[:, 5, :, :] = A + B 

            gradPhi[:, 0:6:2, :, :] *= cell2edgeSign.reshape(-1, 3, 1, 1) 
            gradPhi[:, 1:6:2, :, :] *= cell2edgeSign.reshape(-1, 3, 1, 1) 

        else:
            #TODO:raise a error
            print("error")

        return gradPhi 

    def div_basis(self, bc):
        mesh = self.mesh
        p = self.p

        divPhi = np.zeors((NC, ldof), dtype=self.dtype)

        Dlambda, _ = mesh.grad_lambda()
        if p == 1:
            divPhi[:, 0] = np.sum(Dlambda[:, 1, :]*Dlambda[:, 2, :] - Dlambda[:, 2, :]*Dlambda[:, 1, :], axia=1)
            divPhi[:, 1] = np.sum(Dlambda[:, 1, :]*Dlambda[:, 2, :] + Dlambda[:, 2, :]*Dlambda[:, 1, :], axia=1)
            divPhi[:, 2] = np.sum(Dlambda[:, 2, :]*Dlambda[:, 0, :] - Dlambda[:, 0, :]*Dlambda[:, 2, :], axis=1)
            divPhi[:, 3] = np.sum(Dlambda[:, 2, :]*Dlambda[:, 0, :] + Dlambda[:, 0, :]*Dlambda[:, 2, :], axis=1)
            divPhi[:, 4] = np.sum(Dlambda[:, 0, :]*Dlambda[:, 1, :] - Dlambda[:, 1, :]*Dlambda[:, 0, :], axis=1)
            divPhi[:, 5] = np.sum(Dlambda[:, 0, :]*Dlambda[:, 1, :] + Dlambda[:, 1, :]*Dlambda[:, 0, :], axis=1)
            divPhi[:, 0:6:2] *=cell2edgeSign
            divPhi[:, 1:6:2] *=cell2edgeSign
        else:
            #TODO:raise a error
            print("error")

        return divPhi 

    def dual_basis(self, u):
        pass

    def array(self):
        pass

    def value(self, uh, bc):
        pass

    def grad_value(self, uh, bc):
        pass

    def number_of_global_dofs(self):
        p = self.p
        mesh = self.mesh
        NE = mesh.number_of_edges()
        if p == 1:
            return 2*NE
        else:
            #TODO: raise a error
            print("error!")

    def number_of_local_dofs(self):
        p = self.p
        if p==1:
            return 6
        else:
            #TODO: raise a error
            print("error!")

    def edge_to_dof(self):
        p = self.p
        mesh = self.mesh

        NE = mesh.number_of_edges()

        if p == 1:
            edge2dof = np.arange(2*NE).reshape(NE, 2)
        else:
            #TODO: raise error
            print('error!')

        return edge2dof

    def cell_to_dof(self):
        p = self.p
        mesh = self.mesh
        cell = mesh.ds.cell

        N = mesh.number_of_nodes()
        NC = mesh.number_of_cells()

        ldof = self.number_of_local_dofs()
        edge2dof = self.edge_to_dof()

        cell2edgeSign = mesh.ds.cell_to_edge_sign()
        cell2edge = mesh.ds.cell_to_edge()

        if p == 1:
            cell2dof = np.zeros((NC, ldof), dtype=np.int)

            cell2dof[cell2edgeSign[:, 0], 0:2]= edge2dof[cell2edge[cell2edgeSign[:, 0], 0], :]  
            cell2dof[~cell2edgeSign[:, 0], 0:2]= edge2dof[cell2edge[~cell2edgeSign[:, 0], 0], -1::-1]  

            cell2dof[cell2edgeSign[:, 1], 2:4]= edge2dof[cell2edge[cell2edgeSign[:, 1], 1], :]  
            cell2dof[~cell2edgeSign[:, 1], 2:4]= edge2dof[cell2edge[~cell2edgeSign[:, 1], 1], -1::-1]  

            cell2dof[cell2edgeSign[:, 2], 4:6]= edge2dof[cell2edge[cell2edgeSign[:, 2], 2], :]  
            cell2dof[~cell2edgeSign[:, 2], 4:6]= edge2dof[cell2edge[~cell2edgeSign[:, 2], 2], -1::-1]  

        return cell2dof
