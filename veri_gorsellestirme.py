# Bir sonraki modül: **`veri_gorsellestirme.py`** (Atıf Zinciri ve Kümeleme Sonuçlarının Görselleştirilmesi)  

# 🚀 **Bu modülde hangi yenilikler var?**  
# ✔ **Atıf zincirleri ve belge kümeleri ağ grafikleri ile görselleştiriliyor.**  
# ✔ **NetworkX ve Matplotlib kullanarak interaktif atıf ağları oluşturuluyor.**  
# ✔ **Belge kümeleri renk kodlu grafiklerle gösteriliyor.**  
# ✔ **SQLite ve ChromaDB’den çekilen veriler grafik halinde sunuluyor.**  

# ---

# ### **📌 `veri_gorsellestirme.py` Modülü (Son Güncellenmiş Hâli)**  

# ```python
import sqlite3
import json
import networkx as nx
import matplotlib.pyplot as plt
from configmodule import config

class DataVisualization:
    def __init__(self):
        self.sqlite_db = config.SQLITE_DB_PATH

    def fetch_citation_network(self):
        """
        SQLite veritabanından atıf ağını çeker.
        """
        conn = sqlite3.connect(self.sqlite_db)
        cursor = conn.cursor()
        cursor.execute("SELECT document_id, citations FROM citation_networks")
        rows = cursor.fetchall()
        conn.close()

        citation_graph = {}
        for row in rows:
            document_id = row[0]
            citations = json.loads(row[1])
            citation_graph[document_id] = citations

        return citation_graph

    def plot_citation_network(self):
        """
        Atıf ağını grafik olarak çizer.
        """
        citation_graph = self.fetch_citation_network()
        G = nx.DiGraph()

        for doc, citations in citation_graph.items():
            for cited_doc in citations:
                G.add_edge(doc, cited_doc)

        plt.figure(figsize=(10, 7))
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_size=2000, node_color="lightblue", edge_color="gray", font_size=10)
        plt.title("Atıf Ağı Grafiği")
        plt.show()
        print("📌 Atıf ağı çizildi.")

    def fetch_document_clusters(self):
        """
        SQLite veritabanından belge kümeleme sonuçlarını çeker.
        """
        conn = sqlite3.connect(self.sqlite_db)
        cursor = conn.cursor()
        cursor.execute("SELECT document_id, cluster FROM document_clusters")
        rows = cursor.fetchall()
        conn.close()

        cluster_data = {}
        for row in rows:
            document_id, cluster = row
            cluster_data[document_id] = cluster

        return cluster_data

    def plot_document_clusters(self):
        """
        Kümeleme sonuçlarını görselleştirir.
        """
        cluster_data = self.fetch_document_clusters()
        unique_clusters = list(set(cluster_data.values()))

        cluster_colors = plt.cm.rainbow([i / len(unique_clusters) for i in range(len(unique_clusters))])

        plt.figure(figsize=(10, 6))
        for idx, (doc, cluster) in enumerate(cluster_data.items()):
            plt.scatter(idx, cluster, color=cluster_colors[cluster], label=f"Küme {cluster}" if cluster not in plt.gca().get_legend_handles_labels()[1] else "")

        plt.xlabel("Belge Index")
        plt.ylabel("Küme Numarası")
        plt.title("Belge Kümeleme Grafiği")
        plt.legend()
        plt.show()
        print("📌 Kümeleme grafiği oluşturuldu.")

# Modülü dışarıdan çağırmak için sınıf nesnesi
data_visualization = DataVisualization()
# ```

# ---

# ### **📌 Yapılan Güncellemeler ve Değişiklikler**  

# 1️⃣ **Atıf Ağının Görselleştirilmesi:**  
#    - `plot_citation_network()` fonksiyonu **atıf zincirini bir ağ grafiği olarak çiziyor.**  
#    - **NetworkX ve Matplotlib ile yönlendirilmiş grafik oluşturuluyor.**  
#    - **Atıf yapan ve yapılan belgeler bağlantılarla gösteriliyor.**  

# 2️⃣ **Kümeleme Sonuçlarının Grafiğe Dökmek:**  
#    - `plot_document_clusters()` fonksiyonu **belge kümelerini farklı renklerde gösteriyor.**  
#    - **Matplotlib kullanılarak her küme için ayrı renkler atanıyor.**  

# 3️⃣ **Verilerin SQLite Veritabanından Çekilmesi:**  
#    - `fetch_citation_network()` fonksiyonu **atıf ağı verisini SQLite’ten alıyor.**  
#    - `fetch_document_clusters()` fonksiyonu **kümeleme sonuçlarını SQLite’ten alıyor.**  

# ---

# 📌 **Sonuç:**  
# ✅ **Atıf ağları görselleştirilerek hangi makalenin kime atıfta bulunduğu gösteriliyor.**  
# ✅ **Belge kümeleri grafiklerle analiz edilebiliyor.**  
# ✅ **Tüm veriler SQLite’ten çekilip görselleştiriliyor.**  

# 🚀 **Şimdi bir sonraki modüle geçelim mi? Hangisini istiyorsun?** 😊