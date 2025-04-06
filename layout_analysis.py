#layout_analysis.py

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