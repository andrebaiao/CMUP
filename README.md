# CMUP
Project CMUP
André Alves
Luís Fonseca

## Setup

Create a venv:

```
$ python3 -m venv venv
$ source venv/bin/activate
```

Install the dependencies:

```
$ pip3 install -r requirements.txt
```

## API

SetUp Database:

```
$ cd API    
$ python db.py
```

Run flask api on port 9000:

```
$ python3 -m app.py
```

## Frontend

```
$ cd Frontend
$ npm install @material-ui/core
$ npm install
$ npm start
```
https://demos.creative-tim.com/paper-dashboard-react/#/documentation/quick-start

### MQTT
As yet another proccess, run `consumer.py`, located in the folder /Pycom.

### PyCom
Run the file `main.py` located in the folder /Pycom on your device, after changing `app_eui` and `app_key` variables in that same file.
