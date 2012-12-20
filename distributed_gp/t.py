import csv

def read_csv(name):
    f = open(name,'r')
    reader = csv.reader(f, delimiter='\t')
    for row in reader:
        print row


read_csv('new_1h.csv')
