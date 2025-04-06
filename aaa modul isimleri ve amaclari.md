📌 1. Zapata M6 Modülleri ve Fonksiyonları

Modül Adı	                    Fonksiyonlar	                                                    Görevi
configmodule.py	                load_config(), setup_logging(), get_env_variable(), get_max_workers()	
                                                                                                    Genel ayarları yönetir, .env dosyasını okur, log sistemini kurar.
pdfprocessing.py	            extract_text_from_pdf(), extract_tables_from_pdf(), detect_layout(), reflow_columns()	
                                                                                                    PDF’den metin ve tablo çıkarma, yapısal haritalama, 
                                                                                                        sütun birleştirme işlemlerini yapar.
zoteromodule.py	                fetch_references_from_zotero(), download_pdf_from_doi(), save_references()	
                                                                                                    Zotero API ile kaynakça çekme, DOI ile PDF indirme, 
                                                                                                        kaynakçaları farklı formatlarda kaydetme.
embeddingmodule.py	            generate_embedding(), save_embedding_to_chromadb()	                Metin embedding işlemleri ve ChromaDB’ye veri kaydetme.
alternativeembeddingmodule.py	use_contriever_embedding(), use_specter_embedding()	                Alternatif embedding modellerini destekler.
citationmappingmodule.py	    extract_references(), map_citations_to_references(), store_citation_mappings()	
                                                                                                    Atıfları tespit eder, kaynaklarla eşleştirir 
                                                                                                        ve ChromaDB’ye, SQLite ve JSON’a kaydeder.
clustering_module.py	        cluster_documents()	                                                Embedding verileriyle makale kümeleme.
robustembeddingmodule.py	    generate_robust_embedding()	                                        Hata toleranslı embedding işlemleri.
helpermodule.py	                clean_text()	                                                    Metin temizleme ve düzenleme işlemleri.
filesavemodule.py	            save_clean_text(), save_tables(), save_citations(), save_clean_text_to_sqlite()	
                                                                                                    Temiz metinleri, tabloları, kaynakçaları ve embedding’leri kaydetme.
redisqueue.py	                enqueue_task(), dequeue_task(), retry_failed_tasks()	            Redis tabanlı işlem kuyruğu yönetimi,
                                                                                                        başarısız görevleri yeniden çalıştırma.
rediscache.py	                cache_embedding(), get_cached_embedding(), cache_map_data(), get_cached_map()	
                                                                                                    Redis önbellekleme: embedding ve map dosyalarını 
                                                                                                        hızlı erişim için saklar.
sqlite_storage.py	            store_clean_text(), store_bibliography(), retrieve_text_by_id()	    Temiz metinleri ve PDF'in bibliyografyasını 
                                                                                                        SQLite veritabanına kaydetme.
veri_isleme.py	                analyze_citation_network()	                                        Atıf zinciri analizini yapar.
veri_gorsellestirme.py	        plot_citation_network()	                                            Atıf zincirlerini ve kümeleme sonuçlarını görselleştirir.
yapay_zeka_finetuning.py	    train_finetune_model()	                                            AI modelini fine-tuning ile geliştirir.
guimodule.py	                setup_gui(), handle_user_input()	                                Customtkinter ile GUI entegrasyonu.
scientific_mapping.py	        map_scientific_sections(), extract_headings_and_sections()	        Bilimsel haritalama işlemleri – 
                                                                                                        Özet, giriş, yöntemler vb. bölümleri belirler ve işaretler.
layout_analysis.py	            map_document_structure(), detect_headers_and_subsections()	        Yapısal analiz haritalaması – 
                                                                                                        Sayfa düzeni, sütun yapıları, başlık-paragraf ayrımı yapılır.
main.py	                                                                                            Ana program	Tüm modülleri birleştirir ve işlemleri yönetir.
