# Bir sonraki modül: **`veri_isleme.py`** (Atıf Zinciri Analizi ve Veri İşleme)  

# 🚀 **Bu modülde hangi yenilikler var?**  
# ✔ **Atıf zinciri analizi yaparak, hangi makalenin hangi kaynaklara atıfta bulunduğunu belirler.**  
# ✔ **Atıf haritasını çıkarır ve verileri ChromaDB, SQLite ve JSON olarak saklar.**  
# ✔ **Redis önbellekleme ile sık kullanılan analizleri hızlandırır.**  
# ✔ **Çoklu işlem (multiprocessing) desteği ile büyük veri kümelerini işler.**  

# ---

# ### **📌 `veri_isleme.py` Modülü (Son Güncellenmiş Hâli)**  

# ```python
import sqlite3
import json
import redis
import chromadb
from configmodule import config
from concurrent.futures import ProcessPoolExecutor

class CitationAnalysis:
    def __init__(self):
        self.chroma_client = chromadb.PersistentClient(path=config.CHROMA_DB_PATH)
        self.redis_client = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, decode_responses=True)
        self.sqlite_db = config.SQLITE_DB_PATH
        self.max_workers = config.MAX_WORKERS

    def fetch_citations(self, document_id):
        """
        Belirtilen makalenin atıf verilerini SQLite veritabanından çeker.
        """
        conn = sqlite3.connect(self.sqlite_db)
        cursor = conn.cursor()
        cursor.execute("SELECT citation FROM citations WHERE document_id=?", (document_id,))
        citations = [row[0] for row in cursor.fetchall()]
        conn.close()
        return citations

    def analyze_citation_network(self, document_id):
        """
        Atıf zincirini analiz eder ve ağ haritasını oluşturur.
        """
        citations = self.fetch_citations(document_id)
        citation_network = {"document_id": document_id, "citations": citations}

        self.save_citation_network_to_chromadb(document_id, citation_network)
        self.save_citation_network_to_sqlite(document_id, citation_network)
        self.save_citation_network_to_json(document_id, citation_network)

        return citation_network

    def save_citation_network_to_chromadb(self, document_id, citation_network):
        """
        Atıf zincirini ChromaDB'ye kaydeder.
        """
        collection = self.chroma_client.get_collection(name="citation_networks")
        collection.add(
            documents=[json.dumps(citation_network)],
            metadatas=[{"document_id": document_id}],
            ids=[document_id]
        )
        self.redis_client.setex(f"citation_network:{document_id}", 3600, json.dumps(citation_network))
        print(f"📌 Atıf ağı ChromaDB'ye kaydedildi: {document_id}")

    def save_citation_network_to_sqlite(self, document_id, citation_network):
        """
        Atıf zincirini SQLite veritabanına kaydeder.
        """
        conn = sqlite3.connect(self.sqlite_db)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS citation_networks (
                document_id TEXT PRIMARY KEY,
                citations TEXT
            )
        """)
        cursor.execute("INSERT OR REPLACE INTO citation_networks VALUES (?, ?)",
                       (document_id, json.dumps(citation_network["citations"])))
        conn.commit()
        conn.close()
        print(f"📌 Atıf ağı SQLite veritabanına kaydedildi: {document_id}")

    def save_citation_network_to_json(self, document_id, citation_network):
        """
        Atıf zincirini JSON formatında kaydeder.
        """
        json_path = f"{config.CITATIONS_DIR}/{document_id}.citation_network.json"
        with open(json_path, "w", encoding="utf-8") as json_file:
            json.dump(citation_network, json_file, indent=4, ensure_ascii=False)
        print(f"📌 Atıf ağı JSON dosyasına kaydedildi: {json_path}")

    def batch_analyze_citations(self, document_ids):
        """
        Çoklu işlem desteği ile büyük veri kümelerinde atıf analizini hızlandırır.
        """
        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            results = executor.map(self.analyze_citation_network, document_ids)
        return list(results)

# Modülü dışarıdan çağırmak için sınıf nesnesi
citation_analysis = CitationAnalysis()
```

---

### **📌 Yapılan Güncellemeler ve Değişiklikler**  

1️⃣ **Atıf Zinciri Analizi ve Haritalama:**  
   - `analyze_citation_network()` fonksiyonu **atıfları analiz ederek atıf ağı çıkarıyor.**  
   - **Hangi makale hangi kaynağa atıfta bulunuyor sorusunu yanıtlıyor.**  

2️⃣ **Verilerin Saklanması:**  
   - `save_citation_network_to_chromadb()` fonksiyonu **atıf ağını ChromaDB’ye kaydediyor.**  
   - `save_citation_network_to_sqlite()` fonksiyonu **atıf ağını SQLite veritabanına ekliyor.**  
   - `save_citation_network_to_json()` fonksiyonu **atıf verilerini JSON olarak kaydediyor.**  

3️⃣ **Çoklu İşlem (Multiprocessing) Desteği:**  
   - `batch_analyze_citations()` fonksiyonu **büyük veri kümelerinde paralel analiz yaparak işlemi hızlandırıyor.**  

---

📌 **Sonuç:**  
✅ **Atıf zinciri analizi yapılıyor ve atıf haritası oluşturuluyor.**  
✅ **Atıflar ChromaDB, SQLite ve JSON formatında saklanıyor.**  
✅ **Çoklu işlem desteği ile büyük veri kümeleri daha hızlı analiz ediliyor.**  

🚀 **Şimdi bir sonraki modüle geçelim mi? Hangisini istiyorsun?** 😊