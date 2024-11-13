# Standard
from typing import Any
import os
import json
from decimal import Decimal

# Third Party
import psycopg2
from dotenv import load_dotenv
from astrapy import DataAPIClient

# Local
# from queries import query_chiefs_of_departments, query_graduated_students, query_professor_academic_record, query_student_academic_record, query_tcc_group

load_dotenv()

postgres_conn = psycopg2.connect(os.environ['POSTGRES_URL'])
client = DataAPIClient(token=os.environ['ASTRADB_TOKEN'])
astra_db = client.get_database_by_api_endpoint(os.environ['ASTRADB_URL'])

def show_tables() -> list[str]:
    print("Buscando nomes das tabelas no banco relacional...")
    with postgres_conn.cursor() as db:
        db.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
        res = db.fetchall()
        postgres_conn.commit()
        return [table[0] for table in res]

def select_all(table_name: str) -> list[Any]:
    print(f"Selecionando registros da tabela '{table_name}'...")
    with postgres_conn.cursor() as db:
        db.execute(f"SELECT * FROM {table_name};")
        res = db.fetchall()
        postgres_conn.commit()
        return res

def select_columns(table_name: str) -> list[str]:
    print(f"Selecionando os nomes das colunas da tabela '{table_name}'...")
    with postgres_conn.cursor() as db:
        db.execute(f"SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='{table_name}';")
        res = db.fetchall()
        postgres_conn.commit()
        return [column[0] for column in res]

def transfer_data():
    tables = show_tables()

    keyspace = astra_db.keyspace

    print("\n-----------------------------------------------------------------------------\n")

    for table in tables:
        cols = select_columns(table)
        rows = select_all(table)

        astra_db.command()

        # Inserindo os registros no Astra DB
        for row in rows:
            record = {}
            for col, value in zip(cols, row):
                if isinstance(value, Decimal):
                    record[col] = float(value)
                else:
                    record[col] = value
            
            # inserir

        print(f"Tabela '{table}' criada e dados transferidos para o Astra DB.")

    print("Transferência concluída!")

if __name__ == '__main__':
    transfer_data()

    print("Outputs estarão na pasta ./output")
    print("\n-----------------------------------------------------------------------------\n")

    if not os.path.exists('./output'):
        os.mkdir('./output')

    # query_student_academic_record()
    # query_professor_academic_record()
    # query_graduated_students()
    # query_chiefs_of_departments()
    # query_tcc_group()

    print("\n-----------------------------------------------------------------------------\n")
    print("Outputs das queries disponíveis na pasta output!")
    print("\n-----------------------------------------------------------------------------\n")
