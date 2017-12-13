import os
from flask import Flask, render_template, session, redirect, url_for, flash, request, jsonify
from flask_script import Manager, Shell
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField, widgets
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy
import requests

from flask_mail import Mail, Message
from threading import Thread
from werkzeug import secure_filename

from flask_migrate import Migrate, MigrateCommand

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_required, logout_user, login_user, UserMixin, current_user

from wtforms import StringField, SubmitField, FileField, PasswordField, BooleanField, SelectMultipleField, ValidationError
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'profiles/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.debug = True
app.config['SECRET_KEY'] = 'hardtoguessstringfromsi364(thisisnotsupersecure)'

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://localhost/bblitzerFinal"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app) 

genre_map = {'comedy': 4404, 'drama': 4406, 'classics': 4403, 'thriller': 4416}


app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587 
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = "blitzer364@gmail.com"
app.config['MAIL_PASSWORD'] = "michigan"
app.config['MAIL_SUBJECT_PREFIX'] = '[Movie Collection App]'
app.config['MAIL_SENDER'] = 'Admin <blitzer364@gmail.com>'
app.config['ADMIN'] = "blitzer364@gmail.com"


manager = Manager(app)
db = SQLAlchemy(app) 
migrate = Migrate(app, db) 
manager.add_command('db', MigrateCommand)
mail = Mail(app) 


def send_email(to, subject, template, **kwargs):
    with app.app_context():
        msg = Message(app.config['MAIL_SUBJECT_PREFIX'] + ' ' + subject, sender=app.config['MAIL_SENDER'], recipients=[to])
        msg.body = render_template(template + '.txt', **kwargs)
        msg.html = render_template(template + '.html', **kwargs)
        mail.send(msg)


class Movie(db.Model):
    __tablename__ = "movies"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(285))
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.id'))
    image_link = db.Column(db.String)

class Genre(db.Model):
    __tablename__ = "genres"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(285))
    itunes_id = db.Column(db.Integer)

class MovieCollection(db.Model):
    __tablename__ = "collections"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'))


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(200))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

class FileUpload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(200))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class ActorForm(FlaskForm):
    actor1 = StringField("Actor 1 ", validators=[Required()])
    actor2 = StringField("Actor 2",validators=[Required()])
    actor3 = StringField("Actor 3", validators=[Required()])
    genre_list = StringField("Comma-separated genre list", validators=[Required()])
    submit = SubmitField('Submit')

def get_or_create_genre(name):
    genre = db.session.query(Genre).filter_by(name=name).first()
    if genre:
        return genre
    new_genre = Genre(name=name, itunes_id=genre_map[name])
    db.session.add(new_genre)
    db.session.commit()
    return new_genre


def get_or_create_movie(title, genre_name, image_link):
    movie = db.session.query(Movie).filter_by(title=title).first()
    if movie:
        return movie
    else:
        genre_id = get_or_create_genre(genre_name.lower()).id
        new_movie = Movie(title=title, genre_id=genre_id, image_link=image_link)
        db.session.add(new_movie)
        db.session.commit()
        return new_movie

def get_or_create_collection_item(user, movie_name):
    user_id = user.id
    movie_id = get_or_create_movie(movie_name, "", "").id
    item = db.session.query(MovieCollection).filter_by(user_id=user_id, movie_id=movie_id).first()
    if item:
        return item
    else:
        item = MovieCollection(user_id=user_id, movie_id=movie_id)
        db.session.add(item)
        db.session.commit()
        return item


def get_data(genre_name, actor_search):
    data = requests.get('https://itunes.apple.com/search', params={'genreId': genre_map[genre_name], 'term': actor_search}).json()["results"]
    for each_movie in data:
        new_movie = get_or_create_movie(each_movie["trackName"], each_movie['primaryGenreName'], each_movie["artworkUrl100"])
    return data


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

class RegistrationForm(FlaskForm):
    email = StringField('Email:', validators=[Required(),Length(1,64),Email()])
    password = PasswordField('Password:',validators=[Required(),EqualTo('password2',message="Passwords must match")])
    password2 = PasswordField("Confirm Password:",validators=[Required()])
    submit = SubmitField('Register User')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1,64), Email()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


@app.route('/login',methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('index'))
        flash('Invalid password.')
    return render_template('login.html',form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('index'))

@app.route('/register',methods=["GET","POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You can now log in!')
        return redirect(url_for('login'))
    return render_template('register.html',form=form)

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = ActorForm()
    return render_template('index.html', form=form)

@app.route("/results", methods=["POST"])
@login_required
def movieResults():
    form = ActorForm()
    if form.validate_on_submit():
        actorsList = [form.actor1.data, form.actor2.data, form.actor3.data]
        genreList = [genre_name.strip().lower() for genre_name in form.genre_list.data.split(",")]
        resultsList = []
        for actor in actorsList:
            for genre in genreList:
                resultsList.extend(get_data(genre, actor))
        return render_template("results.html", results=resultsList)
    return "Form didn't work :("

@app.route("/movie/<movie_name>/description", methods=["GET", "POST"])
@login_required
def getMovieDescription(movie_name):
    if request.method == "POST":
        get_or_create_collection_item(current_user, movie_name)
        return redirect("/collection")
    return render_template("long_description.html", data=requests.get('https://itunes.apple.com/search', params={'entity': "movie", 'term': movie_name}).json()["results"][0])

@app.route("/collection")
@login_required
def collection():
    data = db.session.query(MovieCollection, Genre, Movie).filter(MovieCollection.user_id == current_user.id).join(Movie).join(Genre).all()
    send_email(current_user.email, "Your Collection!!", "mail/collection", lst=data)
    return redirect(url_for("collections"))

@app.route("/collections")
@login_required
def collections():
    data = db.session.query(MovieCollection, Genre, Movie).filter(MovieCollection.user_id == current_user.id).join(Movie).join(Genre).all()
    return render_template("collection.html", list_collection = data)

@app.route("/collections_api")
@login_required
def api():
    lst = [{"title": movie.Movie.title, "genre" : movie.Genre.name } for movie in db.session.query(MovieCollection, Genre, Movie).filter(MovieCollection.user_id == current_user.id).join(Movie).join(Genre).all()]
    return jsonify({
        'user_list' : lst
        })

@app.route('/upload', methods=["POST"])
@login_required
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # Save to db
            new_file = FileUpload(user_id=current_user.id, name=filename)
            db.session.add(new_file)
            db.session.commit()
            return redirect(url_for('uploaded_file'))

from flask import send_from_directory
@app.route('/my_pic')
def uploaded_file():
    filename = db.session.query(FileUpload).filter_by(user_id=current_user.id).first().name
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


if __name__ == '__main__':
    db.create_all()
    manager.run()
