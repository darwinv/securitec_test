from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    """Modelo de Usuario hereda de AbstractUser."""
    pass


class Cliente(models.Model):
    """Clientes"""
    documento = models.CharField(max_length=45)
    nombres = models.CharField(max_length=250)
    telefono = models.CharField(max_length=13)
    resultado = models.CharField(max_length=4, null=True)
    agente = models.ForeignKey(User, on_delete=models.PROTECT, null=True)


class DocumentoAgente(models.Model):
    documento = models.CharField(max_length=45, null=True)
    agente = models.ForeignKey(User, on_delete=models.PROTECT)
