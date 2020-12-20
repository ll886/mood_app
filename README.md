# neuroflow_rest_project

### Setting Up:

Make sure you have python installed.
https://www.python.org/downloads/  
Flask and its dependencies support Python 3.  
You need Python 3.3 or higher.  
https://flask.palletsprojects.com/en/0.12.x/python3/#:~:text=Flask%2C%20its%20dependencies%2C%20and%20most,and%20older%20are%20not%20supported.

#### IN THE PROJECT DIRECTORY:

#### Set up and run with docker (optional):

You can download docker at https://www.docker.com/

You can run with docker if you have it(optional):  
use "docker-compose up"  
after it loads everything, open web browser and test out the app at:  
http://127.0.0.1:5000/ or http://localhost:5000/  
or http://"your ipv4-address":5000

--OTHERWISE, IF NOT USING DOCKER, CONTINUE BELOW--

---

#### To set up the environment and application:

create virtual environment

to create virtual environment and activate it, run these commands:  
"python -m venv venv"  
"venv\scripts\activate" (OR if on MAC, use "source env/bin/activate")

THEN

to install required libraries:  
use "pip install -r requirements.txt"

#### Create the db

enter python interpreter

"from mood_app import db"

"db.create_all()"

"exit()" and proceed to run app

#### Run the application:

simply use "python run.py"

--OR--

If on Windows, run these commands:  
"set FLASK_APP=run.py"  
"flask run"

If on MAC, run these commands:  
"export FLASK_APP=run.py"  
"flask run"

#### Test on your browser:

The application should now be running on:  
http://127.0.0.1:5000/

In a web browser, go to http://127.0.0.1:5000/ or http://localhost:5000/
to test out the app

---

#### Documentation/Answer to Questions:

prompt:  
"Document what, if anything,  
you would do differently if this were a production application and not an assessment?  
What tech would you use?  
How would you handle things differently if it needed to handle more users, more data, etc?"

If this were a production application and not an assessment, I would focus a bit more on the front-end side. For this assessment, I used a simple bootstrap starter template (https://getbootstrap.com/docs/4.3/getting-started/introduction/) to get the project going so I could focus more on the Flask backend. I also think I would add more features for user personalization such as access to modify account details or password reset. For recording moods, some ideas I had while working on the project was implementing some sort of social media aspect so users can share their mood ratings publicly with other users on the platform or privately with a friend system.

As for the technology I would use for the app, I really enjoyed developing with Flask. At first, I was unfamiliar with creating REST applications and I looked at different options to create one with Python. The main options I saw were Django and Flask. After doing research, Flask seemed like the best option to start learning how to develop REST apps with python. It was straight forward to use and easy to pick up. This project was a good experience to work with REST applications and after working on it, I would stick to Flask in a production application unless I had a compelling reason to consider other options like Django.

If the app needed to handle more users and data, I would consider the various different database options. Currently, the project is using SQlite for development purposes. Flask SQLAlchemy can be configured to use other database engines (https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/). Popular database engines such as MySQL or PostgreSQL are potential options. SQLite can be limited and difficult to manage when handling lots of data since the entire database is stored in a single disk file. Using a client/server type database like MySQL would be better in this case. SQLite also only supports one writer to the database at a time and users' access to the database will be queued up if they happen concurrently (these processes are still extremely fast). Client/server databases can handle more write concurrency than SQLite. As for security, MySQL has built-in security features that would help with handle user authentication for the app and data encryption. Overall, I would use MySQL to handle more data, users, and security.
