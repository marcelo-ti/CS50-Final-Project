# Adopt A Paw

#### Video Demo:

<https://www.youtube.com>

#### Description

This repository contains the final project for CS50, Harvard University's Introduction to Computer Science. The project, titled "Adopt A Paw" is a website that aims to facilitate the animal adoption process. This README.md file provides an overview of the project, its features and instructions on how to use.

#### Contents

- [Adopt A Paw](#adopt-a-paw)
  - [Video Demo](#video-demo)
  - [Description](#description)
  - [Contents](#contents)
  - [Technologies](#technologies)
  - [Installation](#installation)
  - [Features](#features)
  - [File Description](#file-description)
  - [Documentations](#documentations)
  - [About CS50](#about-cs50)

#### Technologies

- Python
- Flask
- SQLite
- Javascript
- HTML 5
- CSS 3

**Note** Flask is a microframework aimed mainly at small applications with simpler requirements, such as creating a basic website.

#### Installation

Installing Brew:

```
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
brew update
```

Installing Python and its dependencies:

```
brew install python3
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install cs50
python3 -m pip install flask
python3 -m pip install flask-session
python3 -m pip install requests
python3 -m pip install pytz
```

Debugging project:

```
flask --app app.py --debug run
```

Running project:

```
flask run
```

#### Features

- Register account;
- Login;
- Edit profile (account and personal settings);
- Send a contact message;
- Schedule a visit to a pet;
- Manage a scheduled visit.

#### File Description

- static
  - css
    - styles.css: all custom styles related to the website;
  - js
    - script.js: functions written in javascript related to the interface;
- templates
  - profile
    - account-settings.html: page responsible for updating account settings;
    - personal-settings.html: page responsible for updating personal settings;
    - profile.html: static page responsible for listing the options that a profile can manage (account, personal and visits);
    - visits.html: page responsible for listing and managing visits;
  - about-us.html: static page responsible for describing the company;
  - adopt.html: page responsible for listing, describing and scheduling possible pet visits;
  - apology.html: page responsible for sending error messages to the users;
  - contact-us.html: page responsible for connecting the user and the company;
  - index.html: page page responsible for describing the company and listing the main numbers;
  - layout.html: page responsible for being a header and footer template for all other pages;
  - login.html: page responsible for user login to the logged in area of the website;
  - register.html: page responsible for registering a new user to the website;
  - app.py: all API and database integration available for front-end requests;
  - script.sql: script with the database and its table structure with little dummy data.

#### Documentations

- [Python](https://docs.python.org/3/)
- [Flask](https://flask.palletsprojects.com/en/latest/)
- [SQLite](https://www.sqlite.org/docs.html)
- [Javascript](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
- [HTML 5](https://developer.mozilla.org/en-US/docs/Glossary/HTML5)
- [CSS 3](https://developer.mozilla.org/en-US/docs/Web/CSS)
- [Brew](https://brew.sh/)

#### About CS50

**CS50**, also known as "Introduction to Computer Science," is a renowned introductory course offered by Harvard University. Taught by Professor David J. Malan, the course aims to provide students with a solid foundation in computer science and programming. CS50 is designed for both beginners with no prior programming experience and those who have some background in the field.

CS50 has gained popularity not only for its comprehensive curriculum but also for its effectiveness in making computer science accessible to a broad audience. It has inspired many learners to pursue further studies and careers in the field of computer science. The course materials, including lectures and problem sets, are available for free online, making it a valuable resource for self-learners and educators.
