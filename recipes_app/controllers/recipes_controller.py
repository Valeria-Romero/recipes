from flask import render_template, request, redirect, session
from recipes_app import app
from recipes_app.models import Recipe, User

@app.route("/recipes/new", methods=['GET'])
def load_new_recipe_form():
    if 'user_id' not in session:
        return redirect("/")
    data={
        "id":session['user_id']
    }
    print(data)
    return render_template("create_recipes.html",data =data)

@app.route("/recipes/add", methods=['POST'])
def add_new_recipe():
    if 'user_id' not in session:
        return redirect("/")
    data={
    "name": request.form['recipe_name'],
    "description" : request.form['recipe_description'],
    "instructions" : request.form['recipe_instructions'],
    "date_made" : request.form["recipe_date"],
    "under30" : int(request.form['recipe_time']),
    "user_id": session['user_id']
    } 
    print("Receta")
    if Recipe.Recipe.validateCreate(data):
        Recipe.Recipe.create_recipe(data)
    return redirect('/dashboard')

@app.route("/view/recipe/<id>", methods=['GET'])
def view_recipe(id):
    if 'user_id' not in session:
        return redirect('/')
    user_info = User.User.get_one(session['user_id'])
    data = {
        "id": session['user_id'],
        "user_first_name": user_info[0]['first_name']
    }
    recipe_info = Recipe.Recipe.get_recipe(id)
    return render_template("recipe_info.html", recipe_info=recipe_info, data=data)


@app.route("/edit/<id>")
def edit_recipe(id):
    if 'user_id' not in session:
        return redirect('/')

    recipe_info = Recipe.Recipe.get_recipe(id)
    
    return render_template("edit_recipe.html", recipe_info=recipe_info) 

@app.route("/recipes/edit", methods=['POST'])
def send_edit_info():
    data={
    "name": request.form['recipe_name'],
    "description" : request.form['recipe_description'],
    "instructions" : request.form['recipe_instructions'],
    "made_on" : request.form["recipe_date"],
    "under_30" : int(request.form['recipe_time']),
    "recipe_id": request.form['recipe_id']
    } 
    if Recipe.Recipe.validateUpdate(data):
        Recipe.Recipe.update_recipe(data)

    return redirect ("/dashboard")

@app.route("/delete/<id>")
def delete_recipe(id):
    if 'user_id' not in session:
        return redirect('/')
    Recipe.Recipe.delete_this_recipe(id)
    return redirect ("/dashboard")
