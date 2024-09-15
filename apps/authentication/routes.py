# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import render_template, redirect, request, url_for
import app_cdc.help_functions as hf
from O365 import Account
import app_cdc.office365_login as o365l
import os
from flask import session

from flask_login import (
    current_user,
    login_user,
    logout_user
)

from app_cdc.flask_adminlte.apps import db, login_manager
from app_cdc.flask_adminlte.apps.authentication import blueprint
from app_cdc.flask_adminlte.apps.authentication.forms import LoginForm, CreateAccountForm
from app_cdc.flask_adminlte.apps.authentication.models import Users

from app_cdc.flask_adminlte.apps.authentication.util import verify_pass

class state:
    mystate=''
    
class _o365_user():
    def __init__(self,name,mail,ufficio,authenticated) :
        self.name = name
        self.mail = mail 
        self.ufficio = ufficio
        self.authenticated = authenticated
    def json_serialize(self):
        json_o365_user = {'name':self.name,'mail':self.mail,'ufficio':self.ufficio,'authenticated':self.authenticated}
        return json_o365_user
    @staticmethod
    def json_deserialize(json):
        return _o365_user(json.get('name'),json.get('mail'),json.get('ufficio'),bool(json.get('authenticated')))    

@blueprint.route('/')
def route_default():
    secrets = hf.readYamlFileSecrets()
    credentials = (secrets['cdc_azure']['application_id'],secrets['cdc_azure']['client_secret_value'])
    account = Account(credentials)
    if session.get('o365_user') :
        o_user = _o365_user.json_deserialize(session['o365_user'])
    return redirect(url_for('authentication_blueprint.login'))


# Login & Registration

@blueprint.route('/cdc-get-o365', methods=['GET', 'POST'])
def o365_verify_auth():
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    secrets = hf.readYamlFileSecrets()
    credentials = (secrets['cdc_azure']['application_id'],secrets['cdc_azure']['client_secret_value'])
    account = Account(credentials)
    my_saved_state = '12345' # example...
    requested_url = request.url 
    callback = 'http://localhost:5000/cdc-get-o365'
    result = account.con.request_token(requested_url,
                                       state=state.mystate,
                                       redirect_uri=callback)
    if result:
        if account.is_authenticated:
            
            print('Authenticated!')
            o_user = account.get_current_user()            
            name = o_user.full_name
            mail = o_user.mail
            authenticated = account.is_authenticated
            ufficio = o_user.office_location
            o365_user = _o365_user(name,mail,ufficio,authenticated)
            session['o365_user'] = o365_user.json_serialize()
            mailbox = account.mailbox() 
            m = mailbox.new_message()
            m.to.add('ffuxaq@gmail.com')
            m.subject = 'Testing!'
            m.body = "test ."
            m.save_message()
            ## m.attachment.add = 'filename.txt'
            m.send()
            mailbox = account.mailbox()
            messages = mailbox.get_messages(limit=10)
            #for message in messages:
            #    print(message.subject)
            #andiamo a vedere se è necessario la registrazione o meno perchè già registrati
            # return  render_template('accounts/code.html',
            #                     msg='',
            #                     code = 'ok')   
            return redirect('http://localhost:5000/register')
        else :
            return  render_template('accounts/code.html',
                                msg='Wrong user or password',
                                code = 'ko')      
            
    else :
        return  render_template('accounts/code.html',
                                msg='Wrong user or password',
                                code = 'ko')  
    

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    #controlliamo se dobbiamo loggare con office365/ADN
    settings = hf.readYamlFileApp()
    if settings['use_o365_login'] != 'True':
        login_form = LoginForm(request.form)
        if 'login' in request.form:

            # read form data
            username = request.form['username']
            password = request.form['password']

            # Locate user
            user = Users.query.filter_by(username=username).first()

            # Check the password
            if user and verify_pass(password, user.password):

                login_user(user)
                return redirect(url_for('authentication_blueprint.route_default'))

            # Something (user or pass) is not ok
            return render_template('accounts/login.html',
                                msg='Wrong user or password',
                                form=login_form)
            
        if not current_user.is_authenticated:
            return render_template('accounts/login_o365.html',
                               form=login_form)
        return redirect(url_for('home_blueprint.index'))    
    else:
        login_form = LoginForm(request.form)
        if 'login' in request.form:

            # read form data
            username = request.form['username']
            password = request.form['password']
            callback = 'http://localhost:5000/cdc-get-o365'
            myurl = url_for('authentication_blueprint.route_default', _external=True)
            secrets = hf.readYamlFileSecrets()
            credentials = (secrets['cdc_azure']['application_id'],secrets['cdc_azure']['client_secret_value'])
            account = Account(credentials)
            my_scopes = ['https://graph.microsoft.com/offline_access','https://graph.microsoft.com/Mail.Read','https://graph.microsoft.com/Mail.ReadWrite','https://graph.microsoft.com/User.Read','https://graph.microsoft.com/Mail.Send']
            url, state.mystate = account.con.get_authorization_url(requested_scopes=my_scopes,
                                                   redirect_uri=callback)
            return redirect(url)
            #return redirect(o365l.login())
        
        if not current_user.is_authenticated:
            return render_template('accounts/login_o365.html',
                               form=login_form)
        return redirect(url_for('home_blueprint.index'))
    


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    create_account_form = CreateAccountForm(request.form)
    settings = hf.readYamlFileApp()
    if settings['use_o365_login'] != 'True':
        if 'register' in request.form:

            username = request.form['username']
            email = request.form['email']

            # Check usename exists
            user = Users.query.filter_by(username=username).first()
            if user:
                return render_template('accounts/register.html',
                                    msg='Username already registered',
                                    success=False,
                                    form=create_account_form)

            # Check email exists
            user = Users.query.filter_by(email=email).first()
            if user:
                return render_template('accounts/register.html',
                                    msg='Email already registered',
                                    success=False,
                                    form=create_account_form)

            # else we can create the user
            user = Users(**request.form)
            db.session.add(user)
            db.session.commit()
            

            return render_template('accounts/register.html',
                                msg='User created please <a href="/login">login</a>',
                                success=True,
                                form=create_account_form)

        else:
            return render_template('accounts/register.html', form=create_account_form)
    else:
        #andiamo a gestire quanto l'oauth 365 è stato fatto ma l'utente comunque deve essere registrato nel nostro db
        o_user = _o365_user.json_deserialize(session['o365_user'])
        user = Users.query.filter_by(o365_email=o_user.mail).first()
        if not user:
            #l'utente potrebbe non essere registrato
            if 'register' in request.form :
                username = request.form['username']
                email = request.form['email']

                # Check usename exists
                user = Users.query.filter_by(username=username).first()
                if user:
                    return render_template('accounts/register.html',
                                        msg='Username already registered',
                                        success=False,
                                        form=create_account_form)

                # Check email exists
                user = Users.query.filter_by(email=email).first()
                if user:
                    return render_template('accounts/register.html',
                                        msg='Email already registered',
                                        success=False,
                                        form=create_account_form)

                # else we can create the user
                user = Users(**request.form)
                db.session.add(user)
                user.o365_email = o_user.mail
                user.o365_name = o_user.mail
                user.o365_ufficio = o_user.ufficio
                db.session.commit()
                # registrato redirect tu home page
                return render_template('accounts/register.html',
                                msg='User created please <a href="/login">login</a>',
                                success=True,
                                form=create_account_form)
            else:
                return render_template('accounts/register.html',form = create_account_form)     
                
        else:
            login_user(user)
            return redirect(url_for('home_blueprint.index'))        


@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('authentication_blueprint.login'))

# Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500
