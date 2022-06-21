# Cs50-Final-Project
## Video: [CS50’s Web Programming with Python, SQLite3, HTML and CSS Final Project](https://www.youtube.com/watch?v=K7MIa_CQNxw)
   
I created a website where people can create posts, share blogs and ideas, access to free contents like movies, series, books, softwares, games and learning.
  
### The main purpose of the website is:
- Create a post and share your opinions and ideas
- Access to the best free contents online
- Free learning on the own pace.

## What’s contained in each file:
- [project](https://github.com/Famz88/project/tree/master) is the project folder, It contains:
- [__pycache__](https://github.com/Famz88/project/tree/master/__pycache__): it contains caches of the program.
- [img](https://github.com/Famz88/project/tree/master/img): it contains an image of the logo.
  - [static](https://github.com/Famz88/project/tree/master/static): it contains Favicon.ico and CSS file for the project.
  - [templates](https://github.com/Famz88/project/tree/master/templates): it contains all html files
  - [app.py](https://github.com/Famz88/project/blob/master/app.py): it contains route to:
      - Connection to the database
      - Getting the post and update in the database
      - Routing to the index (it is the default view)
      - Posting and updating
      - Creating content and update in  database
      - Enabling to edit and update in database
      - Enabling to delete the post after already posted
      - Routing to about html
      - Routing to series html
      - Routing to movies html
      - Routing to books html
      - Routing to softwares html
      - Routing to games html
      - Routing to learning html
- [database.db](https://github.com/Famz88/project/blob/master/app.py): The database of the app, used for saving and updating.
- [init_db.py](https://github.com/Famz88/project/blob/master/init_db.py): Python program used to import and create sqlite3 database
- [schema.sql](https://github.com/Famz88/project/blob/master/schema.sql): SQL program which used to create tables in the database.

## How to launch application

1. Make sure that [python](https://www.python.org/downloads/), [pip](https://pip.pypa.io/en/stable/installation/) and [flask](https://github.com/pallets/flask/archive/master.tar.gz) 
2. Clone the code: `git clone https://git@github.com:Famz88/project.git`
3. Once installed run command `flask run`
4. In your browser go to `localhost:5000`
5. You are ready to go!


