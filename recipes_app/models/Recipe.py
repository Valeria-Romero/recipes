from flask import flash
from flask.globals import session
from werkzeug.utils import redirect
from recipes_app.config.MySQLConnection import connectToMySQL
from datetime import datetime


class Recipe:
    def __init__(self, recipe_id, name, description, instructions, under_30, made_on, created_at, updated_at):
        self.recipe_id = recipe_id
        self.name = name
        self.description = description
        self.instructions = instructions
        self.under_30 = under_30
        self.made_on = made_on
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def create_recipe(cls, data):
        print("Query receta")
        query = "INSERT INTO recipes(name,description,instructions,under_30,made_on,created_at,updated_at) VALUES(%(name)s,%(description)s, %(instructions)s, %(under30)s, %(made_on)s, SYSDATE(), SYSDATE());"
        data={
            "name":data['name'],
            "description": data['description'],
            "instructions": data['instructions'],
            "under30": data['under30'],
            "made_on": data['date_made'],
        }
        result = connectToMySQL('recipes').query_db(query, data)
        print("Result is",result)

        query = "INSERT INTO users_recipes(recipes_recipe_id,users_user_id) VALUES(%(recipes_recipe_id)s, %(users_user_id)s);"
        data={
            "recipes_recipe_id": result,
            "users_user_id": session['user_id']
        }

        insert_result = connectToMySQL('recipes').query_db(query, data)
        print("MANY to MANY result", insert_result)

        return redirect('/dashboard')
        
    @classmethod
    def get_all_recipes(cls):
        print("Loading recipes")
        query = "SELECT recipes.name, recipes.description, recipes.instructions, recipes.under_30, recipes.made_on, recipes.recipe_id, users.user_id, users.first_name FROM users JOIN users_recipes ON users.user_id = users_recipes.users_user_id JOIN recipes ON recipes.recipe_id = users_recipes.recipes_recipe_id;"
        result = connectToMySQL('recipes').query_db(query)
        return result

    @classmethod
    def get_recipe(cls, id):
        query = "SELECT recipe_id,name, description, under_30, instructions,made_on FROM recipes WHERE recipe_id = %(id)s;"
        data={
            "id": id
        }
        result = connectToMySQL('recipes').query_db(query,data)
        print (result)
        return result

    @classmethod
    def update_recipe(cls,data):
        query = "UPDATE recipes SET name = %(name)s, description=%(description)s, instructions=%(instructions)s , under_30 = %(under_30)s, made_on = %(made_on)s, updated_at = SYSDATE() WHERE recipe_id = %(recipe_id)s;"
        data={
            "name":data['name'],
            "description":data['description'],
            "instructions":data['instructions'],
            "made_on": data['made_on'],
            "under_30": data['under_30'],
            "recipe_id": data["recipe_id"]
        }

        result = connectToMySQL('recipes').query_db(query,data)
        return result

    @classmethod
    def delete_this_recipe(cls,id):
        data={
            "id":id
        }
        query = "DELETE from recipes WHERE recipe_id = %(id)s;"
        deleted_recipe = connectToMySQL('recipes').query_db(query,data)


        query = "DELETE FROM users_recipes WHERE recipes_recipe_id = %(id)s;"
        deleted_recipe2 = connectToMySQL('recipes').query_db(query,data)

        return deleted_recipe2, deleted_recipe

    @staticmethod
    def validateCreate(cls,data):
        isValid = True

        data={
            "name":data['name'],
            "description":data['description'],
            "instructions":data['instructions'],
            "made_on": data['made_on'],
            "under_30": data['under_30'],
            "recipe_id": data["recipe_id"]
        }

        if len(data['name']) < 3:
            flash("⚠ The Name must be at least 3 characters long")
            isValid = False
        if len(data['description']) < 3:
            flash("⚠ The description must be at least 3 characters long")
            isValid = False
        if len(data['instructions']) < 3:
            flash("⚠ The instructions must be at least 3 characters long")
            isValid = False
        if len(data['name']) == 0 or len(data['description']) == 0 or len(data['instructions']) == 0 or len(data['made_on']) == 0 or len(data['under_30']) == 0:
            flash("⚠ There is an empty data space try to fill it")
            isValid = False
        return isValid

    @staticmethod
    def validateUpdate(data):
        isValid = True

        if len(data['name']) < 3:
            flash("⚠ The Name must be at least 3 characters long")
            isValid = False
        if len(data['description']) < 3:
            flash("⚠ The description must be at least 3 characters long")
            isValid = False
        if len(data['instructions']) < 3:
            flash("⚠ The instructions must be at least 3 characters long")
            isValid = False
        if len(data['name']) == 0 or len(data['description']) == 0 or len(data['instructions']) == 0 or len(data['made_on']) == 0 or len(data['under_30']) == 0:
            flash("⚠ There is an empty data space try to fill it")
            isValid = False

        return isValid
