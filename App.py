from flask import Flask, render_template, request, flash, redirect, url_for, session
from main import test
import os
import sqlite3

app = Flask(__name__)
app.secret_key = 'mySecretKey'

@app.route('/')
def index():
    if len(os.listdir('databases')) != 0:
        if 'db_in_use' in session:
            if os.path.exists(f'databases/{session["db_in_use"]}'):
                conn = sqlite3.connect(f'databases/{session["db_in_use"]}')
                cursor = conn.cursor()
                rows = cursor.execute(r"SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%'")
                tables = rows.fetchall()
                
                database_content = {}
                for table in tables:
                    rows_columns = cursor.execute(f'PRAGMA table_info({table[0]})')
                    if table[0] not in database_content:
                        database_content[table[0]] = rows_columns.fetchall()
                if 'select_result' in session:
                    print(session['select_result'])
                    return render_template('index.html', available_databases = os.listdir('databases'), available_tables = database_content, db_in_use = session["db_in_use"], selected_items = session['select_result'])    
                return render_template('index.html', available_databases = os.listdir('databases'), available_tables = database_content, db_in_use = session["db_in_use"])
            return render_template('index.html', available_databases = os.listdir('databases'))
        return render_template('index.html', available_databases = os.listdir('databases'))
    return render_template('index.html')

@app.route('/execute_command', methods=['POST'])
def execute_command():
    if request.method == 'POST':
        command = request.form['command']
        result = test(command, True)
        if result != None:
            if request.form['is_sql_command'] == 'run':
                op, flash_message = run_command(result, True)
                flash(flash_message)
                return redirect(url_for('index'))
            if request.form['is_sql_command'] == 'evaluate':
                op, flash_message = run_command(result, False)
                flash(flash_message)
                return redirect(url_for('index'))
        return "Sin respuesta"

def run_command(result, allow):
    if not allow:
        return 0, f'Se restringió la operación {result[0]}. Intentaron ejecutar: {result[1]}'
    if result[0] == "create database":
        if os.path.exists('databases/'+ result[1][15:].strip() + '.db'):
            return 1, f"Ya existe la Base de Datos {result[1][15:].strip()}"
        sqlite3.connect('databases/'+ result[1][15:].strip() + '.db')
        return 1, f"Base de datos {result[1][15:]} creada con éxito"
    
    elif result[0] == "create table":
        if 'db_in_use' in session:
            if os.path.exists(f'databases/{session["db_in_use"]}'):
                conn = sqlite3.connect(f'databases/{session["db_in_use"]}')
                cursor = conn.cursor()
                cursor.execute(result[1])
                return 2, "Tabla " + result[1].split(' ')[2] + " creada"
            return 2, "No existe la Base de Datos"
        return 2, "Utiliza una base de datos"
    
    elif result[0] == "use":
        if 'db_in_use' in session:
            session.pop(session['db_in_use'], None)
        session['db_in_use'] = result[1][4:] + '.db'
        return 3, "Usando " + result[1][4:]
   
    elif result[0] == "insert":
        if 'db_in_use' in session:
            if os.path.exists(f'databases/{session["db_in_use"]}'):
                conn = sqlite3.connect(f'databases/{session["db_in_use"]}')
                cursor = conn.cursor()
                cursor.execute(result[1])
                conn.commit()
                return 4, "Registros insertados en " + result[1].split(' ')[2]
            return 4, "No existe la Base de Datos"
        return 4, "Selecciona una Base de Datos"
    
    elif result[0] == "select":
        if 'db_in_use' in session:
            if os.path.exists(f'databases/{session["db_in_use"]}'):
                conn = sqlite3.connect(f'databases/{session["db_in_use"]}')
                cursor = conn.cursor()
                rows = cursor.execute(result[1])
                result = rows.fetchall()
                print(len(result))
                if len(result) != 0:
                    session['select_result'] = result
                    print(session['select_result'])
                    return 5, "Registros: "
                return 5, "No hay registros"
            return 5, "No existe la Base de Datos"
        return 5, "Selecciona una Base de Datos"
    
    elif result[0] == "delete":
        if 'db_in_use' in session:
            if os.path.exists(f'databases/{session["db_in_use"]}'):
                conn = sqlite3.connect(f'databases/{session["db_in_use"]}')
                cursor = conn.cursor()
                cursor.execute(result[1])
                conn.commit()
                return 4, "Registros eliminados"
            return 4, "No existe la Base de Datos"
        return 6, "Selecciona una Base de Datos"
    
    elif result[0] == "update":
        if 'db_in_use' in session:
            if os.path.exists(f'databases/{session["db_in_use"]}'):
                conn = sqlite3.connect(f'databases/{session["db_in_use"]}')
                cursor = conn.cursor()
                cursor.execute(result[1])
                conn.commit()
                return 4, "Registro actualizado"
            return 4, "No existe la Base de Datos"
        return 7, "Selecciona una Base de Datos"

if __name__ == '__main__':
    app.run(port=3000, debug=True)