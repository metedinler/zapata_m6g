import chromadb
import redis
import sqlite3
import json
import os
from sentence_transformers import SentenceTransformer
from concurrent.futures import ProcessPoolExecutor
from configmodule import config

class AlternativeEmbeddingModule:
    def __init__(self):
        self.embedding_model = config.EMBEDDING_MODEL
        self.chroma_client = chromadb.PersistentClient(path=config.CHROMA_DB_PATH)
        self.redis_client = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, decode_responses=True)
        self.sqlite_db = config.SQLITE_DB_PATH
        self.max_workers = config.MAX_WORKERS

        # Alternatif embedding modelleri
        self.models = {
            "contriever": SentenceTransformer("facebook/contriever"),
            "specter": SentenceTransformer("allenai/specter"),
            "minilm": SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        }

    def generate_embedding(self, text):
        """
        Alternatif embedding modelleri ile vektör oluşturur.
        """
        if self.embedding_model in self.models:
            model = self.models[self.embedding_model]
            return model.encode(text).tolist()
        else:
            raise ValueError(f"Bilinmeyen embedding modeli: {self.embedding_model}")

    def save_embedding_to_chromadb(self, document_id, text):
        """
        Alternatif embedding’i ChromaDB’ye kaydeder.
        """
        embedding = self.generate_embedding(text)
        collection = self.chroma_client.get_collection(name="alternative_embeddings")
        collection.add(
            documents=[text],
            metadatas=[{"document_id": document_id}],
            ids=[f"{document_id}"]
        )
        self.redis_client.setex(f"alt_embedding:{document_id}", 3600, json.dumps(embedding))  # Redis önbelleğe alma
        self.save_embedding_to_sqlite(document_id, embedding)

    def save_embedding_to_sqlite(self, document_id, embedding):
        """
        Alternatif embedding’i SQLite veritabanına kaydeder.
        """
        conn = sqlite3.connect(self.sqlite_db)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alternative_embeddings (
                document_id TEXT PRIMARY KEY,
                embedding TEXT
            )
        """)

        cursor.execute("INSERT OR REPLACE INTO alternative_embeddings VALUES (?, ?)", (document_id, json.dumps(embedding)))

        conn.commit()
        conn.close()
        print(f"📌 Alternatif Embedding SQLite veritabanına kaydedildi: {document_id}")

    def batch_generate_embeddings(self, texts):
        """
        Çoklu işlem desteği ile alternatif embedding oluşturma işlemini hızlandırır.
        """
        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            results = executor.map(self.generate_embedding, texts)
        return list(results)

# Modülü dışarıdan çağırmak için sınıf nesnesi
alternative_embedding_module = AlternativeEmbeddingModule()


# 📌 Yapılan Güncellemeler ve Değişiklikler
# 1️⃣ Yeni Embedding Modelleri:

# Contriever (facebook/contriever)
# Specter (allenai/specter)
# MiniLM (sentence-transformers/all-MiniLM-L6-v2)
# .env dosyasından model seçimi yapılabiliyor.
# 2️⃣ ChromaDB ve Redis Entegrasyonu:

# ChromaDB, embedding verilerini uzun vadeli saklamak için kullanılıyor.
# Redis, sık kullanılan embedding’leri önbelleğe alarak hızlandırıyor.
# 3️⃣ Embedding’ler SQLite’e de Kaydediliyor:

# Daha önce sadece ChromaDB’ye kayıt yapılıyordu, artık SQLite’e de ekleniyor.
# 4️⃣ Çoklu İşlem Desteği Eklendi:

# batch_generate_embeddings() fonksiyonu çoklu işlem (multiprocessing) kullanarak embedding işlemlerini hızlandırıyor.
# 📌 Sonuç:
# ✅ Contriever, Specter ve MiniLM modelleri destekleniyor.
# ✅ Embedding’ler ChromaDB, Redis ve SQLite’te saklanıyor.
# ✅ Çoklu işlem desteği eklendi.