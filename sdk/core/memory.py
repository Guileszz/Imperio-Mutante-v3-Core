"""
SOVEREIGN INTELLIGENCE SDK - ANCESTRAL MEMORY
Sistema de Memória Vetorial (RAG) Híbrido
"""

import os
import logging
import chromadb
from chromadb.utils import embedding_functions
from typing import List, Dict, Any, Optional
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [SOVEREIGN-SDK] - %(levelname)s - %(message)s')
logger = logging.getLogger("SOVEREIGN-SDK-MEMORY")

class AncestralMemory:
    def __init__(self, db_path: str = "data/vector_db", provider: Optional[str] = None):
        self.db_path = db_path
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
        
        self.client = chromadb.PersistentClient(path=self.db_path)
        
        # Escolha automática de provedor se não especificado
        if not provider:
            self.provider = "gemini" if self.api_key else "ollama"
        else:
            self.provider = provider

        self.embedding_function = self._setup_embedding(self.provider)
        
        # Coleções são separadas por provedor devido à incompatibilidade de dimensões vetoriais
        self.collection = self.client.get_or_create_collection(
            name=f"ancestral_knowledge_{self.provider}",
            embedding_function=self.embedding_function,
            metadata={"description": f"Memória Ancestral Mutante - {self.provider}", "provider": self.provider}
        )
        
        logger.info(f"Ancestral Memory v4.0 iniciada. Provedor: {self.provider} | Path: {self.db_path}")

    def _setup_embedding(self, provider: str):
        if provider == "gemini":
            if not self.api_key:
                logger.warning("GEMINI_API_KEY ausente. Fazendo fallback para Ollama para embeddings.")
                self.provider = "ollama"
                return self._setup_embedding("ollama")
            return embedding_functions.GoogleGenerativeAiEmbeddingFunction(
                api_key=self.api_key,
                model_name="models/embedding-001"
            )
        else:
            logger.info(f"Configurando embeddings locais via Ollama ({self.ollama_url})...")
            return embedding_functions.OllamaEmbeddingFunction(
                url=f"{self.ollama_url}/api/embeddings",
                model_name="mxbai-embed-large"
            )

    def add_knowledge(self, text: str, metadata: Dict[str, Any], doc_id: str):
        """Adiciona um novo fragmento de conhecimento à memória."""
        try:
            # Enriquecimento de metadados
            metadata["archived_at"] = datetime.now().isoformat()
            metadata["provider"] = self.provider
            
            self.collection.add(
                documents=[text],
                metadatas=[metadata],
                ids=[doc_id]
            )
            logger.debug(f"Conhecimento arquivado [{self.provider}]: {doc_id}")
        except Exception as e:
            logger.error(f"Erro ao adicionar conhecimento {doc_id}: {e}")

    def search(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """Realiza busca semântica na memória ativa."""
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
                        "distance": results['distances'][0][i] if results['distances'] else 0,
                        "provider": self.provider
                    })
            return formatted_results
        except Exception as e:
            logger.error(f"Erro na busca semântica ({self.provider}): {e}")
            return []

    def count(self) -> int:
        return self.collection.count()

    def get_all_collections(self):
        return self.client.list_collections()
