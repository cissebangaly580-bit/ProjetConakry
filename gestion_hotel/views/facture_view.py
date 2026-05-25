from flask import Blueprint, render_template, request, redirect, url_for
from models.facture import lister_factures, ajouter_facture, modifier_facture, supprimer_facture, get_facture
from models.reservation import lister_reservations
from forms.facture_form import FactureForm

facture_bp = Blueprint('facture', __name__)

@facture_bp.route('/factures')
def liste():
    factures = lister_factures()
    return render_template('factures/liste.html', factures=factures)

@facture_bp.route('/factures/ajouter', methods=['GET', 'POST'])
def ajouter():
    form = FactureForm()
    reservations = lister_reservations()
    form.reservation_id.choices = [
        (r[0], f"Réservation {r[0]} - {r[4]}") for r in reservations
    ]
    if form.validate_on_submit():
        ajouter_facture(
            form.reservation_id.data,
            form.montant.data,
            form.mode_paiement.data
        )
        return redirect(url_for('facture.liste'))
    return render_template('factures/ajouter.html', form=form)

@facture_bp.route('/factures/modifier/<int:id>', methods=['GET', 'POST'])
def modifier(id):
    facture = get_facture(id)
    form = FactureForm()
    reservations = lister_reservations()
    form.reservation_id.choices = [
        (r[0], f"Réservation {r[0]} - {r[4]}") for r in reservations
    ]
    if form.validate_on_submit():
        modifier_facture(
            id,
            form.montant.data,
            form.statut_paiement.data,
            form.mode_paiement.data
        )
        return redirect(url_for('facture.liste'))
    return render_template('factures/modifier.html', form=form, facture=facture)

@facture_bp.route('/factures/supprimer/<int:id>')
def supprimer(id):
    supprimer_facture(id)
    return redirect(url_for('facture.liste'))