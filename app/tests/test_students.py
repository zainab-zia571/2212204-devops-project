def test_create_student(client):
    payload = {
        "reg_no": "2212202",
        "name": "Mariam Azam",
        "email": "mariam@test.com",
        "course": "DevOps"
    }
    response = client.post("/students", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["reg_no"] == "2212202"
    assert "id" in data


def test_get_students_empty(client):
    response = client.get("/students")
    assert response.status_code == 200
    assert response.json() == []


def test_get_students_after_create(client):
    client.post("/students", json={
        "reg_no": "2212201",
        "name": "Sara Ahmed",
        "email": "sara@test.com",
        "course": "Cloud"
    })
    response = client.get("/students")
    assert len(response.json()) == 1


def test_get_student_by_reg_no(client):
    client.post("/students", json={
        "reg_no": "2212203",
        "name": "Usman Ali",
        "email": "usman@test.com",
        "course": "Linux"
    })
    response = client.get("/students/2212203")
    assert response.status_code == 200
    assert response.json()["name"] == "Usman Ali"


def test_get_student_not_found(client):
    response = client.get("/students/NOTEXIST")
    assert response.status_code == 404