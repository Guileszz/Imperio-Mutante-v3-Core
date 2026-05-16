"""
QA ENGINE v3.3.0 - Validação Contínua de Estado e Integridade
Valida conectividade dos nós, latência de API e integridade do DB.
"""

import os
import subprocess
import logging
import json
import httpx
import asyncio
import aiosqlite
from typing import Dict, Any, List
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - QA-ENGINE - %(levelname)s - %(message)s')
logger = logging.getLogger("QA-ENGINE")

class QAEngine:
    def __init__(self, db_path: str = "imperio_mutante.db"):
        self.reports_dir = "qa_reports"
        self.db_path = db_path
        os.makedirs(self.reports_dir, exist_ok=True)

    async def validate_system_health(self, nodes: Dict[str, Any]) -> Dict[str, Any]:
        """Valida a saúde de todo o ecossistema."""
        results = {
            "timestamp": datetime.now().isoformat(),
            "nodes_health": {},
            "db_integrity": False,
            "api_latency": {}
        }

        # 1. Validar Nós
        async with httpx.AsyncClient() as client:
            for node_id, config in nodes.items():
                try:
                    start = asyncio.get_event_loop().time()
                    resp = await client.get(f"{config['endpoint']}/health", timeout=2.0)
                    latency = (asyncio.get_event_loop().time() - start) * 1000
                    results["nodes_health"][node_id] = {
                        "status": "online" if resp.status_code == 200 else "degraded",
                        "latency_ms": latency
                    }
                except Exception:
                    results["nodes_health"][node_id] = {"status": "offline", "latency_ms": -1}

        # 2. Validar Integridade do DB
        try:
            async with aiosqlite.connect(self.db_path) as db:
                async with db.execute("PRAGMA integrity_check") as cursor:
                    row = await cursor.fetchone()
                    results["db_integrity"] = (row[0] == "ok")
        except Exception as e:
            logger.error(f"Erro ao verificar DB: {e}")
            results["db_integrity"] = False

        return results

    def run_linter(self, project_path: str) -> Dict[str, Any]:
        """Executa flake8 para verificar conformidade com PEP8."""
        logger.info(f"Executando linter em: {project_path}")
        try:
            result = subprocess.run(
                ["flake8", project_path, "--max-line-length=120", "--exclude=venv,.git"],
                capture_output=True,
                text=True
            )
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "errors": result.stderr
            }
        except Exception as e:
            logger.error(f"Erro ao executar flake8: {e}")
            return {"success": False, "error": str(e)}

    def run_tests(self, project_path: str) -> Dict[str, Any]:
        """Executa pytest para rodar testes unitários."""
        logger.info(f"Executando testes em: {project_path}")
        try:
            result = subprocess.run(
                ["pytest", project_path, "--json-report", "--json-report-file=report.json"],
                capture_output=True,
                text=True,
                cwd=project_path
            )
            
            report_path = os.path.join(project_path, "report.json")
            report_data = {}
            if os.path.exists(report_path):
                with open(report_path, "r") as f:
                    report_data = json.load(f)
            
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "report": report_data
            }
        except Exception as e:
            logger.error(f"Erro ao executar pytest: {e}")
            return {"success": False, "error": str(e)}

    async def validate_asset(self, project_name: str, files: Dict[str, str]) -> Dict[str, Any]:
        """Valida um conjunto de arquivos."""
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            for file_name, content in files.items():
                file_path = os.path.join(tmpdir, file_name)
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
            
            linter_res = self.run_linter(tmpdir)
            test_res = {"success": True, "message": "Nenhum teste encontrado"}
            has_tests = any(f.startswith("test_") or f.endswith("_test.py") for f in files.keys())
            if has_tests:
                test_res = self.run_tests(tmpdir)
            
            overall_success = linter_res["success"] and test_res["success"]
            
            report = {
                "project": project_name,
                "timestamp": datetime.now().isoformat(),
                "overall_success": overall_success,
                "linter": linter_res,
                "tests": test_res
            }
            
            report_file = os.path.join(self.reports_dir, f"{project_name}_qa.json")
            with open(report_file, "w") as f:
                json.dump(report, f, indent=2)
            
            return report
