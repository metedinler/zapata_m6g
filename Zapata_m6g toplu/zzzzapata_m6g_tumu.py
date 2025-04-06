# zapatam6g tarafından paylaşılan tüm modüllerin birleşimi
# Bu dosya, zzzzapata_m6g_tumu.py dosyasına dönüştürülecektir.
#------
# config_module.py
#------


import os
import logging
import colorlog
from pathlib import Path
from dotenv import load_dotenv
import chromadb

class Config:
    def __init__(self):
        # .env dosyasını yükle
        load_dotenv()

        # Dizin Ayarları
        self.KAYNAK_DIZIN = os.getenv("KAYNAK_DIZIN", r"C:\Users\mete\Zotero\zotai")
        self.STORAGE_DIR = Path(os.getenv("STORAGE_DIR", r"C:\Users\mete\Zotero\storage"))
        self.SUCCESS_DIR = Path(os.getenv("SUCCESS_DIR", r"C:\Users\mete\Zotero\zotasistan"))
        self.HEDEF_DIZIN = Path(os.getenv("HEDEF_DIZIN", os.path.join(str(self.KAYNAK_DIZIN), "TemizMetin")))
        self.TEMIZ_TABLO_DIZIN = Path(os.getenv("TEMIZ_TABLO_DIZIN", os.path.join(str(self.KAYNAK_DIZIN), "TemizTablo")))
        self.TEMIZ_KAYNAKCA_DIZIN = Path(os.getenv("TEMIZ_KAYNAKCA_DIZIN", os.path.join(str(self.KAYNAK_DIZIN), "TemizKaynakca")))
        self.PDF_DIR = Path(os.getenv("PDF_DIR", str(self.SUCCESS_DIR) + "/pdfler"))
        self.EMBEDDING_PARCA_DIR = Path(os.getenv("EMBEDDING_PARCA_DIZIN", str(self.SUCCESS_DIR) + "/embedingparca"))
        self.CITATIONS_DIR = Path(os.getenv("CITATIONS_DIR", r"C:\Users\mete\Zotero\zotasistan\citations"))
        self.TABLES_DIR = Path(os.getenv("TABLES_DIR", os.path.join(str(self.KAYNAK_DIZIN), "TemizTablo")))
        self.CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", r"C:\Users\mete\Zotero\zotasistan\chroma_db")

        # API Ayarları
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your_openai_api_key")
        self.ZOTERO_API_KEY = os.getenv("ZOTERO_API_KEY", "your_zotero_api_key")
        self.ZOTERO_USER_ID = os.getenv("ZOTERO_USER_ID", "your_zotero_user_id")
        self.ZOTERO_API_URL = f"https://api.zotero.org/users/{self.ZOTERO_USER_ID}/items"

        # PDF İşleme Ayarları
        self.PDF_TEXT_EXTRACTION_METHOD = os.getenv("PDF_TEXT_EXTRACTION_METHOD", "pdfplumber").lower()
        self.TABLE_EXTRACTION_METHOD = os.getenv("TABLE_EXTRACTION_METHOD", "pymupdf").lower()
        self.COLUMN_DETECTION = os.getenv("COLUMN_DETECTION", "True").lower() == "true"

        # Embedding & NLP Ayarları
        self.EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002")
        self.CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "256"))
        self.PARAGRAPH_BASED_SPLIT = os.getenv("PARAGRAPH_BASED_SPLIT", "True").lower() == "true"
        self.MULTI_PROCESSING = os.getenv("MULTI_PROCESSING", "True").lower() == "true"
        self.MAX_WORKERS = int(os.getenv("MAX_WORKERS", "4"))

        # Citation Mapping & Analiz Ayarları
        self.ENABLE_CITATION_MAPPING = os.getenv("ENABLE_CITATION_MAPPING", "True").lower() == "true"
        self.ENABLE_TABLE_EXTRACTION = os.getenv("ENABLE_TABLE_EXTRACTION", "True").lower() == "true"
        self.ENABLE_CLUSTERING = os.getenv("ENABLE_CLUSTERING", "True").lower() == "true"

        # Loglama & Debug Ayarları
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")
        self.ENABLE_ERROR_LOGGING = os.getenv("ENABLE_ERROR_LOGGING", "True").lower() == "true"
        self.DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"

        # Çalışma Modu Seçimi
        self.RUN_MODE = os.getenv("RUN_MODE", os.getenv("runGUI", "gui")).lower()

        # Veritabanı Ayarları (SQLite ve Redis)
        self.USE_SQLITE = os.getenv("USE_SQLITE", "True").lower() == "true"
        self.SQLITE_DB_PATH = os.getenv("SQLITE_DB_PATH", str(self.SUCCESS_DIR) + "/database.db")
        self.REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
        self.REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

        # Layout Detection Yöntemi
        self.LAYOUT_DETECTION_METHOD = os.getenv("LAYOUT_DETECTION_METHOD", "regex").lower()
        # Alternatifler: regex, pymupdf, layoutparser, detectron2

        # Gerekli dizinleri oluştur
        self.ensure_directories()

        # Loglama sistemini başlat
        self.setup_logging()

        # ChromaDB bağlantısını oluştur
        self.chroma_client = chromadb.PersistentClient(path=self.CHROMA_DB_PATH)

    def ensure_directories(self):
        directories = [
            self.PDF_DIR,
            self.EMBEDDING_PARCA_DIR,
            self.HEDEF_DIZIN,
            self.TEMIZ_TABLO_DIZIN,
            self.TEMIZ_KAYNAKCA_DIZIN,
            self.CITATIONS_DIR,
            self.TABLES_DIR,
        ]
        for directory in directories:
            if not directory.exists():
                try:
                    directory.mkdir(parents=True, exist_ok=True)
                    self.logger.info(f"✅ {directory} dizini oluşturuldu.")
                except Exception as e:
                    self.logger.error(f"❌ {directory} dizini oluşturulamadı: {e}")

    def setup_logging(self):
        log_formatter = colorlog.ColoredFormatter(
            "%(log_color)s%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',
            }
        )
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_formatter)
        file_handler = logging.FileHandler("pdf_processing.log", encoding="utf-8")
        file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(getattr(logging, self.LOG_LEVEL.upper(), logging.DEBUG))
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

    def get_env_variable(self, var_name, default=None):
        return os.getenv(var_name, default)

    def get_max_workers(self):
        return self.MAX_WORKERS

# Global configuration object
config = Config()

#------
# pdfprocessing_module.py
#------

import pdfplumber
import fitz  # PyMuPDF
import pdfminer
import layoutparser as lp
import re
import os
from configmodule import config

class PDFProcessor:
    def __init__(self):
        self.text_extraction_method = config.PDF_TEXT_EXTRACTION_METHOD
        self.table_extraction_method = config.TABLE_EXTRACTION_METHOD
        self.layout_detection_method = config.LAYOUT_DETECTION_METHOD

    def extract_text_from_pdf(self, pdf_path):
        """
        PDF'den metin çıkarma işlemi. Kullanıcı tarafından belirlenen yönteme göre çalışır.
        Varsayılan: pdfplumber, Alternatifler: pdfminer, pymupdf
        """
        if self.text_extraction_method == "pdfplumber":
            return self._extract_text_pdfplumber(pdf_path)
        elif self.text_extraction_method == "pdfminer":
            return self._extract_text_pdfminer(pdf_path)
        elif self.text_extraction_method == "pymupdf":
            return self._extract_text_pymupdf(pdf_path)
        else:
            raise ValueError(f"Bilinmeyen metin çıkarma yöntemi: {self.text_extraction_method}")

    def _extract_text_pdfplumber(self, pdf_path):
        with pdfplumber.open(pdf_path) as pdf:
            text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
        return text

    def _extract_text_pdfminer(self, pdf_path):
        # PDFMiner ile metin çıkarma işlemi
        pass  # Geliştirilecek

    def _extract_text_pymupdf(self, pdf_path):
        doc = fitz.open(pdf_path)
        text = "\n".join([page.get_text("text") for page in doc])
        return text

    def extract_tables_from_pdf(self, pdf_path):
        """
        PDF'den tablo çıkarma işlemi. Kullanıcı tarafından belirlenen yönteme göre çalışır.
        Varsayılan: pymupdf, Alternatifler: pdfplumber, pdfminer
        """
        if self.table_extraction_method == "pymupdf":
            return self._extract_tables_pymupdf(pdf_path)
        elif self.table_extraction_method == "pdfplumber":
            return self._extract_tables_pdfplumber(pdf_path)
        elif self.table_extraction_method == "pdfminer":
            return self._extract_tables_pdfminer(pdf_path)
        else:
            raise ValueError(f"Bilinmeyen tablo çıkarma yöntemi: {self.table_extraction_method}")

    def _extract_tables_pymupdf(self, pdf_path):
        doc = fitz.open(pdf_path)
        tables = []
        for page in doc:
            tables.append(page.find_tables())
        return tables

    def _extract_tables_pdfplumber(self, pdf_path):
        with pdfplumber.open(pdf_path) as pdf:
            tables = [page.extract_table() for page in pdf.pages if page.extract_table()]
        return tables

    def _extract_tables_pdfminer(self, pdf_path):
        # PDFMiner ile tablo çıkarma işlemi
        pass  # Geliştirilecek

    def detect_layout(self, pdf_path):
        """
        PDF sayfa düzenini algılar. Varsayılan: regex, Alternatifler: pymupdf, layoutparser, detectron2
        """
        if self.layout_detection_method == "regex":
            return self._detect_layout_regex(pdf_path)
        elif self.layout_detection_method == "pymupdf":
            return self._detect_layout_pymupdf(pdf_path)
        elif self.layout_detection_method == "layoutparser":
            return self._detect_layout_layoutparser(pdf_path)
        elif self.layout_detection_method == "detectron2":
            return self._detect_layout_detectron2(pdf_path)
        else:
            raise ValueError(f"Bilinmeyen layout analiz yöntemi: {self.layout_detection_method}")

    def _detect_layout_regex(self, pdf_path):
        text = self.extract_text_from_pdf(pdf_path)
        layout = {"headers": re.findall(r'(?m)^\s*[A-Z][A-Za-z\s]+\s*$', text)}
        return layout

    def _detect_layout_pymupdf(self, pdf_path):
        doc = fitz.open(pdf_path)
        layout = []
        for page in doc:
            layout.append({"page": page.number, "blocks": page.get_text("blocks")})
        return layout

    def _detect_layout_layoutparser(self, pdf_path):
        doc = fitz.open(pdf_path)
        layout = []
        model = lp.Detectron2LayoutModel("lp://PubLayNet/faster_rcnn_R_50_FPN_3x/config")
        for page in doc:
            image = page.get_pixmap()
            detected = model.detect(image)
            layout.append(detected)
        return layout

    def _detect_layout_detectron2(self, pdf_path):
        # Detectron2 ile layout analizi işlemi
        pass  # Geliştirilecek

    def reflow_columns(self, text):
        """
        Çok sütunlu makalelerde metni düzene sokar ve tek sütuna indirger.
        """
        lines = text.split("\n")
        refined_text = []
        for line in lines:
            if len(line.strip()) > 3:
                refined_text.append(line.strip())
        return " ".join(refined_text)


#------
# zotero_module.py
#------

import requests
import json
import os
import redis
import sqlite3
from configmodule import config

class ZoteroModule:
    def __init__(self):
        self.api_key = config.ZOTERO_API_KEY
        self.user_id = config.ZOTERO_USER_ID
        self.api_url = f"https://api.zotero.org/users/{self.user_id}/items"
        self.redis_client = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, decode_responses=True)
        self.sqlite_db = config.SQLITE_DB_PATH

    def fetch_references_from_zotero(self, query=""):
        """
        Zotero'dan kaynakça verilerini çeker. Daha önce Redis önbelleğinde varsa oradan alır.
        """
        cache_key = f"zotero_refs:{query}"
        cached_data = self.redis_client.get(cache_key)

        if cached_data:
            print("📌 Zotero verileri Redis önbelleğinden alındı.")
            return json.loads(cached_data)

        headers = {"Zotero-API-Key": self.api_key, "Accept": "application/json"}
        params = {"q": query, "limit": 100}

        response = requests.get(self.api_url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            self.redis_client.setex(cache_key, 3600, json.dumps(data))  # 1 saatlik önbellek
            return data
        else:
            print(f"❌ Zotero API hatası: {response.status_code}")
            return None

    def download_pdf_from_doi(self, doi):
        """
        DOI kullanarak PDF indirir. Önce Zotero'dan kontrol eder, yoksa Sci-Hub üzerinden indirir.
        """
        pdf_path = f"{config.PDF_DIR}/{doi.replace('/', '_')}.pdf"

        if os.path.exists(pdf_path):
            print(f"✅ PDF zaten mevcut: {pdf_path}")
            return pdf_path

        # Zotero'dan PDF kontrolü
        zotero_refs = self.fetch_references_from_zotero(doi)
        for ref in zotero_refs:
            if 'links' in ref and 'enclosure' in ref['links']:
                pdf_url = ref['links']['enclosure']['href']
                return self._download_file(pdf_url, pdf_path)

        # Sci-Hub üzerinden indirme (alternatif)
        sci_hub_url = f"https://sci-hub.se/{doi}"
        return self._download_file(sci_hub_url, pdf_path)

    def _download_file(self, url, save_path):
        """
        Belirtilen URL’den dosya indirir ve kaydeder.
        """
        try:
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                with open(save_path, "wb") as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)
                print(f"✅ PDF indirildi: {save_path}")
                return save_path
        except Exception as e:
            print(f"❌ PDF indirme hatası: {e}")
        return None

    def save_references_to_sqlite(self, references):
        """
        Zotero’dan gelen kaynakçaları SQLite veritabanına kaydeder.
        """
        conn = sqlite3.connect(self.sqlite_db)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bibliography (
                id TEXT PRIMARY KEY,
                title TEXT,
                authors TEXT,
                year INTEGER,
                citation_key TEXT
            )
        """)

        for ref in references:
            ref_id = ref.get("key", "")
            title = ref.get("data", {}).get("title", "Bilinmeyen Başlık")
            authors = ", ".join([author.get("lastName", "") for author in ref.get("data", {}).get("creators", [])])
            year = ref.get("data", {}).get("date", "Bilinmeyen Yıl")[:4]
            citation_key = ref.get("data", {}).get("citationKey", "")

            cursor.execute("INSERT OR IGNORE INTO bibliography VALUES (?, ?, ?, ?, ?)", (ref_id, title, authors, year, citation_key))

        conn.commit()
        conn.close()
        print("📌 Zotero kaynakçaları SQLite veritabanına kaydedildi.")

    def save_references_to_file(self, references, format="ris"):
        """
        Zotero kaynakçalarını RIS veya BibTeX formatında kaydeder.
        """
        output_dir = config.TEMIZ_KAYNAKCA_DIZIN
        os.makedirs(output_dir, exist_ok=True)

        file_path = os.path.join(output_dir, f"zotero_references.{format}")
        with open(file_path, "w", encoding="utf-8") as file:
            if format == "ris":
                for ref in references:
                    file.write(self._convert_to_ris(ref))
            elif format == "bib":
                for ref in references:
                    file.write(self._convert_to_bibtex(ref))

        print(f"📌 Zotero kaynakçaları {format.upper()} formatında kaydedildi: {file_path}")

    def _convert_to_ris(self, ref):
        """
        Zotero kaynağını RIS formatına çevirir.
        """
        ris_template = f"""
        TY  - JOUR
        TI  - {ref.get('data', {}).get('title', '')}
        AU  - {', '.join([author.get("lastName", "") for author in ref.get("data", {}).get("creators", [])])}
        PY  - {ref.get('data', {}).get('date', '')[:4]}
        ID  - {ref.get('key', '')}
        ER  - 
        """
        return ris_template

    def _convert_to_bibtex(self, ref):
        """
        Zotero kaynağını BibTeX formatına çevirir.
        """
        bib_template = f"""
        @article{{{ref.get('key', '')},
            title={{ {ref.get('data', {}).get('title', '')} }},
            author={{ {', '.join([author.get("lastName", "") for author in ref.get('data', {}).get("creators", [])])} }},
            year={{ {ref.get('data', {}).get('date', '')[:4]} }}
        }}
        """
        return bib_template


# Modülü dışarıdan çağırmak için sınıf nesnesi
zotero_module = ZoteroModule()

#------
# embedding_module.py
#------
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

#------
# alternative_embeding_module.py
#------ 
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

#------
# citationmapping_module.py
#------
import re
import json
import sqlite3
import chromadb
import redis
import os
from configmodule import config
from concurrent.futures import ProcessPoolExecutor

class CitationMapping:
    def __init__(self):
        self.chroma_client = chromadb.PersistentClient(path=config.CHROMA_DB_PATH)
        self.redis_client = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, decode_responses=True)
        self.sqlite_db = config.SQLITE_DB_PATH
        self.citation_regex = r"\((.*?)\)"  # Atıfları yakalamak için regex
        self.max_workers = config.MAX_WORKERS
        self.citation_dir = config.CITATIONS_DIR

    def extract_references(self, text):
        """
        Ham metindeki atıfları regex kullanarak tespit eder.
        """
        return re.findall(self.citation_regex, text)

    def map_citations_to_references(self, text, document_id):
        """
        Metindeki atıfları kaynakçalarla eşleştirir ve veritabanına kaydeder.
        """
        atiflar = self.extract_references(text)
        matched_citations = []

        conn = sqlite3.connect(self.sqlite_db)
        cursor = conn.cursor()

        for citation in atiflar:
            cursor.execute("SELECT id, title, authors FROM bibliography WHERE citation_key=?", (citation,))
            result = cursor.fetchone()
            if result:
                matched_citations.append({"citation": citation, "source": result})

        conn.close()

        self.save_citations_to_chromadb(document_id, matched_citations)
        self.save_citations_to_sqlite(document_id, matched_citations)
        self.save_citations_to_json(document_id, matched_citations)

        return matched_citations

    def save_citations_to_chromadb(self, document_id, citations):
        """
        Eşleşen atıfları ChromaDB'ye kaydeder.
        """
        collection = self.chroma_client.get_collection(name="citations")
        for match in citations:
            collection.add(
                documents=[match["citation"]],
                metadatas=[{"source": match["source"], "document_id": document_id}],
                ids=[f"{document_id}_{match['source'][0]}"]
            )
        self.redis_client.setex(f"citations:{document_id}", 3600, json.dumps(citations))  # Redis önbelleğe alma

    def save_citations_to_sqlite(self, document_id, citations):
        """
        Eşleşen atıfları SQLite veritabanına kaydeder.
        """
        conn = sqlite3.connect(self.sqlite_db)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS citation_mappings (
                document_id TEXT,
                citation TEXT,
                source_id TEXT,
                PRIMARY KEY (document_id, citation)
            )
        """)

        for match in citations:
            cursor.execute("INSERT OR IGNORE INTO citation_mappings VALUES (?, ?, ?)", 
                           (document_id, match["citation"], match["source"][0]))

        conn.commit()
        conn.close()
        print(f"📌 Atıf eşleştirmeleri SQLite veritabanına kaydedildi: {document_id}")

    def save_citations_to_json(self, document_id, citations):
        """
        Her PDF için eşleşen atıfları JSON formatında kaydeder.
        """
        os.makedirs(self.citation_dir, exist_ok=True)
        json_filename = os.path.join(self.citation_dir, f"{document_id}.citations.json")
        
        with open(json_filename, "w", encoding="utf-8") as json_file:
            json.dump(citations, json_file, indent=4, ensure_ascii=False)

        print(f"📌 Atıf eşleştirmeleri JSON dosyasına kaydedildi: {json_filename}")

    def batch_process_citations(self, text_document_pairs):
        """
        Çoklu işlem desteği ile büyük veri kümelerinde atıf eşleştirme sürecini hızlandırır.
        """
        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            results = executor.map(lambda pair: self.map_citations_to_references(pair[0], pair[1]), text_document_pairs)
        return list(results)


# Modülü dışarıdan çağırmak için sınıf nesnesi
citation_mapping = CitationMapping()

#------
# clustering_module.py
#------
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

#------
# robust_embeding_module.py
#------
import chromadb
import redis
import sqlite3
import json
import os
import numpy as np
from sentence_transformers import SentenceTransformer
from concurrent.futures import ProcessPoolExecutor
from configmodule import config

class RobustEmbeddingModule:
    def __init__(self):
        self.embedding_model = config.EMBEDDING_MODEL
        self.chroma_client = chromadb.PersistentClient(path=config.CHROMA_DB_PATH)
        self.redis_client = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, decode_responses=True)
        self.sqlite_db = config.SQLITE_DB_PATH
        self.max_workers = config.MAX_WORKERS

        # Alternatif embedding modelleri
        self.models = {
            "bert": SentenceTransformer("bert-base-nli-mean-tokens"),
            "minilm": SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2"),
            "roberta": SentenceTransformer("roberta-base-nli-stsb-mean-tokens")
        }

    def generate_embedding(self, text):
        """
        Hata toleranslı embedding oluşturma işlemi.
        """
        try:
            if self.embedding_model in self.models:
                model = self.models[self.embedding_model]
                return model.encode(text).tolist()
            else:
                raise ValueError(f"Bilinmeyen embedding modeli: {self.embedding_model}")
        except Exception as e:
            print(f"❌ Embedding oluşturulamadı: {e}")
            return np.zeros(768).tolist()  # Boş embedding döndür (hata toleransı)

    def save_embedding_to_chromadb(self, document_id, text):
        """
        Embedding’leri ChromaDB’ye kaydeder.
        """
        embedding = self.generate_embedding(text)
        if embedding:
            collection = self.chroma_client.get_collection(name="robust_embeddings")
            collection.add(
                documents=[text],
                metadatas=[{"document_id": document_id}],
                ids=[f"{document_id}"]
            )
            self.redis_client.setex(f"robust_embedding:{document_id}", 3600, json.dumps(embedding))  # Redis önbelleğe alma
            self.save_embedding_to_sqlite(document_id, embedding)

    def save_embedding_to_sqlite(self, document_id, embedding):
        """
        Embedding’leri SQLite veritabanına kaydeder.
        """
        conn = sqlite3.connect(self.sqlite_db)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS robust_embeddings (
                document_id TEXT PRIMARY KEY,
                embedding TEXT
            )
        """)

        cursor.execute("INSERT OR REPLACE INTO robust_embeddings VALUES (?, ?)", (document_id, json.dumps(embedding)))

        conn.commit()
        conn.close()
        print(f"📌 Hata toleranslı embedding SQLite veritabanına kaydedildi: {document_id}")

    def batch_generate_embeddings(self, texts):
        """
        Çoklu işlem desteği ile büyük veri kümelerinde embedding işlemini hızlandırır.
        """
        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            results = executor.map(self.generate_embedding, texts)
        return list(results)

# Modülü dışarıdan çağırmak için sınıf nesnesi
robust_embedding_module = RobustEmbeddingModule()

#------
# helper_module.py
#------

import os
import json
import logging
import redis
import re
from configmodule import config
from concurrent.futures import ProcessPoolExecutor

class HelperModule:
    def __init__(self):
        self.redis_client = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, decode_responses=True)
        self.max_workers = config.MAX_WORKERS

    def clean_text(self, text):
        """
        Metni temizler ve formatlar: gereksiz boşlukları, özel karakterleri kaldırır.
        """
        text = re.sub(r"\s+", " ", text)  # Fazla boşlukları tek boşluğa indir
        text = re.sub(r"[^\w\s.,;!?()]", "", text)  # Özel karakterleri temizle
        return text.strip()

    def normalize_whitespace(self, text):
        """
        Beyaz boşlukları normalize eder.
        """
        return " ".join(text.split())

    def save_json(self, data, file_path):
        """
        Veriyi JSON formatında kaydeder.
        """
        with open(file_path, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)
        print(f"📌 JSON dosyası kaydedildi: {file_path}")

    def load_json(self, file_path):
        """
        JSON dosyasını okur.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as json_file:
                return json.load(json_file)
        except FileNotFoundError:
            print(f"❌ Hata: {file_path} bulunamadı!")
            return None

    def cache_data(self, key, data, expiry=3600):
        """
        Redis önbelleğe veri kaydeder.
        """
        self.redis_client.setex(key, expiry, json.dumps(data))

    def retrieve_cached_data(self, key):
        """
        Redis önbellekten veri alır.
        """
        cached_data = self.redis_client.get(key)
        return json.loads(cached_data) if cached_data else None

    def batch_process_texts(self, texts):
        """
        Çoklu işlem desteği ile büyük metinleri paralel olarak işler.
        """
        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            results = executor.map(self.clean_text, texts)
        return list(results)

# Modülü dışarıdan çağırmak için sınıf nesnesi
helper_module = HelperModule()

#------
# file_save_module.py
#------
import os
import json
import sqlite3
import redis
import csv
from configmodule import config
from concurrent.futures import ProcessPoolExecutor

class FileSaveModule:
    def __init__(self):
        self.sqlite_db = config.SQLITE_DB_PATH
        self.redis_client = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, decode_responses=True)
        self.max_workers = config.MAX_WORKERS

        # Klasörlerin otomatik oluşturulması
        self.directories = {
            "clean_text": config.HEDEF_DIZIN,
            "tables": config.TEMIZ_TABLO_DIZIN,
            "citations": config.CITATIONS_DIR,
            "embeddings": config.EMBEDDING_PARCA_DIR,
            "references": config.TEMIZ_KAYNAKCA_DIZIN
        }
        self.ensure_directories()

    def ensure_directories(self):
        """
        Gerekli klasörleri oluşturur.
        """
        for key, path in self.directories.items():
            os.makedirs(path, exist_ok=True)
    
    def save_clean_text(self, document_id, text):
        """
        Temiz metni hem TXT hem de JSON formatında kaydeder.
        """
        txt_path = os.path.join(self.directories["clean_text"], f"{document_id}.clean.txt")
        json_path = os.path.join(self.directories["clean_text"], f"{document_id}.clean.json")

        with open(txt_path, "w", encoding="utf-8") as txt_file:
            txt_file.write(text)

        with open(json_path, "w", encoding="utf-8") as json_file:
            json.dump({"document_id": document_id, "text": text}, json_file, indent=4, ensure_ascii=False)

        print(f"📌 Temiz metin kaydedildi: {txt_path} ve {json_path}")

    def save_clean_text_to_sqlite(self, document_id, text):
        """
        Temiz metni SQLite veritabanına kaydeder.
        """
        conn = sqlite3.connect(self.sqlite_db)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clean_texts (
                document_id TEXT PRIMARY KEY,
                text TEXT
            )
        """)

        cursor.execute("INSERT OR REPLACE INTO clean_texts VALUES (?, ?)", (document_id, text))

        conn.commit()
        conn.close()
        print(f"📌 Temiz metin SQLite veritabanına kaydedildi: {document_id}")

    def save_tables(self, document_id, tables):
        """
        Çıkarılan tabloları CSV formatında kaydeder.
        """
        csv_path = os.path.join(self.directories["tables"], f"{document_id}.tables.csv")

        with open(csv_path, "w", encoding="utf-8", newline="") as csvfile:
            writer = csv.writer(csvfile)
            for table in tables:
                for row in table:
                    writer.writerow(row)
                writer.writerow([])  # Boş satır ile ayrım yap

        print(f"📌 Tablolar kaydedildi: {csv_path}")

    def save_citations(self, document_id, citations):
        """
        Atıfları hem JSON hem de SQLite formatında kaydeder.
        """
        json_path = os.path.join(self.directories["citations"], f"{document_id}.citations.json")

        with open(json_path, "w", encoding="utf-8") as json_file:
            json.dump(citations, json_file, indent=4, ensure_ascii=False)

        conn = sqlite3.connect(self.sqlite_db)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS citations (
                document_id TEXT,
                citation TEXT,
                PRIMARY KEY (document_id, citation)
            )
        """)

        for citation in citations:
            cursor.execute("INSERT OR IGNORE INTO citations VALUES (?, ?)", (document_id, citation))

        conn.commit()
        conn.close()
        print(f"📌 Atıflar SQLite veritabanına ve JSON dosyasına kaydedildi: {document_id}")

    def save_references(self, document_id, references, format="ris"):
        """
        Kaynakçaları belirli formatlarda kaydeder (RIS, BibTeX, CSV, VOS).
        """
        format_map = {
            "ris": ".ris",
            "bib": ".bib",
            "csv": ".csv",
            "vos": ".vos"
        }

        if format not in format_map:
            raise ValueError(f"Bilinmeyen format: {format}")

        file_path = os.path.join(self.directories["references"], f"{document_id}{format_map[format]}")

        with open(file_path, "w", encoding="utf-8") as file:
            if format == "ris":
                for ref in references:
                    file.write(self._convert_to_ris(ref))
            elif format == "bib":
                for ref in references:
                    file.write(self._convert_to_bibtex(ref))
            elif format == "csv":
                writer = csv.writer(file)
                for ref in references:
                    writer.writerow([ref["title"], ref["authors"], ref["year"]])
            elif format == "vos":
                json.dump(references, file, indent=4, ensure_ascii=False)

        print(f"📌 Kaynakçalar {format.upper()} formatında kaydedildi: {file_path}")

    def _convert_to_ris(self, ref):
        """
        Kaynakçayı RIS formatına çevirir.
        """
        return f"""
        TY  - JOUR
        TI  - {ref.get('title', '')}
        AU  - {', '.join(ref.get('authors', []))}
        PY  - {ref.get('year', '')}
        ER  - 
        """

    def _convert_to_bibtex(self, ref):
        """
        Kaynakçayı BibTeX formatına çevirir.
        """
        return f"""
        @article{{{ref.get('title', '').replace(' ', '_')}},
            title={{ {ref.get('title', '')} }},
            author={{ {', '.join(ref.get('authors', []))} }},
            year={{ {ref.get('year', '')} }}
        }}
        """

    def batch_save_texts(self, text_document_pairs):
        """
        Çoklu işlem desteği ile büyük veri kümelerinde temiz metinleri paralel olarak kaydeder.
        """
        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            executor.map(lambda pair: self.save_clean_text(pair[0], pair[1]), text_document_pairs)

# Modülü dışarıdan çağırmak için sınıf nesnesi
file_save_module = FileSaveModule()

#------
# redis_cache_module.py
#------
import redis
import json
import time
from configmodule import config

class RedisQueue:
    def __init__(self, queue_name="task_queue"):
        self.redis_client = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, decode_responses=True)
        self.queue_name = queue_name
        self.retry_attempts = int(config.MAX_RETRY_ATTEMPTS)

    def enqueue_task(self, task_data):
        """
        Görevi Redis kuyruğuna ekler.
        """
        task_json = json.dumps(task_data)
        self.redis_client.rpush(self.queue_name, task_json)
        print(f"✅ Görev kuyruğa eklendi: {task_data}")

    def dequeue_task(self):
        """
        Kuyruktan bir görevi çeker ve çözümler.
        """
        task_json = self.redis_client.lpop(self.queue_name)
        if task_json:
            task_data = json.loads(task_json)
            print(f"🔄 İşlem başlatıldı: {task_data}")
            return task_data
        else:
            print("📭 Kuyruk boş.")
            return None

    def retry_failed_tasks(self):
        """
        Başarısız olan görevleri tekrar kuyruğa ekler.
        """
        failed_queue = f"{self.queue_name}_failed"
        while self.redis_client.llen(failed_queue) > 0:
            task_json = self.redis_client.lpop(failed_queue)
            task_data = json.loads(task_json)
            attempts = task_data.get("attempts", 0)

            if attempts < self.retry_attempts:
                task_data["attempts"] = attempts + 1
                self.enqueue_task(task_data)
                print(f"♻️ Görev yeniden kuyruğa eklendi (Deneme {attempts+1}): {task_data}")
            else:
                print(f"❌ Görev başarısız oldu ve tekrar deneme sınırına ulaştı: {task_data}")

    def mark_task_as_failed(self, task_data):
        """
        Görevi başarısız olarak işaretler ve yeniden denemek için kaydeder.
        """
        task_data["status"] = "failed"
        failed_queue = f"{self.queue_name}_failed"
        self.redis_client.rpush(failed_queue, json.dumps(task_data))
        print(f"⚠️ Görev başarısız olarak işaretlendi ve tekrar kuyruğa eklendi: {task_data}")

    def get_queue_length(self):
        """
        Kuyruğun mevcut uzunluğunu döndürür.
        """
        return self.redis_client.llen(self.queue_name)

    def process_tasks(self, task_handler):
        """
        Kuyruktaki görevleri alıp işleyen bir işlem döngüsü.
        """
        while True:
            task_data = self.dequeue_task()
            if task_data:
                try:
                    task_handler(task_data)
                except Exception as e:
                    print(f"❌ Görev işlenirken hata oluştu: {e}")
                    self.mark_task_as_failed(task_data)
            else:
                print("⏳ Yeni görev bekleniyor...")
                time.sleep(5)  # Bekleme süresi

# Modülü dışarıdan çağırmak için sınıf nesnesi
redis_queue = RedisQueue()

#------
# redis_cache_module.py
#------
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

#------
#redis_process_module.py
#------
import redis
import json
import sqlite3
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

# import sqlite3
# import json

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
    add_citation_to_sqlite(citation_id, citation_data)import redis
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

    # Citation verisini Redis'ten çek
    retrieved_citation = get_citation_from_redis(citation_id)
#------
# sqlite_storage.py
#------

import sqlite3
import json
import os
from configmodule import config

class SQLiteStorage:
    def __init__(self):
        self.db_path = config.SQLITE_DB_PATH
        self.ensure_tables()

    def ensure_tables(self):
        """
        Gerekli tabloların oluşturulmasını sağlar.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clean_texts (
                document_id TEXT PRIMARY KEY,
                text TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS embeddings (
                document_id TEXT PRIMARY KEY,
                embedding TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bibliography (
                id TEXT PRIMARY KEY,
                title TEXT,
                authors TEXT,
                year INTEGER,
                citation_key TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS citations (
                document_id TEXT,
                citation TEXT,
                PRIMARY KEY (document_id, citation)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS document_clusters (
                document_id TEXT PRIMARY KEY,
                cluster INTEGER
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS document_maps (
                document_id TEXT PRIMARY KEY,
                structural_map TEXT,
                scientific_map TEXT
            )
        """)

        conn.commit()
        conn.close()
        print("✅ SQLite tabloları oluşturuldu veya zaten mevcut.")

    def store_clean_text(self, document_id, text):
        """
        Temiz metni SQLite veritabanına kaydeder.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO clean_texts VALUES (?, ?)", (document_id, text))
        conn.commit()
        conn.close()
        print(f"📌 Temiz metin kaydedildi: {document_id}")

    def store_embedding(self, document_id, embedding):
        """
        Embedding verisini SQLite veritabanına kaydeder.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO embeddings VALUES (?, ?)", (document_id, json.dumps(embedding)))
        conn.commit()
        conn.close()
        print(f"📌 Embedding SQLite veritabanına kaydedildi: {document_id}")

    def store_bibliography(self, bibliography_data):
        """
        Zotero'dan gelen kaynakça verilerini SQLite veritabanına kaydeder.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        for ref in bibliography_data:
            cursor.execute("INSERT OR IGNORE INTO bibliography VALUES (?, ?, ?, ?, ?)",
                           (ref["id"], ref["title"], ", ".join(ref["authors"]), ref["year"], ref["citation_key"]))
        conn.commit()
        conn.close()
        print("📌 Kaynakça SQLite veritabanına kaydedildi.")

    def store_citation(self, document_id, citations):
        """
        Atıfları SQLite veritabanına kaydeder.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        for citation in citations:
            cursor.execute("INSERT OR IGNORE INTO citations VALUES (?, ?)", (document_id, citation))
        conn.commit()
        conn.close()
        print(f"📌 Atıflar SQLite veritabanına kaydedildi: {document_id}")

    def store_document_cluster(self, document_id, cluster_label):
        """
        Kümeleme sonuçlarını SQLite veritabanına kaydeder.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO document_clusters VALUES (?, ?)", (document_id, cluster_label))
        conn.commit()
        conn.close()
        print(f"📌 Kümeleme sonucu kaydedildi: {document_id} -> Cluster {cluster_label}")

    def store_document_map(self, document_id, structural_map, scientific_map):
        """
        Yapısal ve bilimsel haritalama verilerini SQLite veritabanına kaydeder.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO document_maps VALUES (?, ?, ?)",
                       (document_id, json.dumps(structural_map), json.dumps(scientific_map)))
        conn.commit()
        conn.close()
        print(f"📌 Haritalama verisi kaydedildi: {document_id}")

    def retrieve_text_by_id(self, document_id):
        """
        Belirli bir belgeye ait temiz metni getirir.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT text FROM clean_texts WHERE document_id=?", (document_id,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None

    def retrieve_embedding_by_id(self, document_id):
        """
        Belirli bir belgeye ait embedding verisini getirir.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT embedding FROM embeddings WHERE document_id=?", (document_id,))
        result = cursor.fetchone()
        conn.close()
        return json.loads(result[0]) if result else None

    def retrieve_bibliography(self):
        """
        Tüm kaynakça verilerini getirir.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM bibliography")
        result = cursor.fetchall()
        conn.close()
        return result

    def delete_document(self, document_id):
        """
        Belirli bir belgeye ait tüm verileri veritabanından siler.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        tables = ["clean_texts", "embeddings", "bibliography", "citations", "document_clusters", "document_maps"]
        for table in tables:
            cursor.execute(f"DELETE FROM {table} WHERE document_id=?", (document_id,))
        conn.commit()
        conn.close()
        print(f"🗑️ {document_id} verileri SQLite veritabanından silindi.")

# Modülü dışarıdan çağırmak için sınıf nesnesi
sqlite_storage = SQLiteStorage()

#------
# veri_isleme_modulu.py
#------

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

#------
# veri gorsellestirme_modulu.py
#------
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

#------
# yapay_zeka_finetuning_modulu.py
#------

import os
import json
import sqlite3
import redis
import torch
import transformers
from torch.utils.data import Dataset, DataLoader
from transformers import AutoModelForSequenceClassification, AutoTokenizer, Trainer, TrainingArguments
from configmodule import config

class FineTuningDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_length=512):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        encoding = self.tokenizer(
            self.texts[idx],
            truncation=True,
            padding="max_length",
            max_length=self.max_length,
            return_tensors="pt"
        )
        encoding = {key: val.squeeze() for key, val in encoding.items()}
        encoding["labels"] = torch.tensor(self.labels[idx], dtype=torch.long)
        return encoding

class FineTuner:
    def __init__(self):
        self.model_name = config.FINETUNE_MODEL
        self.batch_size = config.FINETUNE_BATCH_SIZE
        self.epochs = config.FINETUNE_EPOCHS
        self.learning_rate = config.FINETUNE_LR
        self.output_dir = config.FINETUNE_OUTPUT_DIR

        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name, num_labels=2)

        self.sqlite_db = config.SQLITE_DB_PATH
        self.redis_client = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, decode_responses=True)

    def fetch_training_data(self):
        """
        SQLite veritabanından eğitim verisini çeker.
        """
        conn = sqlite3.connect(self.sqlite_db)
        cursor = conn.cursor()
        cursor.execute("SELECT text, label FROM training_data")
        rows = cursor.fetchall()
        conn.close()

        texts = [row[0] for row in rows]
        labels = [row[1] for row in rows]
        return texts, labels

    def train_model(self):
        """
        Modeli fine-tune ederek eğitir.
        """
        texts, labels = self.fetch_training_data()
        dataset = FineTuningDataset(texts, labels, self.tokenizer)

        training_args = TrainingArguments(
            output_dir=self.output_dir,
            per_device_train_batch_size=self.batch_size,
            num_train_epochs=self.epochs,
            learning_rate=self.learning_rate,
            logging_dir=os.path.join(self.output_dir, "logs"),
            save_strategy="epoch"
        )

        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=dataset,
            tokenizer=self.tokenizer
        )

        trainer.train()
        self.model.save_pretrained(self.output_dir)
        self.tokenizer.save_pretrained(self.output_dir)
        print(f"✅ Model eğitildi ve {self.output_dir} dizinine kaydedildi.")

    def save_model_to_redis(self):
        """
        Eğitilen modeli Redis içinde saklar.
        """
        with open(os.path.join(self.output_dir, "pytorch_model.bin"), "rb") as f:
            model_data = f.read()
            self.redis_client.set("fine_tuned_model", model_data)
        print("📌 Eğitilmiş model Redis'e kaydedildi.")

    def load_model_from_redis(self):
        """
        Redis'ten modeli alır ve belleğe yükler.
        """
        model_data = self.redis_client.get("fine_tuned_model")
        if model_data:
            with open(os.path.join(self.output_dir, "pytorch_model.bin"), "wb") as f:
                f.write(model_data)
            self.model = AutoModelForSequenceClassification.from_pretrained(self.output_dir)
            print("📌 Model Redis’ten alındı ve belleğe yüklendi.")
        else:
            print("❌ Redis’te kayıtlı model bulunamadı.")

# Modülü dışarıdan çağırmak için sınıf nesnesi
fine_tuner = FineTuner()

#------
# gui_modulu.py
#------
import customtkinter as ctk
import threading
import os
from tkinter import filedialog
from configmodule import config
from pdfprocessing import extract_text_from_pdf
from citationmappingmodule import citation_mapping
from yapay_zeka_finetuning import fine_tuner
from veri_gorsellestirme import data_visualization

class ZapataGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Zapata M6 - Bilimsel Veri İşleme Sistemi")
        self.geometry("800x600")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.create_widgets()

    def create_widgets(self):
        """
        GUI bileşenlerini oluşturur.
        """

        self.label = ctk.CTkLabel(self, text="Zapata M6 - Bilimsel Makale İşleme", font=("Arial", 18))
        self.label.pack(pady=10)

        self.load_pdf_button = ctk.CTkButton(self, text="📂 PDF Yükle", command=self.load_pdf)
        self.load_pdf_button.pack(pady=5)

        self.process_pdf_button = ctk.CTkButton(self, text="📄 PDF İşle", command=self.process_pdf, state="disabled")
        self.process_pdf_button.pack(pady=5)

        self.citation_analysis_button = ctk.CTkButton(self, text="🔗 Atıf Analizi", command=self.run_citation_analysis, state="disabled")
        self.citation_analysis_button.pack(pady=5)

        self.train_ai_button = ctk.CTkButton(self, text="🤖 AI Modeli Eğit", command=self.train_ai_model, state="disabled")
        self.train_ai_button.pack(pady=5)

        self.visualize_button = ctk.CTkButton(self, text="📊 Atıf Haritası Göster", command=self.show_visualization, state="disabled")
        self.visualize_button.pack(pady=5)

        self.log_text = ctk.CTkTextbox(self, height=10, wrap="word", font=("Arial", 12))
        self.log_text.pack(pady=10, fill="both", expand=True)

    def log_message(self, message):
        """
        İşlem durumlarını GUI üzerinden gösterir.
        """
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")

    def load_pdf(self):
        """
        Kullanıcının PDF dosyası seçmesini sağlar.
        """
        file_path = filedialog.askopenfilename(filetypes=[("PDF Dosyaları", "*.pdf")])
        if file_path:
            self.selected_pdf = file_path
            self.process_pdf_button.configure(state="normal")
            self.log_message(f"✅ PDF seçildi: {file_path}")

    def process_pdf(self):
        """
        Seçilen PDF'yi işleme alır.
        """
        self.log_message("🔄 PDF işleniyor...")
        threading.Thread(target=self._process_pdf_thread, daemon=True).start()

    def _process_pdf_thread(self):
        """
        PDF işleme işlemini ayrı bir iş parçacığında çalıştırır.
        """
        text = extract_text_from_pdf(self.selected_pdf)
        self.log_message("✅ PDF başarıyla işlendi.")
        self.citation_analysis_button.configure(state="normal")

    def run_citation_analysis(self):
        """
        Atıf analizini çalıştırır.
        """
        self.log_message("🔄 Atıf analizi başlatılıyor...")
        threading.Thread(target=self._citation_analysis_thread, daemon=True).start()

    def _citation_analysis_thread(self):
        """
        Atıf analizi işlemini ayrı bir iş parçacığında çalıştırır.
        """
        citation_mapping.map_citations_to_references(self.selected_pdf)
        self.log_message("✅ Atıf analizi tamamlandı.")
        self.visualize_button.configure(state="normal")

    def train_ai_model(self):
        """
        AI modelini eğitir.
        """
        self.log_message("🔄 AI modeli eğitiliyor...")
        threading.Thread(target=self._train_ai_thread, daemon=True).start()

    def _train_ai_thread(self):
        """
        Model eğitim işlemini ayrı bir iş parçacığında çalıştırır.
        """
        fine_tuner.train_model()
        self.log_message("✅ AI modeli eğitildi.")

    def show_visualization(self):
        """
        Atıf haritasını gösterir.
        """
        self.log_message("📊 Atıf haritası oluşturuluyor...")
        threading.Thread(target=self._visualize_thread, daemon=True).start()

    def _visualize_thread(self):
        """
        Görselleştirme işlemini ayrı bir iş parçacığında çalıştırır.
        """
        data_visualization.plot_citation_network()
        self.log_message("✅ Atıf haritası gösterildi.")

    def check_redis_status(self):
        """
        Redis kuyruk durumunu kontrol eder ve GUI'de gösterir.
        """
        status = redis_client.ping()
        return "Online" if status else "Offline"
    
    def update_gui_status(self):       
        """
        GUI'yi günceller ve Redis kuyruk durumunu gösterir.
        """
        status = self.check_redis_status()
        self.status_label.config(text=f"Redis Status: {status}")
        self.after(5000, self.update_gui_status)  # 5 saniyede bir güncelleme yapar

    def create_status_window(self):
        """
        Redis durumu için ayrı bir pencere oluşturur.
        """
        self.status_window = ctk.CTkToplevel(self)
        self.status_window.title("Citation Verisi Durumu")

        self.status_label = ctk.CTkLabel(self.status_window, text="Redis Status: Checking...")
        self.status_label.pack()

        # Başlangıçta durumu kontrol et
        self.update_gui_status()



# Uygulama başlatma
if __name__ == "__main__":
    app = ZapataGUI()
    app.mainloop()

#------
#scientific mapping module
#------

# ==============================
# 📌 Zapata M6H - scientific_mapping.py
# 📌 Bilimsel Haritalama Modülü
# 📌 Özet, giriş, yöntem, sonuç, kaynakça gibi bölümleri tespit eder.
# ==============================

import re
import json
import logging
import colorlog
from configmodule import config

class ScientificMapping:
    def __init__(self):
        """Bilimsel haritalama işlemleri için sınıf."""
        self.logger = self.setup_logging()
        self.section_patterns = {
            "Özet": r"(?:abstract|öz(et)?)",
            "Giriş": r"(?:introduction|giriş)",
            "Yöntem": r"(?:methods?|metot|yöntem)",
            "Bulgular": r"(?:results?|bulgular)",
            "Tartışma": r"(?:discussion|tartışma)",
            "Sonuç": r"(?:conclusion|sonuç)",
            "Kaynakça": r"(?:references?|kaynakça)"
        }

    def setup_logging(self):
        """Loglama sistemini kurar."""
        log_formatter = colorlog.ColoredFormatter(
            "%(log_color)s%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',
            }
        )
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_formatter)
        file_handler = logging.FileHandler("scientific_mapping.log", encoding="utf-8")
        file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        return logger

    def extract_headings_and_sections(self, text):
        """Metin içindeki bilimsel bölümleri belirler ve haritalar."""
        self.logger.info("🔍 Bilimsel bölümler tespit ediliyor...")
        sections = {}
        lines = text.split("\n")

        for i, line in enumerate(lines):
            for section, pattern in self.section_patterns.items():
                if re.search(pattern, line, re.IGNORECASE):
                    sections[section] = i  # Satır numarasını kaydet
        
        self.logger.info(f"✅ Bilimsel bölümler tespit edildi: {list(sections.keys())}")
        return sections

    def map_scientific_sections(self, text):
        """Belirlenen bölümlerin içeriğini ayrıştırır."""
        self.logger.info("📌 Bilimsel bölümler haritalanıyor...")
        section_map = self.extract_headings_and_sections(text)
        mapped_sections = {}

        lines = text.split("\n")
        sorted_sections = sorted(section_map.items(), key=lambda x: x[1])

        for idx, (section, start_line) in enumerate(sorted_sections):
            end_line = sorted_sections[idx + 1][1] if idx + 1 < len(sorted_sections) else len(lines)
            mapped_sections[section] = "\n".join(lines[start_line:end_line])

        self.logger.info(f"✅ Bilimsel haritalama tamamlandı: {list(mapped_sections.keys())}")
        return mapped_sections

    def save_mapping_to_json(self, mapping, file_path):
        """Haritalanan bilimsel bölümleri JSON formatında kaydeder."""
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(mapping, f, ensure_ascii=False, indent=4)
            self.logger.info(f"✅ Bilimsel harita JSON olarak kaydedildi: {file_path}")
        except Exception as e:
            self.logger.error(f"❌ JSON kaydetme hatası: {e}")

# ==============================
# ✅ Test Komutları:
if __name__ == "__main__":
    scientific_mapper = ScientificMapping()

    sample_text = """Abstract: This study investigates...
    Introduction: In recent years...
    Methods: The methodology of this study includes...
    Results: The findings suggest...
    Discussion: The results indicate...
    Conclusion: In summary...
    References: [1] Author 2020..."""

    mapped_sections = scientific_mapper.map_scientific_sections(sample_text)
    print("📄 Bilimsel Bölümler:", mapped_sections)

    scientific_mapper.save_mapping_to_json(mapped_sections, "scientific_map.json")
    print("✅ Bilimsel haritalama tamamlandı!")
# ==============================

#------
# layout_module.py
#------
# ==============================
# 📌 Zapata M6H - layout_analysis.py
# 📌 Yapısal Haritalama Modülü
# 📌 Sayfa düzeni, sütun yapıları, başlık-paragraf ayrımı analiz edilir.
# ==============================

import re
import json
import logging
import colorlog
from configmodule import config

class LayoutAnalysis:
    def __init__(self):
        """Yapısal haritalama işlemleri için sınıf."""
        self.logger = self.setup_logging()

    def setup_logging(self):
        """Loglama sistemini kurar."""
        log_formatter = colorlog.ColoredFormatter(
            "%(log_color)s%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',
            }
        )
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_formatter)
        file_handler = logging.FileHandler("layout_analysis.log", encoding="utf-8")
        file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        return logger

    def detect_headers_and_subsections(self, text):
        """Metindeki başlık ve alt başlıkları tespit eder."""
        self.logger.info("🔍 Başlık ve alt başlıklar tespit ediliyor...")
        headers = re.findall(r"^\s*(\d+\.\d*|\b[A-Z][a-z]+\b):", text, re.MULTILINE)
        self.logger.info(f"✅ Tespit edilen başlıklar: {headers}")
        return headers

    def map_document_structure(self, text):
        """Sayfa düzenini ve sütun yapısını analiz eder."""
        self.logger.info("📌 Sayfa yapısı haritalanıyor...")
        structure_map = {
            "sütun_sayısı": 1 if "\n\n" in text else 2,
            "paragraf_sayısı": len(text.split("\n\n")),
            "başlıklar": self.detect_headers_and_subsections(text)
        }

        self.logger.info("✅ Yapısal haritalama tamamlandı.")
        return structure_map

    def save_layout_to_json(self, layout, file_path):
        """Yapısal haritalama sonuçlarını JSON olarak kaydeder."""
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(layout, f, ensure_ascii=False, indent=4)
            self.logger.info(f"✅ Yapısal harita JSON olarak kaydedildi: {file_path}")
        except Exception as e:
            self.logger.error(f"❌ JSON kaydetme hatası: {e}")

# ==============================
# ✅ Test Komutları:
if __name__ == "__main__":
    layout_analyzer = LayoutAnalysis()

    sample_text = """1. Giriş
    1.1 Problem Tanımı
    1.2 Literatür Taraması
    2. Yöntem
    3. Bulgular
    4. Sonuç ve Tartışma"""

    layout_map = layout_analyzer.map_document_structure(sample_text)
    print("📄 Yapısal Harita:", layout_map)

    layout_analyzer.save_layout_to_json(layout_map, "layout_map.json")
    print("✅ Yapısal haritalama tamamlandı!")
# ==============================
#------
# main.py
#------
import os
import sys
import threading
from configmodule import config
from pdfprocessing import extract_text_from_pdf
from citationmappingmodule import citation_mapping
from yapay_zeka_finetuning import fine_tuner
from redisqueue import redis_queue
from rediscache import redis_cache
from sqlite_storage import sqlite_storage
from guimodule import ZapataGUI

def process_pdf(file_path):
    """
    PDF dosyasını işler ve metni çıkartır.
    """
    print(f"🔄 PDF İşleniyor: {file_path}")
    text = extract_text_from_pdf(file_path)
    sqlite_storage.store_clean_text(os.path.basename(file_path), text)
    print(f"✅ PDF İşleme Tamamlandı: {file_path}")

def run_citation_analysis(file_path):
    """
    Atıf analizini çalıştırır.
    """
    print(f"🔄 Atıf Analizi Başlatıldı: {file_path}")
    citation_mapping.map_citations_to_references(file_path)
    print(f"✅ Atıf Analizi Tamamlandı: {file_path}")

def train_ai_model():
    """
    AI modelini eğitir.
    """
    print("🔄 AI Modeli Eğitiliyor...")
    fine_tuner.train_model()
    print("✅ AI Modeli Eğitildi.")

def queue_processing_loop():
    """
    Redis kuyruğundan gelen görevleri işler.
    """
    print("📌 Kuyruk İşlemeye Başladı...")
    redis_queue.process_tasks(process_pdf)

def main():
    """
    Ana uygulama akışı.
    """
    mode = config.RUN_MODE  # .env dosyasından GUI veya Konsol modunu okur

    if mode.lower() == "gui":
        print("🖥️ GUI Modu Başlatılıyor...")
        app = ZapataGUI()
        app.mainloop()

    elif mode.lower() == "console":
        print("💻 Konsol Modu Başlatılıyor...")
        
        while True:
            print("\n📌 İşlem Seçin:")
            print("1 - PDF İşle")
            print("2 - Atıf Analizi Yap")
            print("3 - AI Modeli Eğit")
            print("4 - Kuyruğu Başlat")
            print("5 - Çıkış")

            choice = input("Seçiminizi girin: ")

            if choice == "1":
                file_path = input("📂 PDF Dosyasının Yolunu Girin: ")
                process_pdf(file_path)

            elif choice == "2":
                file_path = input("📂 PDF Dosyasının Yolunu Girin: ")
                run_citation_analysis(file_path)

            elif choice == "3":
                train_ai_model()

            elif choice == "4":
                threading.Thread(target=queue_processing_loop, daemon=True).start()

            elif choice == "5":
                print("🚀 Programdan çıkılıyor...")
                sys.exit()

            else:
                print("❌ Geçersiz seçim, tekrar deneyin.")

if __name__ == "__main__":
    main()