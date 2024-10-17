# SiBanjir-BE
## Prerequisite
Start off by creating a virtual environment so that your system's dependency doesn't clash with the project's.
```
python -m venv env
```
Activate virtual environment by running:
- On Windows use `env\Scripts\activate`
- On Mac source `env/bin/activate`

### Install requirements.txt file
After activating the virtual environment, install all the required dependencies by running the command:
```
pip install -r requirements.txt
```

### Setting up DB environment variable
This will vary with different OS, and there are many different methods to achive this. On Window's cmd, one of the simplest way it can be done is by:
```
set POSTGRES_DATABASE=...
set POSTGRES_USER=...
set POSTGRES_PASSWORD=...
set POSTGRES_HOST=...
set POSTGRES_PORT=...
```

### Makemigration and Migrate
```
python manage.py makemigrations
python manage.py migrate
```

### Run the server
```
python manage.py runserver
```