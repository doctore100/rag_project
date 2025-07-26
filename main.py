from config import create_settings

settings = create_settings()
print(settings.database.vector_db_uri)