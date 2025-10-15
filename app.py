"""
Enkel to-do app med Flask + MariaDB. Les readme.md før du begynner.
"""

from flask import Flask, render_template, request, redirect
import mysql.connector
from mysql.connector import Error
import getpass
app = Flask(__name__)



def get_connection():
    connection = mysql.connector.connect(
        # Bytt ut informasjonen her med dine egne verdier:
        host = 'localhost', # IP-adressen til databasen (127.0.0.1 = localhost = maskinen som kjører koden)
        user= 'mysqlroot',       
        password = 'root1234',
        database= 'readme',
    )
    
    cursor = connection.cursor()
    
    # 1. Create a new user with mysql_native_password authentication
    create_user_query = """
    CREATE USER IF NOT EXISTS 'mysqlroot'@'localhost' IDENTIFIED WITH mysql_native_password BY 'root1234';
    """

    # 2. Give that user privileges on your database
    grant_privileges_query = """
    GRANT ALL PRIVILEGES ON your_database.* TO 'mysqlroot'@'localhost';
    """

    # 3. Apply changes
    flush_privileges_query = "FLUSH PRIVILEGES;"

    try:
        cursor.execute(create_user_query)
        cursor.execute(grant_privileges_query)
        cursor.execute(flush_privileges_query)
        print("User created and privileges granted successfully.")
    except mysql.connector.Error as err:
        print(f"Could not create user")




    return connection

def create_table():
    try:
        conn = get_connection()
        if conn.is_connected():
            cursor = conn.cursor()  # hva er en 'cursor'? den er det som kobbler mellom python koden og databasen .
            # hva gjør denne koden? ⬇  den lager en syntex inni mysql fra python koden
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    task VARCHAR(255) NOT NULL
                )
            ''')

            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print("Tables:", tables)
            conn.commit()
            cursor.close()
            conn.close()
    except Error as e:
        print(f"Feil under opprettelse av tabell: {e}")

create_table() 

@app.route('/')  # når kjører denne routen? Når root folder åpnes i browser.
def index():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks')  
        tasks = cursor.fetchall()              
        conn.close()
        return render_template('index.html', tasks=tasks) # hva gjør denne linjen? Hva er tasks? Åpner index.html fra templates.
    except Error as e:
        return "Kunne ikke koble til databasen."

@app.route('/add', methods=['POST'])  # når kjører denne routen? Når /add åpnes i browser.
def add_task():
    task = request.form['task']  # hva er request.form['task']? Den spør etter verdien til task fra databasen.

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tasks (task) VALUES (%s)', (task,))
        conn.commit()
    except Error as e:
        print(f"Feil under lagring av oppgave: {e}")
    finally:
        conn.close()

    return redirect('/') # hva skjer hvis du fjerner denne linjen?   den redricter deg til den forstå siden og vis du fjerner den så kan du ikke blir redirecte til forsiden.

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)