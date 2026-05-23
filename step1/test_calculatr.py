from pydantic import ValidationError
from restAPI import Student

def test_valid_student():
    s = Student(name="Yash", age=21, marks=85)
    assert s.name == "Yash"
    assert s.age == 21

def test_invalid_marks():
   
    try:
        Student(name="Yash", age=21, marks=150)
        assert False 
    except ValidationError:
        assert True  

def test_invalid_age():
   
    try:
        Student(name="Yash", age="abcd", marks=85)
        assert False
    except ValidationError:
        assert True