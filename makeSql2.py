import MySQLdb as sql
import numpy as np
import sys

thePass = ""  # Enter your pasword.       
con = sql.connect(host="localhost", user="root", passwd=thePass, db="businessLocationsSF")
cur = con.cursor()
cur.execute('Drop table if exists details')
cur.execute('create table details (id int, zip int, population int, col float, popDens float, house int, income int, unemp float, area float)')

f = open("citydata")
for lp in range(0,26):
  zip = int(f.readline())
  line = f.readline()
  pop = int(f.readline())
  col = float(f.readline())
  popDens = float(f.readline())
  house = int(f.readline())  
  income = int(f.readline())  
  unemp = float(f.readline())  
  area = float(f.readline())    
  f.readline()

  cur.execute('insert into details values (%d,%d,%d,%f,%f,%d,%d,%f,%f)'%(lp+1,zip,pop,col,popDens,house,income,unemp,area))
f.close()

con.commit()
con.close()
