from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Email, Optional

class ClientForm(FlaskForm):
    nom = StringField('Nom', validators=[DataRequired()])
    prenom = StringField('Prénom', validators=[DataRequired()])
    email = StringField('Email', validators=[Optional(), Email()])
    telephone = StringField('Téléphone', validators=[DataRequired()])
    adresse = TextAreaField('Adresse', validators=[Optional()])