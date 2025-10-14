"""
Enkel to-do app med Flask + MariaDB. Les readme.md før du begynner.
"""

from flask import Flask, render_template, request, redirect
import mysql.connector
from mysql.connector import Error
app = Flask(__name__)

def get_connection():
    return mysql.connector.connect(
        # Bytt ut informasjonen her med dine egne verdier:
        host='127.0.0.1', # IP-adressen til databasen (127.0.0.1 = localhost = maskinen som kjører koden)
        user='todo_user',       
        password='strongpassword',
        database='todo',
    )

def create_table():
    try:
        conn = get_connection()
        if conn.is_connected():
            cursor = conn.cursor()  # hva er en 'cursor'?
            # hva gjør denne koden? ⬇
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    task VARCHAR(255) NOT NULL
                )
            ''')

            conn.commit()
            cursor.close()
            conn.close()
    except Error as e:
        print(f"Feil under opprettelse av tabell: {e}")

create_table() 

@app.route('/')  # når kjører denne routen?
def index():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks')  
        tasks = cursor.fetchall()              
        conn.close()
        return render_template('index.html', tasks=tasks) # hva gjør denne linjen? Hva er tasks?
    except Error as e:
        return "Kunne ikke koble til databasen."

@app.route('/add', methods=['POST'])  # når kjører denne routen?
def add_task():
    task = request.form['task']  # hva er request.form['task']?

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tasks (task) VALUES (%s)', (task,))
        conn.commit()
    except Error as e:
        print(f"Feil under lagring av oppgave: {e}")
    finally:
        conn.close()

    return redirect('/') # hva skjer hvis du fjerner denne linjen?

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)