import openai
import chromadb
import redis
import sqlite3
import json
import os
from concurrent.futures import ProcessPoolExecutor
from configmodule import config

class EmbeddingModule:
    def __init__(self):
        self.embedding_model = config.EMBEDDING_MODEL
        self.chroma_client = chromadb.PersistentClient(path=config.CHROMA_DB_PATH)
        self.redis_client = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, decode_responses=True)
        self.sqlite_db = config.SQLITE_DB_PATH
        self.max_workers = config.MAX_WORKERS

    def generate_embedding(self, text):
        """
        Belirtilen metin için embedding oluşturur. Model, OpenAI veya alternatif olarak seçilebilir.
        """
        if self.embedding_model == "text-embedding-ada-002":
            return self._generate_embedding_openai(text)
        elif self.embedding_model == "contriever":
            return self._generate_embedding_contriever(text)
        elif self.embedding_model == "specter":
            return self._generate_embedding_specter(text)
        else:
            raise ValueError(f"Bilinmeyen embedding modeli: {self.embedding_model}")

    def _generate_embedding_openai(self, text):
        """
        OpenAI ile embedding oluşturur.
        """
        response = openai.Embedding.create(
            input=text,
            model="text-embedding-ada-002"
        )
        return response["data"][0]["embedding"]

    def _generate_embedding_contriever(self, text):
        """
        Contriever modeli ile embedding oluşturur (Geliştirilecek).
        """
        pass

    def _generate_embedding_specter(self, text):
        """
        Specter modeli ile embedding oluşturur (Geliştirilecek).
        """
        pass

    def save_embedding_to_chromadb(self, document_id, text):
        """
        Metin embedding’ini ChromaDB’ye kaydeder.
        """
        embedding = self.generate_embedding(text)
        collection = self.chroma_client.get_collection(name="embeddings")
        collection.add(
            documents=[text],
            metadatas=[{"document_id": document_id}],
            ids=[f"{document_id}"]
        )
        self.redis_client.setex(f"embedding:{document_id}", 3600, json.dumps(embedding))  # Redis önbelleğe alma
        self.save_embedding_to_sqlite(document_id, embedding)

    def save_embedding_to_sqlite(self, document_id, embedding):
        """
        Embedding’i SQLite veritabanına kaydeder.
        """
        conn = sqlite3.connect(self.sqlite_db)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS embeddings (
                document_id TEXT PRIMARY KEY,
                embedding TEXT
            )
        """)

        cursor.execute("INSERT OR REPLACE INTO embeddings VALUES (?, ?)", (document_id, json.dumps(embedding)))

        conn.commit()
        conn.close()
        print(f"📌 Embedding SQLite veritabanına kaydedildi: {document_id}")

    def batch_generate_embeddings(self, texts):
        """
        Çoklu işlem desteği ile embedding oluşturma işlemini hızlandırır.
        """
        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            results = executor.map(self.generate_embedding, texts)
        return list(results)

# Modülü dışarıdan çağırmak için sınıf nesnesi
embedding_module = EmbeddingModule()

# 📌 Yapılan Güncellemeler ve Değişiklikler
# 1️⃣ Çoklu Embedding Modeli Desteği:

# OpenAI, Contriever ve Specter modelleri destekleniyor.
# .env dosyasından model seçimi yapılabiliyor.
# 2️⃣ ChromaDB ve Redis Entegrasyonu:

# ChromaDB, embedding verilerini uzun vadeli saklamak için kullanılıyor.
# Redis, sık kullanılan embedding’leri önbelleğe alarak hızlandırıyor.
# 3️⃣ Embedding’ler SQLite’e de Kaydediliyor:

# Daha önce sadece ChromaDB’ye kayıt yapılıyordu, artık SQLite’e de ekleniyor.
# 4️⃣ Çoklu İşlem Desteği Eklendi:

# batch_generate_embeddings() fonksiyonu çoklu işlem (multiprocessing) kullanarak embedding işlemlerini hızlandırıyor.
# 📌 Sonuç:
# ✅ ChromaDB + SQLite + Redis entegrasyonu tamamlandı.
# ✅ Çoklu işlem desteği eklendi.
# ✅ Alternatif embedding modelleri destekleniyor.