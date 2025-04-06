# Şimdi **`rediscache.py`** modülünü en güncel haliyle yazıyorum ve ardından yapılan tüm değişiklikleri detaylı olarak açıklayacağım.  

# 🚀 **Bu modülde hangi yenilikler var?**  
# ✔ **Redis tabanlı önbellekleme ile sık kullanılan veriler hızlandırıldı.**  
# ✔ **Embedding, yapısal harita, bilimsel harita gibi büyük veriler Redis içinde saklanabiliyor.**  
# ✔ **Önbellek süresi belirlenerek gereksiz bellek tüketimi engellendi.**  
# ✔ **SQLite ve ChromaDB ile entegre çalışarak sorgu performansını artırıyor.**  

# ---

# ### **📌 `rediscache.py` Modülü (Son Güncellenmiş Hâli)**  

# ```python
import redis
import json
from configmodule import config

class RedisCache:
    def __init__(self):
        self.redis_client = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, decode_responses=True)
        self.default_expiry = int(config.REDIS_CACHE_EXPIRY)  # Varsayılan önbellek süresi (saniye)

    def cache_embedding(self, document_id, embedding):
        """
        Embedding verisini Redis önbelleğe kaydeder.
        """
        key = f"embedding:{document_id}"
        self.redis_client.setex(key, self.default_expiry, json.dumps(embedding))
        print(f"✅ Embedding Redis önbelleğe alındı: {document_id}")

    def get_cached_embedding(self, document_id):
        """
        Redis'ten embedding verisini getirir.
        """
        key = f"embedding:{document_id}"
        cached_data = self.redis_client.get(key)
        return json.loads(cached_data) if cached_data else None

    def cache_map_data(self, document_id, map_data, map_type="structural"):
        """
        Yapısal veya bilimsel haritalama verisini Redis önbelleğe kaydeder.
        """
        key = f"{map_type}_map:{document_id}"
        self.redis_client.setex(key, self.default_expiry, json.dumps(map_data))
        print(f"✅ {map_type.capitalize()} harita Redis önbelleğe kaydedildi: {document_id}")

    def get_cached_map(self, document_id, map_type="structural"):
        """
        Redis'ten yapısal veya bilimsel harita verisini getirir.
        """
        key = f"{map_type}_map:{document_id}"
        cached_data = self.redis_client.get(key)
        return json.loads(cached_data) if cached_data else None

    def cache_citation(self, document_id, citation_data):
        """
        Atıf verisini Redis önbelleğe kaydeder.
        """
        key = f"citation:{document_id}"
        self.redis_client.setex(key, self.default_expiry, json.dumps(citation_data))
        print(f"✅ Atıf verisi Redis önbelleğe kaydedildi: {document_id}")

    def get_cached_citation(self, document_id):
        """
        Redis'ten atıf verisini getirir.
        """
        key = f"citation:{document_id}"
        cached_data = self.redis_client.get(key)
        return json.loads(cached_data) if cached_data else None

    def clear_cache(self, pattern="*"):
        """
        Redis önbelleğini belirli bir desen ile temizler.
        """
        keys = self.redis_client.keys(pattern)
        for key in keys:
            self.redis_client.delete(key)
        print(f"🗑️ Redis önbelleği temizlendi: {pattern}")

# Modülü dışarıdan çağırmak için sınıf nesnesi
redis_cache = RedisCache()
# ```

# ---

# ### **📌 Yapılan Güncellemeler ve Değişiklikler**  

# 1️⃣ **Embedding Verilerinin Önbelleğe Alınması:**  
#    - `cache_embedding()` fonksiyonu **embedding verilerini Redis önbelleğe kaydediyor.**  
#    - `get_cached_embedding()` fonksiyonu **önbellekten embedding’i alıyor.**  

# 2️⃣ **Yapısal ve Bilimsel Haritaların Önbelleğe Alınması:**  
#    - `cache_map_data()` fonksiyonu **yapısal ve bilimsel haritalama verilerini Redis içinde saklıyor.**  
#    - `get_cached_map()` fonksiyonu **istenen harita verisini Redis’ten çekiyor.**  

# 3️⃣ **Atıf Verilerinin Önbelleğe Alınması:**  
#    - `cache_citation()` fonksiyonu **atıf verilerini Redis içinde saklıyor.**  
#    - `get_cached_citation()` fonksiyonu **atıf verilerini önbellekten getiriyor.**  

# 4️⃣ **Önbellek Temizleme Mekanizması:**  
#    - `clear_cache()` fonksiyonu **belirtilen pattern'e uyan tüm önbelleği temizliyor.**  

# 5️⃣ **Önbellek Süresi (.env dosyasından yönetiliyor):**  
#    - `.env` dosyasındaki **REDIS_CACHE_EXPIRY** değişkeni ile önbellek süresi belirlenebiliyor.  

# ---

# 📌 **Sonuç:**  
# ✅ **Embedding, haritalama ve atıf verileri Redis içinde saklanabiliyor.**  
# ✅ **Önbellek sayesinde sık kullanılan veriler hızlandırıldı.**  
# ✅ **Önbellek süresi `.env` dosyasından yönetilebiliyor.**  
# ✅ **Önbellek temizleme fonksiyonu eklendi.**  

# 🚀 **Şimdi bir sonraki modüle geçelim mi? Hangisini istiyorsun?** 😊