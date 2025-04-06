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
