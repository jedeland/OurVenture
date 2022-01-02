import os
import zipfile

if __name__ == "__main__":
    print("Unzipping all files in DataCollections directory")
    if os.path.exists("ourventure-flask/DataPreperation/DataCollections"):
        print("Path exists!")
        for file in os.listdir("ourventure-flask/DataPreperation/DataCollections"):
            if file.endswith(".zip"):
                print(file)
                with zipfile.ZipFile(f"ourventure-flask/DataPreperation/DataCollections/{file}", "r") as zip:
                    zip.extractall(f"ourventure-flask/DataPreperation/DataCollections/")
    else:
        print("Project directory structure does not conform to the main branch ... please contact a team member for more information")
        print("Prefferd directory structure: ourventure/ourventure-flask/DataPreperation/DataCollections")
