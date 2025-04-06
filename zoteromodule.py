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
