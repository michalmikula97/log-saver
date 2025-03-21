import os
import time
import psycopg2
from psycopg2.extras import DictCursor
from logger import logger
from config import config

CURRENT_DIR = os.path.dirname(__file__)
SQL_FILE = os.path.join(CURRENT_DIR, "create_books.sql")

class Database:

    def __init__(self):
        self.connection = None
        self.retry_delay = 1 
        self.max_delay = 300 # 5 min
        self.reconnect()
        self.ensure_books_table()

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
            if cursor:
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
            if cursor:
                cursor.close()

    def ensure_books_table(self):
        """Check if books table exists; if not, create it."""
        cursor = self.get_cursor()
        if cursor is None:
            return
        try:
            cursor.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'books')")
            exists = cursor.fetchone()[0]
            if not exists:
                logger.info("Table 'books' not found. Creating table...")
                self.create_books_table()
            else:
                logger.info("Table 'books' exists.")
        except Exception as error:
            logger.error(f"Error checking books table: {error}")
            self.connection.rollback()
        finally:
            if cursor:
                cursor.close()

    def create_books_table(self):
        """Run SQL script to create books table."""
        cursor = self.get_cursor()
        if cursor is None:
            return
        try:
            with open(SQL_FILE, "r") as sql_file:
                sql_script = sql_file.read()
            cursor.execute(sql_script)
            self.connection.commit()
            logger.info("Table 'books' created successfully.")
        except Exception as error:
            logger.error(f"Error creating books table: {error}")
        finally:
            if cursor:
                cursor.close()