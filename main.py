from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy
import cgi 
import os

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:jordyn31@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = 'PPPkkkLLL$$$'

db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    entry = db.Column(db.String(255))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    def __init__(self, name, entry, owner):
        self.name = name
        self.entry = entry
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')




    def __init__(self, username, password):
        self.username= username
        self.password = password


"""@app.before_request
def require_login():
    allowed_routes = ['login', 'blog', 'index', 'signup', 'newpost']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')"""


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            session["username"] = username
            return redirect('/newpost')

        else:
            return render_template('login.html', username_error="Username does not exist.")

    return render_template('login.html')




@app.route("/signup", methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        existing_user = User.query.filter_by(username=username).first()

        username_error = ""
        password_error = ""
        verify_error = ""

        if username == "":
            username_error = "Must enter username."

        if len(username) <= 3 or len(username) > 20:
            username_error = "Username must be between 3 and 20 characters long."

        if " " in username:
            username_error = "Username cannot contain any spaces."

        if password == "":
            password_error = "Must enter valid password."
        if len(password) <= 3:
            password_error = "Password must be greater than 3 characters long."


        if " " in password:
            password_error = "Password cannot contain any spaces."
        if password != verify or verify == "":
            verify_error = "Passwords do not match."

        if existing_user:
            username_error = "Username already exists."
        
        if len(username) > 3 and len(password) > 3 and password == verify and not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()


            session['username'] = username

            return redirect('/newpost')
        else:
            return render_template('signup.html',
            username=username,
            username_error=username_error,
            password_error=password_error,
            verify_error=verify_error)

    return render_template('signup.html')





@app.route('/')
def index():
    posts = User.query.all()
    return render_template('index.html', posts=posts)

    

@app.route('/newpost', methods=['POST', 'GET'])
def add_entry():

        
    if request.method == 'POST':
        name = request.form['name']
        entry = request.form['entry']
        owner = User.query.filter_by(username=session['username']).first()



        new_name =Blog(name, entry, owner)
        db.session.add(new_name)
        db.session.commit()

        
        name_error = ''
        entry_error = ''

        if name == "":
            name_error = 'Please fill in the title'
            name = ''
            
        

        if entry == "":
            entry_error = 'Please fill in the body'
            entry =''

        
         

        if not name_error and not entry_error:
           
            post_id = new_name.id
            return redirect('/blog?id={0}'.format(post_id))
            #return render_template('single.html', name=name, entry=entry) 
             
           
        else:
            return render_template('newpost.html', name=name, entry=entry, name_error=name_error, entry_error=entry_error)  

        
        
    return render_template('newpost.html')
    

@app.route('/blog')
def blog_page():
    
   

    blog_id = request.args.get('id')
    user_id = request.args.get('userid')

    posts = Blog.query.order_by(Blog.id.desc()).all()


    if blog_id:
        posts = Blog.query.filter_by(id=int(blog_id)).all()
        return render_template('ind_blog.html', posts=posts)

    if user_id:
        posts = Blog.query.filter_by(owner_id=int(user_id)).all()
        return render_template('singleUser.html', posts=posts)
    
    

        


    return render_template('blog.html', posts=posts)



   


@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')



      
    
if __name__ == '__main__':
    app.run()


