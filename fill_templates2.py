from pathlib import Path

files = {
    'gestion_voyages/templates/gestion_voyages/voyage_detail.html': '''{% extends 'conakry_travel_hotel/base.html' %}

{% block title %}Détail voyage - Conakry Travel & Hôtel{% endblock %}

{% block content %}
<h1>Détails du voyage</h1>
<div class="card">
    <p><strong>Destination :</strong> {{ voyage.destination }}</p>
    <p><strong>Description :</strong> {{ voyage.description }}</p>
    <p><strong>Date départ :</strong> {{ voyage.date_depart }}</p>
    <p><strong>Date retour :</strong> {{ voyage.date_retour }}</p>
    <p><strong>Prix :</strong> {{ voyage.prix }} GNF</p>
    <p><strong>Places disponibles :</strong> {{ voyage.places_dispo }}</p>
</div>
<a href="{% url 'voyage_modifier' voyage.pk %}" class="btn-submit">Modifier</a>
<a href="{% url 'voyage_supprimer' voyage.pk %}" class="btn-submit btn-danger">Supprimer</a>
<a href="{% url 'voyage_liste' %}" class="btn-submit btn-secondary">Retour</a>
{% endblock %}
''',
    'gestion_voyages/templates/gestion_voyages/voyage_form.html': '''{% extends 'conakry_travel_hotel/base.html' %}

{% block title %}{% if voyage %}Modifier l'offre{% else %}Nouvelle offre{% endif %} - Conakry Travel & Hôtel{% endblock %}

{% block content %}
<h1>{% if voyage %}Modifier l'offre de voyage{% else %}Nouvelle offre de voyage{% endif %}</h1>
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit" class="btn-submit">Enregistrer</button>
    <a href="{% url 'voyage_liste' %}" class="btn-submit btn-secondary">Annuler</a>
</form>
{% endblock %}
''',
    'gestion_voyages/templates/gestion_voyages/voyage_confirme_delete.html': '''{% extends 'conakry_travel_hotel/base.html' %}

{% block title %}Supprimer voyage - Conakry Travel & Hôtel{% endblock %}

{% block content %}
<h1>Supprimer l'offre de voyage</h1>
<p>Voulez-vous vraiment supprimer le voyage <strong>{{ voyage.destination }}</strong> ?</p>
<form method="post">
    {% csrf_token %}
    <button type="submit" class="btn-submit btn-danger">Oui, supprimer</button>
    <a href="{% url 'voyage_liste' %}" class="btn-submit btn-secondary">Annuler</a>
</form>
{% endblock %}
''',
    'gestion_hotel/templates/gestion_hotel/chambre.detail.html': '''{% extends 'conakry_travel_hotel/base.html' %}

{% block title %}Détail chambre - Conakry Travel & Hôtel{% endblock %}

{% block content %}
<h1>Détails de la chambre</h1>
<div class="card">
    <p><strong>Numéro :</strong> {{ chambre.numero }}</p>
    <p><strong>Type :</strong> {{ chambre.get_type_chambre_display }}</p>
    <p><strong>Capacité :</strong> {{ chambre.capacite }}</p>
    <p><strong>Prix par nuit :</strong> {{ chambre.prix_nuit }} GNF</p>
    <p><strong>Statut :</strong> {{ chambre.get_statut_display }}</p>
</div>
<a href="{% url 'chambre_modifier' chambre.pk %}" class="btn-submit">Modifier</a>
<a href="{% url 'chambre_supprimer' chambre.pk %}" class="btn-submit btn-danger">Supprimer</a>
<a href="{% url 'chambre_liste' %}" class="btn-submit btn-secondary">Retour</a>
{% if chambre.statut == 'libre' %}
<a href="{% url 'chambre_checkin' chambre.pk %}" class="btn-submit">Check-in</a>
{% else %}
<a href="{% url 'chambre_checkout' chambre.pk %}" class="btn-submit btn-secondary">Check-out</a>
{% endif %}
{% endblock %}
''',
    'gestion_hotel/templates/gestion_hotel/chambre.form.html': '''{% extends 'conakry_travel_hotel/base.html' %}

{% block title %}{% if chambre %}Modifier la chambre{% else %}Nouvelle chambre{% endif %} - Conakry Travel & Hôtel{% endblock %}

{% block content %}
<h1>{% if chambre %}Modifier la chambre{% else %}Nouvelle chambre{% endif %}</h1>
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit" class="btn-submit">Enregistrer</button>
    <a href="{% url 'chambre_liste' %}" class="btn-submit btn-secondary">Annuler</a>
</form>
{% endblock %}
''',
    'gestion_hotel/templates/gestion_hotel/chambre_confirm_detete.html': '''{% extends 'conakry_travel_hotel/base.html' %}

{% block title %}Supprimer chambre - Conakry Travel & Hôtel{% endblock %}

{% block content %}
<h1>Supprimer la chambre</h1>
<p>Voulez-vous vraiment supprimer la chambre <strong>{{ chambre.numero }}</strong> ?</p>
<form method="post">
    {% csrf_token %}
    <button type="submit" class="btn-submit btn-danger">Oui, supprimer</button>
    <a href="{% url 'chambre_liste' %}" class="btn-submit btn-secondary">Annuler</a>
</form>
{% endblock %}
''',
    'gestion_hotel/templates/gestion_hotel/checkin.html': '''{% extends 'conakry_travel_hotel/base.html' %}

{% block title %}Check-in - Conakry Travel & Hôtel{% endblock %}

{% block content %}
<h1>Check-in</h1>
<p>Marquer la chambre <strong>{{ chambre.numero }}</strong> comme occupée.</p>
<form method="post">
    {% csrf_token %}
    <button type="submit" class="btn-submit">Confirmer le check-in</button>
    <a href="{% url 'chambre_detail' chambre.pk %}" class="btn-submit btn-secondary">Annuler</a>
</form>
{% endblock %}
''',
    'gestion_hotel/templates/gestion_hotel/checkout.html': '''{% extends 'conakry_travel_hotel/base.html' %}

{% block title %}Check-out - Conakry Travel & Hôtel{% endblock %}

{% block content %}
<h1>Check-out</h1>
<p>Marquer la chambre <strong>{{ chambre.numero }}</strong> comme libre.</p>
<form method="post">
    {% csrf_token %}
    <button type="submit" class="btn-submit">Confirmer le check-out</button>
    <a href="{% url 'chambre_detail' chambre.pk %}" class="btn-submit btn-secondary">Annuler</a>
</form>
{% endblock %}
''',
    'reservations/templates/reservations/reservation_detail.html': '''{% extends 'conakry_travel_hotel/base.html' %}

{% block title %}Détail réservation - Conakry Travel & Hôtel{% endblock %}

{% block content %}
<h1>Détails de la réservation</h1>
<div class="card">
    <p><strong>Client :</strong> {{ reservation.client.prenom }} {{ reservation.client.nom }}</p>
    <p><strong>Statut :</strong> {{ reservation.get_statut_display }}</p>
    <p><strong>Date :</strong> {{ reservation.date_reservation }}</p>
</div>
{% if concerner %}
<div class="card">
    <h2>Voyage</h2>
    <p><strong>Destination :</strong> {{ concerner.voyage.destination }}</p>
    <p><strong>Nombre de personnes :</strong> {{ concerner.nb_personnes }}</p>
</div>
{% endif %}
{% if inclure %}
<div class="card">
    <h2>Hébergement</h2>
    <p><strong>Chambre :</strong> {{ inclure.chambre.numero }}</p>
    <p><strong>Période :</strong> {{ inclure.date_entree }} à {{ inclure.date_sortie }}</p>
</div>
{% endif %}
{% if facture %}
<div class="card">
    <h2>Facture</h2>
    <p><strong>Montant :</strong> {{ facture.montant }} GNF</p>
    <p><strong>Statut :</strong> {{ facture.get_statut_paiement_display }}</p>
    <p><strong>Mode :</strong> {{ facture.get_mode_paiement_display }}</p>
    <a href="{% url 'facture_detail' facture.pk %}" class="btn-submit">Voir la facture</a>
</div>
{% endif %}
<a href="{% url 'reservation_liste' %}" class="btn-submit btn-secondary">Retour</a>
{% endblock %}
''',
    'reservations/templates/reservations/reservation_conform.html': '''{% extends 'conakry_travel_hotel/base.html' %}

{% block title %}Formulaire réservation - Conakry Travel & Hôtel{% endblock %}

{% block content %}
<h1>{% if reservation %}Modifier la réservation{% else %}Nouvelle réservation{% endif %}</h1>
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit" class="btn-submit">Enregistrer</button>
    <a href="{% url 'reservation_liste' %}" class="btn-submit btn-secondary">Annuler</a>
</form>
{% endblock %}
''',
    'reservations/templates/reservations/reservation_confir_delete.html': '''{% extends 'conakry_travel_hotel/base.html' %}

{% block title %}Annuler réservation - Conakry Travel & Hôtel{% endblock %}

{% block content %}
<h1>Annuler la réservation</h1>
<p>Voulez-vous vraiment annuler la réservation n°{{ reservation.id }} ?</p>
<form method="post">
    {% csrf_token %}
    <button type="submit" class="btn-submit btn-danger">Oui, annuler</button>
    <a href="{% url 'reservation_detail' reservation.pk %}" class="btn-submit btn-secondary">Annuler</a>
</form>
{% endblock %}
''',
    'facturation/templates/facturation/facture_detail.html': '''{% extends 'conakry_travel_hotel/base.html' %}

{% block title %}Détail facture - Conakry Travel & Hôtel{% endblock %}

{% block content %}
<h1>Détails de la facture</h1>
<div class="card">
    <p><strong>Montant :</strong> {{ facture.montant }} GNF</p>
    <p><strong>Statut :</strong> {{ facture.get_statut_paiement_display }}</p>
    <p><strong>Date :</strong> {{ facture.date_emission }}</p>
    <p><strong>Mode :</strong> {{ facture.get_mode_paiement_display }}</p>
</div>
<p><strong>Réservation :</strong> {{ facture.reservation.id }}</p>
<a href="{% url 'facture_paiement' facture.pk %}" class="btn-submit">Saisir le paiement</a>
<a href="{% url 'facture_recu' facture.pk %}" class="btn-submit btn-secondary">Voir le reçu</a>
<a href="{% url 'facture_liste' %}" class="btn-submit btn-secondary">Retour</a>
{% endblock %}
''',
    'facturation/templates/facturation/paiment.html': '''{% extends 'conakry_travel_hotel/base.html' %}

{% block title %}Paiement - Conakry Travel & Hôtel{% endblock %}

{% block content %}
<h1>Validation du paiement</h1>
<div class="card">
    <p><strong>Facture :</strong> {{ facture.id }}</p>
    <p><strong>Montant :</strong> {{ facture.montant }} GNF</p>
</div>
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit" class="btn-submit">Valider le paiement</button>
    <a href="{% url 'facture_detail' facture.pk %}" class="btn-submit btn-secondary">Annuler</a>
</form>
{% endblock %}
''',
    'facturation/templates/facturation/recu.html': '''{% extends 'conakry_travel_hotel/base.html' %}

{% block title %}Reçu - Conakry Travel & Hôtel{% endblock %}

{% block content %}
<h1>Reçu de paiement</h1>
<div class="card">
    <p><strong>Facture :</strong> {{ facture.id }}</p>
    <p><strong>Montant :</strong> {{ facture.montant }} GNF</p>
    <p><strong>Statut :</strong> {{ facture.get_statut_paiement_display }}</p>
    <p><strong>Mode :</strong> {{ facture.get_mode_paiement_display }}</p>
    <p><strong>Date :</strong> {{ facture.date_emission }}</p>
</div>
<a href="{% url 'facture_detail' facture.pk %}" class="btn-submit btn-secondary">Retour</a>
{% endblock %}
''',
}

for rel_path, content in files.items():
    path = Path(rel_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')

print('written', len(files), 'templates')
