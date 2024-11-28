# produtos/models.py
from django.db import models

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.IntegerField()
    imagem = models.ImageField(upload_to='produtos/', null=True, blank=True)  # Campo de imagem

    def __str__(self):
        return self.nome
