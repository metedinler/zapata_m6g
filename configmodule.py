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



# onceki hali

# import os
# import logging
# import colorlog
# from pathlib import Path
# from dotenv import load_dotenv
# import chromadb

# class Config:
#     def __init__(self):
#         # .env dosyasını yükle
#         load_dotenv()

#         # Dizin Ayarları
#         self.KAYNAK_DIZIN = os.getenv("KAYNAK_DIZIN", r"C:\Users\mete\Zotero\zotai")
#         self.STORAGE_DIR = Path(os.getenv("STORAGE_DIR", r"C:\Users\mete\Zotero\storage"))
#         self.SUCCESS_DIR = Path(os.getenv("SUCCESS_DIR", r"C:\Users\mete\Zotero\zotai\egitimpdf"))
#         self.HEDEF_DIZIN = Path(os.getenv("HEDEF_DIZIN", os.path.join(str(self.KAYNAK_DIZIN), "TemizMetin")))
#         self.TEMIZ_TABLO_DIZIN = Path(os.getenv("TEMIZ_TABLO_DIZIN", os.path.join(str(self.KAYNAK_DIZIN), "TemizTablo")))
#         self.TEMIZ_KAYNAKCA_DIZIN = Path(os.getenv("TEMIZ_KAYNAKCA_DIZIN", os.path.join(str(self.KAYNAK_DIZIN), "TemizKaynakca")))
#         self.PDF_DIR = Path(os.getenv("PDF_DIR", str(self.SUCCESS_DIR) + "/pdfler"))
#         self.EMBEDDING_PARCA_DIR = Path(os.getenv("EMBEDDING_PARCA_DIZIN", str(self.SUCCESS_DIR) + "/embedingparca"))
#         self.CITATIONS_DIR = Path(os.getenv("CITATIONS_DIR", r"C:\Users\mete\Zotero\zotasistan\citations"))
#         self.TABLES_DIR = Path(os.getenv("TABLES_DIR", r"C:\Users\mete\Zotero\zotasistan\tables"))
#         self.CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "chroma_db")

#         # API Ayarları
#         self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your_openai_api_key")
#         self.ZOTERO_API_KEY = os.getenv("ZOTERO_API_KEY", "your_zotero_api_key")
#         self.ZOTERO_USER_ID = os.getenv("ZOTERO_USER_ID", "your_zotero_user_id")
#         self.ZOTERO_API_URL = f"https://api.zotero.org/users/{self.ZOTERO_USER_ID}/items"

#         # PDF İşleme Ayarları
#         self.PDF_TEXT_EXTRACTION_METHOD = os.getenv("PDF_TEXT_EXTRACTION_METHOD", "pdfplumber").lower()
#         self.TABLE_EXTRACTION_METHOD = os.getenv("TABLE_EXTRACTION_METHOD", "pdfplumber").lower()
#         self.COLUMN_DETECTION = os.getenv("COLUMN_DETECTION", "True").lower() == "true"

#         # Embedding & NLP Ayarları
#         self.EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002")
#         self.CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "256"))
#         self.PARAGRAPH_BASED_SPLIT = os.getenv("PARAGRAPH_BASED_SPLIT", "True").lower() == "true"
#         self.MULTI_PROCESSING = os.getenv("MULTI_PROCESSING", "True").lower() == "true"
#         self.MAX_WORKERS = int(os.getenv("MAX_WORKERS", "4"))

#         # Citation Mapping & Analiz Ayarları
#         self.ENABLE_CITATION_MAPPING = os.getenv("ENABLE_CITATION_MAPPING", "True").lower() == "true"
#         self.ENABLE_TABLE_EXTRACTION = os.getenv("ENABLE_TABLE_EXTRACTION", "True").lower() == "true"
#         self.ENABLE_CLUSTERING = os.getenv("ENABLE_CLUSTERING", "True").lower() == "true"

#         # Loglama & Debug Ayarları
#         self.LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")
#         self.ENABLE_ERROR_LOGGING = os.getenv("ENABLE_ERROR_LOGGING", "True").lower() == "true"
#         self.DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"

#         # Çalışma Modu Seçimi
#         # "RUN_MODE" veya "runGUI" kullanılarak GUI veya konsol modu belirlenir.
#         self.RUN_MODE = os.getenv("RUN_MODE", os.getenv("runGUI", "gui")).lower()

#         # Loglama Yapılandırması
#         log_formatter = colorlog.ColoredFormatter(
#             "%(log_color)s%(asctime)s - %(levelname)s - %(message)s",
#             datefmt="%Y-%m-%d %H:%M:%S",
#             log_colors={
#                 'DEBUG': 'cyan',
#                 'INFO': 'green',
#                 'WARNING': 'yellow',
#                 'ERROR': 'red',
#                 'CRITICAL': 'bold_red',
#             }
#         )
#         console_handler = logging.StreamHandler()
#         console_handler.setFormatter(log_formatter)
#         file_handler = logging.FileHandler("pdf_processing.log", encoding="utf-8")
#         file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
#         self.logger = logging.getLogger(__name__)
#         self.logger.setLevel(getattr(logging, self.LOG_LEVEL.upper(), logging.DEBUG))
#         self.logger.addHandler(console_handler)
#         self.logger.addHandler(file_handler)

#         # ChromaDB Yapılandırması
#         self.chroma_client = chromadb.PersistentClient(path=self.CHROMA_DB_PATH)

#         # Gerekli Dizilerin Oluşturulması
#         self.ensure_directories()

#     def ensure_directories(self):
#         """Gerekli dizinleri oluşturur."""
#         directories = [
#             self.PDF_DIR,
#             self.EMBEDDING_PARCA_DIR,
#             self.HEDEF_DIZIN,
#             self.TEMIZ_TABLO_DIZIN,
#             self.TEMIZ_KAYNAKCA_DIZIN,
#             self.CITATIONS_DIR,
#             self.TABLES_DIR
#         ]
#         for directory in directories:
#             if not directory.exists():
#                 try:
#                     directory.mkdir(parents=True, exist_ok=True)
#                     self.logger.info(f"✅ {directory} dizini oluşturuldu.")
#                 except Exception as e:
#                     self.logger.error(f"❌ {directory} dizini oluşturulamadı: {e}")

# # Global konfigürasyon nesnesi
# config = Config()
