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

import datetime

app = Flask(__name__)
app.secret_key = 'aplicacao_forms'
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'mysql+mysqlconnector://{usuario}:{senha}@{servidor}:{porta}/{database}'
    .format(
        usuario='root',
        senha='cbeb6c44B13gbg2AEEdfABdhbg4-F3bb',
        servidor='viaduct.proxy.rlwy.net',
        porta='46689',
        database='forms_admin'
    )
)

db = SQLAlchemy(app)

class Usuarios(db.Model):
    nome = db.Column(db.String(255), nullable=True)
    nickname = db.Column(db.String(20), primary_key=True, nullable=False)  # Corrigido: nullable=False
    senha = db.Column(db.String(100), nullable=False)  # Corrigido: nullable=False

    def __repr__(self):
        return '<Name %r>' % self.nickname  # Corrigido: self.nickname

class Alunos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(255), nullable=True)
    data_cadastro = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return '<Name %r>' % self.nome  # Corrigido: self.nome

@app.route('/')
def index():
    alunos = Alunos.query.order_by(Alunos.id).all()  # Corrigido: Adicione .all() para obter todos os registros
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login', proxima=url_for('index')))

    return render_template('lista.html', titulo='Alunos cadastrados', alunos=alunos)

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST'])
def autenticar_usuario():
    usuario = Usuarios.query.filter_by(nickname=request.form['usuario']).first()
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

    novo_usuario = Alunos(nome=nome, email=email, data_cadastro=data_cadastro)
    db.session.add(novo_usuario)
    db.session.commit()

    return redirect(url_for('link_grupo'))

if(__name__ == '__main__'):
    app.run()