#!/usr/bin/python3
from os import getenv
from dotenv import load_dotenv


load_dotenv() # Load the .env file

storage_t = getenv("HBNB_TYPE_STORAGE")

if storage_t == "db":
    from models.engine.db_storage import DBStorage
    
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage

    storage = FileStorage()
storage.reload()
