from pydantic import BaseModel, validator,field_validator

class Student(BaseModel):
  name:str
  age:int
  marks:float

  @field_validator("marks")
  def marks_valid(cls, v):
    if v < 0 or v > 100:
         raise ValueError("Marks 0-100 ke beech hone chahiye")
    return v

s1 = Student(name="yash",age=21,marks=90)
print(s1)