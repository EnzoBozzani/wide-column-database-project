create_tables = {
    "course": """
        CREATE TABLE course (
            id TEXT,
            title TEXT,
            PRIMARY KEY (id)
        );
    """,
    "professor": """
        CREATE TABLE professor (
            id TEXT,
            name TEXT,
            dept_name TEXT, 
            salary DECIMAL,
            PRIMARY KEY (id)
        );
    """,
    "tcc_group": """
        CREATE TABLE tcc_group (
            id TEXT,
            professor_id TEXT,
            PRIMARY KEY (id)
        );
    """,
    "department": """
        CREATE TABLE department (
            dept_name TEXT,
            budget DECIMAL,
            boss_id TEXT,
            PRIMARY KEY (dept_name)
        );
    """,
    "student": """
        CREATE TABLE student (
            id TEXT, 
            name TEXT,
            course_id TEXT,
            group_id TEXT,
            PRIMARY KEY (id)
        );
    """,
    "subj": """
        CREATE TABLE subj (
            id TEXT,
            title TEXT, 
            dept_name TEXT,
            PRIMARY KEY (id)
        );
    """,
    "takes": """
        CREATE TABLE takes (
            student_id TEXT, 
            subj_id TEXT,
            semester INT,
            year INT,
            grade DECIMAL,
            subjroom TEXT,
            PRIMARY KEY (student_id, subj_id, semester, year)
        );
    """,
    "teaches": """
        CREATE TABLE teaches (
            subj_id TEXT,
            professor_id TEXT,
            semester INT,
            year INT,
            PRIMARY KEY (subj_id, professor_id, semester, year)
        );
    """,
    "req": """
        CREATE TABLE req (
            course_id TEXT,
            subj_id TEXT,
            PRIMARY KEY (course_id, subj_id)
        );
    """,
    "graduate": """
        CREATE TABLE graduate (
            course_id TEXT, 
            student_id TEXT,
            semester INT,
            year INT,
            PRIMARY KEY (course_id, student_id)
        );
    """
}
