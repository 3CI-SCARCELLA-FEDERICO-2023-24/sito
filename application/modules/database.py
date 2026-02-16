"""
Database module for managing face recognition data with SQLite
"""
import sqlite3
import os
import json
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from modules import config


class FaceDatabase:
    """Manages the SQLite database for face recognition"""
    
    def __init__(self, db_path: str = config.DB_PATH):
        """Initialize database connection"""
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self._connect()
        self._create_tables()
    
    def _connect(self):
        """Create database connection"""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
    
    def _create_tables(self):
        """Create necessary database tables"""
        # Table for registered persons
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS persons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                surname TEXT,
                photo_path TEXT,
                face_embedding TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_unknown BOOLEAN DEFAULT 0
            )
        ''')
        
        # Table for face detection history
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS detections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                person_id INTEGER,
                detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                confidence REAL,
                FOREIGN KEY (person_id) REFERENCES persons(id) ON DELETE CASCADE
            )
        ''')
        
        # Create index for faster lookups
        self.cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_person_name 
            ON persons(name, surname)
        ''')
        
        self.conn.commit()
    
    def add_person(self, name: str, surname: str = "", photo_path: str = "", 
                   face_embedding: List[float] = None, is_unknown: bool = False) -> int:
        """
        Add a new person to the database
        
        Args:
            name: Person's first name
            surname: Person's surname
            photo_path: Path to person's photo
            face_embedding: Face embedding vector
            is_unknown: Whether this is an unknown person
            
        Returns:
            ID of the newly created person
        """
        embedding_json = json.dumps(face_embedding) if face_embedding else None
        
        self.cursor.execute('''
            INSERT INTO persons (name, surname, photo_path, face_embedding, is_unknown)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, surname, photo_path, embedding_json, is_unknown))
        
        self.conn.commit()
        return self.cursor.lastrowid
    
    def update_person(self, person_id: int, name: str = None, surname: str = None, 
                     photo_path: str = None, face_embedding: List[float] = None) -> bool:
        """
        Update person information
        
        Args:
            person_id: ID of the person to update
            name: New name (optional)
            surname: New surname (optional)
            photo_path: New photo path (optional)
            face_embedding: New face embedding (optional)
            
        Returns:
            True if update successful, False otherwise
        """
        updates = []
        params = []
        
        if name is not None:
            updates.append("name = ?")
            params.append(name)
        if surname is not None:
            updates.append("surname = ?")
            params.append(surname)
        if photo_path is not None:
            updates.append("photo_path = ?")
            params.append(photo_path)
        if face_embedding is not None:
            updates.append("face_embedding = ?")
            params.append(json.dumps(face_embedding))
        
        if not updates:
            return False
        
        updates.append("updated_at = CURRENT_TIMESTAMP")
        updates.append("is_unknown = 0")  # No longer unknown if being updated
        params.append(person_id)
        
        query = f"UPDATE persons SET {', '.join(updates)} WHERE id = ?"
        self.cursor.execute(query, params)
        self.conn.commit()
        
        return self.cursor.rowcount > 0
    
    def delete_person(self, person_id: int) -> bool:
        """
        Delete a person from the database
        
        Args:
            person_id: ID of the person to delete
            
        Returns:
            True if deletion successful, False otherwise
        """
        # Get photo path before deletion to remove file
        person = self.get_person(person_id)
        if person and person['photo_path'] and os.path.exists(person['photo_path']):
            try:
                os.remove(person['photo_path'])
            except Exception as e:
                print(f"Error deleting photo file: {e}")
        
        self.cursor.execute("DELETE FROM persons WHERE id = ?", (person_id,))
        self.conn.commit()
        
        return self.cursor.rowcount > 0
    
    def get_person(self, person_id: int) -> Optional[Dict]:
        """
        Get person by ID
        
        Args:
            person_id: ID of the person
            
        Returns:
            Dictionary with person data or None if not found
        """
        self.cursor.execute('''
            SELECT id, name, surname, photo_path, face_embedding, 
                   created_at, updated_at, is_unknown
            FROM persons WHERE id = ?
        ''', (person_id,))
        
        row = self.cursor.fetchone()
        if row:
            return self._row_to_dict(row)
        return None
    
    def get_all_persons(self, include_unknown: bool = True) -> List[Dict]:
        """
        Get all persons from database
        
        Args:
            include_unknown: Whether to include unknown persons
            
        Returns:
            List of dictionaries with person data
        """
        query = '''
            SELECT id, name, surname, photo_path, face_embedding, 
                   created_at, updated_at, is_unknown
            FROM persons
        '''
        
        if not include_unknown:
            query += " WHERE is_unknown = 0"
        
        query += " ORDER BY created_at DESC"
        
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        
        return [self._row_to_dict(row) for row in rows]
    
    def search_person_by_name(self, name: str, surname: str = "") -> Optional[Dict]:
        """
        Search for person by name and surname
        
        Args:
            name: Person's name
            surname: Person's surname
            
        Returns:
            Dictionary with person data or None if not found
        """
        self.cursor.execute('''
            SELECT id, name, surname, photo_path, face_embedding, 
                   created_at, updated_at, is_unknown
            FROM persons 
            WHERE LOWER(name) = LOWER(?) AND LOWER(surname) = LOWER(?)
        ''', (name, surname))
        
        row = self.cursor.fetchone()
        if row:
            return self._row_to_dict(row)
        return None
    
    def person_exists(self, name: str, surname: str = "") -> bool:
        """
        Check if a person exists in the database
        
        Args:
            name: Person's name
            surname: Person's surname
            
        Returns:
            True if person exists, False otherwise
        """
        return self.search_person_by_name(name, surname) is not None
    
    def add_detection(self, person_id: int, confidence: float):
        """
        Record a face detection event
        
        Args:
            person_id: ID of the detected person
            confidence: Detection confidence score
        """
        self.cursor.execute('''
            INSERT INTO detections (person_id, confidence)
            VALUES (?, ?)
        ''', (person_id, confidence))
        
        self.conn.commit()
    
    def get_detection_count(self, person_id: int) -> int:
        """
        Get number of times a person has been detected
        
        Args:
            person_id: ID of the person
            
        Returns:
            Number of detections
        """
        self.cursor.execute('''
            SELECT COUNT(*) FROM detections WHERE person_id = ?
        ''', (person_id,))
        
        return self.cursor.fetchone()[0]
    
    def _row_to_dict(self, row: Tuple) -> Dict:
        """
        Convert database row to dictionary
        
        Args:
            row: Database row tuple
            
        Returns:
            Dictionary with person data
        """
        embedding = None
        if row[4]:  # face_embedding
            try:
                embedding = json.loads(row[4])
            except json.JSONDecodeError:
                embedding = None
        
        return {
            'id': row[0],
            'name': row[1],
            'surname': row[2] or "",
            'photo_path': row[3] or "",
            'face_embedding': embedding,
            'created_at': row[5],
            'updated_at': row[6],
            'is_unknown': bool(row[7])
        }
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
    
    def __del__(self):
        """Cleanup on deletion"""
        self.close()
