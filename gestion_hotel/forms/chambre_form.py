from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SelectField
from wtforms.validators import DataRequired, NumberRange

class ChambreForm(FlaskForm):
    numero = StringField('Numéro', validators=[DataRequired()])
    type_chambre = SelectField('Type', choices=[
        ('Simple', 'Simple'),
        ('Double', 'Double'),
        ('VIP', 'VIP'),
        ('Suite', 'Suite')
    ])
    prix_nuit = FloatField('Prix par nuit', validators=[DataRequired(), NumberRange(min=0)])
    capacite = IntegerField('Capacité', validators=[DataRequired(), NumberRange(min=1)])
    statut = SelectField('Statut', choices=[
        ('disponible', 'Disponible'),
        ('occupée', 'Occupée'),
        ('maintenance', 'Maintenance')
    ])