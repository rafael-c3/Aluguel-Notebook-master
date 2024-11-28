# produtos/models.py
from django.db import models
from django.contrib.auth.models import User

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.TextField(blank=True, null=True)
    estoque = models.PositiveIntegerField(default=0)
    disponivel = models.BooleanField(default=True)
    imagem = models.ImageField(upload_to='produtos/', blank=True, null=True)

    def save(self, *args, **kwargs):
        # Atualiza automaticamente o status de disponibilidade
        self.disponivel = self.estoque > 0
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome

class Aluguel(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    notebook = models.ForeignKey(Produto, on_delete=models.CASCADE)  # Substitua 'Notebook' pelo nome do modelo de produto
    meses = models.IntegerField()
    data_aluguel = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.notebook.nome} ({self.meses} meses)"