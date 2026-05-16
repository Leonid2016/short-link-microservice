import os

class Config:
    DATABASE_URL = os.getenv('DATABASE_URL')
    BOOTSTRAP_ADMIN_EMAIL = os.getenv('BOOTSTRAP_ADMIN_EMAIL', 'admin@example.com')
    BOOTSTRAP_ADMIN_PASSWORD = os.getenv('BOOTSTRAP_ADMIN_PASSWORD', '123')
