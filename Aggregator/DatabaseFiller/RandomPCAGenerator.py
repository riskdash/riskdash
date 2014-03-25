'''
Created on Nov 26, 2013

@author: Hanwen Xu
'''

import csv, pickle, random

def getRandomPCList():
    randomList = []
    remaining = 1
    for i in xrange(3):
        nextNum = remaining*random.random()
        randomList.append(nextNum)
        remaining = remaining - nextNum
    randomList.append(remaining)
    return randomList

def getRandomEigenvectorList():
    randomList = []
    for i in xrange(4):
        randomList.append((2*random.random()-1))
    return randomList

def getRandomEigenValueDict():
    randomDict = {}
    sectors = ["All sectors", "Hedge-fund sectors"]
    timeframes = ["1994 to 2000", "2001 to 2008", "2009 to 2013"]
    for s in sectors:
        randomDict[s] = {}
        for t in timeframes:
            randomDict[s][t] = getRandomPCList()
    
    return randomDict

def getRandomEigenVectorDict():
    randomDict = {}
    timeframes = ["1994 to 2000", "2001 to 2008", "2009 to 2013"]
    sectors = ["Hedge Funds", "Brokers", "Banks", "Insurers"]
    h_sectors = ["Global Macro", "Long/Short Equity", "Illiquid HFunds", "Liquid HFunds"]
    for t in timeframes:
        randomDict[t] = {}
        for s in sectors:
            randomDict[t][s] = getRandomEigenvectorList()
        for h in h_sectors:
            randomDict[t][h] = getRandomEigenvectorList()
    return randomDict

def getRandomPCA():
    randomDict = {}
    randomDict["Eigenvalues"] = getRandomEigenValueDict()
    randomDict["Eigenvectors"] = getRandomEigenVectorDict()
    
    return randomDict

def main():
    output = getRandomPCA()
    print output

if __name__ == '__main__':
    main()