import sqlite3
from bs4 import BeautifulSoup
import os
import re
import time
from pprint import pprint
import json
import requests
from functools import cache

def get_name_targets():
    # This function reads wikipedia and wiktionary, it then looks for valid name categories (ones with more than 50 results) and passes them to a list.
    # This list is then returned to main, and added to the next function which reads every category for the names within
    # https://en.wikipedia.org/wiki/Category:Feminine_given_names
    urls = ["https://en.wikipedia.org/wiki/Category:Masculine_given_names", "https://en.wiktionary.org/wiki/Category:Male_given_names_by_language", 
    "https://en.wiktionary.org/w/index.php?title=Category:Male_given_names_by_language&subcatfrom=Rwanda-Rundi%0ARwanda-Rundi+male+given+names#mw-subcategories",
    "https://en.wikipedia.org/wiki/Category:Feminine_given_names", "https://en.wiktionary.org/wiki/Category:Female_given_names_by_language",
    "https://en.wikipedia.org/wiki/Category:Surnames_by_language", "https://en.wiktionary.org/wiki/Category:Surnames_by_language"]
    
    # List of viable links found in each URL page
    viable_links = []
    for url in urls:
        # Gets a HTML Object of the url for processing
        # Beatiful soup processes the html objects text value, allowing us to use BeatifulSoup class functions to search through it
        soup = get_soup(url)
        # Used to create new URLs found from the next page section, slices the url value from start, up until the .org section eg: https://en.wikipedia.org
        start_text = url[0:url.find(".org") + 4]

        # Returns all subcategory names on wikipedia, need to extract names (e.g. <a title="Category:Vietnamese" extract the cultural name)
        section = soup.find("div", {"id": "mw-subcategories"}).findAll("div", {"class": "CategoryTreeItem"})
        # print("Section type is : ", type(section))
        # Looping over found sections from the soup.findAll call (all divs with class CategoryTreeItem)

        for i in section:
            # Assign section by finding span
            sec = i.find("span", {"dir": "ltr"})
            #print("Section is : ", sec.text)
            # Use regex to produce a list of values that are digits in the section text, this returns the value which states how many names exist >
            # eg: 21 c, 734 e
            sec = list(map(int, re.findall("\d+", sec.text)))
            # Checks max sec value (usually the number of elements or "e"), skips unisex
            # TODO: fix the checks for line 54
            # print(i.a.text.capitalize().split()[0], " value")
            # if i.a.text.lower().split()[0] == "korean":
            #     print(viable_links)
            # print(i.a.text.capitalize().split()[0] in viable_links)
            
            if max(sec) > 55 and "unisex" not in i.a.text.lower():
                # Create url string using the start text and the link to the section
                final_text = start_text + i.a["href"]
                # Add link text to viable_links list for processing later
                viable_links.append(final_text)
            elif i.a.text.lower().split(" ")[0] in viable_links and max(sec) > 20:
                final_text = start_text + i.a["href"]
                # Add link text to viable_links list for processing later
                viable_links.append(final_text)
        print(viable_links[-1])

    # print("Example: ", viable_links[-3])        
    # Export end value to main function
    return viable_links
    
def read_targets(female, male, last_names):
    # Dummy function
    print("Looping over values, combining dicts")
    # Init dict
    combined_dict = {}

    # print(female["name_values"].keys(), male["name_values"].keys())
    # Get values that dont exist in both lists, aka naughty values
    outliers = set(list(female["name_values"].keys())) ^ set(list(male["name_values"].keys())) ^ set(list(last_names["name_values"].keys()))
    print(outliers)
    print(len(outliers))
    print("_"*20 + "\n"*2)
    print(sorted(list(female["name_values"].keys())))
    print("_"*20 + "\n"*2)
    print(sorted(list(male["name_values"].keys())))
    print("_"*20 + "\n"*2)
    print(sorted(list(last_names["name_values"].keys())))


    # This line below looks very complicated, it first maps out a the lists into sets, this is then extracted using the * operator, the function set.intersection is then used
    # To find values that exist in all 3 sets, and this is then converted to a list which is stored in shared values
    shared_values = list(set.intersection(*map(set, [list(female["name_values"].keys()), list(male["name_values"].keys()), list(last_names["name_values"].keys())])))
    print(sorted(shared_values))
    print(len(shared_values))
    # if len(outliers) == 0:
    #     print("No outliers found!")
    #     for x in female["name_values"].keys():
    #         combined_dict.update({x: [*female["name_values"][x], *male["name_values"][x], *last_names["name_values"][x]]})
    # else:
        # Loop over locations in female, as female has less values on wikipedia / wiktionary it should be smaller
    for x in shared_values:
        # If x is in the naughty list, we skip it
        print(x)
        # Update the dictionary with a literal list using the * operator
        combined_dict.update({x: [*female["name_values"][x], *male["name_values"][x], *last_names["name_values"][x]]})
    # print("Combined Dict!")                
    # print(combined_dict["spanish"])
    return combined_dict
    
def get_name_values(gender_arg, list_arg):
    name_data = {"name_values": {}}
    
    for val in list_arg:
        soup = get_soup(val)
        
        # print(f.split(":", 1)[-1])
        #TODO: Refactor me to look nicer
        origin = re.findall(r"^(.*?)_", val.lower().replace("old_", "").replace("high_", "").replace("langauge_", "").replace("-language", "").split(":")[-1])[0]
        print(origin.capitalize())

        section = soup.find("div", {"id": "mw-pages"})
        if "next page" in section.text:
            #config name data checks if the dictionary needs to be reset for the key value (or initialised), or if no change is needed
            configure_name_data(name_data, origin)
            
            next_link = section.find("a", string="next page")
            print(val, next_link)
            #Assign names function takes the current section and uses it to update the name_data dictionary
            assign_names(gender_arg, name_data, origin, section, val)
            #If a next page exists, recursive search is activates, this will search recursively until it find no more hyperlink on the "next page" value
            recursive_search(gender_arg, name_data, val, origin, next_link)
                    
        else:
            configure_name_data(name_data, origin)
            print(f"Single page can be read!: {val}")
            assign_names(gender_arg, name_data, origin, section, val)
    return name_data 

#Header text: Mozilla/5.0 (Windows NT 10.0; WOW64; rv:77.0) Gecko/20100101 Firefox/77.0
# {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:77.0) Gecko/20100101 Firefox/77.0'}

def get_soup(val):
    #Sleep is required so our robot doesnt rush ahead too fast and get shot down by wikipedia
    time.sleep(0.0055)
    #Get the value and send user-agent header, pretending like we are making a relevant request from a machine
    html = requests.get(val, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:77.0) Gecko/20100101 Firefox/77.0'})
    soup = BeautifulSoup(html.text, "lxml")
    #Returns the BS4 soup object
    return soup


def get_recursive_soup(url, href_link):
    # This function searches through all "next pages" that are found for certain values,
    #href_link is changed to ensure that the ampersand: "&" is output correctly, currently it translates to "&amp"
    href_link = re.sub(r'&amp;', r'&', href_link)
    formed_url = f"{url.split('.org')[0]}.org{href_link}"
    print(formed_url)
    soup = get_soup(formed_url)
    section = soup.find("div", {"id": "mw-pages"})
    return section

def recursive_search(gender_arg, name_data, val, origin, next_link):
    #If link from call exists 
    if next_link:
        #Last found URL for logging
        last_url = re.sub(r'&amp;', r'&', next_link["href"])
        #Gets soup object of next link
        new_page = get_recursive_soup(val, next_link["href"])
        #Checks for next page, and looks for hyperlink
        if "next page" in new_page.text:
            next_link = new_page.find("a", string="next page")
            if next_link:
                # Read names into object
                assign_names(gender_arg, name_data, origin, new_page, last_url)
                # Call function again using new link
                recursive_search(gender_arg, name_data, val, origin, next_link)
            else:
                #Log the last used link in recursive search, for human checking
                print(f"Last page {last_url}")
                #Update dict with values from the last page found before recursive loop is broken
                assign_names(gender_arg, name_data, origin, new_page, last_url)
                    

def configure_name_data(name_data, origin):
    if origin in name_data["name_values"].keys():
        print("Name already exists, not overwriting past data")
    else:
        name_data["name_values"].update({origin: []})

def assign_names(gender_arg, name_data, origin, section, assigned_from):
    names = section.find_all("li")
    for name in names:
                #print()
        name_data["name_values"][origin].append({"name": name.text.split(" ")[0], "gender": gender_arg, "origin": origin})  # "location": assigned_from})           

def get_female_values(female_list):
    #TODO: get names from the soup followed in this list
    female_data = {"name_values": []}
    test_data = {"name_values": {}}
    for f in female_list:
        soup = get_soup(f)
        # print(f.split(":", 1)[-1])
        #TODO: Refactor me to look nicer
        origin = re.findall(r"^(.*?)_", f.lower().replace("old_", "").replace("high_", "").replace("langauge_", "").split(":")[-1])[0]
        print(origin.capitalize())

        section = soup.find("div", {"id": "mw-pages"})
        if "next page" in section.text:
            #TODO: add way to follow down the pages
            links = section.find("a", string="next page")
            print(links)
        else:
            if origin in test_data["name_values"].keys():
                print("Name already exists, not overwriting past data")
            else:
                test_data["name_values"].update({origin: []})
            print(f"Single page can be read!: {f}")
            names = section.find_all("li")
            for name in names:
                #print()
                test_data["name_values"][origin].append({"name": name.text.split(" ")[0], "gender": "female", "origin": origin})
                female_data["name_values"].append({"name": name.text.split(" ")[0], "gender": "female", "origin": origin})
                
            print(names[-1].text.split(" ")[0])

                
            print(type(names))
    pprint(female_data)

    return test_data

def transliterate_values(input_dict):
    print()


if __name__ == '__main__':
    # The BS4 code should read over the wikipedia entries, the wiktionary entries, and one other entry
    # Reads wikipedia into json or df object
    start = time.time()
    JSON_PATH = "ourventure-flask/DataPreperation/DataCollections/name_collection_output.json"
    #Remove me if you want to change the data aggregation system
    if os.path.exists("ourventure-flask/DataPreperation/DataCollections/name_collection_output.json"):
        print()
        output_values = json.load(JSON_PATH, ensure_ascii=False)
        latinized_values = transliterate_values(output_values)

    else:


        # Reads name values and outputs a list
        name_values = get_name_targets()
        
        #Split list before for loop
        female_list = list(filter(lambda k: "_feminine_" in k.lower() or "_female_" in k.lower(), name_values))
        male_list = list(filter(lambda k: "_masculine_" in k.lower() or "_male_" in k.lower(), name_values))
        surname_list = list(filter(lambda k: "_surnames" in k.lower() or "_male_" in k.lower(), name_values))
        
        
        # print(female_list, "\n\n\n", male_list)

        female_vals = get_name_values("female" , female_list)
        male_vals = get_name_values("male", male_list)
        surname_vals = get_name_values("surname", surname_list)
        #TODO: add last names here

        #print(f"Time taken to read targets ... {time.time() - start} ")
        time.sleep(2)
        # Create json object, and combine dicts 
        output_values = read_targets(female_vals, male_vals, surname_vals)
        pprint(output_values["spanish"])
        
        with open("ourventure-flask/DataPreperation/DataCollections/name_collection_output.json", "w") as f:
            json.dump(output_values, f, sort_keys=True, ensure_ascii=False)
        latinized_values = transliterate_values(output_values)

    
    print(f"Time taken to read targets ... {time.time() - start} ")
