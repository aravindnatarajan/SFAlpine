from minepy import MINE
import random as rd
import MySQLdb as sql
import matplotlib.pyplot as plt
import numpy as np
import sys
from scipy.stats import pearsonr

features = ["popDens", "col", "house", "inc"]
desc = { "popDens": "Pop. Density",
         "col": "Cost of living index",
         "house": "Cost of house",
         "inc": "Annual income" 
       }  
thePass = ""  # Enter your pasword.       
con = sql.connect(host="localhost", user="root", passwd=thePass, db="businessLocationsSF")
cur = con.cursor()

def getData(feature):
  comd = 'select Q1.C/Q0.A, Q2.A from ' \
  + '(select sf.zip Z, count(distinct sf.name) C from sf group by sf.zip) Q1 ' \
  + 'join (select distinct sf.zip Z, sf.area A from sf) Q0 on Q1.Z = Q0.Z '\
  + 'join (select distinct sf.zip Z, sf.' 
  comd += feature 
  comd += ' A from sf) Q2 on Q1.Z = Q2.Z order by Q1.C' 

  cur.execute(comd)
  allData = cur.fetchall()
  numBiz = []; X = []
  for i in range(0,len(allData)):
    numBiz.append(allData[i][0]) 
    X.append(allData[i][1])   

  return X,numBiz
  
ct = 1  
for feature in features:
  X,Y = getData(feature)
  sc = []
  for lp in range(0,1000):
    randomData = [rd.randint(int(np.min(Y)), int(np.max(Y))) for i in X]
    sc.append(pearsonr(randomData,X)[0])
  
  print feature, pearsonr(Y,X)[0], np.mean(sc)  
  plt.figure(ct)
  plt.xlabel(feature)
  plt.ylabel ("Number of Businesses / square mile")
  plt.xlabel(desc[feature])
  plt.scatter(X,Y)
  ct += 1
plt.show()  

con.close()
