from flask import render_template, request, redirect, session
from recipes_app import app
from recipes_app.models import User
from flask_bcrypt import Bcrypt
from flask import flash

from recipes_app.models import Recipe

bcrypt = Bcrypt(app)

@app.route("/", methods=['GET'])
def load_main_page():
    return render_template("index.html")

@app.route("/dashboard", methods=['GET'])
def load_dashboard_page():
    if 'user_id' not in session:
        return redirect('/')
    user_info = User.User.get_one(session['user_id'])
    print("This is the user info:",user_info)
    data = {
        "id": session['user_id'],
        "user_first_name": user_info[0]['first_name']
    }
    recipe_info = Recipe.Recipe.get_all_recipes()
    print()
    return render_template("dashboard.html", data=data, recipes = recipe_info)

@app.route("/user/add", methods=['POST'])
def add_new_user():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = request.form['password']
    encrypted_password = bcrypt.generate_password_hash(password)
    password_confirmation = request.form['confirm_password']


    if User.User.validate_registry(first_name, last_name, email, encrypted_password, password, password_confirmation):
        new_user = User.User(first_name, last_name, email, encrypted_password)
        User.User.add_new_user(new_user)
        return redirect("/")
    else:
        print("something went wrong")
        return redirect("/")

@app.route("/login", methods=['POST'])
def login_validation():
    email = request.form['login_email']
    password = request.form['login_password']

    result = User.User.validate_login(email)
    print("Reslt: ", result)
    if result == ():
        flash("email not registered")
        return render_template("index.html")
    else:
        database_password = result[0]['password']
        if result[0]['email'] == email:

            if bcrypt.check_password_hash(database_password, password):
                session.clear()
                data={
                    'user_id':result[0]['user_id'],
                    'user_first_name': result[0]['first_name']
                }
                session['user_id'] = result[0]['user_id']
                print(session['user_id'])
                return redirect("/dashboard")
            else:
                print("Not working")
                flash("Wrong password, try again")

    return redirect("/")

@app.route("/logout", methods=['GET'])
def logout_session():
    session.clear()
    return redirect("/")