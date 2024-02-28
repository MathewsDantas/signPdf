# -*- coding: utf-8 -*-
from safedelete.managers import SafeDeleteManager
from django.contrib.auth.models import UserManager


class UsuarioManager(SafeDeleteManager, UserManager):
    def authenticate(self, request, username=None, email=None, password=None, **kwargs):
        # Implemente a lógica de autenticação aqui, considerando ambos username e email
        print("aqui", request.data)
        user = self.get_by_natural_key(username) if username else None
        if user and user.check_password(password):
            return user
        user = self.get_by_natural_key(email) if email else None
        if user and user.check_password(password):
            return user
        return
