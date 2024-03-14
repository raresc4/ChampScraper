from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import numpy as np
import os
import signal
import sys
from collections.abc import Mapping
import json

specialnumbers = [11, 13, 14, 16, 20, 22, 28, 29, 30, 32, 33, 34, 36, 37, 39, 40, 41, 42, 45, 46, 48, 49, 50, 51, 52, 53, 54, 55]

def get_soup(url): 
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    return soup

class Table:
    def __init__(self,url):
        self.url = url
    def get_soup(self): 
        r = requests.get(self.url)
        soup = BeautifulSoup(r.text, "html.parser")
        return soup
    
class Table1(Table):
    def __init__(self,url,df = None):
        super().__init__(url)
        self.df = pd.DataFrame(columns = self.gettablehead())
    def gettablehead(self):
        soup = self.get_soup()
        table = soup.find_all("table")
        table0 = table[0]    
        title = table0.find_all("tr")[0]
        head = title.find_all("th")
        cap  = [th.get_text().strip() for th in head]
        return cap
    def gettable(self):
        soup = self.get_soup()
        table = soup.find_all("table")
        table0 = table[0]
        for i in range(1,56):
            title = table0.find_all("tr")[i]
            if(i in specialnumbers):
                list1 = [i,title.find_all("th")[0].get_text().strip(),title.find_all("td")[0].get_text().strip(),title.find_all("td")[1].get_text().strip(),title.find_all("td")[2].get_text().strip(),title.find_all("td")[3].get_text().strip(),title.find_all("td")[4].get_text().strip()]
                self.df.loc[i] = list1
                #print(title.find_all("td")[5].get_text().strip())
            else:
                list1 = [i,title.find_all("th")[0].get_text().strip(),title.find_all("td")[1].get_text().strip(),title.find_all("td")[2].get_text().strip(), title.find_all("td")[3].get_text().strip(),title.find_all("td")[4].get_text().strip(),title.find_all("td")[5].get_text().strip()]
                self.df.loc[i] = list1
        return self.df
    def printtocsv(self):
        self.df.to_csv("UEFA_Champions_League_top_scorers.csv",index = False)
    
table1 = Table1("https://en.wikipedia.org/wiki/List_of_UEFA_Champions_League_top_scorers")
table1.df = table1.gettable()
print(table1.df)
#soup = get_soup("https://en.wikipedia.org/wiki/List_of_UEFA_Champions_League_top_scorers")
#table = soup.find_all("table")
#table0 = table[0]    
#df = pd.DataFrame(columns = table1.gettablehead())
#for i in range(1,56):
    #title = table0.find_all("tr")[i]
    #if(i in specialnumbers):
      #  list1 = [i,title.find_all("th")[0].get_text().strip(),title.find_all("td")[0].get_text().strip(),title.find_all("td")[1].get_text().strip(),title.find_all("td")[2].get_text().strip(),title.find_all("td")[3].get_text().strip(),title.find_all("td")[4].get_text().strip()]
      #  df.loc[i] = list1
        #print(title.find_all("td")[5].get_text().strip())
    #else:
     #   list1 = [i,title.find_all("th")[0].get_text().strip(),title.find_all("td")[1].get_text().strip(),title.find_all("td")[2].get_text().strip(), title.find_all("td")[3].get_text().strip(),title.find_all("td")[4].get_text().strip(),title.find_all("td")[5].get_text().strip()]
      #  df.loc[i] = list1
#print(df)
#df.to_csv("UEFA_Champions_League_top_scorers.csv",index = False)