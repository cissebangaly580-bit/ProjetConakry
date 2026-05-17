from django.contrib import admin
from .models import Client, Voyage, Chambre, Agent, Reservation, Concerner, Inclure, Facture

admin.site.register(Client)
admin.site.register(Voyage)
admin.site.register(Chambre)
admin.site.register(Agent)
admin.site.register(Reservation)
admin.site.register(Concerner)
admin.site.register(Inclure)
admin.site.register(Facture)