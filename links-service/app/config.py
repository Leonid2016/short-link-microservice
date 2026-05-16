import os

class Config:
    DATABASE_URL = os.getenv('DATABASE_URL')
    BASE_URL = os.getenv('BASE_URL', 'http://localhost')
    ANALYTICS_INTERNAL_URL = os.getenv('ANALYTICS_INTERNAL_URL', 'http://analytics-service:5003')
