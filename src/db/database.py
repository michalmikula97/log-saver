import os
import time
import psycopg2
from psycopg2.extras import DictCursor
from logger import logger
from config import config

CURRENT_DIR = os.path.dirname(__file__)
LOG_DIR = CURRENT_DIR + "/data"
LOG_FILE = os.path.join(LOG_DIR, "logs.txt")

class Database:

    def __init__(self):
        self.connection = None
        self.retry_delay = 1 
        self.max_delay = 300 # 5 min
        self.reconnect()

    def connect_db(self):
        try:
            connection_string = (
                f"dbname='{config.DB_NAME}' "
                f"user='{config.DB_USER}' "
                f"host='{config.DB_HOST}' "
                f"password='{config.DB_PASSWORD}' "
                f"port='{config.DB_PORT}'"
            )
            connection = psycopg2.connect(connection_string)
            logger.info("Connected to PostgreSQL")
            self.retry_delay = 1
            return connection
        except (Exception, psycopg2.Error) as error:
            logger.error(f"Error while connecting to {config.DB_HOST} on port {config.DB_PORT}.")
            return None
        
    def reconnect(self, max_attempts=5, base_delay=1.0):
        while self.connection is None or self.connection.closed:
            self.connection = self.connect_db()
            if self.connection:
                return  
            
            logger.warning(f"Database unavailable. Retrying in {self.retry_delay} seconds...")
            time.sleep(self.retry_delay)
            self.retry_delay = min(self.retry_delay * 2, self.max_delay)  # Exponential increase up to 30 mins
        
    def get_cursor(self):
        if self.connection is None or self.connection.closed:
            logger.warning("Lost connection to database. Reconnecting...")
            self.reconnect()

        if self.connection:
            return self.connection.cursor(cursor_factory=DictCursor)
        else:
            logger.error("No database connection available.")
            return None
        
    def get_books(self):
        """Fetch books from the database."""
        cursor = self.get_cursor()
        if cursor is None:
            return []  # Return empty list if there's no DB connection
        try:
            cursor.execute("SELECT * FROM books")
            return cursor.fetchall()
        except Exception as error:
            logger.error(f"Error fetching books: {error}")
            return []
        finally:
            cursor.close()

    def insert_book(self, title, author):
        """Insert a new book into the database."""
        cursor = self.get_cursor()
        if cursor is None:
            logger.error("Cannot insert book: No database connection.")
            return
        try:
            cursor.execute(
                "INSERT INTO books (title, author) VALUES (%s, %s)",
                (title, author,),
            )
            self.connection.commit()
            logger.info(f"Book added: {title} by {author}")
        except Exception as error:
            logger.error(f"Error inserting book: {error}")
        finally:
            cursor.close()