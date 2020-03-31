# DebateStar Web App

## Introduction 

This implements an online data visualization platform for our NLP engine [DebateStar](https://github.com/maoli131/DebateStar). 
The main page highlights our project features, links to Github open source codes 
and introduces our team members. The visualization page serves as the main 
interface to interact with our NLP engine. It dynamically presents our model's prediction scores for varied debates.

![intropage](debatestar/static/img/intropage.jpg)

## Technology

The backend is built with micro web framework Flask while the frontend is built with modern HTML5/CSS/Javascript and Bootstrap 4 (I used Flask's built-in Jinja 
template engine for easy deployment). The platform is deployed with AWS Elastic Beanstalk for high maintainability and extensibility. 

## Run on Local Machine

This web app requires Python 3 and all dependencies in virtual environment venv.

### Virtual Environment

Activate the virtual environment and install dependency packages.
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Run Flask

Run the backend Flask app with `application.py`
```
python application.py
```