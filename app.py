from flask import Flask, jsonify, request


def create_app():
    app = Flask(__name__)

    # Data is kept in memory and resets when the application restarts.
    employees = {
        1: {"id": 1, "name": "Rahul Sharma", "department": "Engineering", "status": "Active"},
        2: {"id": 2, "name": "Priya Patel", "department": "HR", "status": "Active"},
        3: {"id": 3, "name": "Amit Verma", "department": "Engineering", "status": "Inactive"},
    }
    next_id = 4

    def read_body():
        data = request.get_json(silent=True)
        return data if isinstance(data, dict) else None

    @app.get("/employees")
    def list_employees():
        result = list(employees.values())
        department = request.args.get("department")
        if department is not None:
            result = [
                employee for employee in result
                if employee["department"].casefold() == department.strip().casefold()
            ]
        return jsonify(result)

    @app.get("/employees/<int:employee_id>")
    def get_employee(employee_id):
        employee = employees.get(employee_id)
        if employee is None:
            return jsonify({"error": "Employee not found"}), 404
        return jsonify(employee)

    @app.post("/employees")
    def add_employee():
        nonlocal next_id
        data = read_body()
        if data is None:
            return jsonify({"error": "Request body must be a JSON object"}), 400

        name = data.get("name")
        department = data.get("department")
        if not isinstance(name, str) or not name.strip():
            return jsonify({"error": "Name must be a non-empty string"}), 400
        if not isinstance(department, str) or not department.strip():
            return jsonify({"error": "Department must be a non-empty string"}), 400

        employee = {
            "id": next_id,
            "name": name.strip(),
            "department": department.strip(),
            "status": "Active",
        }
        employees[next_id] = employee
        next_id += 1
        return jsonify(employee), 201

    @app.patch("/employees/<int:employee_id>/status")
    def update_status(employee_id):
        employee = employees.get(employee_id)
        if employee is None:
            return jsonify({"error": "Employee not found"}), 404

        data = read_body()
        if data is None:
            return jsonify({"error": "Request body must be a JSON object"}), 400
        status = data.get("status")
        if status not in ("Active", "Inactive"):
            return jsonify({"error": "Status must be Active or Inactive"}), 400

        employee["status"] = status
        return jsonify(employee)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({"error": "Method not allowed"}), 405

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, threaded=False)
