#!/usr/bin/python
# coding:utf8

from analysishelper.accessData import accessData
from stockhelper.getstockcode import ReadQuotes
import pdb
import numpy as np
import random


class treeNode:
    def __init__(self, nameValue, numOccur, parentNode):
        self.name = nameValue
        self.count = numOccur
        self.nodeLink = None
        # needs to be updated
        self.parent = parentNode
        self.children = {}

    def inc(self, numOccur):
        self.count += numOccur

    def disp(self, ind=1):
        print('  '*ind, self.name, ' ', self.count)
        for child in self.children.values():
            child.disp(ind+1)

class FPGrowth():

    def __init__(self):
        self.all_quotes = ReadQuotes()
        self.all_data  = None
        self.search_index_name, self.search_index_quote = None, None
        self.accessData = accessData()

    def loadData(self, samples=200, windowsize=48, windowrange=48, threshold=0.1, max_try=100000):
        if self.all_data is None:
            all_data = []
            new_quotes = []
            
            for quote in self.all_quotes:
                temp_data = self.accessData.getdata(quote['Symbol'])
                if temp_data.size != 0 and temp_data.size > 1020: 
                    all_data.append(np.reshape(temp_data, (1, -1)))
                    new_quotes.append(quote)


            self.all_data = np.concatenate(all_data)
            self.all_quotes = new_quotes
            self.search_index_name, self.search_index_quote = self.build_index()

        sampDat = []
        shapes = self.all_data.shape
        # pdb.set_trace()
        sample_try_times = 0
        while samples > 0:
            sample_try_times += 1
            windowsize_t = int(windowsize + windowrange * random.random())
            start_t = int(random.random() * (shapes[0] - windowsize_t))
            data_t = (self.all_data[:, start_t+windowsize_t] -
                      self.all_data[:, start_t]) / self.all_data[:, start_t+windowsize_t]
            indexs = np.argsort(-data_t)
            count = 0
            for index_t in indexs:
                if data_t[index_t] < threshold:
                    break
                count += 1

            a_recard = []
            for i in range(count):
                a_recard.append(self.getQuoteUsingIndex(indexs[i]))
            
            if len(a_recard)>2:
                sampDat.append(a_recard)
                samples -= 1

            if sample_try_times > max_try:
                break

        # pdb.set_trace()
        ########################## for testing.
        # sampDat = [['r', 'z', 'h', 'j', 'p'],
        #         ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
        #         ['z'],
        #         ['r', 'x', 'n', 'o', 's'],
        #         #    ['r', 'x', 'n', 'o', 's'],
        #         ['y', 'r', 'x', 'z', 'q', 't', 'p'],
        #         ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]
        return sampDat

    def createInitSet(self, dataSet):
        retDict = {}
        for trans in dataSet:
            if frozenset(trans) not in retDict:
                retDict[frozenset(trans)] = 1
            else:
                retDict[frozenset(trans)] += 1
        return retDict


    def updateHeader(self, nodeToTest, targetNode):
        while (nodeToTest.nodeLink is not None):
            nodeToTest = nodeToTest.nodeLink
        nodeToTest.nodeLink = targetNode


    def updateTree(self, items, inTree, headerTable, count):

        if items[0] in inTree.children:
            inTree.children[items[0]].inc(count)
        else:
            inTree.children[items[0]] = treeNode(items[0], count, inTree)
            if headerTable[items[0]][1] is None:
                headerTable[items[0]][1] = inTree.children[items[0]]
            else:
                self.updateHeader(headerTable[items[0]][1], inTree.children[items[0]])
        if len(items) > 1:
            self.updateTree(items[1:], inTree.children[items[0]], headerTable, count)

    def createTree(self, dataSet, minSup=3):
        headerTable = {}
        for trans in dataSet:
            for item in trans:
                headerTable[item] = headerTable.get(item, 0) + dataSet[trans]

        # keys_ = headerTable.keys()
        for k in list(headerTable):
            if headerTable[k] < minSup:
                del(headerTable[k])

        freqItemSet = set(headerTable.keys())
        if len(freqItemSet) == 0:
            return None, None
        for k in headerTable:
            headerTable[k] = [headerTable[k], None]

        # create tree
        retTree = treeNode('Null Set', 1, None)
        for tranSet, count in dataSet.items():
            # print 'tranSet, count=', tranSet, count
            localD = {}
            for item in tranSet:
                if item in freqItemSet:
                    # print 'headerTable[item][0]=', headerTable[item][0], headerTable[item]
                    localD[item] = headerTable[item][0]
            # print 'localD=', localD
            if len(localD) > 0:
                orderedItems = [v[0] for v in sorted(
                    localD.items(), key=lambda p: p[1], reverse=True)]
                self.updateTree(orderedItems, retTree, headerTable, count)

        return retTree, headerTable


    def ascendTree(self, leafNode, prefixPath):
        if leafNode.parent is not None:
            prefixPath.append(leafNode.name)
            self.ascendTree(leafNode.parent, prefixPath)

    def findPrefixPath(self, basePat, treeNode):
        condPats = {}

        while treeNode is not None:
            prefixPath = []

            self.ascendTree(treeNode, prefixPath)

            if len(prefixPath) > 1:
                condPats[frozenset(prefixPath[1:])] = treeNode.count
            treeNode = treeNode.nodeLink
            # print treeNode
        return condPats

    def mineTree(self, inTree, headerTable, minSup, preFix, freqItemList):
        bigL = [v[0] for v in sorted(headerTable.items(), key=lambda p: p[1][0])]
        # print('-----', sorted(headerTable.items(), key=lambda p: p[1][0]))
        # print('bigL=', bigL)
        for basePat in bigL:
            newFreqSet = preFix.copy()
            newFreqSet.add(basePat)
            # print('newFreqSet=', newFreqSet, preFix)

            freqItemList.append(newFreqSet)
            # print('freqItemList=', freqItemList)
            condPattBases = self.findPrefixPath(basePat, headerTable[basePat][1])
            # print('condPattBases=', basePat, condPattBases)
            myCondTree, myHead = self.createTree(condPattBases, minSup)
            # print('myHead=', myHead)
            if myHead is not None:
                myCondTree.disp(1)
                # print('\n\n\n')
                self.mineTree(myCondTree, myHead, minSup, newFreqSet, freqItemList)
            # print('\n\n\n')


    
    
    
    
    
    
    
    
    # helper functions
    def build_index(self):
        count = 0
        name_index = {}
        quote_index = {}
        name_quote = {}
        for quote in self.all_quotes:
            name_index[quote['Name']] = count
            quote_index[quote['Symbol']] = count
            count += 1

        return name_index, quote_index

    def getIndexUsingName(self, name):

        return self.search_index_name[name] if name in self.search_index_name else -1

    def getIndexUsingQuote(self, Companycode):

        return self.search_index_quote[Companycode] if Companycode in self.search_index_quote else -1

    def getNameUsingIndex(self, index):

        return self.all_quotes[index]['Name']

    def getQuoteUsingIndex(self, index):

        return self.all_quotes[index]['Symbol']

    def getQuoteUsingName(self, name):

        return self.getQuoteUsingIndex(self.getIndexUsingName(name))
