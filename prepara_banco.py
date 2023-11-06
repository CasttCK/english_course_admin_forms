import mysql.connector
from mysql.connector import errorcode

print("Conectando...")
try:
      conn = mysql.connector.connect(
        host='viaduct.proxy.rlwy.net',
        user='root',
        password='cbeb6c44B13gbg2AEEdfABdhbg4-F3bb',
        database='railway',
        port='46689'
    )
except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Existe algo errado no nome de usuário ou senha')
      else:
            print(err)

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS `forms_admin`;")

cursor.execute("CREATE DATABASE `forms_admin`;")

cursor.execute("USE `forms_admin`;")

# criando tabelas
TABLES = {}
TABLES['Alunos'] = ('''
      CREATE TABLE `alunos` (
      `id` int NOT NULL AUTO_INCREMENT,
      `nome` varchar(255) NOT NULL,
      `email` varchar(255) NOT NULL,
      `data_cadastro` datetime NOT NULL,
      PRIMARY KEY (`id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['Usuarios'] = ('''
      CREATE TABLE `usuarios` (
      `nome` varchar(255) NOT NULL,
      `nickname` varchar(20) NOT NULL,
      `senha` varchar(100) NOT NULL,
      PRIMARY KEY (`nickname`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

for tabela_nome in TABLES:
      tabela_sql = TABLES[tabela_nome]
      try:
            print('Criando tabela {}:'.format(tabela_nome), end=' ')
            cursor.execute(tabela_sql)
      except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                  print('Já existe')
            else:
                  print(err.msg)
      else:
            print('OK')

# inserindo usuarios
usuario_sql = 'INSERT INTO usuarios (nome, nickname, senha) VALUES (%s, %s, %s)'
usuarios = [
      ("Vinicius Kronemberger", "CasttCK", "AdminTI"),
      ("Matheus Farchi", "MattFarchi", "matias1914")
]
cursor.executemany(usuario_sql, usuarios)

cursor.execute('select * from forms_admin.usuarios')
print(' -------------  Usuários:  -------------')
for user in cursor.fetchall():
    print(user[1])

# inserindo jogos
alunos_sql = 'INSERT INTO alunos (nome, email, data_cadastro) VALUES (%s, %s, %s)'
alunos = [
      ('Vinicius Teste', 'teste@ti.com', '2023-11-06 23:21:21.240752'),
]
cursor.executemany(alunos_sql, alunos)

cursor.execute('select * from forms_admin.alunos')
print(' -------------  Alunos:  -------------')
for aluno in cursor.fetchall():
    print(aluno[1])

# commitando se não nada tem efeito
conn.commit()

cursor.close()
conn.close()