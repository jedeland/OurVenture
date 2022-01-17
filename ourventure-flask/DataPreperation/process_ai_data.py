import json
import os
from traceback import print_list
import zipfile


#TODO: Automate the removal of certain patterns for any future data
def unpack_files():
    print(os.getcwd())
    path = f"{os.getcwd()}\AI_Data"
    
    for i in os.listdir(path):
        if i.endswith(".zip"):
            print(i)
            with zipfile.ZipFile(f"{path}/{i}", "r") as zip:
                zip.extractall(f"{path}")

def get_wiki_data():
    if os.path.exists("DataCollections/name_collection_latin.json"):
        print("Names exists")
        with open("DataCollections/name_collection_latin.json", "r") as json_file:
            names_file = json.load(json_file)
            print(names_file.keys())
            return names_file
    elif not os.path.exists("DataCollections/name_collection_latin.json"):
        print("Please run the 'unzipper' file first")
    
    #TODO: create hashmap linking dict values to csv values

def identify_names(input_file):
    print("Finding overlaps")
    print(input_file)
    


if __name__ == "__main__":
    unpack_files()
    results = get_wiki_data()
    identify_names(results)