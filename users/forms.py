from django import forms
from utils.users.utils import verify_email, is_valid_cpf
import re

class LoginForm(forms.Form):
    cpf = forms.CharField(
        max_length=11, 
        widget=forms.TextInput(attrs={'placeholder': 'CPF'}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Digite sua senha'})
    )

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf', '')

        if not cpf.isdigit() or len(cpf) != 11:
            raise forms.ValidationError('O CPF deve conter exatamente 11 dígitos numéricos.')

        if not is_valid_cpf(cpf):
            raise forms.ValidationError('O CPF fornecido é inválido.')

        return cpf


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Confirme seu e-mail'}),
        error_messages={'required': 'Este campo é obrigatório.'}
    )
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not verify_email(email):
            raise forms.ValidationError('O e-mail fornecido não é válido.')
        return email
    


class PasswordResetForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Nova Senha'}),
        error_messages={'required': 'Este campo é obrigatório.'}
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirme a Senha'}),
        error_messages={'required': 'Este campo é obrigatório.'}
    )

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')

        if password != password_confirm:
            raise forms.ValidationError('As senhas não coincidem.')

        return password_confirm

    def clean_password(self):
        password = self.cleaned_data.get('password')
        
        if len(password) < 6:
            raise forms.ValidationError('A senha deve ter pelo menos 6 caracteres.')

        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError('A senha deve conter pelo menos uma letra maiúscula.')

        if not re.search(r'\d', password):
            raise forms.ValidationError('A senha deve conter pelo menos um número.')

        if not re.search(r'[\W_]', password):
            pass

        return password