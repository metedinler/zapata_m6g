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