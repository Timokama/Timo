How to Use Flask-SQLAlchemy to Interact with Databases in a Flask Application
Published on March 10, 2022
Development
Flask
Python Frameworks
SQLite
Databases
Python
Default avatar
By Abdelhadi Dyouri

How to Use Flask-SQLAlchemy to Interact with Databases in a Flask Application
The author selected the Free and Open Source Fund to receive a donation as part of the Write for DOnations program.

Introduction
In web applications, you usually need a database, which is an organized collection of data. You use a database to store and maintain persistent data that can be retrieved and manipulated efficiently. For example, in a social media application, you have a database where user data (personal information, posts, comments, followers) is stored in a way that can be efficiently manipulated. You can add data to a database, retrieve it, modify it, or delete it, depending on different requirements and conditions. In a web application, these requirements might be a user adding a new post, deleting a post, or deleting their account, which may or may not delete their posts. The actions you perform to manipulate data will depend on specific features in your application. For example, you might not want users to add posts with no titles.

Flask is a lightweight Python web framework that provides useful tools and features for creating web applications in the Python Language. SQLAlchemy is an SQL toolkit that provides efficient and high-performing database access for relational databases. It provides ways to interact with several database engines such as SQLite, MySQL, and PostgreSQL. It gives you access to the database’s SQL functionalities. It also gives you an Object Relational Mapper (ORM), which allows you to make queries and handle data using simple Python objects and methods. Flask-SQLAlchemy is a Flask extension that makes using SQLAlchemy with Flask easier, providing you tools and methods to interact with your database in your Flask applications through SQLAlchemy.

In this tutorial, you’ll build a small student management system that demonstrates how to use the Flask-SQLAlchemy extension. You’ll use it with Flask to perform basic tasks, such as connecting to a database server, creating a table, adding data to your table, retrieving it, and updating and deleting items from your database. You’ll use SQLAlchemy with SQLite, although you can use it with other database engines too, such as PostgreSQL and MySQL. SQLite works well with Python because the Python standard library provides the sqlite3 module, which is used by SQLAlchemy behind the scenes to interact with SQLite databases without having to install anything. SQlite is installed on Linux systems by default, and is installed as part of the Python package on Windows.

Prerequisites
A local Python 3 programming environment. Follow the tutorial for your distribution in How To Install and Set Up a Local Programming Environment for Python 3 series. In this tutorial we’ll call our project directory flask_app.

An understanding of basic Flask concepts, such as routes, view functions, and templates. If you are not familiar with Flask, check out How to Create Your First Web Application Using Flask and Python and How to Use Templates in a Flask Application.

An understanding of basic HTML concepts. You can review our How To Build a Website with HTML tutorial series for background knowledge.

Step 1 — Installing Flask and Flask-SQLAlchemy
In this step, you’ll install the necessary packages for your application.

With your virtual environment activated, use pip to install Flask and Flask-SQLAlchemy:

pip install Flask Flask-SQLAlchemy
Once the installation is successfully finished, you’ll see a line similar to the following at the end of the output:

Output
Successfully installed Flask-2.0.3 Flask-SQLAlchemy-2.5.1 Jinja2-3.0.3 MarkupSafe-2.1.0 SQLAlchemy-1.4.31 Werkzeug-2.0.3 click-8.0.4 greenlet-1.1.2 itsdangerous-2.1.0
With the required Python packages installed, you’ll set up the database next.

Step 2 — Setting up the Database and Model
In this step, you’ll set up your database connection, and create an SQLAlchemy database model, which is a Python class that represents the table that stores your data. You’ll initiate the database, create a table for students based on the model you’ll declare, and add a few students into your students table.

Setting up The Database Connection
Open a file called app.py in your flask_app directory. This file will have code for setting up the database and your Flask routes:

nano app.py
This file will connect to an SQLite database called database.db, and have a class called Student that represents your database students table for storing student information, in addition to your Flask routes. Add the following import statements at the top of app.py:

flask_app/app.py
import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.sql import func
Here, you import the os module, which gives you access to miscellaneous operating system interfaces. You’ll use it to construct a file path for your database.db database file.

From the flask package, you then import the necessary helpers you need for your application: the Flask class to create a Flask application instance, the render_template() function to render templates, the request object to handle requests, the url_for() function to construct URLs for routes, and the redirect() function for redirecting users. For more information on routes and templates, see How To Use Templates in a Flask Application.

You then import the SQLAlchemy class from the Flask-SQLAlchemy extension, which gives you access to all the functions and classes from SQLAlchemy, in addition to helpers, and functionality that integrates Flask with SQLAlchemy. You’ll use it to create a database object that connects to your Flask application, allowing you to create and manipulate tables using Python classes, objects, and functions without needing to use the SQL language.

You also import the func helper from the sqlalchemy.sql module to access SQL functions. You’ll need it in your student management system to set a default creation date and time for when a student record is created.

Below the imports, you’ll set up a database file path, instantiate your Flask application, and configure and connect your application with SQLAlchemy. Add the following code:

flask_app/app.py

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Here, you construct a path for your SQLite database file. You first define a base directory as the current directory. You use the os.path.abspath() function to get the absolute path of the current file’s directory. The special __file__ variable holds the pathname of the current app.py file. You store the absolute path of the base directory in a variable called basedir.

You then create a Flask application instance called app, which you use to configure two Flask-SQLAlchemy configuration keys:

SQLALCHEMY_DATABASE_URI: The database URI to specify the database you want to establish a connection with. In this case, the URI follows the format sqlite:///path/to/database.db. You use the os.path.join() function to intelligently join the base directory you constructed and stored in the basedir variable, and the database.db file name. This will connect to a database.db database file in your flask_app directory. The file will be created once you initiate the database.

SQLALCHEMY_TRACK_MODIFICATIONS: A configuration to enable or disable tracking modifications of objects. You set it to False to disable tracking and use less memory. For more, see the configuration page in the Flask-SQLAlchemy documentation.

Note:

If you want to use another database engine such as PostgreSQL or MySQL, you’ll need to use the proper URI.

For PostgreSQL, use the following format:

postgresql://username:password@host:port/database_name
For MySQL:

mysql://username:password@host:port/database_name
For more, see the SQLAlchemy documentation for engine configuration.

After configuring SQLAlchemy by setting a database URI and disabling tracking, you create a database object using the SQLAlchemy class, passing the application instance to connect your Flask application with SQLAlchemy. You store your database object in a variable called db. You’ll use this db object to interact with your database.

Declaring The Table
With the database connection established and the database object created, you’ll use the database object to create a database table for students, which is represented by a model — a Python class that inherits from a base class Flask-SQLAlchemy provides through the db database instance you created earlier. To define a student table as a model, add the following class to your app.py file:

flask_app/app.py
# ...

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    age = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    bio = db.Column(db.Text)

    def __repr__(self):
        return f'<Student {self.firstname}>'
Here, you create a Student model, which inherits from the db.Model class. This represents the student table. You use the db.Column class to define columns for your table. The first argument represents the column type, and additional arguments represent column configuration.

You define the following columns for the Student model:

id: The student ID. You define it as an integer with db.Integer. primary_key=True defines this column as a primary key, which will assign it a unique value by the database for each entry (that is a student).
firstname: The student’s first name. A string with a maximum length of 100 characters. nullable=False signifies that this column should not be empty.
lastname: The student’s last name. A string with a maximum length of 100 characters. nullable=False signifies that this column should not be empty.
email: The student’s email. A string with a maximum length of 80 characters. unique=True signifies that each email should be unique for each student. nullable=False signifies that this column should not be empty.
age: The student’s age.
created_at: The time the student record was created at in the database. You use db.DateTime to define it as a Python datetime object. timezone=True enables timezone support. server_default sets the default value in the database when creating the table, so that default values are handled by the database rather than the model. You pass it the func.now() function which calls the SQL now() datetime function. In SQLite, it is rendered as CURRENT_TIMESTAMP when creating the student table.
bio: The student’s bio. db.Text() indicates the column holds long texts.
See the SQLAlchemy documentation for column types other than the types you used in the preceding code block.

The special __repr__ function allows you to give each object a string representation to recognize it for debugging purposes. In this case you use the student’s first name.

The app.py file will now look as follows:

flask_app/app.py
import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.sql import func


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    age = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    bio = db.Column(db.Text)

    def __repr__(self):
        return f'<Student {self.firstname}>'
Save and close app.py.

Creating the Database
Now that you’ve set the database connection and the student model, you’ll use the Flask shell to create your database and your student table based on the Student model.

With your virtual environment activated, set the app.py file as your Flask application using the FLASK_APP environment variable. Then open the Flask shell using the following command in your flask_app directory:

export FLASK_APP=app
flask shell
A Python interactive shell will be opened. This special shell runs commands in the context of your Flask application, so that the Flask-SQLAlchemy functions you’ll call are connected to your application.

Import the database object and the student model, and then run the db.create_all() function to create the tables that are associated with your models. In this case you only have one model, which means that the function call will only create one table in your database:

from app import db, Student
db.create_all()
Leave the shell running, open another terminal window and navigate to your flask_app directory. You will now see a new file called database.db in flask_app.

Note:

The db.create_all() function does not recreate or update a table if it already exists. For example, if you modify your model by adding a new column, and run the db.create_all() function, the change you make to the model will not be applied to the table if the table already exists in the database. The solution is to delete all existing database tables with the db.drop_all() function and then recreate them with the db.create_all() function like so:

db.drop_all()
db.create_all()
This will apply the modifications you make to your models, but will also delete all the existing data in the database. To update the database and preserve existing data, you’ll need to use schema migration, which allows you to modify your tables and preserve data. You can use the Flask-Migrate extension to perform SQLAlchemy schema migrations through the Flask command-line interface.

If you receive an error, make sure your database URI and your model declaration are correct.

Populating the Table
After creating the database and student table, you’ll use the flask shell to add some students to your database through the Student model.

Use the same flask shell you opened earlier, or open a new one with your virtual environment activated in your flask_app directory:

flask shell
To add a student to your database, you’ll import the database object and the Student model, and create an instance of the Student model, passing it student data through keyword arguments as follows:

from app import db, Student
student_john = Student(firstname='john', lastname='doe',
                       email='jd@example.com', age=23,
                       bio='Biology student')
The student_john object represents a student that will be added to the database, but this object has not been written to the database yet. Check out the object in the flask shell to see its representation string you constructed with the __repr__() method:

student_john
You’ll receive the following output:

Output
<Student john>
You can get the value of columns using the class attributes you defined in the Student model:

student_john.firstname
student_john.bio
Output
'john'
'Biology student'
Because this student has not been added to the database yet, its ID will be None:

print(student_john.id)
Output
None
To add this student to the database, you’ll first need to add it to a database session, which manages a database transaction. Flask-SQLAlchemy provides the db.session object through which you can manage your database changes. Add the student_john object to the session using the db.session.add() method to prepare it to be written to the database:

db.session.add(student_john)
This will issue an INSERT statement, but you won’t get an ID back because the database transaction is still not committed. To commit the transaction and apply the change to database, use the db.session.commit() method:

db.session.commit()
Now that student John is added to the database, you can get its ID:

print(student_john.id)
Output
1
You can also use the db.session.add() method to edit an item in the database. For example, you can modify the student’s email like so:

student_john.email = 'john_doe@example.com'
db.session.add(student_john)
db.session.commit()
Use the Flask shell to add a few more students to your database:

sammy = Student(firstname='Sammy',
               lastname='Shark',
               email='sammyshark@example.com',
               age=20,
               bio='Marine biology student')

carl = Student(firstname='Carl',
               lastname='White',
               email='carlwhite@example.com',
               age=22,
               bio='Marine geology student')

db.session.add(sammy)
db.session.add(carl)
db.session.commit()
Now, you can query all the records in the student table using the query attribute with the all() method:

Student.query.all()
You’ll receive the following output:

Output
[<Student john>, <Student Sammy>, <Student Carl>]
At this point, you have three students in your database. Next, you’ll create a Flask route for the index page and display all of the students in your database on it.

Step 3 — Displaying All Records
In this step, you’ll create a route and a template to display all the students in the database on the index page.

Leave the Flask shell running and open a new terminal window.

Open your app.py file to add a route for the index page to it:

nano app.py
Add the following route at the end of the file:

flask_app/app.py

# ...

@app.route('/')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)
Save and close the file.

Here, you create an index() view function using the app.route() decorator. In this function, you query the database and get all the students using the Student model with the query attribute, which allows you to retrieve one or more items from the database using different methods. You use the all() method to get all student entries in the database. You store the query result in a variable called students and pass it to a template called index.html that you render using the render_template() helper function.

Before you create the index.html template file on which you’ll display the existing students in the database, you’ll first create a base template, which will have all the basic HTML code other templates will also use to avoid code repetition. Then you’ll create the index.html template file you rendered in your index() function. To learn more about templates, see How to Use Templates in a Flask Application.

Create a templates directory, then open a new template called base.html:

mkdir templates
nano templates/base.html
Add the following code inside the base.html file:

flask_app/templates/base.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{% block title %} {% endblock %} - FlaskApp</title>
    <style>
        .title {
            margin: 5px;
        }

        .content {
            margin: 5px;
            width: 100%;
            display: flex;
            flex-direction: row;
            flex-wrap: wrap;
        }

        .student {
            flex: 20%;
            padding: 10px;
            margin: 5px;
            background-color: #f3f3f3;
            inline-size: 100%;
        }

        .bio {
            padding: 10px;
            margin: 5px;
            background-color: #ffffff;
            color: #004835;
        }

        .name a {
            color: #00a36f;
            text-decoration: none;
        }

        nav a {
            color: #d64161;
            font-size: 3em;
            margin-left: 50px;
            text-decoration: none;
        }
    </style>
</head>
<body>
    <nav>
        <a href="{{ url_for('index') }}">FlaskApp</a>
        <a href="#">Create</a>
        <a href="#">About</a>
    </nav>
    <hr>
    <div class="content">
        {% block content %} {% endblock %}
    </div>
</body>
</html>
Save and close the file.

This base template has all the HTML boilerplate you’ll need to reuse in your other templates. The title block will be replaced to set a title for each page, and the content block will be replaced with the content of each page. The navigation bar has three links: one for the index page, which links to the index() view function using the url_for() helper function, one for a Create page, and one for an About page if you choose to add one to your application. You’ll edit this file later after you add a page for creating new students to make the Create link functional.

Next, open a new index.html template file. This is the template you referenced in the app.py file:

nano templates/index.html
Add the following code to it:

flask_app/templates/index.html
{% extends 'base.html' %}

{% block content %}
    <h1 class="title">{% block title %} Students {% endblock %}</h1>
    <div class="content">
        {% for student in students %}
            <div class="student">
                <p><b>#{{ student.id }}</b></p>
                <b>
                    <p class="name">{{ student.firstname }} {{ student.lastname }}</p>
                </b>
                <p>{{ student.email }}</p>
                <p>{{ student.age }} years old.</p>
                <p>Joined: {{ student.created_at }}</p>
                <div class="bio">
                    <h4>Bio</h4>
                    <p>{{ student.bio }}</p>
                </div>
            </div>
        {% endfor %}
    </div>
{% endblock %}
Save and close the file.

Here, you extend the base template and replace the contents of the content block. You use an <h1> heading that also serves as a title. You use a Jinja for loop in the line {% for student in students %} to go through each student in the students variable that you passed from the index() view function to this template. You display the student ID, their first and last name, email, age, the date at which they were added to the database, and their bio.

While in your flask_app directory with your virtual environment activated, tell Flask about the application (app.py in this case) using the FLASK_APP environment variable. Then set the FLASK_ENV environment variable to development to run the application in development mode and get access to the debugger. For more information about the Flask debugger, see How To Handle Errors in a Flask Application. Use the following commands to do this:

export FLASK_APP=app
export FLASK_ENV=development
Next, run the application:

flask run
With the development server running, visit the following URL using your browser:

http://127.0.0.1:5000/
You’ll see the students you added to the database in a page similar to the following:

Index Page

You’ve displayed the students you have in your database on the index page. Next, you’ll create a route for a student page, where you can display the details of each individual student.

Step 4 — Displaying a Single Record
In this step, you’ll use the Flask shell to query students by their ID, and create a route and a template to display the details of each student on a dedicated page.

By the end of this step, the URL http://127.0.0.1:5000/1 will be a page that displays the first student (because it has the ID 1). The URL http://127.0.0.1:5000/ID will display the post with the associated ID number, if it exists.

Leave the development server running and open a new terminal window.

Open the Flask shell for a demonstration of how to query students:

flask shell
To query records and retrieve data from the database, Flask-SQLAlchemy provides a query attribute on the model class. You can use its methods to get records with a specific filter.

For example, you can use the filter_by() method with a parameter such as firstname that matches a column in the table with an argument to retrieve a specific student:

from app import db, Student
Student.query.filter_by(firstname='Sammy').all()
Output
[<Student Sammy>]
Here you retrieve all the students with Sammy as their first name. You use the all() method to get a list of all the results. To get the first result, which is the only result here, you can use the first() method:

Student.query.filter_by(firstname='Sammy').first()
Output
<Student Sammy>
To get a student by its ID, you can use filter_by(id=ID):

Student.query.filter_by(id=3).first()
Or, you can use the shorter get() method, which allows you to retrieve a specific item using its primary key:

Student.query.get(3)
Both will give the same output:

Output
<Student Carl>
You can now exit the shell:

exit()
To retrieve a student by their ID, you’ll create a new route that renders a page for each individual student. You’ll use the get_or_404() method Flask-SQLAlchemy provides, which is a variant of the get() method. The difference is that get() returns the value None when no result matches the given ID, and get_or_404() returns a 404 Not Found HTTP response. Open app.py for modification:

nano app.py
Add the following route at the end of the file:

flask_app/app.py
# ...

@app.route('/<int:student_id>/')
def student(student_id):
    student = Student.query.get_or_404(student_id)
    return render_template('student.html', student=student)
Save and close the file.

Here, you use the route '/<int:student_id>/', with int: being a converter that converts the default string in the URL into an integer. And student_id is the URL variable that will determine the student you’ll display on the page.

The ID is passed from the URL to the student() view function through the student_id parameter. Inside the function, you query the students collection and retrieve a student by the ID using the get_or_404() method. This will save the student data in the student variable if it exists, and respond with a 404 Not Found HTTP error if no student with the given ID exists in the database.

You render a template called student.html and pass it the student you retrieved.

Open this new student.html template file:

nano templates/student.html
Type the following code in this new student.html file. This will be similar to the index.html template, except that it will only display a single student:

flask_app/templates/student.html
{% extends 'base.html' %}

{% block content %}
    <span class="title">
        <h1>{% block title %} {{ student.firstname }} {{ student.lastname }}{% endblock %}</h1>
    </span>
    <div class="content">
            <div class="student">
                <p><b>#{{ student.id }}</b></p>
                <b>
                    <p class="name">{{ student.firstname }} {{ student.lastname }}</p>
                </b>
                <p>{{ student.email }}</p>
                <p>{{ student.age }} years old.</p>
                <p>Joined: {{ student.created_at }}</p>
                <div class="bio">
                    <h4>Bio</h4>
                    <p>{{ student.bio }}</p>
                </div>
            </div>
    </div>
{% endblock %}
Save and close the file.

In this file, you extend the base template, setting the student’s full name as a title for the page. You display the student ID, the student’s first and last name, email, age, the date of record creation, and their bio.

Use your browser to navigate to the URL for the second student:

http://127.0.0.1:5000/2
You’ll see a page similar to the following:

Single Student Page

Now, edit index.html to make each student name link to their page:

nano templates/index.html
Edit the for loop to look as follows:

flask_app/templates/index.html
{% for student in students %}
    <div class="student">
        <p><b>#{{ student.id }}</b></p>
        <b>
            <p class="name">
                <a href="{{ url_for('student', student_id=student.id)}}">
                    {{ student.firstname }} {{ student.lastname }}
                </a>
            </p>
        </b>
        <p>{{ student.email }}</p>
        <p>{{ student.age }} years old.</p>
        <p>Joined: {{ student.created_at }}</p>
        <div class="bio">
            <h4>Bio</h4>
            <p>{{ student.bio }}</p>
        </div>
    </div>
{% endfor %}
Save and close the file.

You added an <a> tag to the student’s full name which links to the student page using the url_for() function, passing the student ID that’s stored in student.id to the student() view function.

Navigate to your index page or refresh it:

http://127.0.0.1:5000/
You’ll now see that each student name links to the proper student page.

After creating a page for individual students, you’ll next add a page for adding new students to the database.

Step 5 — Creating a New Record
In this step, you’ll add a new route to your application for adding new students to the database using web forms.

You’ll render a page with a web form where users enter the student’s data. Then you’ll handle the form submission, create an object for the new student using the Student model, add it to the session, then commit the transaction, similar to how you’ve added student entries in Step 2.

Leave the development server running and open a new terminal window.

First, open your app.py file:

nano app.py
Add the following route at the end of the app.py file:

flask_app/app.py
# ...


@app.route('/create/', methods=('GET', 'POST'))
def create():
    return render_template('create.html')
Save and close the file.

In this route, you pass the tuple ('GET', 'POST') to the methods parameter to allow both GET and POST requests. GET requests are used to retrieve data from the server. POST requests are used to post data to a specific route. By default, only GET requests are allowed. When the user first requests the /create route using a GET request, a template file called create.html will be rendered. You will later edit this route to handle POST requests for when users fill in and submit the web form for adding new students.

Open the new create.html template:

nano templates/create.html
Add the following code to it:

{% extends 'base.html' %}

{% block content %}
    <h1 style="width: 100%">{% block title %} Add a New Student {% endblock %}</h1>
    <form method="post">
        <p>
            <label for="firstname">First Name</label>
            <input type="text" name="firstname"
                   placeholder="First name">
            </input>
        </p>

        <p>
            <label for="lastname">Last Name</label>
            <input type="text" name="lastname"
                   placeholder="Last name">
            </input>
        </p>

        <p>
            <label for="email">Email</label>
            <input type="email" name="email"
                   placeholder="Student email">
            </input>
        </p>

        <p>
            <label for="age">Age</label>
            <input type="number" name="age"
                   placeholder="Age">
            </input>
        </p>

        <p>
        <label for="bio">Bio</label>
        <br>
        <textarea name="bio"
                  placeholder="Bio"
                  rows="15"
                  cols="60"
                  ></textarea>
        </p>
        <p>
            <button type="submit">Submit</button>
        </p>
    </form>
{% endblock %}
Save and close the file.

You extend the base template, set a heading as a title, and use a <form> tag with the attribute method set to post to indicate that the form will submit a POST request.

You have two text fields with the names firstname and lastname. You’ll use these names to access the form data the user submits in your view function later.

You have an email field with the name email, a number field for the student’s age, and a text area for the student’s bio.

Last, you have a Submit button at the end of the form.

Now, with the development server running, use your browser to navigate to the /create route:

http://127.0.0.1:5000/create
You will see an Add a New Student page with a web form and a Submit button like so:

Add a New Student

If you fill in the form and submit it, sending a POST request to the server, nothing happens because you did not handle POST requests on the /create route.

Open app.py to handle the POST request the user submits:

nano app.py
Edit the /create route to look as follows:

flask_app/app.py

@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        age = int(request.form['age'])
        bio = request.form['bio']
        student = Student(firstname=firstname,
                          lastname=lastname,
                          email=email,
                          age=age,
                          bio=bio)
        db.session.add(student)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('create.html')
Save and close the file.

You handle POST requests inside the if request.method == 'POST' condition. You extract the first name, last name, email, age, and bio the user submits from the request.form object. You convert the age that gets passed as a string into an integer using the int() Python function. You construct a student object using the Student model. You add the student object to the database session, then commit the transaction.

Lastly, you redirect the user to the index page where they can see the newly added student below the existing students.

With the development server running, use your browser to navigate to the /create route:

http://127.0.0.1:5000/create
Fill in the form with some data and submit it.

You’ll be redirected to the index page where you’ll see your newly added student.

Now that you have the functionality to add new students, you’ll need to add a link to the Create page in the navigation bar. Open base.html:

nano templates/base.html
Edit the <body> tag by modifying the value of the href attribute for the Create link:

flask_app/templates/base.html
<body>
    <nav>
        <a href="{{ url_for('index') }}">FlaskApp</a>
        <a href="{{ url_for('create') }}">Create</a>
        <a href="#">About</a>
    </nav>
    <hr>
    <div class="content">
        {% block content %} {% endblock %}
    </div>
</body>
Save and close the file.

Refresh your index page and you’ll notice the Create link in the navigation bar is now functional.

You now have a page with a web form for adding new students. For more on web forms, see How To Use Web Forms in a Flask Application. For a more advanced and more secure method of managing web forms, see How To Use and Validate Web Forms with Flask-WTF. Next, you’ll add a page for editing the data of existing students.

Step 6 — Editing a Record
In this step, you’ll add a new page to your application for editing existing student data. You’ll add a new /ID/edit/ route to edit the data of students based on their ID.

Open app.py:

nano app.py
Add the following route to the end of the file. This fetches the student entry you want to edit using its ID. It extracts the new student data submitted via a web form you’ll will create later. Then it edits the student data, and redirects the user to the index page:

flask_app/app.py
# ...


@app.route('/<int:student_id>/edit/', methods=('GET', 'POST'))
def edit(student_id):
    student = Student.query.get_or_404(student_id)

    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        age = int(request.form['age'])
        bio = request.form['bio']

        student.firstname = firstname
        student.lastname = lastname
        student.email = email
        student.age = age
        student.bio = bio

        db.session.add(student)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('edit.html', student=student)
Save and close the file.

Here, you have the route /<int:student_id>/edit/ that accepts both POST and GET methods, with student_id as a URL variable that passes the ID to the edit() view function.

You use the get_or_404() query method on the Student model to get the student associated with the given student ID. This will respond with a 404 Not Found error in case no student with the given ID exists in the database.

If the given ID has a student associated with it, code execution continues to the if request.method == 'POST' condition. If the request was a GET request, meaning that the user did not submit a form, then this condition is false, and the code inside it will be skipped to the line return render_template('edit.html', student=student). This renders an edit.html template, passing it the student object you got from the database, allowing you to fill the student web form with current student data. You will create this edit.html template later.

When a user edits student data and submits the form, the code inside the if request.method == 'POST' is executed. You extract the submitted student data from the request.form object into corresponding variables. You set each attribute of the student object to the newly submitted data to change column values as you’ve done in Step 2. If no change was performed on a field on the web form, the value of that column will stay the same in the database.

After you set the student data to the newly submitted data, you add the student object to the database session, then you commit the changes. Lastly, you redirect the user to the index page.

Next, you need to create a page where users can do the editing. Open a new edit.html template:

nano templates/edit.html
This new file will have a web form similar to the one that’s in the create.html file with current student data as default values for the fields. Add the following code inside it:

flask_app/templates/edit.html

{% extends 'base.html' %}

{% block content %}
    <h1 style="width: 100%">
        {% block title %} Edit {{ student.firstname }}
                               {{ student.lastname }}'s Details
        {% endblock %}
    </h1>
    <form method="post">
        <p>
            <label for="firstname">First Name</label>
            <input type="text" name="firstname"
                   value={{ student.firstname }}
                   placeholder="First name">
            </input>
        </p>

        <p>
            <label for="lastname">Last Name</label>
            <input type="text" name="lastname"
                   value={{ student.lastname }}
                   placeholder="Last name">
            </input>
        </p>

        <p>
            <label for="email">Email</label>
            <input type="email" name="email"
                   value={{ student.email }}
                   placeholder="Student email">
            </input>
        </p>

        <p>
            <label for="age">Age</label>
            <input type="number" name="age"
                   value={{ student.age }}
                   placeholder="Age">
            </input>
        </p>

        <p>
        <label for="bio">Bio</label>
        <br>
        <textarea name="bio"
                  placeholder="Bio"
                  rows="15"
                  cols="60"
                  >{{ student.bio }}</textarea>
        </p>
        <p>
            <button type="submit">Submit</button>
        </p>
    </form>
{% endblock %}
Save and close the file.

The title has the student’s first name and last name. The value attribute of each input field and the value of the bio text area are set to the corresponding value in the student object you passed from the edit() view function to the edit.html template.

Now, navigate to the following URL to edit the first student’s details:

http://127.0.0.1:5000/1/edit
You will see a page similar to the following:

Edit a Student

Edit the student’s data and submit the form. You’ll be redirected to the index page, and the student’s information will be updated.

Next, you’ll add an Edit button below each student on the index page to link to their edit page. Open the index.html template file:

nano templates/index.html
Edit the for loop in this index.html file to look exactly like the following:

flask_app/templates/index.html

{% for student in students %}
    <div class="student">
        <p><b>#{{ student.id }}</b></p>
        <b>
            <p class="name">
                <a href="{{ url_for('student', student_id=student.id)}}">
                    {{ student.firstname }} {{ student.lastname }}
                </a>
            </p>
        </b>
        <p>{{ student.email }}</p>
        <p>{{ student.age }} years old.</p>
        <p>Joined: {{ student.created_at }}</p>
        <div class="bio">
            <h4>Bio</h4>
            <p>{{ student.bio }}</p>
        </div>
        <a href="{{ url_for('edit', student_id=student.id) }}">Edit</a>
    </div>
{% endfor %}
Save and close the file.

Here you add an <a> tag to link to the edit() view function, passing in the student.id value to link to the edit page of each student with an Edit link.

You now have a page for editing existing students. Next, you’ll add a Delete button to delete students from the database.

Step 7 — Deleting a Record
In this step, you’ll add a new route and Delete button for deleting existing students.

First, you’ll add a new /id/delete route that accepts POST requests. Your new delete() view function will receive the ID of the student you want to delete, pass the ID to the get_or_404() query method on the Student model to get it if it exists, or respond with a 404 Not Found page if no student with the given ID was found on the database.

Open app.py for editing:

nano app.py
Add the following route to the end of the file:

flask_app/app.py

# ...

@app.post('/<int:student_id>/delete/')
def delete(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('index'))
Save and close the file.

Here, instead of using the usual app.route decorator, you use the app.post decorator introduced in Flask version 2.0.0, which added shortcuts for common HTTP methods. For example, @app.post("/login") is a shortcut for @app.route("/login", methods=["POST"]). This means that this view function only accepts POST requests, and navigating to the /ID/delete route on your browser will return a 405 Method Not Allowed error, because web browsers default to GET requests. To delete a student, the user clicks on a button that sends a POST request to this route.

This delete() view function receives the ID of the student to be deleted via the student_id URL variable. You use the get_or_404() method to get a student and save it in a student variable, or respond with a 404 Not Found in case the student doesn’t exist. You use the delete() method on the database session in the line db.session.delete(student), passing it the student object. This sets up the session to delete the student whenever the transaction is committed. Because you don’t need to perform any other modifications, you directly commit the transaction using db.session.commit(). Lastly, you redirect the user to the index page.

Next, edit the index.html template to add a Delete Student button:

nano templates/index.html
Edit the for loop by adding a new <form> tag directly below the Edit link:

flask_app/templates/index.html

{% for student in students %}
    <div class="student">
        <p><b>#{{ student.id }}</b></p>
        <b>
            <p class="name">
                <a href="{{ url_for('student', student_id=student.id)}}">
                    {{ student.firstname }} {{ student.lastname }}
                </a>
            </p>
        </b>
        <p>{{ student.email }}</p>
        <p>{{ student.age }} years old.</p>
        <p>Joined: {{ student.created_at }}</p>
        <div class="bio">
            <h4>Bio</h4>
            <p>{{ student.bio }}</p>
        </div>
        <a href="{{ url_for('edit', student_id=student.id) }}">Edit</a>

        <hr>
        <form method="POST"
                action="{{ url_for('delete', student_id=student.id) }}">
            <input type="submit" value="Delete Student"
                onclick="return confirm('Are you sure you want to delete this entry?')">
        </form>

    </div>
{% endfor %}
Save and close the file.

Here, you have a web form that submits a POST request to the delete() view function. You pass student.id as an argument for the student_id parameter to specify the student entry to be deleted. You use the confirm() method function available in web browsers to display a confirmation message before submitting the request.

Now refresh your index page.

You’ll see a Delete Student button below each student entry. Click on it, and confirm the deletion. You’ll be redirected to the index page, and the student will no longer be there.

You now have a way of deleting students from the database in your student management application.

Conclusion
You built a small Flask web application for managing students using Flask and Flask-SQLAlchemy with an SQLite database. You learned how to connect to your database, set up database models that represent your tables, add items to your database, query your table, and modify database data.

Using SQLAlchemy in your application allows you to use Python classes and objects to manage your SQL database. Instead of SQLite, you can use another database engine, and other than the SQLALCHEMY_DATABASE_URI configuration responsible for the connection, you don’t need to change anything in your core application code. That allows you to move from one SQL database engine to another with minimal code change. See the Flask-SQLAlchemy documentation for more information.

If you would like to read more about Flask, check out the other tutorials in the How To Build Web Applications with Flask series.