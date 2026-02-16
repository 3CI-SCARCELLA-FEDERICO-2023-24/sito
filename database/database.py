"""SQLite database operations for user management."""
import sqlite3
import os
import logging
from typing import Optional, List, Tuple
import config

logger = logging.getLogger(__name__)


class Database:
    """Handles all database operations for the facial recognition system."""
    
    def __init__(self, db_path: str = None):
        """Initialize database connection.
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path or config.DATABASE_PATH
        self._init_database()
    
    def _init_database(self):
        """Create database tables if they don't exist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create users table with unique constraint
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cognome TEXT NOT NULL,
                foto_path TEXT,
                embedding_path TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(nome, cognome)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_user(self, nome: str, cognome: str, foto_path: str = None, 
                 embedding_path: str = None) -> Optional[int]:
        """Add a new user to the database.
        
        Args:
            nome: User's first name
            cognome: User's last name
            foto_path: Path to user's photo
            embedding_path: Path to user's face embedding file
            
        Returns:
            User ID if successful, None if duplicate
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO users (nome, cognome, foto_path, embedding_path)
                VALUES (?, ?, ?, ?)
            ''', (nome, cognome, foto_path, embedding_path))
            
            user_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return user_id
        except sqlite3.IntegrityError:
            # Duplicate user
            return None
    
    def get_user(self, user_id: int) -> Optional[Tuple]:
        """Get user by ID.
        
        Args:
            user_id: User ID
            
        Returns:
            Tuple of (id, nome, cognome, foto_path, embedding_path, created_at)
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        
        conn.close()
        return user
    
    def get_all_users(self) -> List[Tuple]:
        """Get all users from the database.
        
        Returns:
            List of tuples (id, nome, cognome, foto_path, embedding_path, created_at)
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users ORDER BY created_at DESC')
        users = cursor.fetchall()
        
        conn.close()
        return users
    
    def update_user(self, user_id: int, nome: str = None, cognome: str = None,
                   foto_path: str = None, embedding_path: str = None) -> bool:
        """Update user information.
        
        Args:
            user_id: User ID
            nome: New first name (optional)
            cognome: New last name (optional)
            foto_path: New photo path (optional)
            embedding_path: New embedding path (optional)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            updates = []
            values = []
            
            if nome is not None:
                updates.append('nome = ?')
                values.append(nome)
            if cognome is not None:
                updates.append('cognome = ?')
                values.append(cognome)
            if foto_path is not None:
                updates.append('foto_path = ?')
                values.append(foto_path)
            if embedding_path is not None:
                updates.append('embedding_path = ?')
                values.append(embedding_path)
            
            if not updates:
                return False
            
            values.append(user_id)
            query = f"UPDATE users SET {', '.join(updates)} WHERE id = ?"
            
            cursor.execute(query, values)
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            logger.error(f"Database error updating user {user_id}: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error updating user {user_id}: {e}")
            return False
    
    def delete_user(self, user_id: int) -> bool:
        """Delete a user from the database.
        
        Args:
            user_id: User ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get user data to delete associated files
            user = self.get_user(user_id)
            if user:
                foto_path = user[3]
                embedding_path = user[4]
                
                # Delete associated files
                if foto_path and os.path.exists(foto_path):
                    try:
                        os.remove(foto_path)
                    except OSError as e:
                        logger.warning(f"Could not delete photo file {foto_path}: {e}")
                        
                if embedding_path and os.path.exists(embedding_path):
                    try:
                        os.remove(embedding_path)
                    except OSError as e:
                        logger.warning(f"Could not delete embedding file {embedding_path}: {e}")
            
            cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            logger.error(f"Database error deleting user {user_id}: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error deleting user {user_id}: {e}")
            return False
    
    def user_exists(self, nome: str, cognome: str) -> bool:
        """Check if a user already exists.
        
        Args:
            nome: First name
            cognome: Last name
            
        Returns:
            True if user exists, False otherwise
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT id FROM users WHERE nome = ? AND cognome = ?', 
                      (nome, cognome))
        exists = cursor.fetchone() is not None
        
        conn.close()
        return exists
