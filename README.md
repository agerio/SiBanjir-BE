# SiBanjir-BE

## SiBanjir brief description

The innovative SiBanjir application aims to provide real-time notifications regarding rainfall levels in Queensland that may indicate potential flooding. This platform is designed to enhance the preparedness of Queensland residents for flood events, enabling them to evacuate valuable belongings and move to safer areas in a timely manner. “SiBanjir” offers a variety of features that allow users to access up-to-date information on heavy rainfall and flood risks, as well as easily monitor the locations of friends and family connected through the app. Additionally, the app enables users to stay informed about the flood readiness status in their local area. During emergencies, users can communicate with loved ones, ensuring collective safety and strengthening coordination in response to disasters.


## Django Rest API Set Up
### Create a virtual environment to isolate our package dependencies locally
python3 -m venv env
On Mac source env/bin/activate  
On Windows use env\Scripts\activate

### Install Django and Django REST framework into the virtual environment (if you not install django frame )
pip install djangorestframework

### Install requirements.txt file
pip install -r requirements.txt

### If you make update in models.py please run the command below
Run the 'python manage.py makemigrations' command to prepare to migrate the model schema into the local Django database and 'python manage.py migrate' to deploy the created model schema into the local Django database.

### Run the server
python manage.py runserver