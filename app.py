import os
from flask import Flask, render_template, request, redirect, flash, send_from_directory, url_for, jsonify
from models import db, connect_db, Pet
from forms import AddPetForm, EditPetForm
from wtforms.validators import ValidationError
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)))

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "xjdjrh474hf744nf"
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

@app.route("/")
def show_pet_list():
    """Shows pet list home page"""

    pets = Pet.query.all()

    return render_template("pet_list.html", pets=pets)

@app.route("/add", methods=["GET", "POST"])
def add_pet():
    """Shows add pet form; handles form submit."""

    form = AddPetForm()

    if form.validate_on_submit():
        data = {key: value for key, value in form.data.items() if key not in 
                ["csrf_token", "photo_url","photo_upload"]}
        pet = Pet(**data)
                
        if form.photo_upload.data:
            f = form.photo_upload.data
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            pet.photo = url_for('static', filename=filename)

        elif form.photo_url.data:
            pet.photo = form.photo_url.data
        
        db.session.add(pet)
        db.session.commit()
        flash(f"Added {pet.name}")        
    
        return redirect("/")

    else:
        return render_template(
            "add_pet.html", form=form)       

@app.route("/<int:pet_id>", methods=["GET", "POST"])
def show_pet_details(pet_id):
    """Shows pet details and edit form page"""

    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)

    if form.validate_on_submit():
        if form.photo_upload.data:
            f = form.photo_upload.data
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            pet.photo = url_for('static', filename=filename)

        elif form.photo_url.data:
            pet.photo = form.photo_url.data
       
        pet.notes = form.notes.data
        pet.available = form.available.data

        db.session.commit()
        flash(f"{pet.name} updated!")
        return redirect(f"/{pet.id}")

    else:
        return render_template("pet_details.html", pet=pet, form=form)


          

    
