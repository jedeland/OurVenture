import sqlite3
from bs4 import BeautifulSoup
import os
import re
import pprint
import json
import requests


def read_wikipedia():
    #https://en.wikipedia.org/wiki/Category:Feminine_given_names
    urls = ["https://en.wikipedia.org/wiki/Category:Feminine_given_names", "https://en.wiktionary.org/wiki/Category:Female_given_names_by_language"]
    for url in urls:
        print(url)
        html = requests.get(url)
        soup = BeautifulSoup(html.text, "html.parser")
        # Returns all subcategory names on wikipedia, need to extract names (e.g. <a title="Category:Vietnamese" extract the cultural name)
        section = soup.find("div", {"id": "mw-subcategories"}).findAll("div", {"class": "CategoryTreeItem"})
        print("Section type is : ", type(section))
        for i in section:
            sec = i.find("span", {"dir": "ltr"})
            #print("Section is : ", sec.text)
            sec = list(map(int, re.findall("\d+", sec.text)))
            if max(sec) > 50 and "unisex" not in i.a.text.lower():
                print(i.a.text.lower(), max(sec))
                
            #print(sec)
            
    return soup
    

def read_wiktionary():
    url = "https://en.wiktionary.org"
    print()





if __name__ == '__main__':
    # The BS4 code should read over the wikipedia entries, the wiktionary entries, and one other entry
    # Reads wikipedia into json or df object
    wikipedia_values = read_wikipedia()
    #print(wikipedia_values)