from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import DataRequired

class AgentForm(FlaskForm):
    nom = StringField('Nom', validators=[DataRequired()])
    prenom = StringField('Prénom', validators=[DataRequired()])
    login = StringField('Login', validators=[DataRequired()])
    mdp = PasswordField('Mot de passe', validators=[DataRequired()])
    role = SelectField('Rôle', choices=[
        ('admin', 'Admin'),
        ('réceptionniste', 'Réceptionniste'),
        ('gérant', 'Gérant')
    ])