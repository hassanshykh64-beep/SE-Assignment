from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('university.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''CREATE TABLE IF NOT EXISTS students 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                 name TEXT NOT NULL, 
                 department TEXT NOT NULL, 
                 email TEXT NOT NULL)''')
    conn.commit()
    conn.close()

@app.route('/students', methods=['GET'])
def get_all_students():
    conn = get_db()
    students = conn.execute('SELECT * FROM students').fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in students])

@app.route('/students/<int:id>', methods=['GET'])
def get_student(id):
    conn = get_db()
    student = conn.execute('SELECT * FROM students WHERE id = ?', (id,)).fetchone()
    conn.close()
    if student is None:
        return jsonify({'error': 'Student nahi mila'}), 404
    return jsonify(dict(student))

@app.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()
    conn = get_db()
    conn.execute('INSERT INTO students (name, department, email) VALUES (?, ?, ?)',
                 (data['name'], data['department'], data['email']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Student add ho gaya'}), 201

@app.route('/students/<int:id>', methods=['PUT'])
def update_student(id):
    data = request.get_json()
    conn = get_db()
    conn.execute('UPDATE students SET name=?, department=?, email=? WHERE id=?',
                 (data['name'], data['department'], data['email'], id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Data update hogaya'})

@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    conn = get_db()
    conn.execute('DELETE FROM students WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Student delete ho gaya'})

if __name__ == '__main__':
    init_db()
    app.run(port=5000, debug=True)