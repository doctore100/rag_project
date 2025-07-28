from config import create_settings as s
settings = s()
print(settings.database.vector_db_uri)