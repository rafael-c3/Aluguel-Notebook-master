# produtos/forms.py
from django import forms
from .models import Produto

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'preco', 'estoque', 'imagem']  # Incluindo imagem

class AlugarProdutoForm(forms.Form):
    meses = forms.ChoiceField(
        choices=[(i, f"{i} mês(es)") for i in range(1, 13)],
        widget=forms.Select,
        label="Tempo de aluguel (meses)"
    )