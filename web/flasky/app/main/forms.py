from flask_wtf import Form
from wtforms import StringField,PasswordField,BooleanField,SubmitField,TextAreaField,SelectField
from wtforms.validators import Required,Length,Email,Regexp,EqualTo
from ..models import Role,User
from wtforms import ValidationError

class EditProfileForm(Form):
    name=StringField('Real name',validators=[Length(0,64)])
    location=StringField('Location',validators=[Length(0,64)])
    about_me=TextAreaField('About me')
    submit=SubmitField('submit')

class NameForm(Form):
    pass

class PostForm(Form):
    body=TextAreaField("What`s on your mind?",validators=[Required()])
    submit=SubmitField('Submit')




class EditProfileAdminForm(Form):
    email=StringField('Email',validators=[Required(),Length(1,64),Email()])
    username=StringField('Username',validators=[Required(),Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'Username must have only letters,''numbers,dots or underscores')])
    confirmed=BooleanField('Confirmed')
    role=SelectField('Role',coerce=int)
    name=StringField('Real name',validators=[Length(0,64)])
    location=StringField('Location',validators=[Length(0,64)])
    about_me=TextAreaField('About me')
    submit=SubmitField('submit')

    def __init__(self,user,*argv,**kwargs):
        super(EditProfileAdminForm, self).__init__(*argv,**kwargs)
        self.role.choices=[(role.id,role.name) for role in Role.querry.order_by(Role.name).all()]
        self.user=user

    def validate_email(self,field):
        if field.data!=self.user.email and User.querry.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validata_username(self,field):
        if field.data!=self.user.username and \
            User.querry.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')
