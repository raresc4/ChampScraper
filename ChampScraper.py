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
specialnumbers2 = [8, 9, 10, 13, 14, 16, 18, 20, 26, 27, 28, 32, 35, 39, 40, 41, 46, 50, 51, 52, 53, 54, 55, 58, 60, 62, 65, 71, 73, 74, 90, 91]


def get_closest_smaller(number, data_list):
    filtered_data = [x for x in range(number) if x not in data_list]
    if not filtered_data:
        return None
    return max(filtered_data)

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
        self.df = pd.DataFrame(columns = self.get_table_head())
    def get_table_head(self):
        soup = self.get_soup()
        table = soup.find_all("table")
        table0 = table[0]    
        title = table0.find_all("tr")[0]
        head = title.find_all("th")
        list1  = [th.get_text().strip() for th in head]
        return list1
    def get_table(self):
        soup = self.get_soup()
        table = soup.find_all("table")
        table0 = table[0]
        db = pd.DataFrame(columns = self.get_table_head())
        for i in range(1,56):
            title = table0.find_all("tr")[i]
            if(i in specialnumbers):
                list1 = [i,title.find_all("th")[0].get_text().strip(),title.find_all("td")[0].get_text().strip(),title.find_all("td")[1].get_text().strip(),title.find_all("td")[2].get_text().strip(),title.find_all("td")[3].get_text().strip(),title.find_all("td")[4].get_text().strip()]
                db.loc[i] = list1
                #print(title.find_all("td")[5].get_text().strip())
            else:
                list1 = [i,title.find_all("th")[0].get_text().strip(),title.find_all("td")[1].get_text().strip(),title.find_all("td")[2].get_text().strip(), title.find_all("td")[3].get_text().strip(),title.find_all("td")[4].get_text().strip(),title.find_all("td")[5].get_text().strip()]
                db.loc[i] = list1
        return db
    def print_to_csv(self):
        string = input("Enter the name of the file: ")
        name = string + ".csv"
        self.df.to_csv(name,index = False)

class Table2(Table):
    def __init__(self,url,df = None):
        super().__init__(url)
        self.df = pd.DataFrame(columns = self.get_table_head())
    def get_table_head(self):
        soup = self.get_soup()
        table = soup.find_all("table")
        table0 = table[1]    
        title = table0.find_all("tr")[0]
        head = title.find_all("th")
        list1  = [th.get_text().strip() for th in head]
        return list1
    def get_closest_smaller(self,number, data_list):
        filtered_data = [x for x in range(number) if x not in data_list]
        if not filtered_data:
            return None
        return max(filtered_data)
    def get_table(self):
        soup = self.get_soup()
        table = soup.find_all("table")
        table0 = table[1]
        db = pd.DataFrame(columns = self.get_table_head())
        for i in range(1,100):
            title = table0.find_all("tr")[i]
            if(i in specialnumbers2):
                title2 = table0.find_all("tr")[self.get_closest_smaller(i,specialnumbers2)]
                list1 = [title2.find_all("td")[0].get_text().strip(),title.find_all("th")[0].get_text().strip(),title.find_all("td")[0].get_text().strip(),title2.find_all("td")[2].get_text().strip()]
                db.loc[i] = list1
                #print(title.find_all("td")[5].get_text().strip())
            else:
                list1 = [title.find_all("td")[0].get_text().strip(),title.find_all("th")[0].get_text().strip(),title.find_all("td")[1].get_text().strip(),title.find_all("td")[2].get_text().strip()]
                db.loc[i] = list1
        return db
    def print_to_csv(self):
        string = input("Enter the name of the file: ")
        name = string + ".csv"
        self.df.to_csv(name,index = False)

class Table3(Table):
    def __init__(self,url,df = None):
        super().__init__(url)
        self.df = pd.DataFrame(columns = self.get_table_head())
    def get_table_head(self):
        soup = self.get_soup()
        table = soup.find_all("table")
        table0 = table[2]
        title = table0.find_all("tr")[0]
        list1 = [th.get_text().strip() for th in title.find_all("th")]
        return list1
    def get_table(self):
        soup = self.get_soup()
        table = soup.find_all("table")
        table0 = table[2]
        db = pd.DataFrame(columns = self.get_table_head())
        c = 0
        for i in range(0,4):
            list1 = [table0.find_all("th")[i+3].get_text().strip(),table0.find_all("td")[i*2].get_text().strip(),table0.find_all("td")[i*2 + 1].get_text().strip()]
            db.loc[c] = list1
            c += 1
        for i in range(4,7):
            list1 = [table0.find_all("th")[i+3].get_text().strip(),table0.find_all("td")[6].get_text().strip(),table0.find_all("td")[i+3].get_text().strip()]
            db.loc[c] = list1
            c += 1
        db.loc[c] = [table0.find_all("th")[10].get_text().strip(),table0.find_all("td")[11].get_text().strip(),table0.find_all("td")[12].get_text().strip()]
        c += 1
        for i in range(8,13):
            list1 = [table0.find_all("th")[i+3].get_text().strip(),table0.find_all("td")[11].get_text().strip(),table0.find_all("td")[i+5].get_text().strip()]
            db.loc[c] = list1
            c += 1
        return db
    def print_to_csv(self):
        string = input("Enter the name of the file: ")
        name = string + ".csv"
        self.df.to_csv(name,index = False)
table1 = Table3("https://en.wikipedia.org/wiki/List_of_UEFA_Champions_League_top_scorers")
table1.df = table1.get_table_head()
table1.df = table1.get_table()
print(table1.df)
#soup = get_soup("https://en.wikipedia.org/wiki/List_of_UEFA_Champions_League_top_scorers")
#table = soup.find_all("table")
#table0 = table[2]