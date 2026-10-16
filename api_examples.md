# API examples

Start the server before running these commands. On Windows use `curl.exe`; on macOS/Linux use `curl`. Run the examples in order against a freshly started server.

## List employees

```powershell
curl.exe -i http://127.0.0.1:5000/employees
```

200 OK:

```json
[
  {"id": 1, "name": "Rahul Sharma", "department": "Engineering", "status": "Active"},
  {"id": 2, "name": "Priya Patel", "department": "HR", "status": "Active"},
  {"id": 3, "name": "Amit Verma", "department": "Engineering", "status": "Inactive"}
]
```

## Retrieve one employee

```powershell
curl.exe -i http://127.0.0.1:5000/employees/2
```

200 OK:

```json
{"id": 2, "name": "Priya Patel", "department": "HR", "status": "Active"}
```

## Filter by department

```powershell
curl.exe -i "http://127.0.0.1:5000/employees?department=Engineering"
```

200 OK: returns employees 1 and 3 from the first example. An unmatched department returns `[]`.

## Create an employee

Save this body in `new_employee.json`:

```json
{"name": "Neha Shah", "department": "Sales"}
```

```powershell
curl.exe -i -X POST http://127.0.0.1:5000/employees -H "Content-Type: application/json" --data-binary "@new_employee.json"
```

201 Created:

```json
{"id": 4, "name": "Neha Shah", "department": "Sales", "status": "Active"}
```

## Update status

Save this body in `status.json`:

```json
{"status": "Inactive"}
```

```powershell
curl.exe -i -X PATCH http://127.0.0.1:5000/employees/4/status -H "Content-Type: application/json" --data-binary "@status.json"
```

200 OK:

```json
{"id": 4, "name": "Neha Shah", "department": "Sales", "status": "Inactive"}
```

GET `/employees/4` now returns the updated record.

## Error cases

| Request | Body | Status | Response |
| --- | --- | --- | --- |
| GET /employees/999 | None | 404 | `{"error":"Employee not found"}` |
| POST /employees | `{"name":" ","department":"HR"}` | 400 | `{"error":"Name must be a non-empty string"}` |
| POST /employees | `{"name":"Neha"}` | 400 | `{"error":"Department must be a non-empty string"}` |
| PATCH /employees/1/status | `{"status":"Pending"}` | 400 | `{"error":"Status must be Active or Inactive"}` |
| PATCH /employees/999/status | `{"status":"Active"}` | 404 | `{"error":"Employee not found"}` |
| POST /employees | `[]` | 400 | `{"error":"Request body must be a JSON object"}` |

POST and PATCH bodies must be sent with `Content-Type: application/json`.
