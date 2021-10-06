from flask import Flask, render_template, request, redirect, session
from recipes_app.controllers import users_controller, recipes_controller
from recipes_app import app

if __name__ == "__main__":
    app.run( debug = True )