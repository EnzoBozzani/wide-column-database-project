# Standard
import json
from cassandra.cluster import Session, ResultSet


def query_student_academic_record(session: Session):
    print("Buscando o histórico escolar do aluno de RA 100000001")
    
    takes: ResultSet = session.execute("SELECT * FROM takes WHERE student_id = '100000001';")

    records = []

    for t in takes:
        s: ResultSet = session.execute(f"SELECT * FROM subj WHERE id = '{t.subj_id}'")
        records.append({ 
            "subj_id": t.subj_id,
            "semester": t.semester,
            "year": t.year,
            "grade": float(t.grade),
            "title": s[0].title 
        })

    with open('./output/query-1.json', 'w') as f:
        json.dump({ "student_id": "100000001", "academic_record": records }, f, ensure_ascii=False)

def query_professor_academic_record(session: Session):
    print("Buscando o histórico de disciplinas ministradas pelo professor de ID P005")
    
    teaches: ResultSet = session.execute("ALLOW FILTERING SELECT * FROM teaches WHERE professor_id = 'P005';")

    records = []

    for t in teaches:
        records.append({ 
            "subj_id": t.subj_id,
            "semester": t.semester,
            "year": t.year,
        })

    prof = session.execute("SELECT * FROM professor WHERE id = 'P005';")

    with open('./output/query-2.json', 'w') as f:
        json.dump({ "professor_id": "P005", "professor_name": prof[0].name, "academic_record": records }, f, ensure_ascii=False)


# def query_graduated_students(session):
#     print("Buscando os alunos que se formaram no segundo semestre de 2018")
#     query = """
#     MATCH (s:Student)-[:GRADUATED {semester: 2, year: 2018}]->(c:Course)
#     RETURN s.id AS student_id, s.name AS name
#     """

#     with neo4j_driver.session() as session:
#         result = session.run(query)
#         records = [record.data() for record in result]

#     with open('./output/query-3.json', 'w') as f:
#         json.dump(records, f, ensure_ascii=False)

# def query_chiefs_of_departments(session):
#     print("Buscando os professores que são chefes de departamento")
#     query = """
#     MATCH (p:Professor)-[:HEADS]->(d:Department)
#     RETURN p.id AS professor_id, p.name AS professor_name, d.dept_name AS department_name, d.budget AS department_budget
#     """

#     with neo4j_driver.session() as session:
#         result = session.run(query)
#         records = [record.data() for record in result]

#     with open('./output/query-4.json', 'w') as f:
#         json.dump(records, f, ensure_ascii=False)

# def query_tcc_group(session):
#     print("Buscando os alunos que formaram o grupo de TCC de ID CC1111111")
#     query = """
#     MATCH (s:Student {group_id: 'CC1111111'})-[:MENTORED_BY]->(p:Professor)
#     RETURN s.id AS student_id, s.name AS student_name, p.name AS professor_name
#     """

#     with neo4j_driver.session() as session:
#         result = session.run(query)
#         records = [record.data() for record in result]

#     with open('./output/query-5.json', 'w') as f:
#         json.dump(records, f, ensure_ascii=False)
