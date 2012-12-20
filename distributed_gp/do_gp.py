import time
import csv
import sys
import os
from subprocess import call

path = '/grad/users/kx19/CityBeat/distributed_gp/tmp/'

def LoadFromCSV(fileName):
    reader = csv.reader(open(fileName))
    buffer = []
    for t, mu, sigma in reader:
        buffer.append([t, mu, sigma])
    return buffer

def SaveToCSV(fileName, data):
    writer = csv.writer(file(fileName, 'w'));
    for item in data:
        writer.writerow(item)


def Predict(arg1, arg2, arg3):
    trainingDataFile = path + 'trainingData' + str(arg3) + '.in'
    SaveToCSV(trainingDataFile, arg1)

    testDataFile = path + 'testData' + str(arg3) + '.in'
    fout = open(testDataFile, 'w')
    for t in arg2:
        fout.write(str(t)+'\n')
    fout.close()

    outputFile = path + 'prediction' + str(arg3) + '.out'

    os.chdir('/grad/users/kx19/CityBeat/distributed_gp')

    shellComm = "matlab -r \'my_gp2 %s %s %s %s\'" %(trainingDataFile, testDataFile, outputFile, str(arg3))
    call([shellComm], shell=True)
    buffer = LoadFromCSV(outputFile) 
    print buffer
    return buffer

def TestPredict():
    fileName = '/grad/users/kx19/CityBeat/distributed_gp/new_1h.csv'
    reader = csv.reader(open(fileName), delimiter='\t')
    buffer = []
    for t, pop in reader:
        buffer.append([t, pop])

    trainingData = buffer
    testData = []
    cur = 14
    for i in range(100):
        cur+=0.04166666
        testData.append(cur,)

    Predict(trainingData, testData, -1)
    
    



def main():
    TestPredict()


if __name__ == "__main__":
    main()

"""
sw_ne = (40.75953,-73.9863145)
periods = []
cur_time = int (time.time())
pre = cur_time
jobs = []
client = client = InstagramAPI(client_id =config.instagram_client_id, client_secret = config.instagram_client_secret)
while pre>=cur_time-10*3600:
    do_func( (40,30,(pre-60*3,pre),client))
    pre = pre-3*60
    #periods.append( (pre-3*60, pre) )
"""
