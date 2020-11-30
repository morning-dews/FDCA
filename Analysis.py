from analysishelper.pearsonrAnalysis import pearsonH
import numpy as np
from analysishelper.FP_Growth import FPGrowth


###################################
# For the analysis of using Pearson Correlation Coefficient.

pearsonHelper = pearsonH()
res, p_value = pearsonHelper.PearsonDelay()
# res, p_value = pearsonHelper.PearsonSimple()
ranking = np.argsort(-res)

# pdb.set_trace()

index = pearsonHelper.getIndexUsingName('浦发银行')
rankForTarget = ranking[index, :]


def showTopN(result, n=100):
    for i in range(n):
        print(pearsonHelper.getNameUsingIndex(
            result[i]), res[index][result[i]])


showTopN(rankForTarget)

#######################################
# For the analysis of using Frequent Pattern Mining


fpGrowth = FPGrowth()

simpDat = fpGrowth.loadData()
initSet = fpGrowth.createInitSet(simpDat)
print(initSet)

myFPtree, myHeaderTab = fpGrowth.createTree(initSet, 3)
myFPtree.disp()

freqItemList = []
fpGrowth.mineTree(myFPtree, myHeaderTab, 5, set([]), freqItemList)


def showTopN(n=1000):
    print('Mined frequent patterns:')
    for items in freqItemList:
        outresults = ''
        for company in items:
            outresults += fpGrowth.getNameUsingIndex(
                fpGrowth.getIndexUsingQuote(company)) + ', '
        print(outresults[:-2])
        n -= 1
        if n < 0:
            break


showTopN()
