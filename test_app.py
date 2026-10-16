import unittest

from app import create_app


class EmployeeApiTests(unittest.TestCase):
    def setUp(self):
        self.client = create_app().test_client()

    def test_sample_data_and_filter(self):
        response = self.client.get("/employees")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 3)
        response = self.client.get("/employees?department=engineering")
        self.assertEqual([employee["id"] for employee in response.json], [1, 3])
        self.assertEqual(self.client.get("/employees?department=Sales").json, [])

    def test_get_employee(self):
        response = self.client.get("/employees/2")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["name"], "Priya Patel")
        self.assertEqual(self.client.get("/employees/999").status_code, 404)

    def test_create_then_update_and_retrieve(self):
        response = self.client.post("/employees", json={
            "name": "  Neha Shah  ", "department": " Sales ", "id": 1, "status": "Inactive"
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {
            "id": 4, "name": "Neha Shah", "department": "Sales", "status": "Active"
        })
        second = self.client.post("/employees", json={"name": "Kiran", "department": "HR"})
        self.assertEqual(second.json["id"], 5)
        for status in ["Inactive", "Active"]:
            response = self.client.patch("/employees/4/status", json={"status": status})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(self.client.get("/employees/4").json["status"], status)
        self.assertEqual(len(self.client.get("/employees?department=Sales").json), 1)

    def test_invalid_employee_fields(self):
        for field in ["name", "department"]:
            for value in [None, "", "   ", 123, [], {}, False]:
                with self.subTest(field=field, value=value):
                    data = {"name": "Neha", "department": "HR", field: value}
                    self.assertEqual(self.client.post("/employees", json=data).status_code, 400)
            data = {"name": "Neha", "department": "HR"}
            del data[field]
            self.assertEqual(self.client.post("/employees", json=data).status_code, 400)
        self.assertEqual(len(self.client.get("/employees").json), 3)

    def test_invalid_status_does_not_change_employee(self):
        for status in ["active", "Pending", "", None, [], {}, 1]:
            with self.subTest(status=status):
                response = self.client.patch("/employees/1/status", json={"status": status})
                self.assertEqual(response.status_code, 400)
                self.assertEqual(self.client.get("/employees/1").json["status"], "Active")
        self.assertEqual(self.client.patch("/employees/999/status", json={"status": "Active"}).status_code, 404)

    def test_bad_request_bodies(self):
        for method, url in [(self.client.post, "/employees"), (self.client.patch, "/employees/1/status")]:
            for body in ["", "{broken", "null", "[]", '"text"', "123"]:
                with self.subTest(url=url, body=body):
                    response = method(url, data=body, content_type="application/json")
                    self.assertEqual(response.status_code, 400)
            self.assertEqual(method(url, data="name=Neha").status_code, 400)

    def test_unknown_route_and_unsupported_method(self):
        self.assertEqual(self.client.get("/employees/abc").status_code, 404)
        response = self.client.delete("/employees/1")
        self.assertEqual(response.status_code, 405)
        self.assertIn("error", response.json)


if __name__ == "__main__":
    unittest.main()
