from flask import Blueprint, render_template, request, redirect, url_for
from models.voyage import lister_voyages, ajouter_voyage, modifier_voyage, supprimer_voyage, get_voyage
from forms.voyage_form import VoyageForm

voyage_bp = Blueprint('voyage', __name__)

@voyage_bp.route('/voyages')
def liste():
    voyages = lister_voyages()
    return render_template('voyages/liste.html', voyages=voyages)

@voyage_bp.route('/voyages/ajouter', methods=['GET', 'POST'])
def ajouter():
    form = VoyageForm()
    if form.validate_on_submit():
        ajouter_voyage(
            form.destination.data,
            form.description.data,
            form.date_depart.data,
            form.date_retour.data,
            form.prix.data,
            form.places_dispo.data
        )
        return redirect(url_for('voyage.liste'))
    return render_template('voyages/ajouter.html', form=form)

@voyage_bp.route('/voyages/modifier/<int:id>', methods=['GET', 'POST'])
def modifier(id):
    voyage = get_voyage(id)
    form = VoyageForm()
    if form.validate_on_submit():
        modifier_voyage(
            id,
            form.destination.data,
            form.description.data,
            form.date_depart.data,
            form.date_retour.data,
            form.prix.data,
            form.places_dispo.data
        )
        return redirect(url_for('voyage.liste'))
    return render_template('voyages/modifier.html', form=form, voyage=voyage)

@voyage_bp.route('/voyages/supprimer/<int:id>')
def supprimer(id):
    supprimer_voyage(id)
    return redirect(url_for('voyage.liste'))