from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    flash,
    url_for
)

from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

import datetime

app = Flask(__name__)

load_dotenv()

app.secret_key = 'aplicacao_forms'
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'mysql+mysqlconnector://{usuario}:{senha}@{servidor}:{porta}/{database}'
    .format(
        usuario=os.getenv('DB_USERNAME'),
        senha=os.getenv('DB_PASSWORD'),
        servidor=os.getenv('DB_HOST'),
        porta=os.getenv('DB_PORT'),
        database=os.getenv('DB_NAME')
    )
)

db = SQLAlchemy(app)

class FormsAdminUsuarios(db.Model):
    nome = db.Column(db.String(255), nullable=True)
    nickname = db.Column(db.String(20), primary_key=True, nullable=False)  # Corrigido: nullable=False
    senha = db.Column(db.String(100), nullable=False)  # Corrigido: nullable=False

    def __repr__(self):
        return '<Name %r>' % self.nickname  # Corrigido: self.nickname

class FormsAdminAlunos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(255), nullable=True)
    data_cadastro = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return '<Name %r>' % self.nome  # Corrigido: self.nome

@app.route('/')
def index():
    alunos = FormsAdminAlunos.query.order_by(FormsAdminAlunos.id).all()  # Corrigido: Adicione .all() para obter todos os registros
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login', proxima=url_for('index')))

    return render_template('lista.html', titulo='Alunos cadastrados', alunos=alunos)

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST'])
def autenticar_usuario():
    usuario = FormsAdminUsuarios.query.filter_by(nickname=request.form['usuario']).first()
    if usuario:
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nome + ' logado com sucesso!')
            proxima_pagina = request.form['proxima']
            if proxima_pagina != 'None':
                return redirect(proxima_pagina)

            return redirect(url_for('index'))
        else:
            flash('Usuário ou senha incorretos!')
            return redirect(url_for('login'))

    else:
        flash('Usuário ou senha incorretos!')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout feito com sucesso!')
    return redirect(url_for('login'))

@app.route('/link-to')
def link_grupo():
    return render_template('link_to.html', titulo='Solicite acesso ao grupo de whatsapp')

@app.route('/novo')
def novo_aluno():
    return render_template('novo_aluno.html', titulo='Cadastre suas informações')

@app.route('/criar', methods=['POST',])
def criar_novo_aluno():
    nome = request.form['nome']
    email = request.form['email']
    data_cadastro = datetime.datetime.now()

    verifica_aluno = FormsAdminAlunos.query.filter_by(email=email).first()

    if(not verifica_aluno):
        novo_usuario = FormsAdminAlunos(nome=nome, email=email, data_cadastro=data_cadastro)
        db.session.add(novo_usuario)
        db.session.commit()
    else:
        flash('Email {email} já cadastrado!'.format(email=email))
        return redirect(url_for('novo_aluno'))

    return redirect('https://chat.whatsapp.com/IFvJCSOdSuCHV94ERCvG41')

@app.route('/excluir/<int:aluno_id>')
def excluir_aluno(aluno_id):
    aluno_para_excluir = FormsAdminAlunos.query.get(aluno_id)
    db.session.delete(aluno_para_excluir)
    db.session.commit()

    return redirect(url_for('index'))

if(__name__ == '__main__'):
    app.run()