"""
Gestione del database SQLite per il riconoscimento facciale.
"""

import sqlite3
import numpy as np
import pickle
from typing import List, Tuple, Optional
import os
import config


class DatabaseManager:
    """Gestisce tutte le operazioni sul database SQLite."""
    
    def __init__(self, db_path: str = None):
        """
        Inizializza il database manager.
        
        Args:
            db_path: Percorso del database SQLite
        """
        self.db_path = db_path or config.DATABASE_PATH
        self.conn = None
        self.cursor = None
        self._initialize_database()
    
    def _initialize_database(self):
        """Inizializza il database e crea le tabelle se non esistono."""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        
        # Crea tabella utenti
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cognome TEXT NOT NULL,
                foto_profilo BLOB,
                embedding BLOB NOT NULL,
                data_registrazione TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(nome, cognome)
            )
        """)
        
        self.conn.commit()
    
    def add_user(self, nome: str, cognome: str, embedding: np.ndarray, 
                 foto_profilo: bytes = None) -> int:
        """
        Aggiunge un nuovo utente al database.
        
        Args:
            nome: Nome dell'utente
            cognome: Cognome dell'utente
            embedding: Embedding facciale (numpy array)
            foto_profilo: Foto profilo in bytes (opzionale)
            
        Returns:
            ID dell'utente inserito
        """
        # Serializza l'embedding
        embedding_blob = pickle.dumps(embedding)
        
        try:
            self.cursor.execute("""
                INSERT INTO users (nome, cognome, embedding, foto_profilo)
                VALUES (?, ?, ?, ?)
            """, (nome, cognome, embedding_blob, foto_profilo))
            
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            # Utente già esistente
            return -1
    
    def get_user(self, user_id: int) -> Optional[dict]:
        """
        Recupera un utente dal database.
        
        Args:
            user_id: ID dell'utente
            
        Returns:
            Dizionario con i dati dell'utente o None
        """
        self.cursor.execute("""
            SELECT id, nome, cognome, foto_profilo, embedding, data_registrazione
            FROM users WHERE id = ?
        """, (user_id,))
        
        row = self.cursor.fetchone()
        if row:
            return {
                'id': row[0],
                'nome': row[1],
                'cognome': row[2],
                'foto_profilo': row[3],
                'embedding': pickle.loads(row[4]),
                'data_registrazione': row[5]
            }
        return None
    
    def get_all_users(self) -> List[dict]:
        """
        Recupera tutti gli utenti dal database.
        
        Returns:
            Lista di dizionari con i dati degli utenti
        """
        self.cursor.execute("""
            SELECT id, nome, cognome, foto_profilo, embedding, data_registrazione
            FROM users ORDER BY cognome, nome
        """)
        
        users = []
        for row in self.cursor.fetchall():
            users.append({
                'id': row[0],
                'nome': row[1],
                'cognome': row[2],
                'foto_profilo': row[3],
                'embedding': pickle.loads(row[4]),
                'data_registrazione': row[5]
            })
        return users
    
    def get_all_embeddings(self) -> List[Tuple[int, str, np.ndarray]]:
        """
        Recupera tutti gli embeddings dal database.
        
        Returns:
            Lista di tuple (id, nome_completo, embedding)
        """
        self.cursor.execute("""
            SELECT id, nome, cognome, embedding FROM users
        """)
        
        embeddings = []
        for row in self.cursor.fetchall():
            user_id = row[0]
            nome_completo = f"{row[1]} {row[2]}"
            embedding = pickle.loads(row[3])
            embeddings.append((user_id, nome_completo, embedding))
        
        return embeddings
    
    def delete_user(self, user_id: int) -> bool:
        """
        Elimina un utente dal database.
        
        Args:
            user_id: ID dell'utente da eliminare
            
        Returns:
            True se eliminato con successo, False altrimenti
        """
        self.cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        self.conn.commit()
        return self.cursor.rowcount > 0
    
    def update_user(self, user_id: int, nome: str = None, cognome: str = None,
                   foto_profilo: bytes = None) -> bool:
        """
        Aggiorna i dati di un utente.
        
        Args:
            user_id: ID dell'utente
            nome: Nuovo nome (opzionale)
            cognome: Nuovo cognome (opzionale)
            foto_profilo: Nuova foto profilo (opzionale)
            
        Returns:
            True se aggiornato con successo, False altrimenti
        """
        updates = []
        params = []
        
        if nome is not None:
            updates.append("nome = ?")
            params.append(nome)
        
        if cognome is not None:
            updates.append("cognome = ?")
            params.append(cognome)
        
        if foto_profilo is not None:
            updates.append("foto_profilo = ?")
            params.append(foto_profilo)
        
        if not updates:
            return False
        
        params.append(user_id)
        query = f"UPDATE users SET {', '.join(updates)} WHERE id = ?"
        
        self.cursor.execute(query, params)
        self.conn.commit()
        return self.cursor.rowcount > 0
    
    def check_duplicate(self, embedding: np.ndarray, threshold: float = None) -> Optional[int]:
        """
        Controlla se esiste già un utente con un embedding simile.
        
        Args:
            embedding: Embedding da confrontare
            threshold: Soglia di similarità (default da config)
            
        Returns:
            ID dell'utente duplicato o None
        """
        if threshold is None:
            threshold = config.MAX_DUPLICATE_DISTANCE
        
        all_embeddings = self.get_all_embeddings()
        
        for user_id, _, stored_embedding in all_embeddings:
            distance = np.linalg.norm(embedding - stored_embedding)
            if distance < threshold:
                return user_id
        
        return None
    
    def close(self):
        """Chiude la connessione al database."""
        if self.conn:
            self.conn.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
