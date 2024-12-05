from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = "sqlite:///./db.test"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI()

class Record(Base):
    __tablename__ = 'records'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

Base.metadata.create_all(bind=engine)

@app.post("/add")
def add_record(name: str):
    db: Session = SessionLocal()
    new_record = Record(name=name)
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    db.close()
    return {"message": f"Запись добавлена: {new_record.name}"}

@app.delete("/delete/{record_id}")
def delete_record(record_id: int):
    db: Session = SessionLocal()
    record = db.query(Record).filter(Record.id == record_id).first()
    if record:
        db.delete(record)
        db.commit()
        db.close()
        return {"message": f"Запись {record_id} удалена."}
    db.close()
    raise HTTPException(status_code=404, detail="Запись не найдена.")

@app.get("/records")
def get_records():
    db: Session = SessionLocal()
    records = db.query(Record).all()
    db.close()
    return [{"id": record.id, "name": record.name} for record in records]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
