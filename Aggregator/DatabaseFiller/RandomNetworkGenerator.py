'''
Created on Nov 20, 2013

@author: Hanwen Xu
'''
import csv, pickle, random

HedgeFunds = []
Brokers = []
Banks = []
Insurers = []
numberOfNames = 25
files = ['banks.csv', 'brokers.csv', 'hedgeFunds.csv', 'insurers.csv']

#p is the probability of a linkage occuring
def generateRandomNetwork(p):
    returnDict = {}
    allComps = []
    for f in files:
        pkl_file = open(f+'.pkl', 'rb')
        data1 = pickle.load(pkl_file)
        key = f.split('.')[0]
        returnDict[key] = []
        for comp in data1[:numberOfNames]:
            returnDict[key].append((comp, key))
            allComps.append((comp, key))
    returnDict['links'] = []
    for index, comp_tuple in enumerate(allComps):
        for index2, comp_tuple2 in enumerate(allComps[index:]):
            if random.random()<p:
                if random.random()<.5:
                    returnDict['links'].append((comp_tuple[0], comp_tuple2[0], comp_tuple[1])) 
                else:
                    returnDict['links'].append((comp_tuple2[0], comp_tuple[0], comp_tuple2[1])) 
    return returnDict


def createPickles():
    for f in files:
        with open(f, 'rb') as csvfile:
            filereader = csv.reader(csvfile)
            list1 = []
            for row in filereader:
                list1.append(row[0])
            output = open(f+'.pkl', 'wb')
            pickle.dump(list1, output)

def main():
    returnDict = generateRandomNetwork(0.05)
    print returnDict

if __name__ == '__main__':
    main()