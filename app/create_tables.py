from app.db import Base, engine
from .models import *

def create_tables(engine):
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    create_tables(engine)