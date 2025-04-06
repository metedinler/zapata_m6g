import redis
import json

# Redis bağlantısı
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

def add_citation_to_redis(citation_data, citation_id):
    """
    Citation verisini Redis'e ekler.
    citation_data: Citation verisi (JSON formatında)
    citation_id: Citation ID
    """
    redis_client.set(f'citation:{citation_id}', json.dumps(citation_data))

def get_citation_from_redis(citation_id):
    """
    Citation verisini Redis'ten çeker.
    citation_id: Citation ID
    """
    citation_json = redis_client.get(f'citation:{citation_id}')
    if citation_json:
        return json.loads(citation_json)
    return None

import sqlite3
import json

# SQLite bağlantısı
conn = sqlite3.connect('citations.db')
cursor = conn.cursor()

# Citation JSON verilerini SQLite tablosuna ekleme
def create_citation_table():
    """
    Citation JSON verilerini saklamak için SQLite tablosu oluşturur.
    """
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS citation_json (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        citation_id TEXT NOT NULL,
        citation_data TEXT NOT NULL
    );
    ''')
    conn.commit()

def add_citation_to_sqlite(citation_id, citation_data):
    """
    Citation verisini SQLite veri tabanına ekler.
    citation_id: Citation ID
    citation_data: Citation verisi (JSON formatında)
    """
    cursor.execute('''
    INSERT INTO citation_json (citation_id, citation_data)
    VALUES (?, ?)
    ''', (citation_id, json.dumps(citation_data)))
    conn.commit()

def get_citation_from_sqlite(citation_id):
    """
    Citation verisini SQLite veri tabanından çeker.
    citation_id: Citation ID
    """
    cursor.execute('''
    SELECT citation_data FROM citation_json WHERE citation_id = ?
    ''', (citation_id,))
    row = cursor.fetchone()
    if row:
        return json.loads(row[0])
    return None

def process_and_store_citation(citation_id, citation_data):
    """
    Citation verisini hem Redis'e ekler hem de SQLite'ta saklar.
    citation_id: Citation ID
    citation_data: Citation verisi (JSON formatında)
    """
    # Citation verisini Redis'e ekle
    add_citation_to_redis(citation_data, citation_id)

    # Citation verisini SQLite'a ekle
    add_citation_to_sqlite(citation_id, citation_data)
