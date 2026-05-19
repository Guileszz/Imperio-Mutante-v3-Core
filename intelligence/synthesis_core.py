"""
SYNTHESIS CORE v1.0 - Fusão de Alquimia e Brain Drain.
Orquestrador de destilação de conhecimento e geração de planos de ativos.
Protocolo de Síntese Soberana ativado.
"""

import os
import asyncio
import json
import time
import hashlib
import multiprocessing as mp
import glob
import logging
import re
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
from dataclasses import dataclass, asdict
from functools import partial

import httpx
import google.generativeai as genai
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from contextlib import asynccontextmanager

from intelligence.ancestral_memory import AncestralMemory

# =============================================================================
# CONFIGURAÇÃO E LOGGING
# =============================================================================

load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - SYNTHESIS-CORE - %(levelname)s - %(message)s')
logger = logging.getLogger("SYNTHESIS-CORE")

try:
    import redis.asyncio as aioredis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    aioredis = None

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False
    BeautifulSoup = None

# =============================================================================
# WORKER FUNCTIONS (Multi-processing)
# =============================================================================

def _clean_html_worker(raw_html: str) -> str:
    if not BS4_AVAILABLE:
        return raw_html[:5000]
    try:
        soup = BeautifulSoup(raw_html, 'html.parser')
        for element in soup(["script", "style", "nav", "footer", "header", "aside", "noscript"]):
            element.decompose()
        text = soup.get_text(separator="\n", strip=True)
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        return "\n".join(lines)[:10000]
    except Exception:
        return raw_html[:5000]

def _extract_entities_worker(text: str) -> Dict[str, Any]:
    entities = {"models": [], "metrics": [], "links": []}
    model_patterns = [
        r'(?:gpt|claude|gemini|llama|mistral|phi|qwen|mixtral)[\- ]?[0-9]+(?:\.[0-9]+)?',
        r'(?:model|version|v)[0-9]+(?:\.[0-9]+)?',
        r'(?:openai|anthropic|google|meta|microsoft)[\- ]?(?:ai|llm)?',
    ]
    for pattern in model_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        entities["models"].extend(matches[:5])
    metric_patterns = [
        r'\b(?:accuracy|precision|recall|f1|mse|mae|bleu|rouge)[_\s]?(?:score|rate)?\s*[=:]\s*[0-9.]+',
        r'\b[0-9]+(?:\.[0-9]+)?\s*%',
        r'\b(?:benchmark|sota)\s*[=:]\s*[0-9.]+',
    ]
    for pattern in metric_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        entities["metrics"].extend(matches[:5])
    link_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    entities["links"] = re.findall(link_pattern, text)[:10]
    entities["models"] = list(set(entities["models"]))[:10]
    entities["metrics"] = list(set(entities["metrics"]))[:10]
    return entities

def _normalize_text_worker(text: str) -> str:
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\n\s*\n+', r'\n\n', text)
    allowed = re.compile('[^a-zA-Z0-9 .,;:!?()\\[\\]{}]')
    text = allowed.sub('', text)
    return text[:8000].strip()

def _process_chunk_worker(chunk: Dict[str, Any]) -> Dict[str, Any]:
    result = {
        "original_hash": chunk.get("hash", ""),
        "processed_at": datetime.now().isoformat(),
        "status": "success"
    }
    if "html" in chunk:
        result["text"] = _clean_html_worker(chunk["html"])
    elif "raw_text" in chunk:
        result["text"] = _normalize_text_worker(chunk["raw_text"])
    else:
        result["text"] = str(chunk.get("content", ""))[:5000]
    result["entities"] = _extract_entities_worker(result["text"])
    result["content_hash"] = hashlib.sha256(result["text"].encode()).hexdigest()
    return result

# =============================================================================
# DATA DISTILLER
# =============================================================================

class DataDistiller:
    def __init__(self, workers: int = None):
        self.workers = workers or max(mp.cpu_count() - 1, 2)
        self.pool = None
    def start(self):
        self.pool = mp.Pool(processes=self.workers)
    def stop(self):
        if self.pool:
            self.pool.close()
            self.pool.join()
    def distill(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if not self.pool: self.start()
        chunks = [{"hash": hashlib.md5(str(item).encode()).hexdigest(), **item} for item in data]
        return self.pool.map(_process_chunk_worker, chunks)
    async def distill_async(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.distill, data)

# =============================================================================
# KNOWLEDGE STORE
# =============================================================================

@dataclass
class KnowledgeBlock:
    id: str
    content: str
    source: str
    entities: Dict[str, Any]
    nectar_score: float
    timestamp: str
    tags: List[str]
    def to_dict(self) -> Dict[str, Any]: return asdict(self)

class RedisKnowledgeStore:
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis_url = redis_url
        self.redis_client = None
        self.fallback_store: Dict[str, KnowledgeBlock] = {}
        self.connected = False
        if REDIS_AVAILABLE:
            self._connect_task = asyncio.create_task(self._connect())
    async def _connect(self):
        try:
            self.redis_client = await aioredis.from_url(self.redis_url, encoding="utf-8", decode_responses=True)
            await self.redis_client.ping()
            self.connected = True
        except: self.connected = False
    def _generate_id(self, content: str) -> str:
        return hashlib.sha256(content.encode()).hexdigest()[:16]
    async def store(self, block: KnowledgeBlock, is_nectar: bool = False) -> bool:
        prefix = "nectar" if is_nectar else "knowledge"
        try:
            if self.connected and self.redis_client:
                key = f"{prefix}:{block.id}"
                await self.redis_client.hset(key, mapping={
                    "id": block.id,
                    "content": block.content[:8000 if is_nectar else 5000],
                    "source": block.source,
                    "entities": json.dumps(block.entities),
                    "nectar_score": str(block.nectar_score),
                    "timestamp": block.timestamp,
                    "tags": json.dumps(block.tags)
                })
                await self.redis_client.expire(key, 86400 * (30 if is_nectar else 7))
                await self.redis_client.sadd(f"{prefix}:index", block.id)
                return True
            else:
                self.fallback_store[f"{prefix}:{block.id}"] = block
                return True
        except Exception as e:
            logger.error(f"Erro ao armazenar {prefix}: {e}")
            return False
    async def retrieve(self, block_id: str, prefix: str = "knowledge") -> Optional[KnowledgeBlock]:
        try:
            if self.connected and self.redis_client:
                key = f"{prefix}:{block_id}"
                data = await self.redis_client.hgetall(key)
                if data:
                    return KnowledgeBlock(
                        id=data["id"], content=data["content"], source=data["source"],
                        entities=json.loads(data["entities"]), nectar_score=float(data["nectar_score"]),
                        timestamp=data["timestamp"], tags=json.loads(data["tags"])
                    )
            return self.fallback_store.get(f"{prefix}:{block_id}")
        except: return None
    async def search(self, query: str, limit: int = 10) -> List[KnowledgeBlock]:
        results = []
        for block in self.fallback_store.values():
            if query.lower() in block.content.lower():
                results.append(block)
                if len(results) >= limit: break
        return results

# =============================================================================
# SYNTHESIS ENGINE (Merging Brain Drain)
# =============================================================================

class SynthesisCore:
    def __init__(self, redis_url: str = "redis://localhost:6379", legacy_dir: str = "legacy"):
        self.distiller = DataDistiller()
        self.knowledge_store = RedisKnowledgeStore(redis_url)
        self.ancestral_memory = AncestralMemory()
        self.legacy_dir = legacy_dir
        self.distiller.start()
        
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        if self.gemini_key:
            genai.configure(api_key=self.gemini_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            self.model = None
            logger.warning("GEMINI_API_KEY não encontrada para SynthesisCore.")

    async def process_and_store(self, raw_data: List[Dict[str, Any]], source: str = "unknown") -> Dict[str, Any]:
        distilled = await self.distiller.distill_async(raw_data)
        stored_count = 0
        for item in distilled:
            is_nectar = source in ["shadow_market_oracle", "zenith_automation", "shadow_oracle"]
            block = KnowledgeBlock(
                id=self.knowledge_store._generate_id(item.get("text", "")),
                content=item.get("text", ""), source=source,
                entities=item.get("entities", {}),
                nectar_score=item.get("nectar_score", 2.0 if is_nectar else 1.0),
                timestamp=item.get("processed_at", datetime.now().isoformat()),
                tags=["NECTAR"] if is_nectar else []
            )
            if await self.knowledge_store.store(block, is_nectar=is_nectar):
                stored_count += 1
                self.ancestral_memory.add_knowledge(
                    text=block.content,
                    metadata={"source": block.source, "type": "nectar" if is_nectar else "knowledge"},
                    doc_id=f"synthesis_{block.id}"
                )
        return {"processed": len(distilled), "stored": stored_count}

    async def distill_legacy_idea(self, file_path: str) -> Optional[Dict[str, Any]]:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                raw_content = f.read()
            if not raw_content.strip() or not self.model: return None
            
            prompt = f"[SISTEMA: SYNTHESIS CORE - BRAIN DRAIN]\nTransforme o texto legado abaixo em um Plano de Execução Estruturado.\n\n{raw_content}\n\nSAÍDA EM MARKDOWN."
            response = await asyncio.to_thread(self.model.generate_content, prompt)
            return {"file": os.path.basename(file_path), "plan": response.text, "timestamp": datetime.now().isoformat()}
        except Exception as e:
            logger.error(f"Erro ao destilar legado {file_path}: {e}")
            return None

    async def generate_business_plan(self, topic: str = None) -> Dict[str, Any]:
        if not self.model: return {"error": "Gemini indisponível"}
        prompt = f"[SISTEMA: SYNTHESIS CORE - BUSINESS PLANNER]\nGere um plano de negócio JSON para um Micro-SaaS/Bot sobre: {topic or 'Automação IA'}. Retorne APENAS JSON."
        response = await asyncio.to_thread(self.model.generate_content, prompt)
        content = response.text
        try:
            if "```json" in content: content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content: content = content.split("```")[1].split("```")[0].strip()
            return json.loads(content)
        except: return {"error": "Falha ao decodificar JSON do plano"}

    def scan_legacy_files(self) -> List[str]:
        pattern = os.path.join(self.legacy_dir, "*.txt")
        return glob.glob(pattern)

    async def run(self):
        """Executa o processo completo de Brain Drain / Legacy Distillation."""
        files = self.scan_legacy_files()
        if not files:
            logger.info("Nenhum arquivo legado encontrado.")
            return []
        results = []
        for f in files:
            plan = await self.distill_legacy_idea(f)
            if plan:
                # Armazena o plano na base de conhecimento
                block = KnowledgeBlock(
                    id=self.knowledge_store._generate_id(plan["plan"]),
                    content=plan["plan"], source=f"legacy:{plan['file']}",
                    entities={}, nectar_score=1.5, timestamp=plan["timestamp"],
                    tags=["LEGACY_IDEA", "EXECUTION_PLAN"]
                )
                success = await self.knowledge_store.store(block)
                results.append({"file": f, "success": success})
        return results

    def stop(self):
        self.distiller.stop()

# =============================================================================
# API
# =============================================================================

processor: SynthesisCore = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global processor
    processor = SynthesisCore()
    yield
    processor.stop()

app = FastAPI(title="Synthesis Core v1.0", lifespan=lifespan)

class DistillRequest(BaseModel):
    items: List[Dict[str, Any]]
    source: str = "unknown"

@app.post("/distill")
async def distill(request: DistillRequest):
    result = await processor.process_and_store(request.items, request.source)
    return {"status": "success", "result": result}

@app.get("/health")
async def health():
    return {"status": "operational", "workers": processor.distiller.workers}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
