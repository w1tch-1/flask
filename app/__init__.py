from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .forms import LoginForm, RegistrationForm
from flask_login import login_user, UserMixin, LoginManager, current_user, login_required


app = Flask(__name__)
app.config['SECRET_KEY'] = '<KEY>'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    img = db.Column(db.String)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    post = db.Column(db.Integer, db.ForeignKey('post.id'))
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)


@login_manager.user_loader
def user_loaders(id):
    return User.query.get(id)


@app.route('/')
@login_required
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)


@app.route('/add-post', methods=['POST'])
def add_post():
    file = request.files['image']
    file.save(f'app/static/img/{file.filename}')
    post = Post(text=request.form['text'], img=f'/static/img/{file.filename}', user=current_user.id)
    db.session.add(post)
    db.session.commit()
    return render_template('list_of_posts.html', posts=Post.query.all())


@app.route('/post/<int:id>')
def post_detail(id):
    post = Post.query.get(id)
    comments = Comments.query.filter_by(post=id)
    likes = Like.query.filter_by(post=id).count()
    is_liked = True if Like.query.filter_by(post=id, user=current_user.id).first() else False
    return render_template('post_details.html', post=post, comments=comments, likes=likes, is_liked=is_liked)


@app.route('/post/<int:id>/add-comment', methods=['POST'])
def add_comment(id):
    comment = Comments(text=request.form['text'], post=id, user=current_user.id)
    db.session.add(comment)
    db.session.commit()
    return render_template('list_of_comments.html', comments=Comments.query.filter_by(post=id))


@app.route('/htmx')
def htmx():
    return render_template('htmx.html')


@app.route('/htmx-ajax')
def htmx_ajax():
    return render_template('list.html', names=['vlad', 'kyryl', 'veronika'])


@app.route('/delete-comment/<int:id>', methods=['DELETE'])
def delete_comment(id):
    comment = Comments.query.get(id)
    db.session.delete(comment)
    db.session.commit()
    return render_template('list_of_comments.html', comments=Comments.query.filter_by(post=id))


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    forms = RegistrationForm()
    if forms.validate_on_submit():
        username = forms.username.data
        email = forms.email.data
        password = forms.password.data
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect('/')
    return render_template('registration.html', forms=forms)


@app.route('/login', methods=['GET', 'POST'])
def login():
    logins = LoginForm()
    if logins.validate_on_submit():
        username = logins.username.data
        password = logins.password.data
        user = User.query.filter_by(username=username).first()
        if user is None or user.password != password:
            return render_template('login.html')
        login_user(user)
        return redirect('/')
    return render_template('login.html', logins=logins)


@app.route('/post/<int:post_id>/add-like', methods=['POST'])
def add_like(post_id):
    like = Like(post=post_id, user=current_user.id)
    db.session.add(like)
    db.session.commit()
    likes = Like.query.filter_by(post=post_id).count()
    return render_template('like-section.html', likes=likes, is_liked=True, post_id=post_id)


@app.route('/post/<int:post_id>/remove-like', methods=['POST'])
def remove_like(post_id):
    like = Like.query.filter_by(post=post_id, user=current_user.id).first()
    db.session.delete(like)
    db.session.commit()
    likes = Like.query.filter_by(post=post_id).count()
    return render_template('like-section.html', likes=likes, is_liked=False, post_id=post_id)


@app.route('/profile')
def profile():
    return render_template('profile.html', user=current_user)


@app.route('/profile/edit', methods=['GET'])
def edit():
    return render_template('edit.html', user=current_user)


@app.route('/profile/edit/new-name/', methods=['POST'])
def new_name():
    user = current_user
    user.username = request.form['new-username']
    db.session.commit()
    return render_template('profile.html', user=user)
