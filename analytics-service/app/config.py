import os

class Config:
    DATABASE_URL = os.getenv('DATABASE_URL')
    LINKS_INTERNAL_URL = os.getenv('LINKS_INTERNAL_URL', 'http://links-service:5002')
