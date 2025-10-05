import requests

# These tests assume the server is running locally at http://127.0.0.1:8000
BASE = "http://127.0.0.1:8000"


def test_all_students():
    r = requests.get(BASE + "/api")
    assert r.status_code == 200
    data = r.json()
    assert "students" in data
    assert isinstance(data["students"], list)


def test_filter_single():
    r = requests.get(BASE + "/api", params={"class": "1A"})
    assert r.status_code == 200
    data = r.json()
    assert all(s["class"] == "1A" for s in data["students"])


def test_filter_multi():
    r = requests.get(BASE + "/api", params=[("class", "1A"), ("class", "2A")])
    assert r.status_code == 200
    data = r.json()
    classes = [s["class"] for s in data["students"]]
    assert any(c == "2A" for c in classes)
