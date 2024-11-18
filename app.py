# Standard
from typing import Any
import os
import json
from decimal import Decimal

# Third Party
import psycopg2
from dotenv import load_dotenv
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

# Local
from constants import create_tables
from queries import query_student_academic_record, query_professor_academic_record, query_graduated_students, query_chiefs_of_departments, query_tcc_group

load_dotenv()

postgres_conn = psycopg2.connect(os.environ['POSTGRES_URL'])
astra_session = Cluster(
    cloud={"secure_connect_bundle": os.environ["ASTRADB_SECURE_BUNDLE_PATH"]},
    auth_provider=PlainTextAuthProvider(os.environ["ASTRADB_CLIENT_ID"], os.environ["ASTRADB_CLIENT_SECRET"]),
).connect()


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


def insert_into_astra(table_name: str, columns: list[str], rows: list[Any]) -> None:
    print(f"Inserindo dados na tabela '{table_name}' no Astra DB...")
    
    for row in rows:
        formatted = [str(value) if isinstance(value, Decimal) or isinstance(value, int) else f"'{value}'" for value in row]
        astra_session.execute(f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(formatted)});")


def drop_tables_from_astra():
    tables = astra_session.execute(f"SELECT table_name FROM system_schema.tables WHERE keyspace_name = '{os.environ['ASTRADB_KEYSPACE']}';")

    print("\nDeletando todas as tabelas existentes do AstraDB...")

    for table in tables:
        astra_session.execute(f"DROP TABLE {table.table_name}")
        

def transfer_data():
    tables = show_tables()

    print("\n-----------------------------------------------------------------------------\n")

    for table in tables:
        cols = select_columns(table)
        rows = select_all(table)

        print(f"Criando a tabela {table} no Astra DB")
        astra_session.execute(create_tables[table])

        insert_into_astra(table, cols, rows)

        print(f"Dados da tabela {table} inseridos no Astra DB.")
    
        print("\n-----------------------------------------------------------------------------\n")

    print("Transferência concluída!")

if __name__ == '__main__':
    astra_session.set_keyspace(os.environ["ASTRADB_KEYSPACE"])

    drop_tables_from_astra()

    transfer_data()

    if not os.path.exists('./output'):
        os.mkdir('./output')

    query_student_academic_record(astra_session)

    query_professor_academic_record(astra_session)

    query_graduated_students(astra_session)
    
    query_chiefs_of_departments(astra_session)

    query_tcc_group(astra_session)

    print("\n-----------------------------------------------------------------------------\n")
    print("Outputs das queries disponíveis na pasta ./output!")
    print("\n-----------------------------------------------------------------------------\n")
