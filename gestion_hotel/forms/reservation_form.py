from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.validators import DataRequired

class ReservationForm(FlaskForm):
    client_id = SelectField('Client', coerce=int, validators=[DataRequired()])
    agent_id = SelectField('Agent', coerce=int, validators=[DataRequired()])
    statut = SelectField('Statut', choices=[
        ('en cours', 'En cours'),
        ('terminée', 'Terminée'),
        ('annulée', 'Annulée')
    ])