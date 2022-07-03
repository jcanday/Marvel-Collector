from lib2to3.pgen2 import token
from flask import Blueprint, render_template, request, redirect, url_for, flash
from marvel.models import User, db, check_password_hash
from marvel.forms  import UserSignupForm
from marvel.forms import UserLoginForm

#imports from flask login
from flask_login import login_user, logout_user, current_user, login_required
auth = Blueprint('auth',__name__,template_folder='auth_templates')

@auth.route('/signup', methods = ['GET','POST'])
def signup():
    form = UserSignupForm()
    try:
        if request.method == "POST" and form.validate_on_submit():
            email = form.email.data
            name = form.name.data
            password = form.password.data
            print(name, email, password)

            user = User(email,name=name,password = password)

            db.session.add(user)
            db.session.commit()

            flash(f"You have succesfully created a user account {email}", 'user-created')

            return redirect(url_for('auth.signin'))
    except:
        raise Exception('Invalid Form Data: Please Check Your Form')   

    
    return render_template('signup.html', form=form)


@auth.route('/signin', methods = ['GET','POST'])
def signin():
    form = UserLoginForm()
    
    try:
        if request.method == "POST" and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email, password)
            
            logged_user = User.query.filter(User.email == email).first()
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                flash('You were successfully login in via Email/Password', 'auth-success')
                return redirect("/collections/" + str(logged_user.token))
            else:
                flash('Your Email/Password is incorrect', 'auth-failed')
                return redirect(url_for('auth.signin'))
            
    except:
        raise Exception('Invalid Form Dat: Please check your form.')
    
    
    return render_template('signin.html',form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))