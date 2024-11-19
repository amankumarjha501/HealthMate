from flask import Flask, render_template, request, jsonify, redirect, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy
import bcrypt
from sqlalchemy.exc import IntegrityError
import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import _tree
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.svm import SVC
import csv
import warnings
from googletrans import Translator
import re
import json
import spacy
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from googletrans import Translator
 
translator = Translator() 

warnings.filterwarnings("ignore", category=DeprecationWarning)
from sklearn.datasets import load_iris

# Load dataset
data = load_iris()
app = Flask(__name__)
app.secret_key = 'aman123'  # Required for session management

training = pd.read_csv(r'C:\Users\USER\Desktop\HealthMate\Training.csv')
testing= pd.read_csv(r'C:\Users\USER\Desktop\HealthMate\Testing.csv')
cols= training.columns
cols= cols[:-1]
x = training[cols]
y = training['prognosis']
y1= y


reduced_data = training.groupby(training['prognosis']).max()

#mapping strings to numbers
le = preprocessing.LabelEncoder()
le.fit(y)
y = le.transform(y)


x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=42)
testx    = testing[cols]
testy    = testing['prognosis']  
testy    = le.transform(testy)


clf1  = DecisionTreeClassifier()
clf = clf1.fit(x_train,y_train)
# print(clf.score(x_train,y_train))
# print ("cross result========")
scores = cross_val_score(clf, x_test, y_test, cv=3) # cv****
# print (scores)
print (scores.mean())

importances = clf.feature_importances_
indices = np.argsort(importances)[::-1]
feature_names = cols
tree = clf




symptoms_present = []
def readn(nstr):
    engine = pyttsx3.init()

    engine.setProperty('voice', "english+f5")
    engine.setProperty('rate', 130)

    engine.say(nstr)
    engine.runAndWait()
    engine.stop()


severityDictionary=dict()
description_list = dict()
precautionDictionary=dict()
feature_names=data.feature_names
symptoms_dict = {}

for index, symptom in enumerate(x):
    symptoms_dict[symptom] = index
def calc_condition(exp,days):
    sum=0
    for item in exp:
        sum=sum+severityDictionary[item]
    if((sum*days)/(len(exp)+1)>13):
        return ("You should take the consultation from doctor. ")
    else:
        return ("It might not be that bad but you should take precautions.")


def getDescription():
    global description_list
    with open(r'C:\Users\USER\Desktop\HealthMate\symptom_Description.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            _description={row[0]:row[1]}
            description_list.update(_description)




def getSeverityDict():
    global severityDictionary
    with open(r'C:\Users\USER\Desktop\HealthMate\Symptom_severity.csv') as csv_file:

        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        try:
            for row in csv_reader:
                _diction={row[0]:int(row[1])}
                severityDictionary.update(_diction)
        except:
            pass

def getprecautionDict():
    global precautionDictionary
    with open(r'C:\Users\USER\Desktop\HealthMate\symptom_precaution.csv') as csv_file:

        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            _prec={row[0]:[row[1],row[2],row[3],row[4]]}
            precautionDictionary.update(_prec)


def check_pattern(chk_dis, disease_input):
    matched_symptoms = [sym for sym in chk_dis if disease_input in sym]
    return (1, matched_symptoms) if matched_symptoms else (0, [])

def sec_predict(symptoms_exp):
    df = pd.read_csv(r'C:\Users\USER\Desktop\HealthMate\Training.csv')
    X = df.iloc[:, :-1]
    y = df['prognosis']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=20)
    rf_clf = DecisionTreeClassifier()
    rf_clf.fit(X_train, y_train)
    symptoms_dict = {}

    for index, symptom in enumerate(X):
        symptoms_dict[symptom] = index

    input_vector = np.zeros(len(symptoms_dict))
    for item in symptoms_exp:
        input_vector[[symptoms_dict[item]]] = 1


    return rf_clf.predict([input_vector])

def get_user_symptom(symptoms_list):
    response = "Enter the symptom you are experiencing:"
    for num, sym in enumerate(symptoms_list):
        response += f"\n{num}) {sym}...."
    response += f"\n..... Select the one you meant (0 - {len(symptoms_list)-1}):"
    return response

def print_disease(node):
    #print(node)
    node = node[0]
    #print(len(node))
    val  = node.nonzero() 
    # print(val)
    disease = le.inverse_transform(val[0])
    return disease

def handle_tree_to_code_stage(user_input):
    if 'tree_stage' not in session:
        session['tree_stage'] = 0
        session['symptoms_present'] = []
        session['symptom_input'] = None
        session['num_days'] = None

    # Stage 0: Get initial symptom
    if session['tree_stage'] == 0:
        feature_names = cols
        chk_dis = ",".join(feature_names).split(",")
        conf, cnf_dis = check_pattern(chk_dis, user_input)
        if conf == 1:
            session['conf_dis'] = cnf_dis
            if len(cnf_dis) > 1:
                session['tree_stage'] = 1
                return get_user_symptom(cnf_dis)
            else:
                session['symptom_input'] = cnf_dis[0]
                session['tree_stage'] = 2
                return "Okay. From how many days?"
        else:
            return "Enter a valid symptom."

    # Stage 1: Disambiguate symptom if multiple options found
    if session['tree_stage'] == 1:
        try:
            conf_inp = int(user_input)
            if conf_inp < len(session['conf_dis']):
                session['symptom_input'] = session['conf_dis'][conf_inp]
                session['tree_stage'] = 2
                return "Okay. From how many days?"
            else:
                return "Invalid selection. Please try again."
        except ValueError:
            return "Invalid input. Please enter a number."

    # Stage 2: Get number of days
    if session['tree_stage'] == 2:
        try:
            session['num_days'] = int(user_input)
            session['tree_stage'] = 3
            return "Are you experiencing anything else? (Yes/No)"
        except ValueError:
            return "Please enter a valid number of days."

    if session['tree_stage'] ==3:
        if user_input.lower() in ['yes','no']:
            recurse_tree_to_code(session['symptom_input'], session['num_days'], 0, 1)
            response = ask_next_symptom(user_input)
            if response:
                return response
        else:
            return "Please respond with 'yes' or 'no'."
    

def recurse_tree_to_code(symptom_input, num_days, node, depth):
    tree = clf
    tree_ = tree.tree_
    feature_names = cols
    feature_names_list = feature_names
    feature_name = []
    for i in tree_.feature:
        if i != _tree.TREE_UNDEFINED:
            feature_name.append(feature_names[i])
        else:
            feature_name.append("undefined!")
    indent = "  " * depth
    symptoms_present = session['symptoms_present']
    
    if tree_.feature[node] != _tree.TREE_UNDEFINED:
        name = feature_name[node]
        threshold = tree_.threshold[node]

        if name == symptom_input:
            val= 1
        else:
            val= 0
        if val <= threshold:
            return recurse_tree_to_code(symptom_input, num_days, tree_.children_left[node], depth + 1)
        else:
            symptoms_present.append(name)
            session['symptoms_present'] = symptoms_present
            return recurse_tree_to_code(symptom_input, num_days, tree_.children_right[node], depth + 1)
    else:
        present_disease = print_disease(tree_.value[node])
        red_cols = reduced_data.columns 
        symptoms_given = red_cols[reduced_data.loc[present_disease].values[0].nonzero()]
        print(symptoms_given)
        
        session['present_disease'] = present_disease
        session['symptoms_given'] = symptoms_given
        session['symptoms_exp'] = []
        session['current_symptom_index'] = 0
        session['tree_stage'] = 4
        print("recurse_tree_to_code executed successfully")

def ask_next_symptom(user_response):
    symptoms_given = session.get('symptoms_given',[]).tolist()
    current_index = session.get('current_symptom_index', 0)
    symptoms_exp = session['symptoms_exp']
    # Check if there are more symptoms to ask about
    if current_index < len(symptoms_given):
        # Only append if the user response is 'yes'
        if user_response == 'yes' and current_index > 0:
            symptoms_exp.append(symptoms_given[current_index - 1])
            session['symptoms_exp'] = symptoms_exp

        # Get the next symptom to ask about
        symptom = symptoms_given[current_index]
        session['current_symptom_index'] = current_index + 1
        response =  ' '.join(f"{(symptom)} ?")
        return response
    else:
        return evaluate_disease_prediction()
# Function to ask about the next symptom
#def ask_next_symptom():
#    if 'symptoms_given' in session and session['current_symptom_index'] < len(session['symptoms_given']):
#       symptom = session['symptoms_given'][session['current_symptom_index']]
#        session['current_symptom_index'] += 1
#        print("working4")
#        return f"Are you experiencing {symptom}? (yes/no) :"
#    print("working4.1")
#    return evaluate_disease_prediction()

# Function to evaluate the disease prediction

def evaluate_disease_prediction():
    symptoms_exp = session['symptoms_exp']
    print(symptoms_exp)
    second_prediction = sec_predict(symptoms_exp)
    present_disease = session['present_disease']

    if present_disease == second_prediction[0]:
        response = f"You may have {present_disease}.\n{description_list[present_disease]}"
    else:
        response = f"You may have {present_disease} or {second_prediction[0]}.\n{description_list[present_disease]}\n{description_list[second_prediction[0]]}"

    precautions = precautionDictionary[present_disease]
    response += "\nTake the following measures: " + ", ".join(precautions)

    confidence_level = (1.0 * len(session['symptoms_present'])) / len(session['symptoms_given'])
    response += f"\nConfidence level: {confidence_level}"

    # Clear session for new interaction
    session.clear()
    return response
getSeverityDict()
getDescription()
getprecautionDict()


@app.route('/')
def index():
    return render_template('home1.html')

@app.route('/sendMessage', methods=['POST'])
def send_message():
    user_input = request.form['user_input']
    if 'chat_stage' not in session:
        session['chat_stage'] = 0
    
    if session['chat_stage'] == 0:
        session['chat_stage'] = 1
        if user_input.lower() in ['hi', 'hello', 'hey']:
            response = "Hello! Please tell me your name"
            return jsonify(response=response)
        
    if session['chat_stage'] == 1:
        session['name'] = user_input
        session['chat_stage'] = 2
        return jsonify(response=f"Hello {user_input}! Are you not feeling well?... Please enter the symptom you are experiencing.")

    if session['chat_stage'] == 2:
        message = handle_tree_to_code_stage(user_input)
        if message:
            response = [message]
            print(response)
            return jsonify(response=response)
        return jsonify(response="Sorry, something went wrong. Please try again.")
            

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///HealthMate.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.secret_key = 'aman123'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    phonenumber = db.Column(db.Integer, unique=True)
    email = db.Column(db.String(50), unique=True)
    DOB = db.Column(db.String(10))
    gender = db.Column(db.String(15))
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, name, phonenumber, email, DOB, gender, password):
        self.name = name
        self.phonenumber = phonenumber
        self.email = email
        self.DOB = DOB
        self.gender = gender
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self,password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
    
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    rating = db.Column(db.String(20))
    comments = db.Column(db.Text)

    def __init__(self, name, email, rating, comments):
        self.name = name
        self.email = email
        self.rating = rating
        self.comments = comments
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    phonenumber = db.Column(db.Integer, unique=True)
    email = db.Column(db.String(50), unique=True)
    DOB = db.Column(db.String(10))
    gender = db.Column(db.String(15))
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, name, phonenumber, email, DOB, gender, password):
        self.name = name
        self.phonenumber = phonenumber
        self.email = email
        self.DOB = DOB
        self.gender = gender
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self,password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
with app.app_context():
    db.create_all()


@app.route('/signup' , methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        # Handle request
        name = request.form.get('name')
        phonenumber = request.form.get('phonenumber')
        email = request.form.get('email')
        DOB = request.form.get('DOB')
        password = request.form.get('password')
        gender = request.form.get('gender')

        if not name or not phonenumber or not email or not DOB or not gender or not password:
            flash('Please fill out all fields', 'error')
            return redirect('/signup')

        try:
            new_user = User(name=name, phonenumber=phonenumber, email=email, DOB=DOB, gender=gender, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('User registered successfully!', 'success')
            return redirect('/login')
        except IntegrityError as e:
            db.session.rollback()
            if 'UNIQUE constraint failed: user.phonenumber' in str(e.orig):
                flash('Phone number already exists!', 'error')
            elif 'UNIQUE constraint failed: user.email' in str(e.orig):
                flash('Email already exists!', 'error')
            else:
                flash('An error occurred. Please try again.', 'error')
            return redirect('/signup')

    return render_template('signup.html')

@app.route('/admin_signup' , methods=['GET','POST'])
def admin_signup():
    if request.method == 'POST':
        # Handle request
        name = request.form.get('name')
        phonenumber = request.form.get('phonenumber')
        email = request.form.get('email')
        DOB = request.form.get('DOB')
        password = request.form.get('password')
        gender = request.form.get('gender')

        if not name or not phonenumber or not email or not DOB or not gender or not password:
            flash('Please fill out all fields', 'error')
            return redirect('/admin_signup')

        try:
            new_user = Admin(name=name, phonenumber=phonenumber, email=email, DOB=DOB, gender=gender, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('User registered successfully!', 'success')
            return redirect('/admin_login')
        except IntegrityError as e:
            db.session.rollback()
            if 'UNIQUE constraint failed: user.phonenumber' in str(e.orig):
                flash('Phone number already exists!', 'error')
            elif 'UNIQUE constraint failed: user.email' in str(e.orig):
                flash('Email already exists!', 'error')
            else:
                flash('An error occurred. Please try again.', 'error')
            return redirect('/admin_signup')

    return render_template('admin_signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    print("Reached login route")  # Added debug statement
    if request.method == 'POST':
        print("Received POST request")  # Added debug statement
        email = request.form.get('email')
        password = request.form.get('password')
        print(f"Email: {email}, Password: {password}")  # Added debug statement

        user = User.query.filter_by(email=email).first()
        if user:
            print("User found")  # Added debug statement
        else:
            print("User not found")  # Added debug statement

        if user and user.check_password(password):
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['user_email'] = user.email
            flash('Logged in successfully!', 'success')
            return redirect('/dashboard')
        else:
            flash('Invalid email or password.', 'error')
            return redirect('/login')
    return render_template('login.html')

@app.route('/admincorner', methods=['GET', 'POST'])
def admincorner():
    print("Reached login route")  # Added debug statement
    if request.method == 'POST':
        print("Received POST request")  # Added debug statement
        email = request.form.get('email')
        password = request.form.get('password')
        print(f"Email: {email}, Password: {password}")  # Added debug statement

        user = Admin.query.filter_by(email=email).first()
        if user:
            print("User found")  # Added debug statement
        else:
            print("User not found")  # Added debug statement

        if user and user.check_password(password):
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['user_email'] = user.email
            flash('Logged in successfully!', 'success')
            return redirect('/admin_dash')
        else:
            flash('Invalid email or password.', 'error')
            return redirect('/admincorner')
    return render_template('admin_login.html')
@app.route('/dashboard')
def dashboard():
    if 'user_email' not in session:
        flash('You need to log in first.', 'error')
        return redirect('/login')
    else:
        user_name = session.get('user_name')
        user_email = session.get('user_email')
        return render_template("dashboard1.html", user_name = user_name, user_email = user_email)

@app.route('/admin_dash')
def admin_dash():
    if 'user_email' not in session:
        flash('You need to log in first.', 'error')
        return redirect('/admincorner')
    else:
        user_name = session.get('user_name')
        user_email = session.get('user_email')
        return render_template("admin_Dash.html", user_name = user_name, user_email = user_email)

@app.route('/new_chat', methods=['POST'])
def new_chat():
    session.pop('chat_stage', None)
    session.pop('tree_stage', None)
    return redirect('/')

@app.route('/new_chat1', methods=['POST'])
def new_chat1():
    session.pop('chat_stage', None)
    session.pop('tree_stage', None)
    return redirect('/dashboard')

@app.route('/new_chat2', methods=['POST'])
def new_chat2():
    session.pop('chat_stage', None)
    session.pop('tree_stage', None)
    return redirect('/admin_dash')
@app.route('/dashboard1')
def dashboard1():
    return render_template('dashboard1.html')

@app.route('/resetSession', methods=['GET'])
def reset_session():
    # Reset the chat stage on page refresh
    session.pop('chat_stage', None)
    session.pop('tree_stage', None)
    return jsonify(success=True)


#Dashboard Part
@app.route('/aboutus')
def aboutus():
    return render_template('AboutUs.html')
    
@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

# Submit feedback route
@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    name = request.form['name']
    email = request.form['email']
    rating = request.form['rating']
    comments = request.form['comments']

    if not name or not email or not rating or not comments:
        flash('Please fill out all fields', 'error')
        return redirect('/feedback')

    try:
        new_feedback = Feedback(name=name, email=email, rating=rating, comments=comments)
        db.session.add(new_feedback)
        db.session.commit()
        flash('Thank you for your feedback!', 'success')
        return redirect('/feedback')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred. Please try again.', 'error')
        return redirect('/feedback')

@app.route('/adminfeedback')
def view_feedback():
        feedback_list = Feedback.query.all()
        return render_template('admin_feedback.html', feedback=feedback_list)

@app.route('/userdetails')
def userdetails():
    User_list = User.query.all()
    return render_template('user_details.html', Details=User_list)

@app.route('/home')
def home():
    return render_template('home1.html')

@app.route('/logout')
def logout():
    session.pop('email',None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
