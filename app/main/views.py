from . import main
from flask import render_template, redirect, url_for, flash, current_app, request

@main.route('/')
def index():
    return render_template('index.html')