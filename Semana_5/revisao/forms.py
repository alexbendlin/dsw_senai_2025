from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email

# Define a classe do formulário de contato.
# Cada campo é uma instância de uma classe de campo.
# Os validadores são passados como uma lista para o parâmetro `validators`.
class ContactForm(FlaskForm):
    nome = StringField('Nome:', validators=[DataRequired(message='Por favor, insira seu nome.')])
    email = StringField('E-mail:', validators=[DataRequired(message='Por favor, insira seu e-mail.'), Email(message='E-mail inválido.')])
    mensagem = TextAreaField('Mensagem:', validators=[DataRequired(message='Por favor, insira sua mensagem.')])
    submit = SubmitField('Enviar Mensagem')