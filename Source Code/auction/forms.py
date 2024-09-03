from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, IntegerField, SelectField, DecimalField
from wtforms.validators import InputRequired, Length, Email, EqualTo, ValidationError
from flask_wtf.file import FileRequired, FileAllowed, FileField

ALLOWED_FILE = {'png', 'jpg', 'JPG', 'PNG'}

# Form to add item - Connected to Item class in models.py
class ItemForm(FlaskForm):
  style = {'style': 'color: white; background-color: #657ee0; border-color: #657ee0;'} # same styling as 'but btn-theme' class

  title = StringField('Game Title', validators=[InputRequired()])

  genre = SelectField('Genre', choices=[('1', 'Action'), ('2', 'Fantasy'), ('3', 'Sports'), ('4', 'Family/Kids')], validators=[InputRequired()])
  platform = SelectField('Platform', choices=[('1', '3DS'), ('2', 'Wii'), ('3', 'Switch'), ('4', 'Xbox'), ('5', 'PS4')], validators=[InputRequired()])
  classification = SelectField('Classification', choices=[('1', 'G'), ('2', 'PG'), ('3', 'M'), ('4', 'MA15+'), ('5', 'R18+')], validators=[InputRequired()])
  release_year = SelectField('Relase Year', choices=[('1', '2020'), ('2', '2019'), ('3', '2018'), ('4', '2017'), ('5', '2016'), ('6', '2015')], validators=[InputRequired()])

  description = TextAreaField('Description', validators=[InputRequired()])
  image = FileField('Destination Image', validators=[FileRequired(message='Must choose image for game listing.'),
                                                    FileAllowed(ALLOWED_FILE, message='Only supports png, jpg, PNG, and JPG file formats.')])

  starting_bid = StringField('Starting Bid', validators=[InputRequired()])
  def validate_starting_bid(form, field):
      # Remove spaces
      number = field.data.replace(" ", "")
      print(number)
      # Check if only integers were used
      try:
        int(number)
      except:
        raise ValidationError("Please only use digits 0-9 in starting price.")

  submit = SubmitField("Create", render_kw=style)
  
# Add a comment
class CommentForm(FlaskForm):
  style = {'style': 'color: white; background-color: #657ee0; border-color: #657ee0;'} # same styling as 'but btn-theme' class
  text = TextAreaField('Comment', validators=[InputRequired()])
  submit = SubmitField('Post', render_kw=style)


# Place Bid
class PlaceBidForm(FlaskForm):
  style = {'style': 'color: white; background-color: #657ee0; border-color: #657ee0;'} # same styling as 'but btn-theme' class
  bid = DecimalField('Bid amount', validators=[InputRequired()])
  submit = SubmitField('Place bid', render_kw=style)


# Watch Item
class WatchForm(FlaskForm):
  style = {'style': 'color: white; background-color: #657ee0; border-color: #657ee0;'} # same styling as 'but btn-theme' class
  submit = SubmitField('Watch', render_kw=style)


# Close Auction
class CloseAuctionForm(FlaskForm):
  style = {'style': 'color: white; background-color: #657ee0; border-color: #657ee0;'} # same styling as 'but btn-theme' class
  submit = SubmitField('Close Auction', render_kw=style)


# Open Auction
class OpenAuctionForm(FlaskForm):
  style = {'style': 'color: white; background-color: #657ee0; border-color: #657ee0;'} # same styling as 'but btn-theme' class
  submit = SubmitField('Open Auction', render_kw=style)

# creates the login information
class LoginForm(FlaskForm):
    user_name=StringField("Username", validators=[InputRequired('Enter user name')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")


# this is the registration form - Connected to the User class in models.py
class RegisterForm(FlaskForm):
    user_name=StringField("Username", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[InputRequired(), Email("Please enter a valid email")])
    
    address_line1 = StringField("Address Line 1", validators=[InputRequired(message="This line must be filled.")])
    address_line2 = StringField("Address Line 2")

    states = [("1", "QLD"), ("2", "NSW"), ("3", "ACT"), ("4", "VIC"), ("5", "NT"), ("6", "SA"), ("7", "WA")]
    state = SelectField("State", choices = states, validators=[InputRequired()])
    
    # Zip field with custom validator
    zip = IntegerField("Zip Code", validators=[InputRequired()])
    def validate_zip(form, field):
        if not len(str(field.data)) == 4:
            raise ValidationError("Zip code must be 4 digits long")

    # Phone number field with custom validator
    phone_number = StringField("Phone Number", validators=[InputRequired()])
    def validate_phone_number(form, field):
        # Remove spaces
        number = field.data.replace(" ", "")
        print(number)
        # Check if only integers were used
        try:
          int(number)
        except:
          raise ValidationError("Please only use digits 0-9 in phone number.")
        # Check length of number
        if len(str(number)) < 8 or len(str(number)) > 10:
            raise ValidationError(f"Phone number is {len(str(number))} digit(s) long. Number must be must be between 8 and 10 digits")

    #linking two fields
    password=PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords must match")])
    confirm = PasswordField("Confirm Password")

    #submit button
    submit = SubmitField("Register")