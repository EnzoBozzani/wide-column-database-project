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
    
    teaches: ResultSet = session.execute("SELECT * FROM teaches WHERE professor_id = 'P005' ALLOW FILTERING;")

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


def query_graduated_students(session):
    print("Buscando os alunos que se formaram no segundo semestre de 2018")

    graduates: ResultSet = session.execute("SELECT * FROM graduate WHERE semester = 2 AND year = 2018 ALLOW FILTERING")

    records = []

    for g in graduates:
        student: ResultSet = session.execute(f"SELECT * FROM student WHERE id = '{g.student_id}';")
        course: ResultSet = session.execute(f"SELECT * FROM course WHERE id = '{g.course_id}';")

        records.append({ 
            "student_id": g.student_id,
            "student_name": student[0].name,
            "course_name": course[0].title
        })

    with open('./output/query-3.json', 'w') as f:
        json.dump({ "year": 2018, "semester": 2, "students": records }, f, ensure_ascii=False)


def query_chiefs_of_departments(session):
    print("Buscando os professores que são chefes de departamento")
    
    department: ResultSet = session.execute("SELECT * FROM department;")

    records = []

    for d in department:
        boss: ResultSet = session.execute(f"SELECT * FROM professor WHERE id = '{d.boss_id}';")

        records.append({
            "name": boss[0].name,
            "department": d.dept_name
        })

    with open('./output/query-4.json', 'w') as f:
        json.dump(records, f, ensure_ascii=False)


def query_tcc_group(session):
    print("Buscando os alunos que formaram o grupo de TCC de ID CC1111111")
    
    tcc_group = session.execute("SELECT * FROM tcc_group WHERE id = 'CC1111111';")
    students = session.execute("SELECT * FROM student WHERE group_id = 'CC1111111' ALLOW FILTERING;")
    prof = session.execute(f"SELECT * FROM professor WHERE id = '{tcc_group[0].professor_id}'")

    records = []

    for s in students:
        records.append({
            "name": s.name,
            "id": s.id
        })

    with open('./output/query-5.json', 'w') as f:
        json.dump({ "prof": prof[0].name, "id": "CC1111111", "students": records }, f, ensure_ascii=False)
