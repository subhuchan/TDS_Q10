from server import load_students, filter_students


def test_load_students():
    students = load_students()
    assert isinstance(students, list)
    assert len(students) >= 5
    assert students[0]["studentId"] == 1
    assert students[0]["class"] == "1A"


def test_filter_students_single_class():
    students = load_students()
    filtered = filter_students(students, ["1A"])
    assert all(s["class"] == "1A" for s in filtered)
    # order should be preserved: ids 1 then 4 from sample CSV
    ids = [s["studentId"] for s in filtered]
    assert ids == [1, 4]


def test_filter_students_multi_class():
    students = load_students()
    filtered = filter_students(students, ["1A", "2A"])
    ids = [s["studentId"] for s in filtered]
    # expected order from CSV: 1(1A),3(2A),4(1A)
    assert ids == [1, 3, 4]


if __name__ == "__main__":
    test_load_students()
    test_filter_students_single_class()
    test_filter_students_multi_class()
    print("All tests passed")
