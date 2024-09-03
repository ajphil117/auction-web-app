from flask import ( 
    Blueprint, flash, render_template, request, url_for, redirect, session
) 
from werkzeug.security import generate_password_hash,check_password_hash
#from .models import User
from .forms import LoginForm,RegisterForm
from .models import User
from flask_login import login_user, login_required, logout_user
from flask_bootstrap import Bootstrap

from . import db


#create a blueprint
bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    register_form_instance = RegisterForm()
    
    # Create user in database
    if register_form_instance.validate_on_submit():
        phone_number = register_form_instance.phone_number.data.replace(" ", "")
        username = register_form_instance.user_name.data
        email = register_form_instance.email_id.data
        pwd = register_form_instance.password.data
        address_line1 = register_form_instance.address_line1.data
        address_line2 = register_form_instance.address_line2.data
        state = register_form_instance.state.data
        zip = register_form_instance.zip.data

        # If user exists already:
        u = User.query.filter_by(user_name=username).first()
        if u:
            flash('This username already exists, please log in', 'info')
            return redirect(url_for('auth.login'))

        u = User.query.filter_by(phone_number=phone_number).first()
        if u:
            flash('Phone number associated with a user already. Please log in', 'info')
            return redirect(url_for('auth.login'))

        u = User.query.filter_by(emailid=email).first()
        if u:
            flash('Email associated with a user already. Please log in', 'info')
            return redirect(url_for('auth.login'))

        # Generate password hash and check against existing hash
        pwd_hash = generate_password_hash(pwd)
        new_user = User(phone_number=phone_number, user_name=username, emailid=email, password_hash=pwd_hash, address_line1=address_line1, address_line2=address_line2, state=state, zip=zip)

        # Add user
        db.session.add(new_user)
        db.session.commit()

        flash("Success! User created. Please log in", "success")
        return redirect(url_for("auth.login"))
    else:
        return render_template('auth/register.html', form=register_form_instance)


# Login user function
@bp.route('/login', methods=['GET', 'POST'])
def login(): #view function
    login_form = LoginForm()
    # Initialise error variable
    error=None
    if(login_form.validate_on_submit()==True):
        user_name = login_form.user_name.data
        password = login_form.password.data

        # Check that user is in database
        u1 = User.query.filter_by(user_name=user_name).first()
        if u1 is None:
            error='Incorrect Username'
        elif not check_password_hash(u1.password_hash, password): # takes the hash and password
            error='Incorrect password'
        if error is None:
            login_user(u1)
            session['user_name'] = user_name
            return redirect(url_for("main.index"))
        else:
            flash(error, 'danger')
    else:
        print(login_form.errors)
    return render_template('auth/login.html', form=login_form, heading='Login')

# Logout user
@bp.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('user_name')
    flash('Successfully logged out', 'info')
    return redirect(url_for('auth.login'))