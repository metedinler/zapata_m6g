# Zapata M6 - Bilimsel Makale İşleme ve Atıf Analizi Sistemi  

📌 **Zapata M6**, bilimsel makaleleri işleyerek temiz metin çıkaran, atıf zinciri analizi yapan, yapısal haritalama gerçekleştiren ve AI modelini eğiten bir sistemdir.

## 🚀 Kurulum  

### 1️⃣ **Gereksinimler**  
- Python 3.9+
- Redis  
- SQLite  
- ChromaDB  

### 2️⃣ **Gerekli Paketleri Yükleyin**  
Aşağıdaki komutu çalıştırarak tüm bağımlılıkları yükleyin:  

```bash
pip install -r requirements.txt

#

Şimdi **`.env`, `requirements.txt` ve `README.md`** dosyalarını oluşturuyorum.  

🚀 **Bu dosyalarda hangi içerikler olacak?**  
✔ **`.env`** → Programın tüm yapılandırma ayarlarını içerir.  
✔ **`requirements.txt`** → Tüm bağımlılıkları listeler ve kurulumu kolaylaştırır.  
✔ **`README.md`** → Zapata M6'nın nasıl çalıştığını anlatır, kurulum ve kullanım yönergeleri içerir.  

---

### **📌 `.env` Dosyası (Yapılandırma Ayarları)**  

```ini
# Sistem Genel Ayarları
RUN_MODE=gui  # Çalıştırma modu: gui veya console
MAX_WORKERS=4  # Çoklu işlem için kullanılacak maksimum iş parçacığı sayısı
LOG_LEVEL=INFO  # Loglama seviyesi (DEBUG, INFO, WARNING, ERROR)

# Veritabanı ve Önbellek Ayarları
SQLITE_DB_PATH=data/zapata_m6.sqlite  # SQLite veritabanı dosyasının yolu
REDIS_HOST=localhost  # Redis sunucusunun adresi
REDIS_PORT=6379  # Redis sunucusunun portu
REDIS_CACHE_EXPIRY=3600  # Redis’te verinin ne kadar süre tutulacağı (saniye)

# ChromaDB Ayarları
CHROMA_DB_PATH=data/chromadb  # ChromaDB dizini

# Embedding Model Ayarları
EMBEDDING_MODEL=bert  # Varsayılan embedding modeli (bert, minilm, roberta)
EMBEDDING_PARCA_DIR=data/embeddings  # Embedding parçalarının saklandığı dizin

# Yapısal Haritalama
MAP_DIR=data/maps  # Yapısal ve bilimsel haritaların saklandığı dizin

# PDF İşleme Yöntemleri
PDF_TEXT_EXTRACTION_METHOD=pdfplumber  # Alternatif: pdfminer, pymupdf
TABLE_EXTRACTION_METHOD=pymupdf  # Alternatif: pdfplumber, pdfminer

# Yapay Zeka Fine-Tuning Ayarları
FINETUNE_MODEL=bert-base-uncased
FINETUNE_BATCH_SIZE=16
FINETUNE_EPOCHS=3
FINETUNE_LR=2e-5
FINETUNE_OUTPUT_DIR=models/fine_tuned

# Dosya Dizinleri
HEDEF_DIZIN=data/clean_texts
TEMIZ_TABLO_DIZIN=data/tables
CITATIONS_DIR=data/citations
TEMIZ_KAYNAKCA_DIZIN=data/references
```

---

### **📌 `requirements.txt` Dosyası (Bağımlılık Listesi)**  

```txt
torch==2.0.0
transformers==4.30.0
sentence-transformers==2.2.2
chromadb==0.3.26
redis==5.0.0
sqlite3
pdfplumber==0.7.5
pdfminer.six==20221105
pymupdf==1.22.3
customtkinter==5.1.3
networkx==3.1
matplotlib==3.7.1
scikit-learn==1.2.2
concurrent-log-handler==0.9.21
```

---

### **📌 `README.md` Dosyası (Kullanım Kılavuzu)**  

```md
# Zapata M6 - Bilimsel Makale İşleme ve Atıf Analizi Sistemi  

📌 **Zapata M6**, bilimsel makaleleri işleyerek temiz metin çıkaran, atıf zinciri analizi yapan, yapısal haritalama gerçekleştiren ve AI modelini eğiten bir sistemdir.

## 🚀 Kurulum  

### 1️⃣ **Gereksinimler**  
- Python 3.9+
- Redis  
- SQLite  
- ChromaDB  

### 2️⃣ **Gerekli Paketleri Yükleyin**  
Aşağıdaki komutu çalıştırarak tüm bağımlılıkları yükleyin:  

```bash
pip install -r requirements.txt
```

### 3️⃣ **.env Dosyanızı Yapılandırın**  
`.env` dosyanızda **çalıştırma modu (GUI/Konsol), veritabanı yolları ve embedding modeli gibi ayarları** düzenleyin.

### 4️⃣ **Programı Çalıştırın**  

**📌 GUI Modunda Çalıştırmak İçin:**  
```bash
python main.py
```

**📌 Konsol Modunda Çalıştırmak İçin:**  
```bash
RUN_MODE=console python main.py
```

---

## 🛠️ **Özellikler**  

### 📄 1️⃣ PDF İşleme  
- PDF’lerden metin çıkarma (pdfplumber, pdfminer, pymupdf desteği)  
- **Sütun düzenleme & tablo ayrıştırma**  

### 🔗 2️⃣ Atıf Analizi  
- **Makalelerdeki atıfları kaynaklarla eşleştirme**  
- **ChromaDB’ye atıf verilerini kaydetme**  

### 🤖 3️⃣ AI Modeli Eğitme  
- **Hugging Face Transformers ile fine-tuning**  
- **Eğitim verilerini SQLite’ten alıp AI modelini eğitme**  

### 📊 4️⃣ Görselleştirme  
- **Atıf ağını NetworkX ile interaktif grafik olarak gösterme**  
- **Makale kümelerini renk kodlu grafiklerle görselleştirme**  

---

## 📁 **Dizin Yapısı**  

```
📂 zapata_m6  
 ┣ 📂 data  
 ┃ ┣ 📂 embeddings  
 ┃ ┣ 📂 tables  
 ┃ ┣ 📂 citations  
 ┃ ┣ 📂 references  
 ┃ ┣ 📂 clean_texts  
 ┃ ┣ chromadb/  
 ┃ ┗ zapata_m6.sqlite  
 ┣ 📂 models  
 ┃ ┗ fine_tuned/  
 ┣ 📜 main.py  
 ┣ 📜 configmodule.py  
 ┣ 📜 pdfprocessing.py  
 ┣ 📜 citationmappingmodule.py  
 ┣ 📜 yapay_zeka_finetuning.py  
 ┣ 📜 redisqueue.py  
 ┣ 📜 rediscache.py  
 ┣ 📜 sqlite_storage.py  
 ┣ 📜 veri_isleme.py  
 ┣ 📜 veri_gorsellestirme.py  
 ┣ 📜 guimodule.py  
 ┣ 📜 requirements.txt  
 ┣ 📜 .env  
 ┗ 📜 README.md  
```

---

## 🚀 **Desteklenen Veri Formatları**  
📂 **Kaynakça Saklama Formatları:**  
- **RIS, BibTeX, CSV, VOS**  

📂 **Embedding Saklama:**  
- **ChromaDB, SQLite, Redis**  

📂 **Temiz Metin Saklama:**  
- **TXT, JSON, SQLite**  

📂 **Tablo Saklama:**  
- **CSV**  

---

## 🏆 **Geliştiriciler İçin Notlar**  
- **Yeni AI modeli eklemek için** `yapay_zeka_finetuning.py` dosyasını güncelleyin.  
- **Yeni veritabanı entegrasyonu için** `sqlite_storage.py` veya `redisqueue.py` içinde ilgili fonksiyonları genişletin.  
- **GUI'yi özelleştirmek için** `guimodule.py` içinde `create_widgets()` fonksiyonunu değiştirin.  

---

📌 **Zapata M6'nın son sürümünü kullanın, bilimsel veriyi en iyi şekilde işleyin!**  
📧 **Sorularınız için: support@zapataM6.com**  
```

---

📌 **Sonuç:**  
✅ **`.env` dosyası tüm yapılandırma ayarlarını içeriyor.**  
✅ **`requirements.txt` ile bağımlılıklar kolayca yüklenebiliyor.**  
✅ **`README.md` kapsamlı bir kurulum ve kullanım kılavuzu sağlıyor.**  

🚀 **Bunları proje dizinine ekleyelim mi? Veya düzenlemek istediğin bir kısım var mı?** 😊


config modulu
Bu modül, son 4 gün boyunca yapılan yoğun güncellemeleri ve entegrasyonları içeriyor. Modülde:

Tüm ayarlar .env dosyasından okunuyor.
Çalışma modu (GUI/console) RUN_MODE ile belirleniyor.
PDF işleme, embedding, citation mapping ve layout analiz ayarları eklendi.
Veritabanı (SQLite ve Redis) ayarları, ChromaDB entegrasyonu da yapılandırıldı.
Gerekli dizinler otomatik oluşturuluyor.
Gelişmiş loglama (colorlog) yapılandırması mevcut.
Bu, Zapata M6'nın en güncel konfigürasyon modülüdür.

📌 Yapılan Güncellemeler ve Değişiklikler
1️⃣ PDF Metin Çıkarma Güncellemeleri:

extract_text_from_pdf() fonksiyonunda .env dosyasına bağlı olarak pdfplumber, pdfminer veya pymupdf seçimi yapıldı.
Daha önce sabit pdfplumber yöntemi vardı, şimdi dinamik hale getirildi.
PDFMiner ve PyMuPDF desteği eklendi.
2️⃣ Tablo Çıkarma Güncellemeleri:

extract_tables_from_pdf() fonksiyonuna pdfplumber, pymupdf ve pdfminer desteği eklendi.
Önceden yalnızca pdfplumber kullanılıyordu, şimdi kullanıcı seçimine göre çalışıyor.
PymuPDF, sayfa üzerindeki tablo konumlarını algılayabiliyor.
3️⃣ Sayfa Düzeni Algılama (Layout Detection):

LayoutParser ve Detectron2 desteği eklendi.
detect_layout() fonksiyonu 4 farklı yöntemi destekleyecek şekilde genişletildi:
Regex (Varsayılan)
PyMuPDF
LayoutParser
Detectron2 (Geliştirilecek)
4️⃣ Sütunları Tek Sütuna İndirme (Reflow Columns):

reflow_columns() fonksiyonu çok sütunlu PDF'lerde metni düzenli hale getirmek için optimize edildi.
Satır boşluklarını ve yanlış bölünmeleri düzelten algoritma geliştirildi.
Regex yerine daha akıllı satır birleştirme yöntemi eklendi.
📌 Sonuç: ✅ Metin ve tablo çıkarma işlemleri artık daha esnek.
✅ Sayfa düzeni algılama (layout analysis) için yeni yöntemler eklendi.
✅ Sütunları düzgün birleştiren reflow_columns() fonksiyonu optimize edildi.

📌 Yapılan Güncellemeler ve Değişiklikler
1️⃣ Zotero Kaynakça Getirme Güncellemeleri:

Zotero’dan veri çekerken Redis önbellekleme desteği eklendi.
Zotero’ya yapılan gereksiz API istekleri azaltıldı.
Kaynakçalar artık SQLite veritabanına da kaydediliyor.
2️⃣ DOI ile PDF İndirme:

Zotero’da PDF varsa oradan indiriliyor.
Eğer yoksa Sci-Hub üzerinden PDF indirme desteği eklendi.
3️⃣ Kaynakçaları RIS & BibTeX Olarak Kaydetme:

Zotero kaynakçaları .ris ve .bib uzantılı dosyalara kaydedilebiliyor.
RIS ve BibTeX formatı desteklendi.
📌 Sonuç:
✅ Redis önbellekleme ile Zotero API çağrıları optimize edildi.
✅ DOI ile PDF indirme ve Sci-Hub entegrasyonu eklendi.
✅ Kaynakçalar SQLite veritabanına ve RIS/BibTeX dosyalarına kaydediliyor.

📌 Yapılan Güncellemeler ve Değişiklikler
1️⃣ Çoklu Embedding Modeli Desteği:

OpenAI, Contriever ve Specter modelleri destekleniyor.
.env dosyasından model seçimi yapılabiliyor.
2️⃣ ChromaDB ve Redis Entegrasyonu:

ChromaDB, embedding verilerini uzun vadeli saklamak için kullanılıyor.
Redis, sık kullanılan embedding’leri önbelleğe alarak hızlandırıyor.
3️⃣ Embedding’ler SQLite’e de Kaydediliyor:

Daha önce sadece ChromaDB’ye kayıt yapılıyordu, artık SQLite’e de ekleniyor.
4️⃣ Çoklu İşlem Desteği Eklendi:

batch_generate_embeddings() fonksiyonu çoklu işlem (multiprocessing) kullanarak embedding işlemlerini hızlandırıyor.
📌 Sonuç:
✅ ChromaDB + SQLite + Redis entegrasyonu tamamlandı.
✅ Çoklu işlem desteği eklendi.
✅ Alternatif embedding modelleri destekleniyor.


📌 Yapılan Güncellemeler ve Değişiklikler
1️⃣ Yeni Embedding Modelleri:

Contriever (facebook/contriever)
Specter (allenai/specter)
MiniLM (sentence-transformers/all-MiniLM-L6-v2)
.env dosyasından model seçimi yapılabiliyor.
2️⃣ ChromaDB ve Redis Entegrasyonu:

ChromaDB, embedding verilerini uzun vadeli saklamak için kullanılıyor.
Redis, sık kullanılan embedding’leri önbelleğe alarak hızlandırıyor.
3️⃣ Embedding’ler SQLite’e de Kaydediliyor:

Daha önce sadece ChromaDB’ye kayıt yapılıyordu, artık SQLite’e de ekleniyor.
4️⃣ Çoklu İşlem Desteği Eklendi:

batch_generate_embeddings() fonksiyonu çoklu işlem (multiprocessing) kullanarak embedding işlemlerini hızlandırıyor.
📌 Sonuç:
✅ Contriever, Specter ve MiniLM modelleri destekleniyor.
✅ Embedding’ler ChromaDB, Redis ve SQLite’te saklanıyor.
✅ Çoklu işlem desteği eklendi.