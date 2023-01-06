import json
import bcrypt
from operator import contains
from os import replace

from flask import Flask, render_template, jsonify, request, json, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.db"
app.config['SECRET_KEY'] = 'my secretsss'
db = SQLAlchemy(app)
admin = Admin(app)

login_manager = LoginManager() 
login_manager.init_app(app) 
login_manager.login_view = 'login'

joined = db.Table('joined',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True), 
    db.Column('comm_id', db.Integer, db.ForeignKey('community.id'), primary_key=True)
)

like = db.Table('liked',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True), 
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True)
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String, unique=False, nullable=False)
    posts = db.relationship('Post', backref='user')

    joined = db.relationship('Community', secondary=joined, lazy='subquery',
           backref=db.backref('users', lazy=True))

    like = db.relationship('Post', secondary=like, lazy='subquery',
           backref=db.backref('upvotes', lazy=True))

    def __repr__(self):
          return f"{self.userName}"

    def check_password(self, password): 
        return self.password == password

    def get_id(self):
           return (self.id)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.String, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) 

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    community_name = db.relationship('Community', backref=db.backref('posts', lazy=True)) 
    community_id = db.Column(db.Integer, db.ForeignKey('community.id'), nullable=False) 
    
    def __repr__(self):
        starter = "{"
        closer = "}"
        return f" {starter} \"id\": \"{self.id}\" , \"community\": {self.community_name} , \"title\": \"{self.title}\" , \"body\": \"{self.body}\" , \"date\": \"{self.pub_date}\", \"user\": \"{self.user}\" {closer}" 
    
    def print_table(self):
        return f"{self.community_name} , {self.title} , {self.body} , {self.pub_date}"

class Community(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    
    def __repr__(self):
        starter = "{"
        closer = "}"
        return f"\"{self.name}\""

db.create_all()

admin.add_view(ModelView(User,db.session))
admin.add_view(ModelView(Post,db.session))
admin.add_view(ModelView(Community,db.session))

@login_manager.user_loader 
def load_user(id): 
    return User.query.get(id) 

@app.route("/")
@login_required
def index():
    return render_template("index.html")

@app.route("/login")
def loginForm():
    return render_template("login.html")

@app.route("/register")
def registerForm():
    return render_template("register.html")

@app.route('/submit', methods = ['GET', 'POST'])
@login_required
def submitPage():
    return render_template("submit.html")

@app.route('/feed') 
@login_required
def feedPage():
    data = current_user
    return render_template('feed.html', name = data.userName) 

@app.route('/<comm>') 
@login_required
def commPage(comm):
    py =  Community.query.filter_by(name=comm).first()
    data = current_user
    return render_template('comm.html', name = py) 

@app.route('/<comm>/<post>') 
@login_required
def postPage(comm , post):
    py = Community.query.filter_by(name=comm).first()
    py1 = Post.query.filter_by(id=post).first()
    data = current_user
    return render_template('post.html', comm = py, post = py1) 

@app.route('/profile') 
@login_required
def profilePage():
    data = current_user
    return render_template('profile.html', name = data.userName) 

@app.route('/profileview/<user>') 
@login_required
def profileViewPage(user):
    py =  User.query.filter_by(userName=user).first()
    data = current_user
    return render_template('profileview.html', name = py) 

#Code to register log into database
@app.route('/registerlog',methods = ['POST'])
def logreg():
    comm = request.form['community']
    comm1 = Community.query.filter_by(name = comm).first()
    title = request.form['title']
    des = request.form['about']

    log = Post(title = title, body = des, community_id = comm1.id, user_id = current_user.id)

    db.session.add(log) 
    db.session.commit()
    return redirect(url_for('profilePage')) 

#route to GET all communities 
@app.route("/comm", methods=["GET"])
@login_required
def getCommunities():
    data = str(Community.query.all())
    return data

#route to GET all post
@app.route("/post", methods=["GET"])
def getPost():
    data = str(Post.query.order_by(desc(Post.pub_date)).all())
    #data = str(Post.query.all())
    data = "{\"employees\":" + data + "}"
    return data

#route to GET all post in a certain community identified by their name
#@app.route("/<comm>/post", methods=["GET"])
#def getPostFromComm(comm):
   # py =  Community.query.filter_by(name=comm).first()
   # data = py.posts
   # db.session.commit()
   # return str(data)

#route to GET the users who have joined a certain community identified by their name
@app.route("/<comm>/user", methods=["GET"])
def getUsersFromComm(comm):
    assignComm = Community.query.filter_by(name = comm).first()
    data = assignComm.users
    db.session.commit()
    return str(data)

#route to GET the communities of current user
@app.route("/user/comm", methods=["GET"])
@login_required
def getCommFromUser():

    data = str(current_user.joined)
    #return str(data)


    #data = str(current_user.posts)
    #assignComm = Community.query.filter_by(name = comm).first()
    #data = str(assignComm.posts)

   
    return data

#route to GET the all post of current user
@app.route("/user/post", methods=["GET"])
@login_required
def getPostFromUser():

    data = str(current_user.posts)
    data = "{\"employees\":" + data + "}"
   
    return data

@app.route("/user/post/view/<user>", methods=["GET"])
@login_required
def getPostFromProfile(user):
    assignData = User.query.filter_by(userName = user).first()
    data = str(assignData.posts)
    data = "{\"employees\":" + data + "}"
   
    return data

@app.route("/post/single/<title>", methods=["GET"])
@login_required
def getSinglePost(title):
    data = str(Post.query.filter_by(title = title).first())

    #data = str(Post.query.order_by(desc(Post.pub_date)).all())
    #data = str(Post.query.all())
    data = "{\"employees\":" + data + "}"
    return data


#route to GET the all post of current community
@app.route("/<comm>/post", methods=["GET"])
@login_required
def getPostFromComm(comm):


    assignComm = Community.query.filter_by(name = comm).first()
    data = str(assignComm.posts)
    data = "{\"employees\":" + data + "}"
   
    return data

@app.route("/user/<post>", methods=["DELETE"])
def deleteonegrade(post):
    retData = Post.query.filter_by(id = int(post)).first()
    db.session.delete(retData)
    db.session.commit()
    data = str(current_user.posts)
    data = "{\"employees\":" + data + "}"
   
    return data


#route to GET the upvotes of a certain post identified by their id
#will most likely change this something like <comm>/post/upvotes
#were it will return a specific communities post and the upvotes each post has
@app.route("/user", methods=["GET"])
@login_required
def getCurrentUser():
    data = current_user
    return str(data.userName)

@app.route("/post/<id>/upvotes", methods=["GET"])
def getUpvotesFromPost(id):
    assignPost = Post.query.filter_by(id = id).first()
    data = assignPost.upvotes
    db.session.commit()
    return str(data)

@app.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated: 
        return redirect(url_for('index'))
    user = User.query.filter_by(userName = request.form['username']).first()

    password = request.form['password']

    if bcrypt.checkpw(password.encode('utf-8'), user.password):
        login_user(user)
        return redirect(url_for('feedPage'))


    if user is None or not user.check_password(request.form['password']): 
        return "wrong password"
  

@app.route('/register', methods=['POST'])
def register():
    userName = request.form['username']
    password = request.form['password']
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(10))

    user = User(userName = userName, password = hashed)

    db.session.add(user) 
    db.session.commit()
   
    return redirect(url_for('feedPage'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
