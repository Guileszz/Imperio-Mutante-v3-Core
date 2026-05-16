"""
INDEX LEGACY v3.4.0 - Script de Indexação Inicial
Varre a pasta /legacy e alimenta a Memória Ancestral.
"""

import os
import hashlib
import logging
from intelligence.ancestral_memory import AncestralMemory

logging.basicConfig(level=logging.INFO, format='%(asctime)s - INDEX-LEGACY - %(levelname)s - %(message)s')
logger = logging.getLogger("INDEX-LEGACY")

def get_file_hash(content: str) -> str:
    return hashlib.md5(content.encode('utf-8')).hexdigest()

def index_legacy_files():
    legacy_dir = "legacy"
    memory = AncestralMemory()
    
    indexed_count = 0
    skipped_count = 0
    
    logger.info(f"Iniciando indexação da pasta {legacy_dir}...")
    
    for root, dirs, files in os.walk(legacy_dir):
        # Evitar indexar o próprio banco vetorial
        if "vector_db" in root:
            continue
            
        for file in files:
            if file.endswith(('.py', '.txt', '.md', '.json')):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    if not content.strip():
                        continue
                        
                    file_id = f"legacy_{get_file_hash(file_path)}_{file}"
                    metadata = {
                        "path": file_path,
                        "filename": file,
                        "type": file.split('.')[-1],
                        "source": "legacy_cold_start"
                    }
                    
                    memory.add_knowledge(content[:10000], metadata, file_id) # Limitando tamanho do doc
                    indexed_count += 1
                    
                except Exception as e:
                    logger.error(f"Erro ao processar {file_path}: {e}")
                    skipped_count += 1

    logger.info(f"Indexação concluída. Indexados: {indexed_count}, Falhas: {skipped_count}")
    print(f"✅ Memória Ancestral agora contém {memory.count()} documentos.")

if __name__ == "__main__":
    index_legacy_files()
