from flask import Blueprint, request, render_template, abort,flash,redirect,url_for, session,Flask
from ..models.validity import RegistrationForm,loginform
from flask_login import current_user,login_required,LoginManager,login_user,logout_user
from ..models.User import User
import uuid
from ..models.User import db
from ..models.database import user
from werkzeug.security import generate_password_hash, check_password_hash

main = Blueprint('main', __name__, template_folder="../templates")

myuser=user("flask-mvc\instance\MainDB.db")
login_manager = LoginManager()

def loginmanager_init(app):
   login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
   print("ths is the id",user_id)
   return User.query.get(user_id) 

@main.route('/')
def index():
   return render_template("index.html")

@main.route('/signuppage')
def signuppage():
   form = RegistrationForm(request.form)
   return render_template("signup.html",form=form)

@main.route('/profile/<user_id>', methods=['GET','POST'])
@login_required
def profile(user_id):
   print("this is the id",user_id)
   info=myuser.get_info(user_id)
   bio = myuser.getbio(user_id)
   users=myuser.search()
   print('this is the info', info)
   print('this is the bio', bio)
   if myuser.getposts(user_id)!=None:
      posts=myuser.getposts(user_id)[0]
      print('this is the posts',posts)
      count_of_posts=myuser.getposts(user_id)[1]
      return render_template('profile.html', info=info, bio=bio, posts=posts, count=count_of_posts, users=users)
   return render_template("profile.html",info=info, bio=bio,users=users)

@main.route('/signup', methods=['POST'])
def signup():
   form = RegistrationForm(request.form)
   fname = request.form.get('firstName')
   lname =request.form.get('lastName')
   email=request.form.get('email')
   password=request.form.get('password1')
   if form.validate():
      print("im valid")
      if (User.query.filter_by(email=email).first()==None):
         print("im here")
         new_user = User(id=str(uuid.uuid4()), email=email,  password=generate_password_hash(password, method='pbkdf2:sha256'), first_name=fname, last_name=lname)
         db.session.add(new_user)
         db.session.commit()
         login_user(new_user, remember=True)
         return render_template('index.html', userr=current_user)
   return render_template('signup.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
   form = loginform(request.form)
   email=request.form.get('email')
   password=request.form.get('password')
   print(form.validate())
   user = User.query.filter_by(email=email).first()
   if form.validate() and check_password_hash(user.password, password):
      print("i got in")
      login_user(user,remember=True)
      #   session['user_id']=user.id
      #   session.permanent=True
      print(user.email)
      print(user.id)
      flash('Logged in successfully.')
      #   next = request.args.get('next')
      return render_template('index.html',)
   print("i didnt get in")
   return render_template('login.html',form=form)

@main.route('/logout')
@login_required
def logout():
   # print("this is the sessions id:",session['user_id'])
   logout_user()
   flash("you have been logged out.")
   return render_template('login.html')

@main.route("/add_bio/<user_id>", methods=['GET', 'POST'])
@login_required
def add_bio(user_id):
   bio=request.form.get("bioinput")
   info=myuser.get_info(user_id)
   none_test=myuser.getbio(user_id)
   if myuser.bio_exists(user_id)!=0 and (none_test=="" or none_test is None ):
      myuser.editbio(user_id,bio)
   else:
      myuser.addbio(user_id,bio)
   dbbio=myuser.getbio(user_id)
   if myuser.getposts(user_id)!=None:
      posts=myuser.getposts(user_id)[0]
      count_of_posts=myuser.getposts(user_id)[1]
      return render_template('profile.html', info=info, bio=dbbio, posts=posts, count=count_of_posts)
   return render_template('profile.html',bio=dbbio, info=info)

@main.route("/add_post/<user_id>", methods=['GET', 'POST'])
@login_required
def add_post(user_id):
   post=request.form.get("postinput")
   info=myuser.get_info(user_id)
   bio=myuser.getbio(user_id)
   myuser.addpost(user_id,post)
   if myuser.getposts(user_id)!=None:
      posts=myuser.getposts(user_id)[0]
      count_of_posts=myuser.getposts(user_id)[1]
      return render_template('profile.html', info=info, bio=bio, posts=posts, count=count_of_posts)
   return render_template('profile.html',bio=bio, info=info)

@main.route("/show_bio/<user_id>", methods=['GET', 'POST'])
def edit_bio(user_id):
   bio=request.form.get("editbio")
   myuser.editbio(user_id,bio)
   info=myuser.get_info(user_id)
   if myuser.getposts(user_id)!=None:
      posts=myuser.getposts(user_id)[0]
      count_of_posts=myuser.getposts(user_id)[1]
      return render_template('profile.html', info=info, bio=bio, posts=posts, count=count_of_posts)
   return render_template('profile.html',bio=bio, info=info)

@main.route("/display_posts/<user_id>", methods=['GET'])
def display_posts(user_id):
   bio=myuser.getbio(user_id)
   info=myuser.get_info(user_id)
   print("these are my posts",posts)
   if myuser.getposts(user_id)!=None:
      posts=myuser.getposts(user_id)[0]
      count_of_posts=myuser.getposts(user_id)[1]
      return render_template('profile.html', info=info, bio=bio, posts=posts, count=count_of_posts)
   return render_template('profile.html',bio=bio, info=info)