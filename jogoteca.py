from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    flash,
    url_for
)
import datetime

class Usuario:
    def __init__(self, nome, nickname, senha):
        self.nome = nome
        self.nickname = nickname
        self.senha = senha

usuario1 = Usuario('Matheus Farchi', 'MattFarchi', 'matias1914')
usuario2 = Usuario('Vinicius Kronemberger', 'CasttCK', 'Castt')
usuarios = { usuario1.nickname : usuario1,
             usuario2.nickname : usuario2 }

class Aluno:
    def __init__(self, nome, email, data_cadastro):
        self.nome = nome
        self.email = email
        self.data_cadastro = data_cadastro

aluno1 = Aluno('Vinicius', 'vini.kronemberger@gmail.com', '2023-10-01 12:37:01.107003')
aluno2 = Aluno('TesteTI', 'teste@teste.com.br', '2023-10-13 08:53:01.107003')

alunos = [aluno1, aluno2]

app = Flask(__name__)
app.secret_key = 'aplicacao_forms'

@app.route('/')
def index():
    if ('usuario_logado' not in session or session['usuario_logado'] == None):
        return redirect(url_for('login', proxima=url_for('index')))

    return render_template('lista.html', titulo='Alunos cadastrados', alunos=alunos)

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST'])
def autenticar_usuario():
    if(request.form['usuario'] in usuarios):
        usuario = usuarios[request.form['usuario']]
        if(request.form['senha'] == usuario.senha):
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

@app.route('/novo')
def novo_aluno():
    return render_template('novo_aluno.html', titulo='Cadastre suas informações')

@app.route('/criar', methods=['POST',])
def criar_novo_aluno():
    nome = request.form['nome']
    email = request.form['email']
    data_cadastro = datetime.datetime.now()

    novo_aluno = Aluno(nome, email, data_cadastro)
    alunos.append(novo_aluno)

    return redirect(url_for('index'))

app.run(debug=True)