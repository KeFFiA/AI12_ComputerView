from sqlalchemy import create_engine, Column, Integer, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()
Base = declarative_base()

class Report(Base):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True)
    json_data = Column(JSON)

def save_to_db(data):
    engine = create_engine(os.getenv("DB_URL"))
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    with Session() as session:
        session.add(Report(json_data=data))
        session.commit()
