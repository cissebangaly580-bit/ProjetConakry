from flask import Blueprint, render_template, request, redirect, url_for
from models.client import lister_clients, ajouter_client, modifier_client, supprimer_client, get_client
from forms.client_form import ClientForm

client_bp = Blueprint('client', __name__)

@client_bp.route('/clients')
def liste():
    clients = lister_clients()
    return render_template('clients/liste.html', clients=clients)

@client_bp.route('/clients/ajouter', methods=['GET', 'POST'])
def ajouter():
    form = ClientForm()
    if form.validate_on_submit():
        ajouter_client(
            form.nom.data,
            form.prenom.data,
            form.email.data,
            form.telephone.data,
            form.adresse.data
        )
        return redirect(url_for('client.liste'))
    return render_template('clients/ajouter.html', form=form)

@client_bp.route('/clients/modifier/<int:id>', methods=['GET', 'POST'])
def modifier(id):
    client = get_client(id)
    form = ClientForm()
    if form.validate_on_submit():
        modifier_client(
            id,
            form.nom.data,
            form.prenom.data,
            form.email.data,
            form.telephone.data,
            form.adresse.data
        )
        return redirect(url_for('client.liste'))
    return render_template('clients/modifier.html', form=form, client=client)

@client_bp.route('/clients/supprimer/<int:id>')
def supprimer(id):
    supprimer_client(id)
    return redirect(url_for('client.liste'))