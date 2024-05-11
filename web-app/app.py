# Flask 
from flask import Flask, request, render_template, session , redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Our custom chat wrap API
import sys
sys.path.append('../')
from chat_wrap import chat_wrap

# Data and messages manipulation
import os, csv
from datetime import datetime

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__, template_folder='./templates', static_folder='./static')
app.secret_key = os.environ.get('APP_SECRET_KEY')

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')

db = SQLAlchemy(app)

# Set up the chat API
API_URL = os.environ.get('API_URL')
API_TOKEN = os.environ.get('API_TOKEN')
chat_obj = chat_wrap(API_URL,API_TOKEN)

class Users(db.Model):
    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False) # Passwords are stored as plaintext for now. Whcih is a bit ironic considering this is an information security project.

# Uncomment the following lines to create the database
with app.app_context():
    db.create_all()


def get_user_messages(user_id):
    '''Get the messages of a user from the csv file. Expects user_id to be an integer.'''
    with open('./data/messages/'+str(user_id)+'.csv','r') as f:
            reader = csv.reader(f)
            messages = list(reader)
            return messages

@app.route('/')
def home():
    # Need to add a home page
    return render_template('index.html',loggedIn='user' in session)

@app.route('/register', methods=['GET','POST'])
def register():
    if 'user' in session:
        return redirect('/chat')
    elif request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        # Register a new user and log them in
        username = request.form['username']
        password = request.form['password']
        if Users.query.filter_by(username=username).first() is not None:
            return render_template('register.html',message="User already exists.")
        else:
            # Add to the database
            user = Users(username=username,password=password)
            db.session.add(user)
            db.session.commit()
            # Start a new CSV file to record their chat history. - Might encrypt this later to preserve chat privacy though.
            with open('./data/messages/'+str(user.id)+'.csv','w') as f:
                # Initialize the csv file with the headers - This wasn't working for some reason
                # writer.writeheader(['timestamp','message_type','content'])
                writer = csv.writer(f)
                writer.writerow([datetime.now(),'System','The amazing '+username+' has joined the chat.'])
            # Log them in
            session['user'] = str(user.id)
            return redirect('/chat')

@app.route('/login', methods=['GET','POST'])
def login():
    if 'user' in session:
        return redirect('/chat')
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        # Verify the user
        if Users.query.filter_by(username=request.form['username'],password=request.form['password']).first() is None:
            return render_template('login.html',message="Invalid username or password.")
        else:
            user = Users.query.filter_by(username=request.form['username']).first()
            # Log in the user
            session['user'] = user.id
            return redirect('/chat')

@app.route('/logout')
def logout():
    if 'user' in session:
        session.pop('user')
    return redirect('/')

@app.route('/chat', methods=['GET','POST'])
def chat():
    if 'user' not in session:
        return redirect('/login')
    if request.method == 'GET':
        messages = get_user_messages(session['user'])
        return render_template("chat.html",messages=messages)
    elif request.method == 'POST':
        prompt = request.form['prompt']
        if prompt != '':
            try:
                # try for file handling
                fobj = open('./data/messages/'+str(session['user'])+'.csv','a')
                writer = csv.writer(fobj)
                try:
                    # Try for get chat request
                    writer.writerow([datetime.now(),'User',prompt])
                    res = chat_obj.get_response(prompt)
                    if res == "The model is currently loading. Please try again in a few seconds.":
                        writer.writerow([datetime.now(),'System',res])
                    else:
                        writer.writerow([datetime.now(),'Bot',res])
                except Exception as e:
                    print("An error occurred while trying to get a response from the chat API.", e)
                    writer.writerow([datetime.now(),'System','An error occurred. Please try again.'])
                fobj.close()
            except Exception as e:
                print("A CATASTRPOHIC ERROR OCCURRED!", e)
        messages = get_user_messages(session['user'])
        return render_template("chat.html",messages=messages)

if __name__ == '__main__':
    app.run(debug=True)