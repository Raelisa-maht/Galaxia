from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from User import User
from AccountForms import CreateUserForm, LoginForm
import shelve
import os

app = Flask(__name__) #references the file

SECRET_KEY = os.urandom(24).hex()
app.config['SECRET_KEY'] = SECRET_KEY


# Helper functions
def load_users():
    with shelve.open('users', 'c') as shelf:
        return dict(shelf)


def save_users(users):
    with shelve.open('users', 'c') as shelf:
        for username, user in users.items():
            shelf[username] = user


# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    create_user_form = CreateUserForm(request.form)

    if request.method == 'POST' and create_user_form.validate():
        users = load_users()

        # Check if the username is already taken
        if create_user_form.username.data in users:
            flash('This username is already in use.')
            return render_template('signup.html', form=create_user_form)

        # Create a new user object
        user = User(create_user_form.username.data,
                    create_user_form.email.data,
                    create_user_form.password.data)

        users[create_user_form.username.data] = user
        save_users(users)
        return redirect('/')

    return render_template('signup.html', form=create_user_form)


@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        username = request.form['username']
        password = request.form['password']
        with shelve.open('users') as shelf:
            if username in shelf:
                user = shelf[username]
                if user.get_password() == password:
                    # Successful login
                    session['username'] = user.get_username()  # begin session with user
                    return redirect('/index')
                else:
                    flash('Password entered is incorrect.')
                    return render_template('login.html', form=form)
            else:
                flash('Username entered is not linked to any account.')
                return render_template('login.html', form=form)

    return render_template('login.html', form=form)
@app.route('/index')
def home():
    return render_template('index.html')

@app.route('/dialogue')
def level2():
    return render_template('dialogue.html')

@app.route('/L2question')
def level2_question():
    return render_template('L2question.html')

@app.route('/level2win')
def level2_win():
    return render_template('level2win.html')

@app.route('/L1question')
def level1_question():
    return render_template('L1question.html')

@app.route('/level1win')
def level1_win():
    return render_template('level1win.html')

@app.route("/yoda")
def yoda():
    return render_template("yoda_intro.html")


@app.route("/yoda_change_job")
def change_job():
    return render_template("yoda_change_job.html")
    
if __name__ == '__main__':
    app.run(debug=True)


