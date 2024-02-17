# -*- encoding: utf-8 -*-
"""
Copyright (c) 2024 - FFUXAQ - CDC
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Email, DataRequired,ValidationError



def bisestile(anno):
    if ( (int(anno) - 1960) % 4 == 0) :
        return True
 
def giorno_mese(dd,mm,anno):
     mydict = {1:31,2:28,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}
     if mydict[mm] == dd or ( mydict[mm] + 1 == dd and bisestile(anno) ):
         return True
     return False            

# login and registration

def ItalianDate(min=-1, max=-1):
    message = 'Must be a date del tipo dd/mm/yyyy '

    def _italianDate(FlaskForm, field):
        l = field.data
        if l.split("/")!= 3 :
            raise ValidationError(message)
        dd = l.split("/")[0]
        mm = l.split("/")[1]
        anno = l.split("/")[2]
        if int(mm) > 12 or int(mm) < 1 or anno < 1950 :
            raise ValidationError(message)
        if int(dd) < 1 :
            raise ValidationError(message)
        if giorno_mese(int(dd),int(mm),int(anno)) == False:
            raise ValidationError(message)
        
        return _italianDate

class ReportForm(FlaskForm):
    username = StringField('Username',
                         id='username_login',
                         validators=[DataRequired(),ItalianDate()])
    password = PasswordField('Password',
                             id='pwd_login',
                             validators=[DataRequired()])


class Report2Form(FlaskForm):
    username = StringField('Username',
                         id='username_create',
                         validators=[DataRequired()])
    email = StringField('Email',
                      id='email_create',
                      validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             id='pwd_create',
                             validators=[DataRequired()])