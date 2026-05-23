import json

def delete_student(name):
  with open('students.json', "r") as f:
    students = json.load(f)
    
  students = [s  for s in students if s["name"] != name]

  with open('students.json','w') as f:
    json.dump(students,f,indent=2)

delete_student("Ra")