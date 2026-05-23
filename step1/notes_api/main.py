from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, engine
import models, schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/notes", response_model=schemas.NoteResponse)
def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db)):
    db_note = models.Note(title=note.title, content=note.content)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

# READ ALL
@app.get("/notes", response_model=list[schemas.NoteResponse])
def get_notes(db: Session = Depends(get_db)):
    return db.query(models.Note).all()

# READ ONE
@app.get("/notes/{note_id}", response_model=schemas.NoteResponse)
def get_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note nahi mila")
    return note

# UPDATE
@app.put("/notes/{note_id}", response_model=schemas.NoteResponse)
def update_note(note_id: int, note: schemas.NoteCreate, db: Session = Depends(get_db)):
    db_note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note nahi mila")
    db_note.title = note.title
    db_note.content = note.content
    db.commit()
    db.refresh(db_note)
    return db_note

# DELETE
@app.delete("/notes/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    db_note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note nahi mila")
    db.delete(db_note)
    db.commit()
    return {"message": "Note delete ho gaya"}