from flask import Flask, request, jsonify

app = Flask(__name__)

USERS = {
    "admin": {"password": "adminpass", "role": "Administrator"},
    "emp1": {"password": "emppass", "role": "Employee"}
}

EMPLOYEES = [{"id": 1, "name": "Ali", "position": "Dev"}]

def check_auth(username, password):
    user = USERS.get(username)
    if user and user['password'] == password:
        return user['role']
    return None

@app.route('/employees', methods=['GET', 'POST'])
def manage_employees():
    auth = request.authorization
    if not auth:
        return jsonify({"error": "Login is necessary"}), 401 # Protect from unauthenticated[cite: 3]
        
    role = check_auth(auth.username, auth.password)
    if not role:
        return jsonify({"error": "Invalid credentials"}), 401

    if request.method == 'GET':
  
        return jsonify({"data": EMPLOYEES, "your_role": role})

    if request.method == 'POST':

        if role != "Administrator":
            return jsonify({"error": "Access Denied. Only Admin can add."}), 403
            
        data = request.get_json()
        EMPLOYEES.append(data)
        return jsonify({"message": "Employee added successfully!"})

if __name__ == '__main__':
    app.run(port=5002, debug=True)