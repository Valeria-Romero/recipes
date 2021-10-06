from flask import flash, session
from recipes_app.config.MySQLConnection import connectToMySQL
import re

class User:
    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    @classmethod
    def add_new_user(cls, new_user):
        query = "INSERT INTO users(first_name, last_name, email, password) VALUES (%(first_name)s,%(last_name)s,%(email)s, %(password)s);"
        data={
            "first_name": new_user.first_name,
            "last_name": new_user.last_name,
            "email": new_user.email,
            "password": new_user.password
        }

        result = connectToMySQL("recipes").query_db(query,data)
        return result

    @classmethod
    def validate_login(cls, login_information):
        isValid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"

        email={
            "email": login_information
        }

        result = connectToMySQL('recipes').query_db(query,email)
        
        return result

    @classmethod
    def get_one(cls,data):
        query = "SELECT first_name FROM users WHERE user_id = %(id)s;"
        data = {
            "id": session['user_id'],
        }
        results = connectToMySQL('recipes').query_db(query,data)
        return results

    @staticmethod
    def validate_registry( first_name, last_name, email,encrypted_password, password, password_confirmation):
        isValid = True
        
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        query = "SELECT * FROM users WHERE email = %(email)s;"
        emaildata = {
                "email" : email,
            }
        results = connectToMySQL('recipes').query_db(query,emaildata)

        if len(results)>=1:
            flash("Email already registered")
            isValid = False

        if len( first_name ) < 2:
            flash( "First name must be at least 2 characters long" )
            isValid = False 

        if len( last_name ) < 2:
            flash( "Last name must be at least 2 characters long")
            isValid = False

        if not EMAIL_REGEX.match(email):
            flash("Invalid email, please write email in valid format")
            isValid = False

        if len(password) < 8:
            flash("Password must be at least 8 characters long")
            isValid = False

        if password != password_confirmation:
            flash("Passwords must match, try again")
            isValid = False
        return isValid