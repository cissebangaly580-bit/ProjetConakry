"""
Décorateurs pour la gestion des rôles et droits d'accès.
Conforme au cahier des charges: section 2 (Acteurs) et section 3.4 (Module Administration).
"""

from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from conakry_travel_hotel.models import Agent


def require_role(*roles):
    """
    Décorateur pour vérifier que l'utilisateur a au moins un des rôles spécifiés.
    
    Usage:
        @require_role('agent', 'admin')
        def my_view(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, "Vous devez être connecté.")
                return redirect('connexion')
            
            try:
                agent = Agent.objects.get(user=request.user)
                if agent.role in roles:
                    return view_func(request, *args, **kwargs)
                else:
                    messages.error(request, f"Accès refusé. Vous devez avoir un des rôles suivants: {', '.join(roles)}")
                    return redirect('accueil')
            except Agent.DoesNotExist:
                messages.error(request, "Profil agent non trouvé. Contactez l'administrateur.")
                return redirect('accueil')
        
        return wrapper
    return decorator


def require_agent(view_func):
    """Rôle: Agent de voyage - Gestion des dossiers clients et réservations."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('connexion')
        
        try:
            agent = Agent.objects.get(user=request.user)
            if agent.role in ['agent', 'admin']:  # Agents et admins peuvent accéder
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, "Accès refusé. Seuls les agents de voyage peuvent accéder.")
                return redirect('accueil')
        except Agent.DoesNotExist:
            messages.error(request, "Profil agent non trouvé.")
            return redirect('accueil')
    
    return wrapper


def require_receptionniste(view_func):
    """Rôle: Réceptionniste - Gestion check-in/checkout et émission de factures."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('connexion')
        
        try:
            agent = Agent.objects.get(user=request.user)
            if agent.role in ['receptionniste', 'admin']:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, "Accès refusé. Seuls les réceptionnistes peuvent accéder.")
                return redirect('accueil')
        except Agent.DoesNotExist:
            messages.error(request, "Profil agent non trouvé.")
            return redirect('accueil')
    
    return wrapper


def require_comptable(view_func):
    """Rôle: Comptable - Enregistrement et suivi des paiements."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('connexion')
        
        try:
            agent = Agent.objects.get(user=request.user)
            if agent.role in ['comptable', 'admin']:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, "Accès refusé. Seuls les comptables peuvent accéder.")
                return redirect('accueil')
        except Agent.DoesNotExist:
            messages.error(request, "Profil agent non trouvé.")
            return redirect('accueil')
    
    return wrapper


def require_admin(view_func):
    """Rôle: Administrateur - Gestion des utilisateurs et paramètres."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('connexion')
        
        try:
            agent = Agent.objects.get(user=request.user)
            if agent.role == 'admin':
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, "Accès refusé. Seuls les administrateurs peuvent accéder.")
                return redirect('accueil')
        except Agent.DoesNotExist:
            messages.error(request, "Profil agent non trouvé.")
            return redirect('accueil')
    
    return wrapper
