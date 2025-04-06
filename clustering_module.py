# Şimdi **`clustering_module.py`** modülünü en güncel haliyle yazıyorum ve ardından yapılan değişiklikleri detaylı olarak açıklayacağım.  

# 🚀 **Bu modülde hangi yenilikler var?**  
# ✔ **Embedding vektörleri kullanılarak makaleler kümeleme (clustering) işlemi yapılıyor.**  
# ✔ **K-Means, DBSCAN ve Agglomerative Clustering gibi farklı algoritmalar destekleniyor.**  
# ✔ **ChromaDB’den alınan embedding verileri ile doğrudan kümeleme yapılabiliyor.**  
# ✔ **SQLite ve Redis entegrasyonu sağlandı – kümeleme sonuçları kaydedilip önbelleğe alınıyor.**  
# ✔ **Çoklu işlem desteği (multiprocessing) ile büyük veri kümeleri daha hızlı işleniyor.**  

# ---

# ### **📌 `clustering_module.py` Modülü (Son Güncellenmiş Hâli)**  

# ```python
import numpy as np
import json
import sqlite3
import redis
import chromadb
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from concurrent.futures import ProcessPoolExecutor
from configmodule import config

class ClusteringModule:
    def __init__(self):
        self.chroma_client = chromadb.PersistentClient(path=config.CHROMA_DB_PATH)
        self.redis_client = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, decode_responses=True)
        self.sqlite_db = config.SQLITE_DB_PATH
        self.cluster_algorithm = config.CLUSTERING_ALGORITHM.lower()  # kmeans, dbscan, agglomerative
        self.max_clusters = int(config.MAX_CLUSTERS)
        self.max_workers = config.MAX_WORKERS

    def fetch_embeddings(self):
        """
        ChromaDB’den tüm embedding verilerini çeker.
        """
        collection = self.chroma_client.get_collection(name="embeddings")
        embeddings = collection.get(include=["documents", "metadatas"])
        vectors = [doc["embedding"] for doc in embeddings]
        document_ids = [doc["metadatas"]["document_id"] for doc in embeddings]
        return np.array(vectors), document_ids

    def cluster_documents(self):
        """
        Belirlenen kümeleme algoritmasına göre embedding verilerini kümeler.
        """
        vectors, document_ids = self.fetch_embeddings()

        if self.cluster_algorithm == "kmeans":
            cluster_labels = self._kmeans_clustering(vectors)
        elif self.cluster_algorithm == "dbscan":
            cluster_labels = self._dbscan_clustering(vectors)
        elif self.cluster_algorithm == "agglomerative":
            cluster_labels = self._agglomerative_clustering(vectors)
        else:
            raise ValueError(f"Bilinmeyen kümeleme algoritması: {self.cluster_algorithm}")

        clustered_data = [{"document_id": doc_id, "cluster": cluster} for doc_id, cluster in zip(document_ids, cluster_labels)]
        
        self.save_clusters_to_sqlite(clustered_data)
        self.save_clusters_to_redis(clustered_data)

        return clustered_data

    def _kmeans_clustering(self, vectors):
        """
        K-Means algoritması ile kümeleme yapar.
        """
        model = KMeans(n_clusters=self.max_clusters, random_state=42)
        return model.fit_predict(vectors)

    def _dbscan_clustering(self, vectors):
        """
        DBSCAN algoritması ile kümeleme yapar.
        """
        model = DBSCAN(eps=0.5, min_samples=5)
        return model.fit_predict(vectors)

    def _agglomerative_clustering(self, vectors):
        """
        Hiyerarşik kümeleme (Agglomerative Clustering) yapar.
        """
        model = AgglomerativeClustering(n_clusters=self.max_clusters)
        return model.fit_predict(vectors)

    def save_clusters_to_sqlite(self, clustered_data):
        """
        Kümeleme sonuçlarını SQLite veritabanına kaydeder.
        """
        conn = sqlite3.connect(self.sqlite_db)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS document_clusters (
                document_id TEXT PRIMARY KEY,
                cluster INTEGER
            )
        """)

        for data in clustered_data:
            cursor.execute("INSERT OR REPLACE INTO document_clusters VALUES (?, ?)", 
                           (data["document_id"], data["cluster"]))

        conn.commit()
        conn.close()
        print("📌 Kümeleme sonuçları SQLite veritabanına kaydedildi.")

    def save_clusters_to_redis(self, clustered_data):
        """
        Kümeleme sonuçlarını Redis önbelleğine kaydeder.
        """
        for data in clustered_data:
            self.redis_client.setex(f"cluster:{data['document_id']}", 3600, json.dumps(data))
        print("📌 Kümeleme sonuçları Redis önbelleğine kaydedildi.")

    def batch_cluster_documents(self, document_batches):
        """
        Çoklu işlem desteği ile büyük veri kümelerinde kümeleme sürecini hızlandırır.
        """
        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            results = executor.map(self.cluster_documents, document_batches)
        return list(results)

# Modülü dışarıdan çağırmak için sınıf nesnesi
clustering_module = ClusteringModule()
# ```

# ---

# ### **📌 Yapılan Güncellemeler ve Değişiklikler**  

# 1️⃣ **ChromaDB’den Embedding Verileri Çekiliyor:**  
#    - `fetch_embeddings()` fonksiyonu **ChromaDB’den embedding verilerini alıyor.**  
#    - **Vektörler numpy dizisine çevriliyor ve kümeleme algoritmasına gönderiliyor.**  

# 2️⃣ **Kümeleme Algoritmaları Destekleniyor:**  
#    - **K-Means (Varsayılan)**  
#    - **DBSCAN**  
#    - **Agglomerative Clustering (Hiyerarşik Kümeleme)**  
#    - **.env dosyasından hangi algoritmanın kullanılacağı seçilebiliyor.**  

# 3️⃣ **Kümeleme Sonuçları SQLite’e Kaydediliyor:**  
#    - `save_clusters_to_sqlite()` fonksiyonu **belge kimliği ve küme numarasını veritabanına kaydediyor.**  

# 4️⃣ **Kümeleme Sonuçları Redis’e Kaydediliyor:**  
#    - `save_clusters_to_redis()` fonksiyonu **kümeleme sonuçlarını Redis önbelleğine alıyor.**  
#    - **Önbelleğe alınan veriler, sorguların daha hızlı yapılmasını sağlıyor.**  

# 5️⃣ **Çoklu İşlem (Multiprocessing) Desteği:**  
#    - `batch_cluster_documents()` fonksiyonu ile **büyük veri kümeleri paralel olarak işleniyor.**  
#    - **Çok sayıda makale içeren büyük datasetler daha hızlı kümeleniyor.**  

# ---

# 📌 **Sonuç:**  
# ✅ **Embedding vektörleri ile ChromaDB’den doğrudan kümeleme yapılıyor.**  
# ✅ **K-Means, DBSCAN ve Agglomerative Clustering algoritmaları destekleniyor.**  
# ✅ **Kümeleme sonuçları SQLite ve Redis’e kaydediliyor.**  
# ✅ **Çoklu işlem desteği eklendi – büyük veri kümeleri daha hızlı işleniyor.**  

# 🚀 **Şimdi bir sonraki modüle geçelim mi? Hangisini istiyorsun?** 😊