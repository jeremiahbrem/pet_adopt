from flask_wtf import FlaskForm
from flask import Flask
from wtforms import StringField, IntegerField, TextAreaField, BooleanField
from wtforms.validators import InputRequired, DataRequired, Optional, URL, AnyOf, NumberRange, ValidationError
from flask_wtf.file import FileField, FileAllowed, FileRequired

images = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']

def check_photo_inputs(form, field):
        if field.data and form.photo_upload.data:
            raise ValidationError('Only one photo submission allowed')

class AddPetForm(FlaskForm):
    """Form for adding pets."""

    name = StringField("Pet Name", validators=[InputRequired()])
    species = StringField("Species", 
                          validators=[InputRequired(), 
                                      AnyOf(message="Sorry, you can only choose from cat, dog, or porcupine",
                                            values=["cat", "dog", "porcupine"])])
    photo_url = StringField("Photo URL", validators=[Optional(), URL(), check_photo_inputs])
    photo_upload = FileField("Photo Upload", validators=[Optional(), FileAllowed(images, "Image only!")])
    age = IntegerField("Age", 
                       validators=[Optional(), 
                                   NumberRange(min=0, max=30, 
                                               message="Sorry, the age must be from 0 to 30")])
    notes = TextAreaField("Notes", validators=[Optional()])

class EditPetForm(FlaskForm):
    """Form for editing pets."""

    photo_url = StringField("Photo URL", validators=[Optional(), URL(), check_photo_inputs])
    photo_upload = FileField("Photo Upload", validators=[Optional()])
    notes = TextAreaField("Notes", validators=[Optional()])
    available = BooleanField("Available", validators=[Optional()])