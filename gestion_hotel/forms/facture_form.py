from flask_wtf import FlaskForm
from wtforms import SelectField, FloatField
from wtforms.validators import DataRequired

class FactureForm(FlaskForm):
    reservation_id = SelectField('Réservation', coerce=int, validators=[DataRequired()])
    montant = FloatField('Montant', validators=[DataRequired()])
    mode_paiement = SelectField('Mode de paiement', choices=[
        ('Espèces', 'Espèces'),
        ('Virement', 'Virement'),
        ('Carte', 'Carte'),
        ('Mobile Money', 'Mobile Money')
    ])
    statut_paiement = SelectField('Statut paiement', choices=[
        ('impayée', 'Impayée'),
        ('payée', 'Payée'),
        ('partielle', 'Partielle')
    ])