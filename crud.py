# coding=utf-8
from faker import Faker
import psycopg2


class AppBD:
    def __init__(self):

        print('Método Construtor')

    def abrirConexao(self):
        try:
            self.connection = psycopg2.connect(user="postgres", password="Estacio@123",
                                               host="127.0.0.1", port="5432", database="postgres")
        except (Exception, psycopg2.Error) as error:
            if (self.connection):
                print("Falha ao se conectar ao Banco de Dados", error)

    # inserir dados
    def inserirDados(self, codigo, nome, preco):
        try:
            self.abrirConexao()
            cur = self.connection.cursor()
            postgres_insert_query = """ INSERT INTO public. "PRODUTO"
            ("CODIGO", "NOME", "PRECO") VALUES (%s, %s, %s) """
            record_to_insert = (codigo, nome, preco)
            cur.execute(postgres_insert_query, record_to_insert)
            self.connection.commit()
            count = cur.rowcount
            print(count, "Registro inserido na Tabela ")
        except (Exception, psycopg2.Error) as error:
            if (self.connection) :
                print("Falha ao inserir na Tabela", error)
        finally:
            # closing database connection.
            if (self.connection) :
                cur.close()
                self.connection.close()
                print("A conexão com o PostgreSQL foi encerrada!!")

    # atualizar dados
    def atualizarDados(self, codigo, nome, preco):
        try:
            self.abrirConexao()
            cur = self.connection.cursor()
            sql_update_query = """ Update puclic."PRODUTO" set "NOME" = %s,
             "PRECO" = %s where "CODIGO" = %s """
            cur.execute(sql_update_query, (nome, preco, codigo))
            self.connection.commit()
            cont = cur.rowcount
            print(cont, "Registro atualizado!! ")
            print("Registro depois da atualização ")
            sql_select_query = """Select *from public. "PRODUTO"
             where "CODIGO" = %s """
            cur.execute(sql_select_query, codigo)
            record = cur.fetchone()
            print(record)
        except (Exception, psycopg2.Error) as error:
            print("Erro na atualização", error)
        finally:
            # clossing database connection.
            if (self.connection) :
                cur.close()
                self.connection.close()
                print("A conexão com o PostgreSQL foi encerrada.")

    # excluir dados
    def excluirDados(self, codigo):
        try:
            self.abrirConexao()
            cursor = self.connection.cursor()
            sql_delete_query = """ Delete from public. "PRODUTO"
            where "CODIGO" = %s """
            cursor.execute(sql_delete_query, codigo)
            self.connection.commit()
            cont = cur.rowcount
            print(cont, "Registro excluido!!")
        except(Exception, psycopg2.Error) as error:
            print("Erro na exclusão", error)
        finally:
            # clossing database connection.
            if (self.connection):
                cur.close()
                self.connection.close()
                print("A conexão com o PostgreSQL foi encerrada.")

# criando e conectando com o BD
conn = psycopg2.connect(database="postgres", user="postgres", password="Estacio@123", port="5432")
print("Conexão com o Banco de Dados aberta!!")

cur = conn.cursor()
cur.execute(""" CREATE TABLE PRODUTO
                (CODIGO INT PRIMARY KEY NOT NULL,
                NOME TEXT NOT NULL,
                PRECO REAL NOT NULL);               
                    """)
print("Tabela criada no BD!!")
conn.commit()
conn.close()

# inserindo dados na tabela
conn = psycopg2.connect(database="postgres", user="postgres", password="Estacio@123", port="5432")
print("Conexão com o Banco de Dados aberta!!")

cur = conn.cursor()
fake = Faker('pt_BR')

n=10
for i in range(n):
    codigo = i+10
    nome = 'produto_'+str(i+1)
    preco = fake.pyfloat(left_digits=3, right_digits=2, positive=True, min_value=5, max_value=1000)
    print(codigo)
    print(nome)
    print(preco)
comandoSQL = """INSERT INTO public. PRODUTO (CODIGO, NOME, PRECO)
                VALUES (%s, %s, %s)
                """
registro = codigo, nome, preco
cur.execute(comandoSQL, registro)
conn.commit()
print("Inserção realizada!!!")
conn.close()

# selecionando dados na tabela
conn = psycopg2.connect(database="postgres", user="postgres", password="Estacio@123", port="5432")

cur = conn.cursor()
cur.execute(""" SELECT * FROM PRODUTO where codigo = 2 """)
registro = cur.fetchone()
print("Dados encontrados ->")
conn.commit()
print("Seleção realizada!!!")

# atualizando dados na tabela
conn = psycopg2.connect(database="postgres", user="postgres", password="Estacio@123", port="5432")

cur = conn.cursor()
cur.execute(""" SELECT *FROM PRODUTO where codigo = 1 """)
registro = cur.fetchone()
print(registro)
cur.execute(""" UPDATE PRODUTO set PRECO = 96385471 where codigo = 1""")
conn.commit()
print("Registro Atualizado!!! ")
cur = conn.cursor()
print("--- Consulta após a atualização ---")
cur.execute(""" SELECT *FROM PRODUTO where codigo = 1 """)
registro = cur.fetchone()
print("Dados atualizados ->", registro)
conn.commit()
conn.close()

# excluindo dados na tabela
conn = psycopg2.connect(database="postgres", user="postgres", password="Estacio@123", port="5432")

cur = conn.cursor()
cur.execute(""" DELETE FROM PRODUTO where codigo = 1 """)
conn.commit()
count = cur.rowcount

print(count, "-> Registro excluido!")
print("Exclusão realizada!!!")
conn.close()


