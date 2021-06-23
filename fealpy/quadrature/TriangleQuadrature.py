import numpy as np
from .Quadrature import Quadrature

'''

Reference
--------
 [0] David Dunavant. High degree efficient symmetrical Gaussian
    quadrature rules for the triangle. International journal for numerical
    methods in engineering. 21(6):1129--1148, 1985.
 [1] John Burkardt. DUNAVANT Quadrature Rules for the Triangle.
    https://people.sc.fsu.edu/~jburkardt/cpp_src/triangle_dunavant_rule/triangle_dunavant_rule.html 
'''


class TriangleQuadrature(Quadrature):

    def __init__(self, index):
        if index==1: #  Order 1, nQuad 1
            A = np.array([
                [0.3333333333333330,	0.3333333333333330, 0.3333333333333330,	1.0000000000000000]], dtype=np.float64)
        if index==2: #  Order 2, nQuad 3
            A = np.array([
                [0.6666666666666670,	0.1666666666666670,     0.1666666666666670,	0.3333333333333330],
                [0.1666666666666670,	0.6666666666666670,     0.1666666666666670,	0.3333333333333330],
                [0.1666666666666670,	0.1666666666666670,     0.6666666666666670,	0.3333333333333330]],dtype=np.float64)
        if index==3:    # Order 4, nQuad 6
            A = np.array([
                [0.8168475729804400,	0.0915762135097800,	0.0915762135097800,	0.1099517436553330],
                [0.0915762135097800,	0.8168475729804400,	0.0915762135097800,	0.1099517436553330],
                [0.0915762135097800,	0.0915762135097800,	0.8168475729804400,	0.1099517436553330],
                [0.4459484909159640,	0.4459484909159640,	0.1081030181680710,	0.2233815896780000],
                [0.4459484909159640,	0.1081030181680710,	0.4459484909159640,	0.2233815896780000],
                [0.1081030181680710,	0.4459484909159640,	0.4459484909159640,	0.2233815896780000]],dtype=np.float64)
        if index==4:    # Order 5, nQuad 10
            A = np.array([
                [0.8888718946604130,	0.0555640526697930,	0.0555640526697930,	0.0419555129966490],
                [0.0555640526697930,	0.8888718946604130,	0.0555640526697930,	0.0419555129966490],
                [0.0555640526697930,	0.0555640526697930,	0.8888718946604130,	0.0419555129966490],
                [0.2955337117358930,	0.6342107477457230,	0.0702555405183840,	0.1120984120708870],
                [0.2955337117358930,	0.0702555405183840,	0.6342107477457230,	0.1120984120708870],
                [0.0702555405183840,	0.2955337117358930,	0.6342107477457230,	0.1120984120708870],
                [0.6342107477457230,	0.2955337117358930,	0.0702555405183840,	0.1120984120708870],
                [0.6342107477457230,	0.0702555405183840,	0.2955337117358930,	0.1120984120708870],
                [0.0702555405183840,	0.6342107477457230,	0.2955337117358930,	0.1120984120708870],
                [0.3333333333333330,	0.3333333333333330,	0.3333333333333330,	0.2015429885847300]],dtype=np.float64)
        if index==5:    # Order 7, nQuad 15
            A = np.array([
                [0.9282582446085330,	0.0358708776957340,	0.0358708776957340,	0.0179154550123030],
                [0.0358708776957340,	0.9282582446085330,	0.0358708776957340,	0.0179154550123030],
                [0.0358708776957340,	0.0358708776957340,	0.9282582446085330,	0.0179154550123030],
                [0.5165412084640660,	0.2417293957679670,	0.2417293957679670,	0.1277121958812650],
                [0.2417293957679670,	0.5165412084640660,	0.2417293957679670,	0.1277121958812650],
                [0.2417293957679670,	0.2417293957679670,	0.5165412084640660,	0.1277121958812650],
                [0.4743087877770790,	0.4743087877770790,	0.0513824244458430,	0.0762060623855350],
                [0.4743087877770790,	0.0513824244458430,	0.4743087877770790,	0.0762060623855350],
                [0.0513824244458430,	0.4743087877770790,	0.4743087877770790,	0.0762060623855350],
                [0.2015038818818000,	0.7511836311064840,	0.0473124870117160,	0.0557498100271150],
                [0.2015038818818000,	0.0473124870117160,	0.7511836311064840,	0.0557498100271150],
                [0.0473124870117160,	0.2015038818818000,	0.7511836311064840,	0.0557498100271150],
                [0.7511836311064840,	0.2015038818818000,	0.0473124870117160,	0.0557498100271150],
                [0.7511836311064840,	0.0473124870117160,	0.2015038818818000,	0.0557498100271150],
                [0.0473124870117160,	0.7511836311064840,	0.2015038818818000,	0.0557498100271150]],dtype=np.float64)
        if index==6:   # Order 8, nQuad 21
            A = np.array([
                [0.9437740956346720,	0.0281129521826640,	0.0281129521826640,	0.0103593746965380],
                [0.0281129521826640,	0.9437740956346720,	0.0281129521826640,	0.0103593746965380],
                [0.0281129521826640,	0.0281129521826640,	0.9437740956346720,	0.0103593746965380],
                [0.6457218030613650,	0.1771390984693170,	0.1771390984693170,	0.0753948843267380],
                [0.1771390984693170,	0.6457218030613650,	0.1771390984693170,	0.0753948843267380],
                [0.1771390984693170,	0.1771390984693170,	0.6457218030613650,	0.0753948843267380],
                [0.4055085958674330,	0.4055085958674330,	0.1889828082651340,	0.0975478023732420],
                [0.4055085958674330,	0.1889828082651340,	0.4055085958674330,	0.0975478023732420],
                [0.1889828082651340,	0.4055085958674330,	0.4055085958674330,	0.0975478023732420],
                [0.1485658122708870,	0.8179009800284990,	0.0335332077006140,	0.0289692693724730],
                [0.1485658122708870,	0.0335332077006140,	0.8179009800284990,	0.0289692693724730],
                [0.0335332077006140,	0.1485658122708870,	0.8179009800284990,	0.0289692693724730],
                [0.8179009800284990,	0.1485658122708870,	0.0335332077006140,	0.0289692693724730],
                [0.8179009800284990,	0.0335332077006140,	0.1485658122708870,	0.0289692693724730],
                [0.0335332077006140,	0.8179009800284990,	0.1485658122708870,	0.0289692693724730],
                [0.3571962986156810,	0.6049789117751320,	0.0378247896091860,	0.0460463665959350],
                [0.3571962986156810,	0.0378247896091860,	0.6049789117751320,	0.0460463665959350],
                [0.0378247896091860,	0.3571962986156810,	0.6049789117751320,	0.0460463665959350],
                [0.6049789117751320,	0.3571962986156810,	0.0378247896091860,	0.0460463665959350],
                [0.6049789117751320,	0.0378247896091860,	0.3571962986156810,	0.0460463665959350],
                [0.0378247896091860,	0.6049789117751320,	0.3571962986156810,	0.0460463665959350]],dtype=np.float64)
        if index==7:    # Order 10, nQuad 28
            A = np.array([
                [0.9600456257556130,	0.0199771871221930,	0.0199771871221930,	0.0052721702804950],
                [0.0199771871221930,	0.9600456257556130,	0.0199771871221930,	0.0052721702804950],
                [0.0199771871221930,	0.0199771871221930,	0.9600456257556130,	0.0052721702804950],
                [0.7365564649400050,	0.1317217675299980,	0.1317217675299980,	0.0445529366795040],
                [0.1317217675299980,	0.7365564649400050,	0.1317217675299980,	0.0445529366795040],
                [0.1317217675299980,	0.1317217675299980,	0.7365564649400050,	0.0445529366795040],
                [0.3333333333333330,	0.3333333333333330,	0.3333333333333330,	0.0836082122156370],
                [0.4851353467934610,	0.4851353467934610,	0.0297293064130790,	0.0338157128041980],
                [0.4851353467934610,	0.0297293064130790,	0.4851353467934610,	0.0338157128041980],
                [0.0297293064130790,	0.4851353467934610,	0.4851353467934610,	0.0338157128041980],
                [0.1079519818460110,	0.8679112101179510,	0.0241368080360390,	0.0157104613401830],
                [0.1079519818460110,	0.0241368080360390,	0.8679112101179510,	0.0157104613401830],
                [0.0241368080360390,	0.1079519818460110,	0.8679112101179510,	0.0157104613401830],
                [0.8679112101179510,	0.1079519818460110,	0.0241368080360390,	0.0157104613401830],
                [0.8679112101179510,	0.0241368080360390,	0.1079519818460110,	0.0157104613401830],
                [0.0241368080360390,	0.8679112101179510,	0.1079519818460110,	0.0157104613401830],
                [0.2708407729215670,	0.7008725703807230,	0.0282866566977100,	0.0282051362806160],
                [0.2708407729215670,	0.0282866566977100,	0.7008725703807230,	0.0282051362806160],
                [0.0282866566977100,	0.2708407729215670,	0.7008725703807230,	0.0282051362806160],
                [0.7008725703807230,	0.2708407729215670,	0.0282866566977100,	0.0282051362806160],
                [0.7008725703807230,	0.0282866566977100,	0.2708407729215670,	0.0282051362806160],
                [0.0282866566977100,	0.7008725703807230,	0.2708407729215670,	0.0282051362806160],
                [0.3165495988446170,	0.5366546842061380,	0.1467957169492450,	0.0669959571278300],
                [0.3165495988446170,	0.1467957169492450,	0.5366546842061380,	0.0669959571278300],
                [0.1467957169492450,	0.3165495988446170,	0.5366546842061380,	0.0669959571278300],
                [0.5366546842061380,	0.3165495988446170,	0.1467957169492450,	0.0669959571278300],
                [0.5366546842061380,	0.1467957169492450,	0.3165495988446170,	0.0669959571278300],
                [0.1467957169492450,	0.5366546842061380,	0.3165495988446170,	0.0669959571278300]],dtype=np.float64)
        if index==8:    # Order 12, nQuad 36
            A = np.array([
                [0.9576571544410700,	0.0211714227794650,	0.0211714227794650,	0.0056391237869100],
                [0.0211714227794650,	0.9576571544410700,	0.0211714227794650,	0.0056391237869100],
                [0.0211714227794650,	0.0211714227794650,	0.9576571544410700,	0.0056391237869100],
                [0.7988312052082250,	0.1005843973958880,	0.1005843973958880,	0.0271489681922780],
                [0.1005843973958880,	0.7988312052082250,	0.1005843973958880,	0.0271489681922780],
                [0.1005843973958880,	0.1005843973958880,	0.7988312052082250,	0.0271489681922780],
                [0.4579233845761350,	0.2710383077119320,	0.2710383077119320,	0.0631009125333590],
                [0.2710383077119320,	0.4579233845761350,	0.2710383077119320,	0.0631009125333590],
                [0.2710383077119320,	0.2710383077119320,	0.4579233845761350,	0.0631009125333590],
                [0.4401912584038320,	0.4401912584038320,	0.1196174831923350,	0.0517527956798990],
                [0.4401912584038320,	0.1196174831923350,	0.4401912584038320,	0.0517527956798990],
                [0.1196174831923350,	0.4401912584038320,	0.4401912584038320,	0.0517527956798990],
                [0.1017636794980210,	0.8799796414272320,	0.0182566790747480,	0.0098667535746460],
                [0.1017636794980210,	0.0182566790747480,	0.8799796414272320,	0.0098667535746460],
                [0.0182566790747480,	0.1017636794980210,	0.8799796414272320,	0.0098667535746460],
                [0.8799796414272320,	0.1017636794980210,	0.0182566790747480,	0.0098667535746460],
                [0.8799796414272320,	0.0182566790747480,	0.1017636794980210,	0.0098667535746460],
                [0.0182566790747480,	0.8799796414272320,	0.1017636794980210,	0.0098667535746460],
                [0.3940332716699870,	0.5825620228636730,	0.0234047054663410,	0.0220082048001470],
                [0.3940332716699870,	0.0234047054663410,	0.5825620228636730,	0.0220082048001470],
                [0.0234047054663410,	0.3940332716699870,	0.5825620228636730,	0.0220082048001470],
                [0.5825620228636730,	0.3940332716699870,	0.0234047054663410,	0.0220082048001470],
                [0.5825620228636730,	0.0234047054663410,	0.3940332716699870,	0.0220082048001470],
                [0.0234047054663410,	0.5825620228636730,	0.3940332716699870,	0.0220082048001470],
                [0.2262455309092290,	0.7515306145427820,	0.0222238545479890,	0.0166445700767360],
                [0.2262455309092290,	0.0222238545479890,	0.7515306145427820,	0.0166445700767360],
                [0.0222238545479890,	0.2262455309092290,	0.7515306145427820,	0.0166445700767360],
                [0.7515306145427820,	0.2262455309092290,	0.0222238545479890,	0.0166445700767360],
                [0.7515306145427820,	0.0222238545479890,	0.2262455309092290,	0.0166445700767360],
                [0.0222238545479890,	0.7515306145427820,	0.2262455309092290,	0.0166445700767360],
                [0.6357371832631050,	0.2490792276213320,	0.1151835891155630,	0.0443262381189140],
                [0.6357371832631050,	0.1151835891155630,	0.2490792276213320,	0.0443262381189140],
                [0.1151835891155630,	0.6357371832631050,	0.2490792276213320,	0.0443262381189140],
                [0.2490792276213320,	0.6357371832631050,	0.1151835891155630,	0.0443262381189140],
                [0.2490792276213320,	0.1151835891155630,	0.6357371832631050,	0.0443262381189140],
                [0.1151835891155630,	0.2490792276213320,	0.6357371832631050,	0.0443262381189140]],dtype=np.float64)
        if index==9:    # Order 14, nQuad 45
            A = np.array([
                [0.8432847880024730,	0.0783576059987630,	0.0783576059987630,	0.0170244686950010],
                [0.0783576059987630,	0.8432847880024730,	0.0783576059987630,	0.0170244686950010],
                [0.0783576059987630,	0.0783576059987630,	0.8432847880024730,	0.0170244686950010],
                [0.5593718137145640,	0.2203140931427180,	0.2203140931427180,	0.0454846169853150],
                [0.2203140931427180,	0.5593718137145640,	0.2203140931427180,	0.0454846169853150],
                [0.2203140931427180,	0.2203140931427180,	0.5593718137145640,	0.0454846169853150],
                [0.4903209480069000,	0.4903209480069000,	0.0193581039861990,	0.0167775837271790],
                [0.4903209480069000,	0.0193581039861990,	0.4903209480069000,	0.0167775837271790],
                [0.0193581039861990,	0.4903209480069000,	0.4903209480069000,	0.0167775837271790],
                [0.1979187896795100,	0.7107264142780870,	0.0913547960424030,	0.0291545050288770],
                [0.1979187896795100,	0.0913547960424030,	0.7107264142780870,	0.0291545050288770],
                [0.0913547960424030,	0.1979187896795100,	0.7107264142780870,	0.0291545050288770],
                [0.7107264142780870,	0.1979187896795100,	0.0913547960424030,	0.0291545050288770],
                [0.7107264142780870,	0.0913547960424030,	0.1979187896795100,	0.0291545050288770],
                [0.0913547960424030,	0.7107264142780870,	0.1979187896795100,	0.0291545050288770],
                [0.5423737147303060,	0.3604000118938390,	0.0972262733758550,	0.0379387031836240],
                [0.5423737147303060,	0.0972262733758550,	0.3604000118938390,	0.0379387031836240],
                [0.0972262733758550,	0.5423737147303060,	0.3604000118938390,	0.0379387031836240],
                [0.3604000118938390,	0.5423737147303060,	0.0972262733758550,	0.0379387031836240],
                [0.3604000118938390,	0.0972262733758550,	0.5423737147303060,	0.0379387031836240],
                [0.0972262733758550,	0.3604000118938390,	0.5423737147303060,	0.0379387031836240],
                [0.9641169869984210,	0.0179415065007890,	0.0179415065007890,	0.0041397399518450],
                [0.0179415065007890,	0.9641169869984210,	0.0179415065007890,	0.0041397399518450],
                [0.0179415065007890,	0.0179415065007890,	0.9641169869984210,	0.0041397399518450],
                [0.8969507339866380,	0.0891330987168490,	0.0139161672965130,	0.0066483251099210],
                [0.8969507339866380,	0.0139161672965130,	0.0891330987168490,	0.0066483251099210],
                [0.0139161672965130,	0.8969507339866380,	0.0891330987168490,	0.0066483251099210],
                [0.0891330987168490,	0.8969507339866380,	0.0139161672965130,	0.0066483251099210],
                [0.0891330987168490,	0.0139161672965130,	0.8969507339866380,	0.0066483251099210],
                [0.0139161672965130,	0.0891330987168490,	0.8969507339866380,	0.0066483251099210],
                [0.7904220176991940,	0.1915732379366730,	0.0180047443641330,	0.0106023811444580],
                [0.7904220176991940,	0.0180047443641330,	0.1915732379366730,	0.0106023811444580],
                [0.0180047443641330,	0.7904220176991940,	0.1915732379366730,	0.0106023811444580],
                [0.1915732379366730,	0.7904220176991940,	0.0180047443641330,	0.0106023811444580],
                [0.1915732379366730,	0.0180047443641330,	0.7904220176991940,	0.0106023811444580],
                [0.0180047443641330,	0.1915732379366730,	0.7904220176991940,	0.0106023811444580],
                [0.3260660021570210,	0.6554638123711750,	0.0184701854718040,	0.0144736005720320],
                [0.3260660021570210,	0.0184701854718040,	0.6554638123711750,	0.0144736005720320],
                [0.0184701854718040,	0.3260660021570210,	0.6554638123711750,	0.0144736005720320],
                [0.6554638123711750,	0.3260660021570210,	0.0184701854718040,	0.0144736005720320],
                [0.6554638123711750,	0.0184701854718040,	0.3260660021570210,	0.0144736005720320],
                [0.0184701854718040,	0.6554638123711750,	0.3260660021570210,	0.0144736005720320],
                [0.3861357471597970,	0.3861357471597970,	0.2277285056804050,	0.0522718938961680],
                [0.3861357471597970,	0.2277285056804050,	0.3861357471597970,	0.0522718938961680],
                [0.2277285056804050,	0.3861357471597970,	0.3861357471597970,	0.0522718938961680]],dtype=np.float64)
        if index==10:    # Order 15, nQuad 55
            A = np.array([
                [0.9782848624800070,	0.0108575687599970,	0.0108575687599970,	0.0016443746829210],
                [0.0108575687599970,	0.9782848624800070,	0.0108575687599970,	0.0016443746829210],
                [0.0108575687599970,	0.0108575687599970,	0.9782848624800070,	0.0016443746829210],
                [0.6475993410313730,	0.1762003294843140,	0.1762003294843140,	0.0329741136750500],
                [0.1762003294843140,	0.6475993410313730,	0.1762003294843140,	0.0329741136750500],
                [0.1762003294843140,	0.1762003294843140,	0.6475993410313730,	0.0329741136750500],
                [0.3333333333333330,	0.3333333333333330,	0.3333333333333330,	0.0462793692013860],
                [0.4591252183630440,	0.4591252183630440,	0.0817495632739120,	0.0307214412075590],
                [0.4591252183630440,	0.0817495632739120,	0.4591252183630440,	0.0307214412075590],
                [0.0817495632739120,	0.4591252183630440,	0.4591252183630440,	0.0307214412075590],
                [0.1402751751725660,	0.8478082343726400,	0.0119165904547930,	0.0060736157246010],
                [0.1402751751725660,	0.0119165904547930,	0.8478082343726400,	0.0060736157246010],
                [0.0119165904547930,	0.1402751751725660,	0.8478082343726400,	0.0060736157246010],
                [0.8478082343726400,	0.1402751751725660,	0.0119165904547930,	0.0060736157246010],
                [0.8478082343726400,	0.0119165904547930,	0.1402751751725660,	0.0060736157246010],
                [0.0119165904547930,	0.8478082343726400,	0.1402751751725660,	0.0060736157246010],
                [0.5750628073382710,	0.4091513784133800,	0.0157858142483480,	0.0131778559273610],
                [0.5750628073382710,	0.0157858142483480,	0.4091513784133800,	0.0131778559273610],
                [0.0157858142483480,	0.5750628073382710,	0.4091513784133800,	0.0131778559273610],
                [0.4091513784133800,	0.5750628073382710,	0.0157858142483480,	0.0131778559273610],
                [0.4091513784133800,	0.0157858142483480,	0.5750628073382710,	0.0131778559273610],
                [0.0157858142483480,	0.4091513784133800,	0.5750628073382710,	0.0131778559273610],
                [0.3226499110340910,	0.4871899771893600,	0.1901601117765490,	0.0413117267870520],
                [0.3226499110340910,	0.1901601117765490,	0.4871899771893600,	0.0413117267870520],
                [0.1901601117765490,	0.3226499110340910,	0.4871899771893600,	0.0413117267870520],
                [0.4871899771893600,	0.3226499110340910,	0.1901601117765490,	0.0413117267870520],
                [0.4871899771893600,	0.1901601117765490,	0.3226499110340910,	0.0413117267870520],
                [0.1901601117765490,	0.4871899771893600,	0.3226499110340910,	0.0413117267870520],
                [0.8753539911159670,	0.0623230044420170,	0.0623230044420170,	0.0093613196952160],
                [0.0623230044420170,	0.8753539911159670,	0.0623230044420170,	0.0093613196952160],
                [0.0623230044420170,	0.0623230044420170,	0.8753539911159670,	0.0093613196952160],
                [0.0596135298212760,	0.9275506802245300,	0.0128357899541940,	0.0042323301961180],
                [0.0596135298212760,	0.0128357899541940,	0.9275506802245300,	0.0042323301961180],
                [0.0128357899541940,	0.0596135298212760,	0.9275506802245300,	0.0042323301961180],
                [0.9275506802245300,	0.0596135298212760,	0.0128357899541940,	0.0042323301961180],
                [0.9275506802245300,	0.0128357899541940,	0.0596135298212760,	0.0042323301961180],
                [0.0128357899541940,	0.9275506802245300,	0.0596135298212760,	0.0042323301961180],
                [0.1548062393089040,	0.7763250741788570,	0.0688686865122380,	0.0190280598248270],
                [0.1548062393089040,	0.0688686865122380,	0.7763250741788570,	0.0190280598248270],
                [0.0688686865122380,	0.1548062393089040,	0.7763250741788570,	0.0190280598248270],
                [0.7763250741788570,	0.1548062393089040,	0.0688686865122380,	0.0190280598248270],
                [0.7763250741788570,	0.0688686865122380,	0.1548062393089040,	0.0190280598248270],
                [0.0688686865122380,	0.7763250741788570,	0.1548062393089040,	0.0190280598248270],
                [0.2571195044413040,	0.7281313801727500,	0.0147491153859460,	0.0103422623815450],
                [0.2571195044413040,	0.0147491153859460,	0.7281313801727500,	0.0103422623815450],
                [0.0147491153859460,	0.2571195044413040,	0.7281313801727500,	0.0103422623815450],
                [0.7281313801727500,	0.2571195044413040,	0.0147491153859460,	0.0103422623815450],
                [0.7281313801727500,	0.0147491153859460,	0.2571195044413040,	0.0103422623815450],
                [0.0147491153859460,	0.7281313801727500,	0.2571195044413040,	0.0103422623815450],
                [0.2936042253352780,	0.6275861631583690,	0.0788096115063520,	0.0274369629945590],
                [0.2936042253352780,	0.0788096115063520,	0.6275861631583690,	0.0274369629945590],
                [0.0788096115063520,	0.2936042253352780,	0.6275861631583690,	0.0274369629945590],
                [0.6275861631583690,	0.2936042253352780,	0.0788096115063520,	0.0274369629945590],
                [0.6275861631583690,	0.0788096115063520,	0.2936042253352780,	0.0274369629945590],
                [0.0788096115063520,	0.6275861631583690,	0.2936042253352780,	0.0274369629945590]],dtype=np.float64)
        if index==11:    # Order 17, nQuad 66
            A = np.array([
                [0.9199985374942970,	0.0400007312528510,	0.0400007312528510,	0.0076322380362940],
                [0.0400007312528510,	0.9199985374942970,	0.0400007312528510,	0.0076322380362940],
                [0.0400007312528510,	0.0400007312528510,	0.9199985374942970,	0.0076322380362940],
                [0.4262322842578010,	0.2868838578710990,	0.2868838578710990,	0.0364039862105000],
                [0.2868838578710990,	0.4262322842578010,	0.2868838578710990,	0.0364039862105000],
                [0.2868838578710990,	0.2868838578710990,	0.4262322842578010,	0.0364039862105000],
                [0.6949699285698890,	0.1525150357150550,	0.1525150357150550,	0.0233729265849060],
                [0.1525150357150550,	0.6949699285698890,	0.1525150357150550,	0.0233729265849060],
                [0.1525150357150550,	0.1525150357150550,	0.6949699285698890,	0.0233729265849060],
                [0.4175584765068650,	0.4175584765068650,	0.1648830469862690,	0.0325568221840790],
                [0.4175584765068650,	0.1648830469862690,	0.4175584765068650,	0.0325568221840790],
                [0.1648830469862690,	0.4175584765068650,	0.4175584765068650,	0.0325568221840790],
                [0.2465680217430370,	0.6859089091274810,	0.0675230691294830,	0.0199561722332810],
                [0.2465680217430370,	0.0675230691294830,	0.6859089091274810,	0.0199561722332810],
                [0.0675230691294830,	0.2465680217430370,	0.6859089091274810,	0.0199561722332810],
                [0.6859089091274810,	0.2465680217430370,	0.0675230691294830,	0.0199561722332810],
                [0.6859089091274810,	0.0675230691294830,	0.2465680217430370,	0.0199561722332810],
                [0.0675230691294830,	0.6859089091274810,	0.2465680217430370,	0.0199561722332810],
                [0.1270436681177950,	0.8124192506753400,	0.0605370812068640,	0.0143851520041560],
                [0.1270436681177950,	0.0605370812068640,	0.8124192506753400,	0.0143851520041560],
                [0.0605370812068640,	0.1270436681177950,	0.8124192506753400,	0.0143851520041560],
                [0.8124192506753400,	0.1270436681177950,	0.0605370812068640,	0.0143851520041560],
                [0.8124192506753400,	0.0605370812068640,	0.1270436681177950,	0.0143851520041560],
                [0.0605370812068640,	0.8124192506753400,	0.1270436681177950,	0.0143851520041560],
                [0.5411059289874540,	0.3892670914810180,	0.0696269795315280,	0.0230840030555830],
                [0.5411059289874540,	0.0696269795315280,	0.3892670914810180,	0.0230840030555830],
                [0.0696269795315280,	0.5411059289874540,	0.3892670914810180,	0.0230840030555830],
                [0.3892670914810180,	0.5411059289874540,	0.0696269795315280,	0.0230840030555830],
                [0.3892670914810180,	0.0696269795315280,	0.5411059289874540,	0.0230840030555830],
                [0.0696269795315280,	0.3892670914810180,	0.5411059289874540,	0.0230840030555830],
                [0.2755334401141860,	0.5622286042191000,	0.1622379556667140,	0.0299380898366860],
                [0.2755334401141860,	0.1622379556667140,	0.5622286042191000,	0.0299380898366860],
                [0.1622379556667140,	0.2755334401141860,	0.5622286042191000,	0.0299380898366860],
                [0.5622286042191000,	0.2755334401141860,	0.1622379556667140,	0.0299380898366860],
                [0.5622286042191000,	0.1622379556667140,	0.2755334401141860,	0.0299380898366860],
                [0.1622379556667140,	0.5622286042191000,	0.2755334401141860,	0.0299380898366860],
                [0.9888333333925860,	0.0055833333037070,	0.0055833333037070,	0.0000115761572660],
                [0.0055833333037070,	0.9888333333925860,	0.0055833333037070,	0.0000115761572660],
                [0.0055833333037070,	0.0055833333037070,	0.9888333333925860,	0.0000115761572660],
                [0.0268111896653240,	0.9723655557903410,	0.0008232545443350,	0.0012222309529510],
                [0.0268111896653240,	0.0008232545443350,	0.9723655557903410,	0.0012222309529510],
                [0.0008232545443350,	0.0268111896653240,	0.9723655557903410,	0.0012222309529510],
                [0.9723655557903410,	0.0268111896653240,	0.0008232545443350,	0.0012222309529510],
                [0.9723655557903410,	0.0008232545443350,	0.0268111896653240,	0.0012222309529510],
                [0.0008232545443350,	0.9723655557903410,	0.0268111896653240,	0.0012222309529510],
                [0.1049890791452260,	0.8843260287552040,	0.0106848920995700,	0.0052604599448600],
                [0.1049890791452260,	0.0106848920995700,	0.8843260287552040,	0.0052604599448600],
                [0.0106848920995700,	0.1049890791452260,	0.8843260287552040,	0.0052604599448600],
                [0.8843260287552040,	0.1049890791452260,	0.0106848920995700,	0.0052604599448600],
                [0.8843260287552040,	0.0106848920995700,	0.1049890791452260,	0.0052604599448600],
                [0.0106848920995700,	0.8843260287552040,	0.1049890791452260,	0.0052604599448600],
                [0.2149147783171840,	0.7722800338219470,	0.0128051878608680,	0.0080642341957690],
                [0.2149147783171840,	0.0128051878608680,	0.7722800338219470,	0.0080642341957690],
                [0.0128051878608680,	0.2149147783171840,	0.7722800338219470,	0.0080642341957690],
                [0.7722800338219470,	0.2149147783171840,	0.0128051878608680,	0.0080642341957690],
                [0.7722800338219470,	0.0128051878608680,	0.2149147783171840,	0.0080642341957690],
                [0.0128051878608680,	0.7722800338219470,	0.2149147783171840,	0.0080642341957690],
                [0.3478948459761320,	0.6387048607161610,	0.0134002933077070,	0.0096615327623360],
                [0.3478948459761320,	0.0134002933077070,	0.6387048607161610,	0.0096615327623360],
                [0.0134002933077070,	0.3478948459761320,	0.6387048607161610,	0.0096615327623360],
                [0.6387048607161610,	0.3478948459761320,	0.0134002933077070,	0.0096615327623360],
                [0.6387048607161610,	0.0134002933077070,	0.3478948459761320,	0.0096615327623360],
                [0.0134002933077070,	0.6387048607161610,	0.3478948459761320,	0.0096615327623360],
                [0.4932203038571030,	0.4932203038571030,	0.0135593922857950,	0.0102120341890470],
                [0.4932203038571030,	0.0135593922857950,	0.4932203038571030,	0.0102120341890470],
                [0.0135593922857950,	0.4932203038571030,	0.4932203038571030,	0.0102120341890470]], dtype=np.float64)
	
        self.quadpts = A[:, 0:3]
        self.weights = A[:, 3]
