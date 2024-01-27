# app/views.py
from flask import render_template

@app.route('/')
def home():
    return render_template('home.html')  # Or any response you desire
