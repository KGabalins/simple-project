# Aplikācijas palaišana
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm
from models import User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blogSite.db'
app.config['SECRET_KEY'] = 'fc1fe1d849a56333d60b3b09839d2529'
# Izveidota datubaazes instance
db = SQLAlchemy(app)


posts = [
    {
        'author': 'Karlis Gabalins',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 21, 2020'
    },
    {
        'author': 'Janis Banis',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 22, 2020'
    }
]

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register' , form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@admin.com' and form.password.data == 'admin':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check your email and password!', 'danger')
    return render_template('login.html', title='Login' , form=form)


if __name__ == '__main__':
    app.run(debug=True)