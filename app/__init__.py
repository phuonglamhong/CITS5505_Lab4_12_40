# This file initializes the Flask application, sets up the database connection, 
# and imports routes and models. 
# Using SQLAlchemy (switch from raw SQL to an ORM): Python classes = database tables, Class attributes = table columns, Automatic table creation, Cleaner, safer code
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy
db = SQLAlchemy()
app = Flask(__name__)

# Configuration with security (SECRET_KEY should be more secure in production)
app.config['SECRET_KEY'] = "mysecretkey"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///NewsSentimentDB.db" 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Import models so SQLAlchemy knows them
from app import models

# Import routes
from app import routes