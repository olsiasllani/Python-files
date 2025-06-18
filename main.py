import sqlite3

# Lidhja me databazën
conn = sqlite3.connect('student.db')
cursor = conn.cursor()

# Krijimi i tabelës nëse nuk ekziston
cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    email TEXT UNIQUE
)
''')

# Funksioni për të shtuar një student
def add_student(name, age, email):
    try:
        cursor.execute('INSERT INTO students (name, age, email) VALUES (?, ?, ?)', (name, age, email)) 
        conn.commit()
        print("Studenti u shtua me sukses.")
    except sqlite3.IntegrityError:
        print("Emaili ekziston tashmë në databazë.")

# Funksioni për të shfaqur studentët
def show_students():
    cursor.execute('SELECT * FROM students') 
    students = cursor.fetchall()
    print("\nLista e Studentëve:")
    for student in students:
        print(f"ID: {student[0]}, Emri: {student[1]}, Mosha: {student[2]}, Emaili: {student[3]}")

# Menuja interaktive
while True:
    print("\n1. Shto student")
    print("2. Shfaq studentët")
    print("3. Dil")
    choice = input("Zgjidh një opsion: ")

    if choice == '1':
        name = input("Emri: ")
        age = int(input("Mosha: "))
        email = input("Email: ")
        add_student(name, age, email)
    elif choice == '2':
        show_students()
    elif choice == '3':
        print("Duke dalë...")
        break
    else:
        print("Zgjedhje e pavlefshme. Provo përsëri.")

# Mbyllja e lidhjes me databazën
conn.close()
