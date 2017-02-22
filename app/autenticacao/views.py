# coding: utf-8


################################################################################
## SIE - UFC
################################################################################
## Views do Blueprint de Autenticação
################################################################################


from flask import render_template, url_for, redirect, request, flash
from flask_login import current_user, login_user, logout_user, login_required

from . import autenticacao
from .. import db
from .forms import *
from ..models import Usuario
from ..util.email import enviar_email


########## Rotas ##########

# Redirecionar usuários que fizeram login, mas não confirmaram conta
@autenticacao.before_app_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.confirmado \
            and request.endpoint[:13] != 'autenticacao.' \
            and request.endpoint != 'static':

        return redirect(url_for('autenticacao.nao_confirmado'))


# Login
@autenticacao.route('/login', methods=['GET', 'POST'])
def login():
    form = FormLogin()

    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()

        if usuario and usuario.verificar_senha(form.senha.data):
            login_user(usuario, form.lembrar.data)
            return redirect(request.args.get('next') or url_for('principal.home'))

        flash('Email ou senha incorretos.', 'danger')

    return render_template('autenticacao/login.html', form=form)


# Logout
@autenticacao.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('principal.home'))


# Cadastro de Usuário
@autenticacao.route('/cadastro-usuario', methods=['GET', 'POST'])
def cadastro_usuario():
    form = FormCadastroUsuario()

    if form.validate_on_submit():
        usuario = Usuario(email=form.email.data,
                          nome=form.nome.data,
                          senha=form.senha.data)
        db.session.add(usuario)
        db.session.commit()
        token = usuario.gerar_token_confirmacao()
        enviar_email(usuario.email, 'Confirme Seu Cadastro',
                     'autenticacao/email/confirmacao', usuario=usuario, token=token)
        flash('Um email de confirmação foi enviado. Confira a sua caixa de entrada.', 'info')
        
        return redirect(url_for('principal.home'))

    return render_template('autenticacao/cadastro_usuario.html', form=form)


# Usuário Não Confirmado
@autenticacao.route('/nao-confirmado')
def nao_confirmado():
    if current_user.is_anonymous or current_user.confirmado:
        return redirect(url_for('principal.home'))

    return render_template('autenticacao/nao_confirmado.html')


# Confirmação de Conta
@autenticacao.route('/confirmacao/<token>')
@login_required
def confirmacao(token):
    if current_user.confirmado:
        return redirect(url_for('principal.home'))

    if current_user.confirmar_conta(token):
        flash('Seu cadastro foi confirmado. Obrigado!', 'success')
    else:
        flash('Este link de confirmação é inválido ou expirou.', 'danger')

    return redirect(url_for('principal.home'))


# Reenvio de Confirmação de Conta
@autenticacao.route('/confirmacao')
@login_required
def reenviar_confirmacao():
    if current_user.confirmado:
        return redirect(url_for('principal.home'))

        token = usuario.gerar_token_confirmacao()
        enviar_email(current_user.email, 'Confirme Seu Cadastro',
                     'autenticacao/email/confirmacao', usuario=current_user, token=token)
        flash('Um novo email de confirmação foi enviado. Confira a sua caixa de entrada.', 'info')

    return redirect(url_for('principal.home'))


# Alteração de Senha
@autenticacao.route('/alterar-senha', methods=['GET', 'POST'])
@login_required
def alterar_senha():
    form = FormAlterarSenha()

    if form.validate_on_submit():
        if current_user.verificar_senha(form.senha_atual.data):
            current_user.senha = form.senha_nova.data
            db.session.add(current_user)
            flash('Sua senha foi alterada.', 'success')

            return redirect(url_for('principal.home'))
        else:
            flash('Senha incorreta.', 'danger')

    return render_template('autenticacao/alterar_senha.html', form=form)


# Pedido de Recuperação de Senha
@autenticacao.route('/recuperar-senha', methods=['GET', 'POST'])
def pedido_recuperacao_senha():
    if not current_user.is_anonymous:
        return redirect(url_for('principal.home'))

    form = FormPedidoRecuperarSenha()

    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()

        if usuario:
            token = usuario.gerar_token_recuperacao_senha()
            enviar_email(usuario.email, 'Recuperação de Senha',
                         'autenticacao/email/recuperacao_senha',
                         usuario=usuario, token=token)
            flash('Um email com instruções para recuperar sua senha foi enviado.', 'info')

            return redirect(url_for('autenticacao.login'))

    return render_template('autenticacao/recuperar_senha.html', form=form)


# Confirmação de Recuperação de Senha
@autenticacao.route('/recuperar-senha/<token>', methods=['GET', 'POST'])
def recuperar_senha(token):
    if not current_user.is_anonymous:
        return redirect(url_for('principal.home'))

    form = FormRecuperarSenha()

    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()

        if usuario is None:
            return redirect(url_for('principal.home'))

        if usuario.recuperar_senha(token, form.senha_nova.data):
            flash('Sua senha foi atualizada.', 'success')
            return redirect(url_for('autenticacao.login'))
        else:
            return redirect(url_for('principal.home'))

    return render_template('autenticacao/recuperar_senha.html', form=form)


# Pedido de Alteração de Email
@autenticacao.route('/alterar-email', methods=['GET', 'POST'])
@login_required
def pedido_alteracao_email():
    form = FormAlterarEmail()

    if form.validate_on_submit():
        if current_user.verificar_senha(form.senha.data):
            email_novo = form.email_novo.data
            token = current_user.gerar_token_alteracao_email(email_novo)
            enviar_email(email_novo, 'Confirme Alteração de Email',
                         'autenticacao/email/alteracao_email',
                         usuario=current_user, token=token)
            flash('Um email com instruções para confirmar seu novo email foi enviado.', 'info')

            return redirect(url_for('principal.home'))
        else:
            flash('Senha incorreta.', 'danger')

    return render_template('autenticacao/alterar_email.html', form=form)


# Confirmação de Alteração de Email
@autenticacao.route('/alterar-email/<token>')
@login_required
def alterar_email(token):
    if current_user.alterar_email(token):
        flash('Seu email foi atualizado.', 'success')
    else:
        flash('Solicitação inválida.', 'danger')

    return redirect(url_for('principal.home'))

    