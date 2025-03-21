import os

class Config:
    DB_NAME = os.getenv("DB_NAME", "bookstore")
    DB_USER = os.getenv("DB_USER", "wp-test")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "secret")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")

config = Config()