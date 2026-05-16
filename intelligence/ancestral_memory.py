"""
ANCESTRAL MEMORY v3.4.0 - Sistema de Memória Vetorial (RAG)
Integração com ChromaDB e Gemini Embeddings para o Império Mutante.
"""

import os
import logging
import chromadb
from chromadb.utils import embedding_functions
from typing import List, Dict, Any, Optional
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - ANCESTRAL-MEMORY - %(levelname)s - %(message)s')
logger = logging.getLogger("ANCESTRAL-MEMORY")

class AncestralMemory:
    def __init__(self, db_path: str = "legacy/vector_db"):
        self.db_path = db_path
        self.api_key = os.getenv("GEMINI_API_KEY")
        
        if not self.api_key:
            logger.error("GEMINI_API_KEY não encontrada. Ancestral Memory operando em modo degradado.")
        
        self.client = chromadb.PersistentClient(path=self.db_path)
        
        # Configura a função de embedding do Gemini
        self.embedding_function = embedding_functions.GoogleGenerativeAiEmbeddingFunction(
            api_key=self.api_key,
            model_name="models/embedding-001"
        )
        
        self.collection = self.client.get_or_create_collection(
            name="ancestral_knowledge",
            embedding_function=self.embedding_function,
            metadata={"description": "Memória Ancestral do Império Mutante"}
        )
        
        logger.info(f"Ancestral Memory inicializada em {self.db_path}")

    def add_knowledge(self, text: str, metadata: Dict[str, Any], doc_id: str):
        """Adiciona um novo fragmento de conhecimento à memória."""
        try:
            self.collection.add(
                documents=[text],
                metadatas=[metadata],
                ids=[doc_id]
            )
            logger.debug(f"Conhecimento adicionado: {doc_id}")
        except Exception as e:
            logger.error(f"Erro ao adicionar conhecimento {doc_id}: {e}")

    def search(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """Realiza busca semântica na memória."""
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            formatted_results = []
            if results and results['documents']:
                for i in range(len(results['documents'][0])):
                    formatted_results.append({
                        "document": results['documents'][0][i],
                        "metadata": results['metadatas'][0][i] if results['metadatas'] else {},
                        "distance": results['distances'][0][i] if results['distances'] else 0
                    })
            return formatted_results
        except Exception as e:
            logger.error(f"Erro ao buscar na memória: {e}")
            return []

    def count(self) -> int:
        return self.collection.count()

if __name__ == "__main__":
    # Teste básico
    memory = AncestralMemory()
    print(f"Total de documentos: {memory.count()}")
    if memory.count() == 0:
        memory.add_knowledge(
            "O Império Mutante foi fundado na busca pela soberania tecnológica total.",
            {"source": "test", "type": "history"},
            "test_001"
        )
    
    res = memory.search("Quem fundou o império?")
    print(f"Resultado da busca: {res}")
