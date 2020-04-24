# Mājaslapas maršrutu pārvaldītājs
import secrets, os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/')
@app.route('/home')
# Galvenās lapas maršruts
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)

@app.route('/about')
# Apraksts par mājaslapu maršruts
def about():
    return render_template('about.html', title='About')

@app.route('/register', methods=['GET', 'POST'])
# Reģistrēšanās maršruts
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    # Reģistrēšanās formas instance
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been registered successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register' , form=form)

@app.route('/login', methods=['GET', 'POST'])
# Pieslēgšanās maršruts
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    # Pieslēgšanās formas instance
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check your email and/or password!', 'danger')
    return render_template('login.html', title='Login' , form=form)

@app.route('/logout')
# Izslēgšanās maršruts
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    # Funkcija, kas saglabā pievienoto profila bildi

    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    # Bildes izmēra mainīšana, lai saglabātās bildes neaizņemtu daudz atmiņas.
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route('/account', methods=['GET', 'POST'])
# Profilu apskates maršruts
@login_required
# Māršrutam ir pieeja tikai tiem lietotājiem, kuri ir pieslēgušies
def account():
    form = UpdateAccountForm()
    # Profilu atjaunošanas formas instance
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated successfully!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)

@app.route('/post/new', methods=['GET', 'POST'])
# Jaunu rakstu izveides maršruts
@login_required
# Māršrutam ir pieeja tikai tiem lietotājiem, kuri ir pieslēgušies
def new_post():
    form = PostForm()
    # Rakstu Pievienošanas formas instance
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post',
                            legend='New Post', form=form)

@app.route('/post/<int:post_id>')
# Specifiska raksta apskatīšanas maršruts
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
# Specifiska raksta atjaunošanas maršruts
@login_required
# Māršrutam ir pieeja tikai tiem lietotājiem, kuri ir pieslēgušies
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    # Rakstu Pievienošanas formas instance
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated successfully!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return  render_template('create_post.html', title='Update Post',
                            legend='Update Post' , form=form)

@app.route('/post/<int:post_id>/delete', methods=['POST'])
# Specifiska raksta dzēšanas maršruts
@login_required
# Māršrutam ir pieeja tikai tiem lietotājiem, kuri ir pieslēgušies
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted successfully!', 'success')
    return redirect(url_for('home'))