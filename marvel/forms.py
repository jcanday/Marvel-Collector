from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

class UserLoginForm(FlaskForm):
    #email, password, submit_button
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField ('Password', validators = [DataRequired()])
    submit_button = SubmitField()
    
class UserSignupForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email()])
    name = StringField('Name')
    password = PasswordField('Password', validators = [DataRequired()])
    submit_button = SubmitField()
    
class CharAddForm(FlaskForm):
    name = StringField('Name', validators = [DataRequired()])
    desc = StringField('Description')
    super_power = StringField('Super_Power')
    comics_appeared = StringField('Comics Appeared In')
    submit_button = SubmitField()
    
    
class CommentForm(FlaskForm):
    post = StringField('Comment', validators = [DataRequired()])
    submit_button = SubmitField()
    
    