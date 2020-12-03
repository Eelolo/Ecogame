# Ecogame
Small system that represents economy game

### Create Python virtual environment 
```
python3 -m venv venv
```
### Activate it
```
. venv/bin/activate
```
### To deactivate run:
```
deactivate
```
### Install dependencies
```
pip install -r requirements.txt
```
# Server
### Fill configuration in .env:
```
cp .env-example .env
```
### Reset/Create database:
Run from `${project_root}: 
```
flask reset-db
```
### Start the server:
Run from `${project_root}: 
```
flask run
```
# Client
Run from `${project_root}/client`:
```
python client.py
```
