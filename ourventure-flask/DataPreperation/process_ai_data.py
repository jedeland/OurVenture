import json
import os
from traceback import print_list
import zipfile
import country_converter as coco


#TODO: Automate the removal of certain patterns for any future data
def unpack_files():
    print(os.getcwd())
    path = f"{os.getcwd()}\DataPreperation\AI_Data"
    
    for i in os.listdir(path):
        if i.endswith(".zip"):
            # print(i)
            with zipfile.ZipFile(f"{path}\{i}", "r") as zip:
                zip.extractall(f"{path}")

def get_wiki_data():
    if os.path.exists("DataPreperation/DataCollections/name_collection_latin.json"):
        print("Names exists")
        with open("DataPreperation/DataCollections/name_collection_latin.json", "r", encoding="utf-8") as json_file:
            names_file = json.load(json_file)
            print(names_file.keys())
            return names_file
    elif not os.path.exists("DataPreperation/DataCollections/name_collection_latin.json"):
        print("Please run the 'unzipper' file first")
    

def identify_names(input_file_wiki):
    print("Finding overlaps")
    # print(input_file_wiki)
    #TODO: use coco converter to check overlap
    #TODO: create map for name + location eg {basque: spain, arabic: egypt x y z, }
    shared_values = []
    wiki_keys = input_file_wiki.keys()
    print(type(wiki_keys))
    print(wiki_keys)
    # Making value map for wiki_keys, assigning to "bins"
    bin_data = input_file_wiki.copy()
    print(bin_data.keys())
    print(type(bin_data["albanian"]))
    # print(new_wiki["albanian"])
    bin_data = {"west_europe",
     "east_europe", 
     "middle_east", 
     "africa", 
     "east_asia", "south_asia", "india"}
    ai_data_list = []
    for i in os.listdir(f"{os.getcwd()}\DataPreperation\AI_Data"):
        ai_data_list.append(i)
        if i.lower().split(".")[0] in input_file_wiki.keys() and i:
            # print(i)
            pass
    print(ai_data_list)
    # Relevant names

if __name__ == "__main__":
    unpack_files()
    results = get_wiki_data()
    # print(results)
    shared_names = identify_names(results)