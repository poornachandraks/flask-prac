from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from market.model import Users

class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = Users.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('User already exists!')
    
    def validate_email_address(self, email_to_check):
        email = Users.query.filter_by(email_address=email_to_check.data).first()
        if email:
            raise ValidationError('Email already used!')

    username = StringField(label='Username', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password', validators=[EqualTo('password1'), DataRequired()] )
    submit = SubmitField(label='Create Account')

class LoginForm(FlaskForm):
    username = StringField(label='Username', validators=[Length(min=2, max=30), DataRequired()])
    password = PasswordField(label='Password', validators=[Length(min=6), DataRequired()])
    submit = SubmitField(label='Sign In ')

class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label='Purchase Item')

class SellItemForm(FlaskForm):
    submit = SubmitField(label='Sell Item')
