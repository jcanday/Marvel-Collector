from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash
from flask_login.utils import login_required,current_user
from marvel.models import Character, db, User, Comment
from marvel.forms import CharAddForm, CommentForm
import json
main = Blueprint('main',__name__,template_folder="main-templates")

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/collections/<token>')
@login_required
def collections(token):
    form = CharAddForm()
    commentform = CommentForm()
    owner = token
    poster = current_user.name
    
    chars = Character.query.filter_by(user_token = owner).all()
    viewuser = User.query.filter(User.token == token).first()
    comments = Comment.query.filter_by(user_name = viewuser.token).all()
    others = User.query.filter(User.token != current_user.token).all()
    return render_template('collections.html', res = chars, form = form,comments = comments, commentform = commentform, owner=owner, token=token, others = others, viewuser = viewuser,poster=poster)

    

@main.route('/collections/<token>', methods = ['POST'])
@login_required
def add_character(token):
    form = CharAddForm()
    commentform = CommentForm()
    poster = current_user
    viewuser = User.query.filter(User.token == token).first()
    if form.name.data:
        try:
            if request.method == "POST":
                name = form.name.data
                desc = form.desc.data
                super_power = form.super_power.data
                comics_appeared = form.comics_appeared.data
                print(name,desc,super_power)

                char = Character(name,desc=desc,comics_appeared=comics_appeared,super_power=super_power,user_token=current_user.token)

                db.session.add(char)
                db.session.commit()

                flash(f"You have succesfully created character {name}", 'char-created')

                return redirect(f'/collections/{token}')
        except:
            raise Exception('Invalid Form Data: Please Check Your Form')
    else:
        try:
            if request.method == "POST":
                post = commentform.post.data
                name = poster.email
                on = viewuser.token
                print(poster.email)
                comment = Comment(post,user_name=on,poster = name)
                
                db.session.add(comment)
                db.session.commit()
                
                flash(f"You have succesfully commented {post}", 'comment-posted')
                
                return redirect(f'/collections/{token}')
        except:
            raise Exception("COmment Form Invalid")
    
    
    
@main.route('/collections/delete/<id>')
@login_required   
def del_character(id):
    char = Character.query.get(id)
    
    db.session.delete(char)
    
    db.session.commit()
    return redirect(f"/collections/{current_user.token}")
