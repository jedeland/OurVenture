### Setting up the backend for development

## Using venv / pip

To create a local venv, either use the setup_venv.sh script ```sh setup_venv.sh``` or execute the commands contained within the setup_venv.sh file

```
python3 --version
sudo apt install python3.8-venv
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

This will create a local venv, to create a local virtual environment without using python3, you can use the same commands using whichever local python version you have

for instance python3.9, in my case i executed ```python3.9 -m venv venv```to create my local venv

Once the venv is created, you can execute the following command to activate the venv

```. venv/bin/activate```

Now your terminal will use the virtual environment which encapsulates all of your python project (you should see this on the left), from which you can run the flask server using the command (Please remember that the flask backend is for API purposes, and shouldnt show any real webpages)

```python3 __init__.py```