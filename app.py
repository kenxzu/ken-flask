from flask import Flask, render_template, request, redirect, url_for

from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database2.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f'{self.username}'

@app.route('/')
def helloFlask(): 
    return render_template('index.html', name_in_html = 'doktorandus john doe');


@app.route('/about')
def about(): 
    return render_template('about.html')


#dynamic route
@app.route('/greet/<name>')
def greet(name):
    return render_template('greet.html', username=name)



@app.route('/user/list')
def userList(): 
    all_users = User.query.all()
    return render_template('user.html', user_list = all_users)



@app.route("/search", methods=['GET', 'POST'])
def search() : 
    if request.method == 'POST' : 
        query = request.form['query_input']

        return redirect(url_for("search_results", query=query))
    return render_template('search.html')   



@app.route("/search_results/<query>")
def search_results(query) : 
    return f'Search Results for {query}'



@app.route("/add_user", methods=['GET', 'POST'])
def add_user() : 
    if request.method == 'POST' : 
        username = request.form['username_input']
        new_user = User(username=username)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("userList"))
    return render_template('add_user.html')