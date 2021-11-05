import sqlite3
from bs4 import BeautifulSoup
import os
import re
from pprint import pprint
import json
import requests


def get_name_targets():
    # This function reads wikipedia and wiktionary, it then looks for valid name categories (ones with more than 50 results) and passes them to a list.
    # This list is then returned to main, and added to the next function which reads every category for the names within
    # https://en.wikipedia.org/wiki/Category:Feminine_given_names
    urls = ["https://en.wikipedia.org/wiki/Category:Feminine_given_names", "https://en.wiktionary.org/wiki/Category:Female_given_names_by_language",
            "https://en.wikipedia.org/wiki/Category:Masculine_given_names", "https://en.wiktionary.org/wiki/Category:Male_given_names_by_language"]
    viable_links = {urls[0]: [], urls[1]: [], urls[2]: [], urls[3]: []}
    for url in urls:
        print(url)
        print(viable_links)
        html = requests.get(url)
        soup = BeautifulSoup(html.text, "html.parser")
        # Returns all subcategory names on wikipedia, need to extract names (e.g. <a title="Category:Vietnamese" extract the cultural name)
        section = soup.find("div", {"id": "mw-subcategories"}).findAll("div", {"class": "CategoryTreeItem"})
        print("Section type is : ", type(section))
        for i in section:
            sec = i.find("span", {"dir": "ltr"})
            #print("Section is : ", sec.text)
            sec = list(map(int, re.findall("\d+", sec.text)))
            if max(sec) > 55 and "unisex" not in i.a.text.lower():
                #print(i.a.text.lower(), max(sec))
                print(i.a)
                print(url)
                print(url.find(".org"))
                max_url = url.find(".org") + 4
                print(max_url)
                print(url[0:max_url])
                start_text = url[0:max_url]
                print(i.a["href"])
                end_text = start_text + i.a["href"]
                print(end_text)
                viable_links[url].append(i.a.text.lower().replace("-language", ""))
                #viable_links.append(i.a.text.lower().replace("-language", ""))
                #TODO: replace with dict
            #print(sec)
    pprint(viable_links, width=120, compact=True, sort_dicts=False)
    print(viable_links[urls[3]][-3])        
    return viable_links
    
def read_targets(values):
    print("Looping over values, looking for names")


def read_wiktionary():
    url = "https://en.wiktionary.org"
    print()





if __name__ == '__main__':
    # The BS4 code should read over the wikipedia entries, the wiktionary entries, and one other entry
    # Reads wikipedia into json or df object
    name_values = get_name_targets()
    output_values = read_targets(values=name_values)
    #print(wikipedia_values)