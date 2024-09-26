import os
from flask import Blueprint, Response, Flask, session
from flask import request, render_template, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from cem_package.models import users, news  # import only necessary models
from cem_package import db, create_app
import rec_sys as model

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))
views = Blueprint('views', __name__)

@views.route('/')
def home():
    # You may want to display news articles or other relevant information
    all_news = news.query.all()
    return render_template('index.html', news=all_news)

@views.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('pswd')
        user_a = users.query.filter_by(comp_email=email).first()
        user_i = users.query.filter_by(inf_email=email).first()
        if user_a and check_password_hash(user_a.password, password):
            flash('Logged in successfully!', category='success')
            login_user(user_a, remember=True)
            return redirect('/dashboard')
        elif user_i and check_password_hash(user_i.password, password):
            flash('Logged in successfully!', category='success')
            login_user(user_i, remember=True)
            return redirect('/dashboard')
        else:
            flash('Incorrect credentials. Please try again.', category='error')
    return render_template('login.html')

@views.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully!", category='success')
    return redirect(url_for('views.home'))

# Use the following route if you wish to create a dashboard for users
@views.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if current_user.comp_name:
        # Fetch and display relevant information for company users
        return render_template('dashboard.html', user=current_user)
    else:
        # Fetch and display relevant information for individual users
        return render_template('dashboard.html', user=current_user)
    
@views.route('/register')
def register():
    return render_template('registration.html')

@views.route('/adv_regis', methods=['GET', 'POST'])
def adv_regis():
    if request.method == 'POST':
        comp_name = request.form.get("comp_name")
        acc_handler_name = request.form.get("acc_handler_name")
        acc_handler_desig = request.form.get("acc_handler_desig")
        comp_website = request.form.get("comp_website")
        ph_no = request.form.get("ph_no")
        comp_email = request.form.get("comp_email")
        ah_email = request.form.get("ah_email")
        categories = request.form.get("advt_categories")
        pswd1 = request.form.get("pswd1")
        acc_handler_gender = request.form["gender"]
        acc_type = 'advt'
        max_id = db.session.query(users).order_by(users.id.desc()).first()
        
        # Check for existing user with the same email
        user = users.query.filter_by(comp_email=comp_email).first()
        if user:
            flash('Email already exists.', category='error')
            return render_template('advertiser-registration.html')
        else:
            # Hashing the password for security
            hashed_password = generate_password_hash(pswd1, method='sha256')
            
            # Creating a new user entry
            if max_id:
                adv_regis_user = users(
                    id=max_id.id + 1,
                    comp_name=comp_name,
                    acc_handler_name=acc_handler_name,
                    acc_handler_desig=acc_handler_desig,
                    comp_website=comp_website,
                    ph_no=ph_no,
                    comp_email=comp_email,
                    ah_email=ah_email,
                    categories=categories,
                    password=hashed_password,
                    acc_handler_gender=acc_handler_gender,
                    acc_type=acc_type
                )
            else:
                adv_regis_user = users(
                    id=1,
                    comp_name=comp_name,
                    acc_handler_name=acc_handler_name,
                    acc_handler_desig=acc_handler_desig,
                    comp_website=comp_website,
                    ph_no=ph_no,
                    comp_email=comp_email,
                    ah_email=ah_email,
                    categories=categories,
                    password=hashed_password,
                    acc_handler_gender=acc_handler_gender,
                    acc_type=acc_type
                )
            
            # Adding user to the database
            db.session.add(adv_regis_user)
            db.session.commit()
            flash('Account created! Please login', category='success')
            return redirect(url_for('views.login'))
    
    # Rendering the registration form for advertiser
    return render_template('advertiser-registration.html')

@views.route('/inf_regis', methods=['GET', 'POST'])
def inf_regis():
    if request.method == 'POST':
        # Handling profile picture upload
        file = request.files['infl_pic']
        if file and allowed_file(file.filename):
            fname = request.form.get("fname")
            lname = request.form.get("lname")
            smh = request.form.get("smh")
            ph_no = request.form.get("ph_no")
            inf_email = request.form.get("inf_email")
            categories = request.form.get("inf_categories")
            age = request.form.get("age")
            pswd1 = request.form.get("pswd1")
            gender = request.form["gender"]
            acc_type = 'infl'
            
            # Get the maximum ID for creating a new user ID
            max_id = db.session.query(users).order_by(users.id.desc()).first()
            
            # Secure the filename and get the mimetype
            filename = secure_filename(file.filename)
            mimetype = file.mimetype
            
            # Save the file to the upload folder
            file.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename))

            # Check if email already exists
            user = users.query.filter_by(inf_email=inf_email).first()
            if user:
                flash('Email already exists.', category='error')
                return render_template('influencer-registration.html')
            else:
                # Hash the password for secure storage
                hashed_password = generate_password_hash(pswd1, method='sha256')
                
                # Creating a new user entry with an incremented ID or ID=1
                inf_regis_user = users(
                    id=(max_id.id + 1) if max_id else 1,
                    fname=fname,
                    lname=lname,
                    smh=smh,
                    ph_no=ph_no,
                    inf_email=inf_email,
                    categories=categories,
                    password=hashed_password,
                    age=age,
                    gender=gender,
                    acc_type=acc_type,
                    infl_pic=filename,
                    mimetype=mimetype
                )
                
                # Adding user to the database
                db.session.add(inf_regis_user)
                db.session.commit()
                
                flash('Account created! Please login', category='success')
                return redirect(url_for('views.login'))
    
    # Rendering the influencer registration form
    return render_template('influencer-registration.html')
