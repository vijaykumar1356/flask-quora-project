# Flask Toy Project

## Context of the Project
* The project is about building a **Blog** which meets the requirements below mentioned.
  * It must include **CRUD**(Create, Read, Update, Delete) Operations
  * A User Authentication
  * A Registration Facility to add new users
  * Error handling during uncertainities
* To document the requirements of this project, we used **User Stories** method which has growing popularity in Agile Development of Products. 
  
## Technology Stack for this Project
* **Front End:** Html, CSS, Bootstrap framework
* **Back End:** Flask
* **Database:** Postgres

## Setting up the Environment
1. Make a new directory using the command `mkdir flask-project` from command line and go to that directory using `cd flask-project`
1. Now clone this [repository](https://gitlab.com/mountblue/cohort-14-python/vijay_yarramsetty/flask-toy-project) using the command `git clone git@gitlab.com:mountblue/cohort-14-python/vijay_yarramsetty/flask-toy-project.git` 
1. Now go to that directory from CLI using `cd flask-toy-project`
1. Set up a virtual environment for the project using the command `python3 -m virtualenv flaskenv`
2. Activate the virtual environment using the command `source flaskenv/bin/activate`
3. Now Install the dependencies required for the project using the command `pip install -r requirements.txt` (requirements.txt file is already existed in this cloned repository.)
4. Make sure you have installed **Postgres** in your local machine for creating role and database using following scripts and commands.
5. Go to `sql-scripts` directory with the command `cd sql_scripts` follow the below order of commands to create a role and a database for this project. 
   1. `sudo -su postgres`
   2. `psql -U postgres -f create_user-db.sql` it creates a databse named 'vijaydb' and a user named 'vijaydb'
   3. `exit` for exiting out of postgres shell
   4. `cd ..` for going back to project main directory
6. For initializing the database with tables(models) use the following commands.
   1. `flask db init` (if migrations directory does not exist, if exists run directly the command `flask db upgrade`)
   2. `flask db migrate` (skip this command if migrations directory already exists)
   3. `flask db upgrade`
7. Now the Schema is created in the database and everything is set.
8. To start the project use `python3 run.py` or `flask run`
9. Click on the [Quora Blog](http://127.0.0.1:5000)
10. When you are done, for deleting the Role and Database named 'vijaydb' go to the directory `cd sql_scripts` form parent directory.
11. Now use the following commands
    1.  `sudo -su postgres`
    2.  `psql -U postgres -f drop_user-db.sql`

## About the Quora Blog
* Any user with/ without authentication can ask questions. If a user without authentication asks the question, it will be shown as asked by guest user. If a registered user asks the question, his name will be displayed.
* Only a registered user can answer the questions.
* Many users can answer a single question by clicking on the question.
* Registered user can update their user name or email address by visiting their profile section.
* Registered user can also Update/Delete the answer that he/she answered previously by visiting their profile section on Navigation Bar.
* Any Unanswered questions will be displayed in the right side section of home page. So that users who are interested can answer them by clicking on them.