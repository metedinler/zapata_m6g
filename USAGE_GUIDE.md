# Zapata M6 - Kullanım Kılavuzu ve Örnekler
## Practical Usage Guide & Examples

### 🚀 Hızlı Başlangıç

#### Sistem Gereksinimleri
```bash
# Minimum sistem gereksinimleri
- Python 3.9+
- RAM: 4GB (8GB+ önerilir)
- Disk: 2GB boş alan
- Redis Server (opsiyonel, performans için)
```

#### Kurulum Adımları
```bash
# 1. Repository klonlama
git clone https://github.com/metedinler/zapata_m6g.git
cd zapata_m6g

# 2. Virtual environment oluşturma
python -m venv zapata_env
source zapata_env/bin/activate  # Linux/Mac
# zapata_env\Scripts\activate   # Windows

# 3. Bağımlılıkları yükleme
pip install -r requirements.txt

# 4. .env dosyasını yapılandırma
cp .env.example .env
# .env dosyasını düzenleyin

# 5. Dizin yapısını oluşturma
python -c "from configmodule import config; config.create_directories()"

# 6. Redis başlatma (opsiyonel)
redis-server

# 7. Uygulamayı çalıştırma
python main.py
```

---

## 📖 Kullanım Senaryoları

### 1. Tek PDF Dosyası İşleme

#### GUI Modunda
```python
# .env dosyasında
RUN_MODE=gui

# Çalıştırma
python main.py
```

**GUI Kullanım Adımları:**
1. "PDF Seç" butonuna tıklayın
2. İşlemek istediğiniz PDF dosyasını seçin
3. "İşle" butonuna tıklayın
4. Sonuçları "Sonuçlar" sekmesinde görüntüleyin

#### Console Modunda
```python
# .env dosyasında
RUN_MODE=console

# Çalıştırma
python main.py

# Console menüsünde:
# 1 - PDF İşle seçeneğini seçin
# PDF dosyasının tam yolunu girin
# Örnek: /home/user/documents/makale.pdf
```

#### Programatik Kullanım
```python
from pdfprocessing import PDFProcessor
from sqlite_storage import sqlite_storage

# PDF processor oluştur
processor = PDFProcessor()

# PDF'den metin çıkar
pdf_path = "path/to/your/document.pdf"
clean_text = processor.extract_text_from_pdf(pdf_path)

# Temiz metni veritabanına kaydet
document_id = sqlite_storage.store_clean_text(
    filename="document.pdf",
    content=clean_text,
    metadata={"source": pdf_path, "processed_at": "2024-01-01"}
)

print(f"Document processed and stored with ID: {document_id}")
```

### 2. Toplu PDF İşleme

#### Dizin Tarama
```python
import os
from pathlib import Path
from pdfprocessing import PDFProcessor
from concurrent.futures import ThreadPoolExecutor

class BatchProcessor:
    def __init__(self):
        self.processor = PDFProcessor()
    
    def process_directory(self, directory_path, pattern="*.pdf"):
        """Dizindeki tüm PDF'leri işle"""
        pdf_files = list(Path(directory_path).glob(pattern))
        
        print(f"Bulunan PDF sayısı: {len(pdf_files)}")
        
        results = []
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {
                executor.submit(self.process_single_file, str(pdf)): pdf 
                for pdf in pdf_files
            }
            
            for future in futures:
                try:
                    result = future.result(timeout=300)  # 5 dakika timeout
                    results.append(result)
                    print(f"✅ İşlendi: {futures[future]}")
                except Exception as e:
                    print(f"❌ Hata: {futures[future]} - {e}")
        
        return results
    
    def process_single_file(self, pdf_path):
        """Tek PDF dosyasını işle"""
        text = self.processor.extract_text_from_pdf(pdf_path)
        
        # Metin kalitesi kontrolü
        if len(text.strip()) < 100:
            raise ValueError("Çıkarılan metin çok kısa")
        
        return {
            'file': pdf_path,
            'text_length': len(text),
            'word_count': len(text.split()),
            'status': 'success'
        }

# Kullanım
batch_processor = BatchProcessor()
results = batch_processor.process_directory("/path/to/pdf/directory")

# Sonuçları CSV'ye kaydet
import pandas as pd
df = pd.DataFrame(results)
df.to_csv("batch_processing_results.csv", index=False)
```

### 3. Atıf Analizi ve Haritalama

#### Akademik Makale Atıf Analizi
```python
from citationmappingmodule import CitationMapping
from veri_gorsellestirme import plot_citation_network
import json

# Citation mapper oluştur
citation_mapper = CitationMapping()

# PDF'den atıfları çıkar ve haritalandır
pdf_path = "academic_paper.pdf"
with open("clean_text.txt", "r") as f:
    paper_text = f.read()

# Atıf çıkarma
citations = citation_mapper.extract_references(paper_text)
print(f"Bulunan atıf sayısı: {len(citations)}")

# Atıfları kaynaklarla eşleştir
document_id = "paper_001"
mapping_results = citation_mapper.map_citations_to_references(paper_text, document_id)

# Atıf ağını görselleştir
citation_network = citation_mapper.build_citation_network(document_id)
plot_citation_network(citation_network, save_path="citation_network.png")

# Sonuçları JSON'a kaydet
with open("citation_analysis.json", "w") as f:
    json.dump(mapping_results, f, indent=2, ensure_ascii=False)
```

#### Çoklu Makale Atıf Ağı
```python
class CitationNetworkAnalyzer:
    def __init__(self):
        self.citation_mapper = CitationMapping()
        self.papers_data = {}
    
    def add_paper(self, paper_id, text, metadata=None):
        """Ağa yeni makale ekle"""
        citations = self.citation_mapper.extract_references(text)
        
        self.papers_data[paper_id] = {
            'text': text,
            'citations': citations,
            'metadata': metadata or {},
            'citation_count': len(citations)
        }
    
    def build_network_graph(self):
        """Atıf ağı grafiği oluştur"""
        import networkx as nx
        
        G = nx.DiGraph()
        
        # Düğümleri ekle
        for paper_id, data in self.papers_data.items():
            G.add_node(paper_id, **data['metadata'])
        
        # Kenarları ekle (atıf bağlantıları)
        for citing_paper, data in self.papers_data.items():
            for citation in data['citations']:
                # Citation'ı referans makaleye bağla
                if citation in self.papers_data:
                    G.add_edge(citing_paper, citation)
        
        return G
    
    def analyze_centrality(self):
        """Ağ merkezilik analizi"""
        G = self.build_network_graph()
        
        return {
            'betweenness': nx.betweenness_centrality(G),
            'closeness': nx.closeness_centrality(G),
            'pagerank': nx.pagerank(G),
            'in_degree': dict(G.in_degree()),
            'out_degree': dict(G.out_degree())
        }

# Kullanım örneği
analyzer = CitationNetworkAnalyzer()

# Makaleler ekle
papers = [
    ("paper_1", text_1, {"title": "AI in Medicine", "year": 2023}),
    ("paper_2", text_2, {"title": "ML Applications", "year": 2022}),
    ("paper_3", text_3, {"title": "Deep Learning Review", "year": 2024})
]

for paper_id, text, metadata in papers:
    analyzer.add_paper(paper_id, text, metadata)

# Ağ analizi
centrality_metrics = analyzer.analyze_centrality()
print("En etkili makaleler (PageRank):", 
      sorted(centrality_metrics['pagerank'].items(), 
             key=lambda x: x[1], reverse=True)[:5])
```

### 4. AI Model Eğitimi ve Embedding

#### Custom Model Fine-tuning
```python
from yapay_zeka_finetuning import FineTuner
from sklearn.model_selection import train_test_split

# Fine-tuner oluştur
fine_tuner = FineTuner()

# Eğitim verilerini hazırla
training_texts = []
labels = []

# SQLite'den veri al
conn = sqlite3.connect("data/zapata_m6.sqlite")
cursor = conn.cursor()

cursor.execute("SELECT content, category FROM clean_texts WHERE category IS NOT NULL")
data = cursor.fetchall()

for content, category in data:
    training_texts.append(content)
    labels.append(category)

# Veriyi böl
train_texts, val_texts, train_labels, val_labels = train_test_split(
    training_texts, labels, test_size=0.2, random_state=42
)

# Model eğit
training_config = {
    'model_name': 'bert-base-uncased',
    'num_epochs': 3,
    'batch_size': 16,
    'learning_rate': 2e-5,
    'output_dir': 'models/custom_classifier'
}

fine_tuner.train_classification_model(
    train_texts=train_texts,
    train_labels=train_labels,
    val_texts=val_texts,
    val_labels=val_labels,
    config=training_config
)

# Eğitilen modeli test et
test_text = "This paper discusses machine learning applications in healthcare."
prediction = fine_tuner.predict(test_text)
print(f"Predicted category: {prediction}")
```

#### Embedding Generation ve Similarity Search
```python
from embeddingmodule import EmbeddingModule
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Embedding module oluştur
embedding_module = EmbeddingModule()

# Metin koleksiyonu
documents = [
    "Artificial intelligence in medical diagnosis",
    "Machine learning for drug discovery",
    "Deep learning applications in healthcare",
    "Natural language processing in clinical text",
    "Computer vision for medical imaging"
]

# Embeddings oluştur
embeddings = []
for doc in documents:
    embedding = embedding_module.generate_embedding(doc)
    embeddings.append(embedding)
    
    # ChromaDB'ye kaydet
    embedding_module.save_embedding_to_chromadb(
        text=doc,
        embedding=embedding,
        metadata={"domain": "healthcare"}
    )

# Similarity search
query = "AI applications in medicine"
query_embedding = embedding_module.generate_embedding(query)

# Cosine similarity hesapla
similarities = cosine_similarity(
    [query_embedding], 
    embeddings
)[0]

# En benzer dokümanları bul
top_matches = np.argsort(similarities)[::-1][:3]

print("En benzer dokümanlar:")
for i, idx in enumerate(top_matches):
    print(f"{i+1}. {documents[idx]} (similarity: {similarities[idx]:.3f})")
```

### 5. Zotero Entegrasyonu

#### Zotero'dan Kaynakça Çekme
```python
from zoteromodule import ZoteroModule

# Zotero module oluştur (.env'de API key olmalı)
zotero = ZoteroModule()

# Kütüphaneden tüm kaynakçaları çek
references = zotero.fetch_references_from_zotero(limit=100)

print(f"Çekilen kaynakça sayısı: {len(references)}")

# Kaynakçaları farklı formatlarda kaydet
zotero.save_references(references, format="ris", filename="library.ris")
zotero.save_references(references, format="bibtex", filename="library.bib")
zotero.save_references(references, format="csv", filename="library.csv")

# DOI ile PDF indirme
for ref in references:
    if 'DOI' in ref:
        try:
            pdf_path = zotero.download_pdf_from_doi(
                ref['DOI'], 
                save_directory="downloaded_pdfs"
            )
            print(f"PDF indirildi: {pdf_path}")
        except Exception as e:
            print(f"PDF indirilemedi {ref['DOI']}: {e}")
```

#### Otomatik Kaynakça Güncelleme
```python
import schedule
import time

class AutoZoteroUpdater:
    def __init__(self):
        self.zotero = ZoteroModule()
        self.last_update = None
    
    def update_library(self):
        """Kütüphaneyi otomatik güncelle"""
        try:
            # Yeni referansları çek
            new_refs = self.zotero.fetch_references_from_zotero(
                since=self.last_update
            )
            
            if new_refs:
                print(f"Yeni kaynakça bulundu: {len(new_refs)}")
                
                # Her yeni kaynak için PDF indir ve işle
                for ref in new_refs:
                    self.process_new_reference(ref)
                
                self.last_update = time.time()
            else:
                print("Yeni kaynakça bulunamadı")
                
        except Exception as e:
            print(f"Güncelleme hatası: {e}")
    
    def process_new_reference(self, reference):
        """Yeni kaynakçayı işle"""
        # PDF varsa indir
        if 'DOI' in reference:
            try:
                pdf_path = self.zotero.download_pdf_from_doi(reference['DOI'])
                
                # PDF'i işle
                processor = PDFProcessor()
                text = processor.extract_text_from_pdf(pdf_path)
                
                # Veritabanına kaydet
                sqlite_storage.store_clean_text(
                    filename=f"{reference.get('title', 'unknown')}.pdf",
                    content=text,
                    metadata=reference
                )
                
                print(f"✅ İşlendi: {reference.get('title')}")
                
            except Exception as e:
                print(f"❌ İşlenemedi: {reference.get('title')} - {e}")

# Scheduler kurulumu
updater = AutoZoteroUpdater()

# Her 6 saatte bir güncelle
schedule.every(6).hours.do(updater.update_library)

# Schedule loop
while True:
    schedule.run_pending()
    time.sleep(3600)  # 1 saat bekle
```

---

## 📊 Veri Görselleştirme Örnekleri

### 1. Citation Network Grafiği
```python
from veri_gorsellestirme import VisualizationModule
import matplotlib.pyplot as plt
import networkx as nx

# Görselleştirme modülü
viz = VisualizationModule()

# Citation network oluştur
G = nx.DiGraph()

# Örnek veri ekle
papers = {
    'P1': {'title': 'AI Fundamentals', 'year': 2020},
    'P2': {'title': 'ML Applications', 'year': 2021},
    'P3': {'title': 'Deep Learning', 'year': 2022},
    'P4': {'title': 'NLP Review', 'year': 2023}
}

# Düğümler ve bağlantılar ekle
for paper_id, data in papers.items():
    G.add_node(paper_id, **data)

citations = [('P2', 'P1'), ('P3', 'P1'), ('P3', 'P2'), ('P4', 'P1'), ('P4', 'P3')]
G.add_edges_from(citations)

# İnteraktif görselleştirme
viz.plot_interactive_citation_network(
    G, 
    save_path="interactive_network.html",
    node_size_metric='year',
    color_metric='year'
)

# Statik network grafiği
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G, k=2, iterations=50)

# Düğüm boyutları (atıf sayısına göre)
node_sizes = [300 + G.in_degree(node) * 100 for node in G.nodes()]

# Düğüm renkleri (yıla göre)
node_colors = [papers[node]['year'] for node in G.nodes()]

nx.draw(G, pos, 
        node_size=node_sizes,
        node_color=node_colors,
        cmap='viridis',
        with_labels=True,
        arrows=True,
        arrowsize=20,
        font_size=10,
        font_weight='bold')

plt.colorbar(plt.cm.ScalarMappable(cmap='viridis'), 
             label='Publication Year')
plt.title('Academic Citation Network')
plt.savefig('citation_network.png', dpi=300, bbox_inches='tight')
plt.show()
```

### 2. Embedding Clustering Görselleştirmesi
```python
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np

# Embedding verilerini al
embeddings = []
labels = []
texts = []

# ChromaDB'den embedding'leri çek
collection = embedding_module.chroma_client.get_collection("documents")
results = collection.get(include=['embeddings', 'metadatas', 'documents'])

embeddings = np.array(results['embeddings'])
texts = results['documents']
labels = [meta.get('category', 'unknown') for meta in results['metadatas']]

# K-means clustering
kmeans = KMeans(n_clusters=5, random_state=42)
cluster_labels = kmeans.fit_predict(embeddings)

# t-SNE dimensionality reduction
tsne = TSNE(n_components=2, random_state=42, perplexity=30)
embeddings_2d = tsne.fit_transform(embeddings)

# Görselleştirme
plt.figure(figsize=(15, 10))

# Scatter plot
scatter = plt.scatter(embeddings_2d[:, 0], embeddings_2d[:, 1], 
                     c=cluster_labels, cmap='tab10', alpha=0.7, s=50)

# Cluster merkezlerini göster
centers_2d = tsne.transform(kmeans.cluster_centers_)
plt.scatter(centers_2d[:, 0], centers_2d[:, 1], 
           marker='x', s=200, linewidths=3, color='red', label='Centroids')

# Labels ekle
for i, txt in enumerate(texts[:20]):  # İlk 20 metin için
    plt.annotate(txt[:30] + '...', 
                (embeddings_2d[i, 0], embeddings_2d[i, 1]),
                xytext=(5, 5), textcoords='offset points',
                fontsize=8, alpha=0.7)

plt.colorbar(scatter, label='Cluster')
plt.title('Document Embedding Clusters (t-SNE Visualization)')
plt.xlabel('t-SNE Component 1')
plt.ylabel('t-SNE Component 2')
plt.legend()
plt.savefig('embedding_clusters.png', dpi=300, bbox_inches='tight')
plt.show()
```

---

## 🔧 Troubleshooting (Sorun Giderme)

### Yaygın Hatalar ve Çözümleri

#### 1. PDF İşleme Hataları
```python
# Hata: "PDF file is corrupted"
# Çözüm: Farklı extraction method dene
try:
    text = processor.extract_text_from_pdf("document.pdf")
except PDFProcessingError:
    # pdfminer ile dene
    processor.text_extraction_method = "pdfminer"
    text = processor.extract_text_from_pdf("document.pdf")
```

#### 2. Memory Hatası
```python
# Hata: MemoryError during large PDF processing
# Çözüm: Streaming processing kullan
def process_large_pdf_safely(pdf_path):
    try:
        return processor.extract_text_from_pdf(pdf_path)
    except MemoryError:
        # Sayfa sayfa işle
        return processor.extract_text_streaming(pdf_path)
```

#### 3. Redis Bağlantı Hatası
```python
# Hata: Redis connection failed
# Çözüm: Offline mode'a geç
class ResilientRedisClient:
    def __init__(self, host, port):
        try:
            self.redis = redis.Redis(host=host, port=port)
            self.redis.ping()
            self.connected = True
        except:
            print("Redis bağlantısı başarısız, offline modda çalışıyor")
            self.connected = False
    
    def get(self, key):
        if self.connected:
            try:
                return self.redis.get(key)
            except:
                self.connected = False
        return None
    
    def set(self, key, value, ex=None):
        if self.connected:
            try:
                return self.redis.set(key, value, ex=ex)
            except:
                self.connected = False
        return False
```

#### 4. ChromaDB Hatası
```python
# Hata: ChromaDB collection not found
# Çözüm: Collection'ı otomatik oluştur
def get_or_create_collection(client, name):
    try:
        return client.get_collection(name)
    except:
        return client.create_collection(name)

# Kullanım
collection = get_or_create_collection(chroma_client, "documents")
```

### Performance Monitoring

```python
import time
import psutil
import logging

class PerformanceMonitor:
    def __init__(self):
        self.start_time = None
        self.peak_memory = 0
    
    def __enter__(self):
        self.start_time = time.time()
        self.start_memory = psutil.Process().memory_info().rss
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        end_time = time.time()
        end_memory = psutil.Process().memory_info().rss
        
        duration = end_time - self.start_time
        memory_used = (end_memory - self.start_memory) / 1024 / 1024  # MB
        
        logging.info(f"İşlem süresi: {duration:.2f} saniye")
        logging.info(f"Bellek kullanımı: {memory_used:.2f} MB")
        
        if duration > 30:
            logging.warning("İşlem 30 saniyeden uzun sürdü")
        if memory_used > 500:
            logging.warning("Bellek kullanımı 500MB'ı aştı")

# Kullanım
with PerformanceMonitor():
    result = processor.extract_text_from_pdf("large_document.pdf")
```

---

## 📚 API Referansı

### PDFProcessor Sınıfı
```python
class PDFProcessor:
    """PDF işleme için ana sınıf"""
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        PDF'den metin çıkarır
        
        Args:
            pdf_path: PDF dosyasının yolu
            
        Returns:
            Çıkarılan metin
            
        Raises:
            PDFProcessingError: İşleme hatası
            FileNotFoundError: Dosya bulunamadı
        """
        
    def extract_tables_from_pdf(self, pdf_path: str) -> List[Dict]:
        """
        PDF'den tabloları çıkarır
        
        Returns:
            Tablo verilerinin listesi
        """
        
    def detect_layout(self, pdf_path: str) -> Dict:
        """
        PDF layout analizini yapar
        
        Returns:
            Layout bilgileri
        """
```

### EmbeddingModule Sınıfı
```python
class EmbeddingModule:
    """Metin embedding işlemleri"""
    
    def generate_embedding(self, text: str) -> List[float]:
        """
        Metin için embedding oluşturur
        
        Args:
            text: İşlenecek metin
            
        Returns:
            Embedding vektörü
        """
        
    def batch_generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Toplu embedding oluşturma
        
        Args:
            texts: Metin listesi
            
        Returns:
            Embedding listesi
        """
```

---

## 🎯 Sonuç ve Öneriler

Zapata M6, **akademik araştırma** ve **bilimsel metin analizi** için kapsamlı bir araç seti sunar. Bu kılavuzda sunulan örnekler, sistemin **gerçek dünya kullanım senaryolarını** kapsar.

### En İyi Pratikler:
1. **Küçük başlayın**: Tek PDF ile test edin
2. **Batch processing**: Büyük veri setleri için paralel işlem kullanın
3. **Error handling**: Her zaman hata yakalama mekanizması ekleyin
4. **Monitoring**: Performans ve bellek kullanımını takip edin
5. **Backup**: Önemli verileri düzenli yedekleyin

### Gelecek Geliştirmeler:
- **Web API**: RESTful API endpoints
- **Cloud Support**: AWS/Azure entegrasyonu
- **Real-time Processing**: WebSocket desteği
- **Advanced Analytics**: Dashboard ve raporlama

Bu sistem ile akademik araştırma süreçlerinizi **%80+** hızlandırabilir ve **manuel işlemleri minimize** edebilirsiniz. 🚀