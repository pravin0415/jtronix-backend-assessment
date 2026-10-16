# Employee API

This project uses Python and Flask to manage employee records.
You can view employees, add an employee, change their status and filter by department.

## How to run

You need Python 3.10 or newer.

1. Open this project folder in VS Code.
2. Open Terminal > New Terminal.
3. Install Flask:

```powershell
python -m pip install -r requirements.txt
```

4. Start the application:

```powershell
python app.py
```

Keep the terminal open while using the API. Press Ctrl+C to stop it.
No database setup is needed.

## Check it in your browser

Open these links after starting the application:

- All employees: http://127.0.0.1:5000/employees
- Employee 2: http://127.0.0.1:5000/employees/2
- Engineering employees: http://127.0.0.1:5000/employees?department=Engineering

The browser will show data as JSON. There is no homepage at `/`, so opening only http://127.0.0.1:5000/ returns "Resource not found".

## Available requests

| Method | Address | What it does |
| --- | --- | --- |
| GET | /employees | Shows all employees |
| GET | /employees/2 | Shows employee 2 |
| GET | /employees?department=Engineering | Shows Engineering employees |
| POST | /employees | Adds an employee |
| PATCH | /employees/2/status | Changes employee 2's status |

To add an employee, send this JSON using Postman or PowerShell:

```json
{"name": "Pravin Garje", "department": "Engineering"}
```

The API assigns an ID and sets the new employee's status to Active.

To update a status, send:

```json
{"status": "Inactive"}
```

Use `Content-Type: application/json` for POST and PATCH requests.
See [api_examples.md](api_examples.md) for full commands and example responses.

## Run the tests

Open another terminal in the project folder and run:

```powershell
python -m unittest -v
```

If all tests pass, you will see `Ran 7 tests` and `OK`.

## Notes

- Name and department cannot be empty.
- Status must be Active or Inactive.
- Missing employees return a 404 error. Invalid input returns a 400 error.
- Three sample employees are included when the app starts.
- Data is stored in memory. Added employees and changes are lost when the app restarts.
- This is a local assessment project, not a production server.
