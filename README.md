<p align="center">
  <a href="#">
    <img src="https://i.imgur.com/ywOXkDg.png" alt="wm" />
  </a>
</p>


# Django CRUD Generator

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

[![Maintenance](https://img.shields.io/badge/Django-v3.1.7-%3CCOLOR%3E)](https://img.shields.io/badge/Django-v3.1.7-%3CCOLOR%3E)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)
[![Linux](https://svgshare.com/i/Zhy.svg)](https://svgshare.com/i/Zhy.svg)
[![Windows](https://svgshare.com/i/ZhY.svg)](https://svgshare.com/i/ZhY.svg)

[![PyPi version](https://badgen.net/pypi/v/pip/)](https://pypi.com/project/pip)
[![GitHub latest commit](https://badgen.net/github/last-commit/caiomarinhodev/caiomarinhome)](https://GitHub.com/caiomarinhodev/caiomarinhome/commit/)


### 📝 Description
---


This is the best CRUD generator ever implemented in human history. (laughs)

The main objective of this project is to generate CRUD from models created in "models.py", and thus generate templates, classes, mixins, forms, admin, urls, serializers, viewsets, api routes and utils files.

In our world of web project development I have developed several applications, in different opportunities such as Drones, 5G, Edge Computing, Data Analysis, Machine Learning and Machine Reasoning, WebApps. Faced with so many proofs of concept, we realized that there was a pattern within the application execution flows, as these systems were required by the client:

- WEB System
- Relational Database
- Authentication
- Template CRUD's

Given this, there was a need to have an application that could automate the creation of web applications, facilitating the creation of CRUD's, as well as directing the implementation of what matters, that is, "more fat" for the delivery of projects, increasing the time to develop the more difficult features.

Keywords: Data Analytics, Data Science, Django, Python, Web, REST

Project is written with Django framework.

Below is the list of CRUD endpoint patterns generated for each model:
List: /<model>/
Create: /<model>/create/
Update: /<model>/<id>/update/
View: /<model>/<id>/
Delete: /<model>/<id>/delete/

### 🚀 Status Project
---
<h4> 
	🚧 Django CRUD Generator 🚀 under construction ... 🚧 
</h4>

### 💻 Features
---

- [x] CRUD generator Module
- [x] Templates generator module
- [x] Easy Install
- [ ] Setup.py
- [ ] Automatic/Manual/Load/Assertions Tests

### ⚡Tech Stack
---

The following tools were used in building the project:

- [Python](https://www.python.org/)
- [Django](https://www.djangoproject.com/)


### Author
---

<a href="#">
 <img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/u/7137962?v=4" width="100px;" alt=""/></a>
 <br />
 <sub><b>Caio Marinho</b></sub></a> <a href="#" title="Caio Marinho">🚀

Made with ❤️ by Caio Marinho 👋🏽 Get in touch!

[![Linkedin Badge](https://img.shields.io/badge/-Caio%20Marinho-blue?style=flat-square&logo=Linkedin&logoColor=white&link=https://www.linkedin.com/in/caiomarinho/)](https://www.linkedin.com/in/caiomarinho/) 
[![Gmail Badge](https://img.shields.io/badge/-caiomarinho8@gmail.com-c14438?style=flat-square&logo=Gmail&logoColor=white&link=mailto:caiomarinho8@gmail.com)](mailto:caiomarinho8@gmail.com)


### Application Demo
---
<p align="center">
  <kbd>
    <img style="border-radius: 5px" src="https://i.imgur.com/igDgxbQ.gif" alt="Intro">
  </kbd>
</p>


### Getting Started
---

First clone the repository from Github and switch to the new directory:
    
Activate the virtualenv for your project.
    
Install project dependencies:

    $ pip install -r requirements.txt
    
    
Then simply apply the migrations:

    $ python manage.py migrate
    

You can now run the development server:

    $ python manage.py runserver
