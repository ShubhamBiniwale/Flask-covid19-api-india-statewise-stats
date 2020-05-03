from flask import Flask , redirect , render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager , UserMixin , login_required ,login_user, logout_user,current_user
import requests
import json
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://shubham:shubhamb@localhost:5432/flask_app'
app.config['SECRET_KEY']='619619'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'get_home'
login_manager.init_app(app)

class User(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(200))
    email = db.Column(db.String(200))
    password = db.Column(db.String(200))


@login_manager.user_loader
def get(id):
    return User.query.get(id)

@app.route('/',methods=['GET'])
def get_home():
    return render_template('home.html')

@app.route('/login',methods=['GET'])
def get_login():
    return render_template('login.html')


@app.route('/signup',methods=['GET'])
def get_signup():
    return render_template('signup.html')

@app.route('/user/<username>',methods=['GET'])
@login_required
def get_userhome(username):
    return render_template('home_main.html',username=username)

@app.route('/login',methods=['POST'])
def login_post():
    email = request.form['email']
    password = request.form['password']
    user = User.query.filter_by(email=email).first()
    login_user(user)
    username = user.username
    return redirect(url_for('get_userhome', username=username))

@app.route('/signup',methods=['POST'])
def signup_post():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    user = User(username=username,email=email,password=password)
    db.session.add(user)
    db.session.commit()
    user = User.query.filter_by(email=email).first()
    login_user(user)
    return redirect('/')


@app.route('/stats',methods=['POST'])
@login_required
def show_stats():
    state_name_entered = request.form['country']
    req = requests.get('https://api.rootnet.in/covid19-in/stats/latest')
    content = req.content
    data = json.loads(content)
    elems = []
    for lst_elem in data['data']['regional']:
        if state_name_entered == lst_elem['loc']:
            state_name = lst_elem['loc']
            confirm_cases = lst_elem['totalConfirmed']
            deaths = lst_elem['deaths']
            recovered = lst_elem['discharged']
            elems.append(state_name)
            elems.append(confirm_cases)
            elems.append(deaths)
            elems.append(recovered)    

    print elems
    return render_template('result.html',data=elems)

@app.route('/logout',methods=['GET'])
def logout():
    logout_user()
    return redirect('/login')


if __name__=='__main__':
    app.run(debug=True)