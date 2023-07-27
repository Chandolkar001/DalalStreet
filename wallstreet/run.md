> ### **How to run the project**

#### Cloning Git Repository:
```
git clone https://github.com/Chandolkar001/DalalStreet.git
cd DalalStreet
```

#### Creating Virtual Enviornment:
```
virtualenv venv
```
#### Activating Virtual Env on Windows:
```
venv\Scripts\activate
```

#### Activating Virtual Env on Linux:
```
source venv/bin/activate
```

#### Installing Dependencies:
```
cd wallstreet
pip install -r requirements.txt
```
#### Make migrations:
```
python manage.py makemigrations
python manage.py migrate
```
#### Run Python Development Server:
```
python manage.py runserver
```
> #### Running on Docker:
#### Install Docker on your system:
<href>https://docs.docker.com/engine/install/</href>
```
return to DalalStreet directory: cd ..
```
#### Run the following commands to build Docker image and then run docker container:
```
docker-compose build
docker-compose up -d
```
#### To stop the container:
```
docker-compose down
```






