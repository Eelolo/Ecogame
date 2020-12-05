# Ecogame
Small system that represents economy game

### Create Python virtual environment 
```
python3 -m venv venv
```
### Activate it
Run from `${project_root}:
```
. venv/bin/activate
```
### To deactivate run:
```
deactivate
```
### Install dependencies
Run from `${project_root}:
```
pip install -r requirements.txt
```
# Server
### Fill configuration in .env:
```
cp .env-example .env
```
### Reset/Create database:
Run from `${project_root}/server: 
```
flask reset-db
```
### Start the server:
Run from `${project_root}/server: 
```
flask run
```
# Client
Run from `${project_root}/client`:
```
python client.py
```
