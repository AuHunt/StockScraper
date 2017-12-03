import libxml2
import sys
import os
import commands
import re
import sys

import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb

from xml.dom.minidom import parse, parseString

# for converting dict to xml 
from cStringIO import StringIO
from xml.parsers import expat

def get_elms_for_atr_val(tag,atr,val):
   lst=[]
   elms = dom.getElementsByTagName(tag)
   # ............
   '''
   # check the length of the nodes in the 100 most actives
   x = 0
   y = 0
   for n in elms:
      if len(n.childNodes) > 0:
         print(len(n.childNodes))
         x += 1
         if len(n.childNodes) == 6:
            y += 1
   print(x)
   print(y)
   '''
   fElems = filter(lambda elems: len(elems.childNodes) == 6, elms) #return those elements that have 6 or more nodes (members of the list we want)
   fElems.pop(0) #This removes that first element that holds the header of the table like the title volume change etc.
   lst = fElems
   #print(lst)
   return lst

def get_text(e):
   lst=[]
   # ............
   if e.nodeType not in (3,4): #Bootleg-recursion
      for i in e.childNodes:
         lst += get_text(i)
   else:
      #print(e.data)
      lst.append(e.data)

   #print(lst)
   return lst

# replace whitespace chars
def replace_white_space(str):
   p = re.compile(r'\s+')
   new = p.sub(' ',str)   # a lot of \n\t\t\t\t\t\t
   return new.strip()

def replace_non_alpha_numeric(s):
   p = re.compile(r'[^a-zA-Z0-9:-]+')
   #   p = re.compile(r'\W+') # replace whitespace chars
   new = p.sub(' ',s)
   return new.strip()

# converts to xhtml
def html_to_xml(fn):
   # ............
   os.system('java -jar /usr/share/java/tagsoup.jar --files ' + fn)
   xhtml_file = fn.replace('html', 'xhtml')   
   return xhtml_file

def extract_values(dm):
   lst = []
   l = get_elms_for_atr_val('tr','class','most_actives')
   # ............
   #    get_text(e)
   # ............
   '''
   # FAILSAFE IF LAMBDA DONT WORK
   for e in l:
      txt = get_text(e)
      print(txt) #See the elements and what they store from 1-100
      lst.append(txt)
   '''
   
   lst = map(lambda e: get_text(e), l) #get_text every thing in l

   for elem in lst:
      num = 0
      for x in elem:
         #print(x) # By now, it should only show the values
         if x == '\n': #removes \n values from the elements of the lst
            elem.pop(num)
         num+=1
      elem[1] = elem[1][:-1] #removes a tedious \n value at the end of the company name
      #elem[1] = elem[1].replace("(","")
      #elem[1] = elem[1].replace(" ","")
      #elem[1] = elem[1].replace(")","")
      elem[2] = elem[2].replace(",","") #remove the commas
      elem[3] = elem[3].replace("$","") #remove random dollar symbol

   '''
   # THIS IS TO PRINT HOW THE DATA LOOKS IN THE LIST   
   print('------')
   for elem in lst:
      num = 0
      for x in elem:
         print(str(num) + " : " + x) # By now, it should only show the value
         num += 1
      print('------')
   '''
   #print(lst)
   return lst

def insert_to_db(l,tbl):
   # ............
   # host = localhost, user = test, pass = Test123+, database = hw9
   database = MySQLdb.connect(host="localhost", user="test", passwd="Test123+", db = "hw9")
   sql = database.cursor()
   tCreate = 'CREATE TABLE IF NOT EXISTS ' + tbl + ' (ListNum int primary key, Company varchar(50), Volume int, Price float, Chng float, pChng float)'
   sql.execute(tCreate)
   for elem in l:
      #print(elem[1])
      tInsert = ('INSERT INTO ' + tbl + ' (ListNum, Company, Volume, Price, Chng, pChng) VALUES (%s, %s, %s, %s, %s, %s)')
      sql.execute(tInsert,elem)
      database.commit()
   return sql

# show databases;
# show tables;
def main():
   html_fn = sys.argv[1]
   fn = html_fn.replace('.html','')
   xhtml_fn = html_to_xml(html_fn)

   global dom
   print('Parsing ' + fn + '...')
   dom = parse(xhtml_fn)
   
   #print(dom)
   print('Extracting data from ' + fn + '...')
   lst = extract_values(dom)
   # make sure your mysql server is up and running
   print('Inserting data into MySQL database...')
   cursor = insert_to_db(lst,fn)
   print('Data has been inserted.')
   print('Program complete.')
   # fn = table name for mysql

   # l = select_from_db(cursor,fn) #IDK what this is for and it doesnt seem to have a use 
   # display the table on the screen

   # make sure the Apache web server is up and running
   # write a PHP script to display the table(s) on your browser
   xml = 'pootis'
   return xml

# end of main()

if __name__ == "__main__":
   main()

# end of hw9.py
