from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, DateField, TextAreaField
from wtforms.validators import DataRequired, Optional

class VoyageForm(FlaskForm):
    destination = StringField('Destination', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional()])
    date_depart = DateField('Date de départ', validators=[DataRequired()])
    date_retour = DateField('Date de retour', validators=[DataRequired()])
    prix = FloatField('Prix par personne', validators=[DataRequired()])
    places_dispo = IntegerField('Places disponibles', validators=[DataRequired()])