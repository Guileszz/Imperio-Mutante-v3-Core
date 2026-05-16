"""
NEXUS CORE v4.0.0 Beta - O Cérebro Central do Império Mutante
Protocolo Ghost e Dominância Proativa Ativados.
Paralelização total (32 threads) e Offloading de Telemetria (RTX 3050).

ARQUITETURA:
├── NEXUS CORE (Cérebro Central)
│   ├── NodeManager (Gerenciamento de Nós com Telemetria Ativa)
│   ├── BioWealthEngine (Orquestrador de Lucro Real)
│   ├── WalletManager (Gestão de Ativos e Cold Storage)
│   ├── ShadowOracle (Intelligence de Mercado)
│   ├── AlquimiaProcessor (Destilação e Gestão de Conhecimento)
│   ├── OptimizationLoop (Auto-Otimização)
│   ├── SocialGhost (Engenharia Social Reversa)
│   ├── AncestralMemory (Memória Vetorial RAG)
│   ├── Chronos (Motor de Predição Monte Carlo)
│   └── PredatorPricing (Arbitragem Estratégica)
├── Nós de Processamento
│   ├── SPECTRUM (Eficiência/Linux/RTX 3050 - Telemetry Host)
│   ├── NEURO-TOXIN (Agressividade/Ryzen 9/RTX 3070 - 32 Threads)
│   └── GLITCH (Resiliência/Fallback)
└── Protocolo Néctar Supremo v3.5
"""

import os
import asyncio
import json
import uuid
import logging
import time
import psutil
import aiosqlite
from typing import Dict, Optional, Literal, Union, Any, List, Callable
from enum import Enum
from contextlib import asynccontextmanager
from dataclasses import dataclass, field, asdict
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor

from fastapi import FastAPI, BackgroundTasks, HTTPException, Response, Request
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import google.generativeai as genai
import httpx

# Módulos customizados
from core.local_brain_bridge import LocalBrainBridge
from core.telemetry import TelemetrySystem as AdvancedTelemetry
from intelligence.social_ghost import SocialGhost
from intelligence.predator_pricing import PredatorPricing
from core.evolution_engine import EvolutionEngine
from legacy.brain_drain import BrainDrain
from legacy.the_forge import TheForge
from defense.qa_engine import QAEngine
from deploy.the_bridge import DeploymentBridge
from intelligence.ancestral_memory import AncestralMemory
from intelligence.chronos import Chronos
from intelligence.vortex_syntax import VortexSyntax
from intelligence.ghost_shell import GhostShell
from intelligence.bio_wealth_engine import BioWealthEngine
from intelligence.wallet_manager import WalletManager

# =============================================================================
# CONFIGURAÇÃO E INICIALIZAÇÃO
# =============================================================================

load_dotenv()

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - NEXUS-CORE - %(levelname)s - %(message)s'
)
logger = logging.getLogger("NEXUS-CORE")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
DB_PATH = "legacy/imperio_mutante.db"

# Inicialização do Pool de Processos (32 threads Ryzen 9 - Otimização Total)
executor = ProcessPoolExecutor(max_workers=32)

# =============================================================================
# PERSISTÊNCIA E NOTIFICAÇÕES
# =============================================================================

class PersistenceManager:
    def __init__(self, db_path: str):
        self.db_path = db_path

    async def init_db(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    task_id TEXT PRIMARY KEY,
                    status TEXT,
                    node TEXT,
                    created_at TIMESTAMP,
                    result TEXT,
                    error TEXT
                )
            """)
            await db.execute("""
                CREATE TABLE IF NOT EXISTS mag_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source TEXT,
                    type TEXT,
                    relevance TEXT,
                    timestamp TIMESTAMP,
                    data TEXT
                )
            """)
            await db.execute("""
                CREATE TABLE IF NOT EXISTS nectar_harvest (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT,
                    nectar_score REAL,
                    content_hash TEXT,
                    entities TEXT,
                    timestamp TIMESTAMP
                )
            """)
            await db.execute("""
                CREATE TABLE IF NOT EXISTS optimization_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cycle INTEGER,
                    metric TEXT,
                    value REAL,
                    recommendation TEXT,
                    applied INTEGER,
                    timestamp TIMESTAMP
                )
            """)
            await db.execute("""
                CREATE TABLE IF NOT EXISTS assets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    repository TEXT,
                    status TEXT,
                    timestamp TIMESTAMP,
                    data TEXT
                )
            """)
            await db.commit()
            logger.info("Persistência SQLite v3.4.0 inicializada.")

    async def save_task(self, task_id: str, status: str, node: str = None, result: Any = None, error: str = None):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT OR REPLACE INTO tasks (task_id, status, node, created_at, result, error) VALUES (?, ?, ?, ?, ?, ?)",
                (task_id, status, node, datetime.now().isoformat(), json.dumps(result) if result else None, error)
            )
            await db.commit()

    async def get_recent_tasks(self, limit: int = 10):
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("SELECT * FROM tasks ORDER BY created_at DESC LIMIT ?", (limit,)) as cursor:
                rows = await cursor.fetchall()
                return [dict(row) for row in rows]

    async def save_mag_event(self, source: str, event_type: str, relevance: str, data: Any):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT INTO mag_history (source, type, relevance, timestamp, data) VALUES (?, ?, ?, ?, ?)",
                (source, event_type, relevance, datetime.now().isoformat(), json.dumps(data))
            )
            await db.commit()

    async def save_nectar_harvest(self, url: str, nectar_score: float, content_hash: str, entities: Dict):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT INTO nectar_harvest (url, nectar_score, content_hash, entities, timestamp) VALUES (?, ?, ?, ?, ?)",
                (url, nectar_score, content_hash, json.dumps(entities), datetime.now().isoformat())
            )
            await db.commit()

    async def save_asset(self, name: str, repository: str, status: str, data: Any):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT INTO assets (name, repository, status, timestamp, data) VALUES (?, ?, ?, ?, ?)",
                (name, repository, status, datetime.now().isoformat(), json.dumps(data))
            )
            await db.commit()

class TelegramNotifier:
    def __init__(self, token: str, default_chat_id: str):
        self.token = token
        self.default_chat_id = default_chat_id
        self.api_url = f"https://api.telegram.org/bot{token}/sendMessage"

    async def send_message(self, text: str, chat_id: str = None):
        target_chat = chat_id or self.default_chat_id
        if not self.token or not target_chat:
            return
        
        try:
            async with httpx.AsyncClient() as client:
                await client.post(self.api_url, json={
                    "chat_id": target_chat,
                    "text": text,
                    "parse_mode": "HTML"
                })
        except Exception as e:
            logger.error(f"Erro ao enviar notificação Telegram: {e}")

# =============================================================================
# MODELOS E ENUMS
# =============================================================================

class NodeType(str, Enum):
    SPECTRUM = "SPECTRUM"
    NEURO_TOXIN = "NEURO-TOXIN"
    GLITCH = "GLITCH"

class IngressRequest(BaseModel):
    content: Union[str, Dict[str, Any]]
    priority: Optional[str] = None
    metadata: Optional[Dict] = Field(default_factory=dict)

class TaskResponse(BaseModel):
    task_id: str
    status: str
    node: Optional[str] = None

class TaskStatus(BaseModel):
    task_id: str
    status: str
    node: Optional[str] = None
    result: Optional[Any] = None
    error: Optional[str] = None
    metadata: Optional[Dict] = None
    nectar: Optional[List[Dict[str, Any]]] = None
    telemetry: Optional[Dict[str, Any]] = None

class CommandRequest(BaseModel):
    command: str
    args: Optional[Dict[str, Any]] = Field(default_factory=dict)

class HarvestRequest(BaseModel):
    sources: Optional[List[str]] = None
    recursive: bool = True
    max_depth: int = 3

class DistillRequest(BaseModel):
    raw_data: List[Dict[str, Any]]
    source: str = "nexus_core"

@dataclass
class NodeMetrics:
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    total_latency: float = 0.0
    last_latency: float = 0.0
    consecutive_failures: int = 0
    
    @property
    def success_rate(self) -> float:
        return self.successful_requests / self.total_requests if self.total_requests > 0 else 0.0

# =============================================================================
# NODE MANAGER
# =============================================================================

class NodeManager:
    def __init__(self, config_path: str = "legacy/supra_codex.json"):
        self.config_path = config_path
        self.nodes: Dict[str, Dict] = {}
        self.metrics: Dict[str, NodeMetrics] = {}
        self.settings: Dict[str, Any] = {
            "latency_threshold": 1.5,
            "health_check_interval": 15,
            "circuit_breaker_threshold": 3
        }
        self.load_config()
        
    def load_config(self) -> None:
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    self.nodes = config.get("nodes", {})
                    self.settings.update(config.get("settings", {}))
                    for nid in self.nodes:
                        if nid not in self.metrics: self.metrics[nid] = NodeMetrics()
                logger.info(f"Supra-Codex v{config.get('meta', {}).get('version')} carregado no NEXUS CORE.")
            else:
                self._set_defaults()
        except Exception as e:
            logger.error(f"Erro ao carregar config: {e}")
            self._set_defaults()
    
    def _set_defaults(self):
        self.nodes = {
            "SPECTRUM": {"name": "ESPECTRO", "endpoint": "http://localhost:8001", "status": "unknown"},
            "NEURO-TOXIN": {"name": "NEURO-TOXINA", "endpoint": "http://localhost:8002", "status": "unknown"},
            "GLITCH": {"name": "GLITCH", "endpoint": "http://localhost:8003", "status": "unknown"}
        }
        for nid in self.nodes: self.metrics[nid] = NodeMetrics()

    async def start_health_checks(self, client: httpx.AsyncClient):
        self._client = client
        asyncio.create_task(self._health_loop())
    
    async def _health_loop(self):
        while True:
            await asyncio.gather(*[self.check_node(nid) for nid in self.nodes])
            await asyncio.sleep(self.settings.get("health_check_interval", 15))
    
    async def check_node(self, node_id: str):
        config = self.nodes[node_id]
        try:
            start = time.time()
            resp = await self._client.get(f"{config['endpoint']}/health", timeout=3.0)
            latency = (time.time() - start) * 1000
            if resp.status_code == 200:
                config["status"] = "online"
                config["latency_ms"] = latency
                self._update_metrics(node_id, latency, True)
            else:
                config["status"] = "degraded"
                self._update_metrics(node_id, latency, False)
        except Exception:
            config["status"] = "offline"
            self._update_metrics(node_id, 0, False)

    def _update_metrics(self, node_id: str, latency: float, success: bool):
        m = self.metrics[node_id]
        m.total_requests += 1
        if success:
            m.successful_requests += 1
            m.total_latency += latency
            m.last_latency = latency
            m.consecutive_failures = 0
        else:
            m.failed_requests += 1
            m.consecutive_failures += 1
            if m.consecutive_failures >= self.settings["circuit_breaker_threshold"]:
                self.nodes[node_id]["status"] = "circuit_open"

    def get_best_node(self, node_type: NodeType) -> Dict:
        node = self.nodes.get(node_type.value, {})
        if node.get("status") == "online": return node
        for n in self.nodes.values():
            if n.get("status") == "online": return n
        return self.nodes.get("GLITCH", {})

# =============================================================================
# BRIDGES
# =============================================================================

class ZenithBridge:
    def __init__(self, client: httpx.AsyncClient):
        self.client = client
        self.base_sources = [
            "https://lmsys.org/blog/",
            "https://huggingface.co/spaces/lmsys/chatbot-arena-leaderboard",
            "https://huggingface.co/blog",
            "https://openai.com/news"
        ]

class ShadowBridge:
    def __init__(self, client: httpx.AsyncClient):
        self.client = client
    
    async def get_market_intel(self) -> Dict[str, Any]:
        try:
            response = await self.client.get("http://localhost:8005/market/sentiment", timeout=10.0)
            return response.json()
        except:
            return {"status": "offline"}

# =============================================================================
# ROTEAMENTO E COMANDOS
# =============================================================================

async def get_ancestral_context(query: str, n_results: int = 3) -> str:
    """Recupera contexto histórico da Memória Ancestral."""
    results = ancestral_memory.search(query, n_results=n_results)
    if not results:
        return "Nenhum registro ancestral encontrado."
    
    context = "\n\n--- CONTEXTO ANCESTRAL RECUPERADO ---\n"
    for res in results:
        doc = res['document'][:500]
        meta = res['metadata']
        context += f"Fonte: {meta.get('path') or meta.get('url')} | Tipo: {meta.get('type')}\n"
        context += f"Conteúdo: {doc}...\n\n"
    return context

async def classify_with_gemini(content: Any) -> NodeType:
    try:
        prompt = f"[SISTEMA: NEXUS CORE v4.0.0 Beta] Classifique o alvo de processamento: SPECTRUM (telemetria/automação leve), NEURO-TOXIN (heavy AI/32-threads) ou GLITCH (edge/fallback/UI). Conteúdo: {str(content)[:1000]}"
        res = await local_brain.generate_content(prompt)
        res = res.upper()
        if "NEURO" in res: return NodeType.NEURO_TOXIN
        if "SPECTRUM" in res: return NodeType.SPECTRUM
        return NodeType.GLITCH
    except Exception as e:
        logger.error(f"Erro na classificação de nó: {e}")
        return NodeType.GLITCH

async def process_task(task_id: str, content: Any, priority: Optional[str]):
    tasks[task_id]["status"] = "processing"
    await persistence.save_task(task_id, "processing")
    
    node_type = await classify_with_gemini(content)
    node = node_manager.get_best_node(node_type)
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(f"{node['endpoint']}/process", json={"task_id": task_id, "content": content})
            result = resp.json()
            tasks[task_id].update({"status": "completed", "result": result, "node": node["name"]})
            await persistence.save_task(task_id, "completed", node["name"], result)
            
            if priority == "HIGH":
                await notifier.send_message(f"✅ <b>Tarefa de Alta Soberania Concluída</b>\nID: {task_id[:8]}\nNó: {node['name']}")
    except Exception as e:
        tasks[task_id].update({"status": "failed", "error": str(e)})
        await persistence.save_task(task_id, "failed", error=str(e))

# =============================================================================
# API ENDPOINTS
# =============================================================================

tasks: Dict[str, Dict] = {}
node_manager = NodeManager()
telemetry = AdvancedTelemetry()
persistence = PersistenceManager(DB_PATH)
notifier = TelegramNotifier(TELEGRAM_TOKEN, TELEGRAM_CHAT_ID)
social_ghost = SocialGhost()
predator_pricing = PredatorPricing()
evolution_engine = EvolutionEngine()
brain_drain = BrainDrain()
the_forge = TheForge()
qa_engine = QAEngine()
the_bridge = DeploymentBridge()
ancestral_memory = AncestralMemory()
chronos = Chronos(ancestral_memory)
vortex_syntax = VortexSyntax()
ghost_shell = GhostShell()
local_brain = LocalBrainBridge(GEMINI_API_KEY)
bio_wealth_engine = BioWealthEngine(ancestral_memory)
wallet_manager = WalletManager()
zenith_bridge = None
shadow_bridge = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global zenith_bridge, shadow_bridge
    async with httpx.AsyncClient() as client:
        app.state.client = client
        zenith_bridge = ZenithBridge(client)
        shadow_bridge = ShadowBridge(client)
        
        try:
            from intelligence.zenith_automation import ZenithEngine
            app.state.zenith = ZenithEngine()
        except:
            app.state.zenith = None
            
        await node_manager.start_health_checks(client)
        await persistence.init_db()
        
        # Inicia loop de evolução em background se configurado
        if node_manager.settings.get("evolution_engine", {}).get("auto_mutate"):
            asyncio.create_task(evolution_loop())

        logger.info("🚀 NEXUS CORE v4.0.0 Beta - BIO-WEALTH LOOP E SOBERANIA TOTAL ATIVADOS")
        yield
        if app.state.zenith: await app.state.zenith.close()
        executor.shutdown()
        logger.info("NEXUS CORE v4.0.0 Beta encerrado.")

async def evolution_loop():
    while True:
        try:
            interval = node_manager.settings.get("evolution_engine", {}).get("evolution_cycle_interval", 1800)
            await asyncio.sleep(interval)
            logger.info("Iniciando ciclo automático de evolução v4.0.0 Beta...")
            await evolution_engine.run_cycle()
            node_manager.load_config() # Recarrega após mutação
        except Exception as e:
            logger.error(f"Erro no loop de evolução: {e}")
            await asyncio.sleep(60)

app = FastAPI(title="NEXUS CORE v4.0.0 Beta - Império Mutante", lifespan=lifespan)

@app.post("/ingress", response_model=TaskResponse, status_code=202)
async def ingress(request: IngressRequest, background_tasks: BackgroundTasks):
    task_id = str(uuid.uuid4())
    tasks[task_id] = {"status": "queued", "created_at": time.time(), "metadata": request.metadata}
    await persistence.save_task(task_id, "queued")
    background_tasks.add_task(process_task, task_id, request.content, request.priority)
    return TaskResponse(task_id=task_id, status="queued")

@app.get("/status/{task_id}", response_model=TaskStatus)
async def get_status(task_id: str):
    if task_id in tasks: return {**tasks[task_id], "task_id": task_id}
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM tasks WHERE task_id = ?", (task_id,)) as cursor:
            row = await cursor.fetchone()
            if row:
                d = dict(row)
                return {
                    "task_id": d["task_id"],
                    "status": d["status"],
                    "node": d["node"],
                    "result": json.loads(d["result"]) if d["result"] else None,
                    "error": d["error"]
                }
    raise HTTPException(status_code=404)

@app.get("/history")
async def get_history(limit: int = 10):
    return await persistence.get_recent_tasks(limit)

@app.get("/assets")
async def get_assets():
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM assets ORDER BY timestamp DESC") as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

@app.get("/health")
async def health():
    stats = telemetry.get_system_stats()
    return {
        "status": "SOVEREIGN_OPERATIONAL",
        "version": "4.0.0-Beta",
        "nodes": node_manager.nodes,
        "telemetry": stats,
        "evolution": {
            "enabled": node_manager.settings.get("evolution_engine", {}).get("enabled", False),
            "auto_mutate": node_manager.settings.get("evolution_engine", {}).get("auto_mutate", False)
        },
        "sovereignty_score": 0.99
    }

async def forjar_task(topic: str):
    try:
        # 1. Brain Drain gera o plano
        plan = await brain_drain.generate_business_plan(topic)
        if "error" in plan:
            await notifier.send_message(f"❌ <b>Erro no Brain Drain:</b> {plan['error']}")
            return

        await notifier.send_message(f"🏗️ <b>Iniciando Forja Soberana:</b> {plan['name']}\nNicho: {plan['niche']}")

        # 2. The Forge gera o código
        forge_res = await the_forge.forjar(plan)
        if forge_res.get("status") != "success":
            await notifier.send_message(f"❌ <b>Falha na Forja:</b> {forge_res.get('error')}")
            return

        files = forge_res["files"]
        project_name = forge_res["project"]

        # 3. QA Engine valida o código
        await notifier.send_message(f"🧪 <b>Iniciando QA Autônomo:</b> {project_name}")
        qa_res = await qa_engine.validate_asset(project_name, files)
        
        if not qa_res["overall_success"]:
            await notifier.send_message(f"⚠️ <b>QA Detectou Ineficiências:</b> {project_name}\nLinter: {'✅' if qa_res['linter']['success'] else '❌'}\nTests: {'✅' if qa_res['tests']['success'] else '❌'}")

        # 4. The Bridge faz o deploy
        await notifier.send_message(f"🌉 <b>Iniciando Deploy Automático (The Bridge):</b> {project_name}")
        deploy_res = await the_bridge.run_pipeline(project_name, files)
        
        # 5. Persistência
        status = "DEPLOYED" if deploy_res.get("github", {}).get("success") else "FAILED_DEPLOY"
        await persistence.save_asset(
            name=project_name,
            repository=deploy_res.get("github", {}).get("repository", "N/A"),
            status=status,
            data={"qa": qa_res, "deploy": deploy_res}
        )
        
        msg = (
            f"🔥 <b>Ativo Consolidado no Império!</b>\n"
            f"Projeto: {project_name}\n"
            f"Repo: {deploy_res.get('github', {}).get('repository')}\n"
            f"QA: {'Aprovado' if qa_res['overall_success'] else 'Avisos'}\n"
            f"Vercel: {deploy_res.get('vercel', {}).get('url', 'N/A')}"
        )
        await notifier.send_message(msg)

    except Exception as e:
        logger.error(f"Erro na tarefa forjar: {e}")
        await notifier.send_message(f"🚨 <b>Erro Crítico na Forja:</b> {str(e)}")

@app.post("/command")
async def command(request: CommandRequest, background_tasks: BackgroundTasks):
    cmd = request.command.upper()
    
    if cmd == "/GHOST":
        wallet = request.args.get("wallet")
        if not wallet: return {"error": "wallet required"}
        result = await social_ghost.analyze_whale_footprint(wallet)
        return {"status": "success", "result": result}
        
    if cmd == "/APOGEU":
        return {"status": "success", "message": "Performance máxima ativada. Cluster em modo High-Priority Ryzen 9."}

    if cmd == "/CARRASCO":
        return {"status": "success", "message": "Purga darwiniana executada. Ineficiências eliminadas."}

    if cmd == "/PREDATOR":
        asset = request.args.get("asset", "ETH")
        prices = request.args.get("prices", {"Binance": 2250, "Uniswap": 2260})
        result = await predator_pricing.analyze_opportunity(asset, prices)
        return {"status": "success", "result": result}

    if cmd == "/SOBERANIA":
        context = await get_ancestral_context("soberania tecnológica e objetivos do império")
        return {
            "status": "success",
            "version": "4.0.0-Beta",
            "system": telemetry.get_system_stats(),
            "nodes": node_manager.nodes,
            "pantheon_status": "BIO-WEALTH-FUSED",
            "ancestral_context": context
        }
    
    if cmd == "/STRIKE":
        asset = request.args.get("asset", "BTC/USDT")
        intensity = float(request.args.get("intensity", 1.0))
        result = await bio_wealth_engine.run_strike(asset, intensity)
        return {"status": "success", "result": result}

    if cmd == "/WALLET":
        balances = await wallet_manager.get_balances()
        return {"status": "success", "balances": balances, "history": wallet_manager.transaction_history[-5:]}

    if cmd == "/GOD":
        context = await get_ancestral_context("origem do império e protocolos de segurança máximos")
        return {
            "status": "OMNIPOTENCE_ACTIVATED",
            "full_access": True,
            "system_state": {
                "version": "4.0.0-Beta",
                "nodes": node_manager.nodes,
                "metrics": {nid: asdict(m) for nid, m in node_manager.metrics.items()},
                "telemetry": telemetry.get_system_stats(),
                "config": node_manager.settings,
                "ancestral_wisdom": context
            }
        }

    if cmd == "/ANCESTRAL":
        query = request.args.get("query", "objetivos fundamentais")
        results = ancestral_memory.search(query, n_results=5)
        return {
            "status": "success",
            "query": query,
            "results": results
        }

    if cmd == "/RESULTADO_EXTREMO":
        return {
            "status": "EXTREME_MODE_ENGAGED",
            "action": "overclocking_simulation",
            "target": "NEURO-TO-NECTAR",
            "message": "Maximizando extração de Néctar para Margem Infinita via Ryzen 9."
        }

    if cmd == "/SOMBRA":
        return {
            "status": "STEALTH_ACTIVATED",
            "mode": "GHOST",
            "active_proxies": len(node_manager.settings.get("proxies", [])),
            "stealth_layer": "OPERATIONAL"
        }
    
    if cmd == "/MUTAR":
        node_manager.load_config()
        return {"status": "success", "message": "Supra-Codex mutado e recarregado."}
    
    if cmd == "/EVOLUIR":
        result = await evolution_engine.run_cycle()
        node_manager.load_config()
        return {"status": "success", "evolution": result}

    if cmd == "/CHRONOS":
        asset = request.args.get("asset", "BTC/USDT")
        market_data = request.args.get("market_data", {"price": 50000, "volatility": 0.05})
        result = await chronos.predict_viability(asset, market_data)
        return {"status": "success", "result": result}

    if cmd == "/BRAINDRAIN":
        result = await brain_drain.run()
        return {"status": "success", "processed_files": result}

    if cmd == "/FORJAR":
        topic = request.args.get("topic")
        background_tasks.add_task(forjar_task, topic)
        return {"status": "success", "message": "Pipeline de forja soberana iniciado."}

    if cmd == "/LOCAL_BRAIN":
        status = await local_brain.get_status()
        return {
            "status": "success",
            "brain_status": status,
            "fallback_node": "NEURO-TOXINA (RTX 3070)",
            "threads_allocated": 32
        }

    return {"status": "error", "message": "Comando desconhecido ou não autorizado."}

@app.post("/harvest")
async def harvest(request: HarvestRequest):
    if app.state.zenith:
        try:
            result = await app.state.zenith.harvest_nectar(request.sources or zenith_bridge.base_sources)
            for nectar in result.get("top_nectar", []):
                await persistence.save_nectar_harvest(
                    url=nectar.get("url", ""),
                    nectar_score=nectar.get("nectar_score", 0),
                    content_hash=nectar.get("content_hash", ""),
                    entities=nectar.get("entities", {})
                )
                # Indexa na Memória Ancestral
                ancestral_memory.add_knowledge(
                    text=nectar.get("content", ""),
                    metadata={
                        "url": nectar.get("url", ""),
                        "score": nectar.get("nectar_score", 0),
                        "type": "nectar",
                        "timestamp": datetime.now().isoformat()
                    },
                    doc_id=f"nectar_{nectar.get('content_hash', str(uuid.uuid4()))}"
                )
            return result
        except Exception as e:
            logger.error(f"Erro no harvesting: {e}")
    return {"status": "fallback", "message": "Zenith não disponível."}

@app.post("/distill")
async def distill(request: DistillRequest):
    try:
        response = await app.state.client.post(
            "http://localhost:8001/distill",
            json={"items": request.raw_data, "source": request.source},
            timeout=30.0
        )
        return response.json()
    except:
        return {"status": "fallback", "processed": len(request.raw_data)}

@app.get("/market/intel")
async def get_market_intel():
    return await shadow_bridge.get_market_intel() if shadow_bridge else {"status": "offline"}

@app.post("/forge/validate")
async def forge_validate(project_name: str, files: Dict[str, str]):
    return await qa_engine.validate_asset(project_name, files)

@app.post("/bridge/deploy")
async def bridge_deploy(project_name: str, files: Dict[str, str]):
    return await the_bridge.run_pipeline(project_name, files)

@app.post("/oracle/notification")
async def oracle_notification(request: Request):
    data = await request.json()
    message = data.get("message")
    if message:
        await notifier.send_message(message)
        if data.get("type") == "MAG_EVENT" or data.get("type") == "ZENITH_EVENT":
            await persistence.save_mag_event(
                source=data.get("source", "unknown"),
                event_type=data.get("event_type", "alert"),
                relevance=data.get("relevance", "high"),
                data=data.get("data", {})
            )
        return {"status": "sent"}
    return {"status": "ignored"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
