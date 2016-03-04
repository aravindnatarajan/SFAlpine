import MySQLdb as sql
import numpy as np
import sys

thePass = ""  # Enter your pasword.       
con = sql.connect(host="localhost", user="root", passwd=thePass, db="businessLocationsSF")
cur = con.cursor()
cur.execute('Drop table if exists biz')
cur.execute('create table biz (id int, dbaName varchar(1000), city varchar(100), state char(2), zip int, bizStartDate date, locStartDate date, lat float, lon float)')

f = open("loc.csv"); line = f.readline()
g = open("zip"); line = g.readline()
l = g.read(1)

def check(s):
  if s == "": return False
  ctr = 0
  for c in s:
    if c == '.': ctr += 1
    if c.lower() in 'abcdefghijklmnopqrstuvwxyz': return False
  if ctr > 1: return False
  return True
  
def latLon(g):

  s = ""
  l = g.read(1)
  while l <> '"':
    if l == "\n": l = " "
    if l <> "," and l <> "(" and l <> ")":
      s += l
    l = g.read(1)
  l = g.read(1)
  while l <> '"': l = g.read(1)
  if len(s) < 2: return 0.,0.
  m = s.split(" ")
  if check(m[-2]) and check(m[-1]):
    return float(m[-2]), float(m[-1])
  return 0.,0.    
  
ctr = 0
st = 0
for lp in range(0,100000):

  line = [val.rstrip() for val in f.readline().split(",")]  
  if line == ['']: continue

  dbaName = line[0]
  city = line[1] 
  state = line[2] 
  if state <> "CA": continue
  zip = int(line[3]) 
  bizStartDate = line[4][6:10]+"-"+line[4][0:2]+"-"+line[4][3:5]
  locStartDate = line[5][6:10]+"-"+line[5][0:2]+"-"+line[5][3:5]  

  lat,lon = latLon(g)  
  if lp >= st:
    cur.execute('insert into biz values (%d,%s,%s,%s,%d,%s,%s,%f,%f)'%(lp+1,'"'+dbaName+'"','"'+city+'"','"'+state+'"',zip,'"'+bizStartDate+'"','"'+locStartDate+'"',lat,lon))     

f.close()
con.commit()
con.close()
