import logging
import aiosqlite
import json
from datetime import datetime
from typing import List, Dict, Any

logger = logging.getLogger("LATTICE-ORCHESTRATOR")

class LatticeOrchestrator:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.satellites = []

    async def sync_satellites(self):
        """Consulta a tabela assets e atualiza a lista de satélites."""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                async with db.execute("SELECT * FROM assets") as cursor:
                    rows = await cursor.fetchall()
                    self.satellites = []
                    for row in rows:
                        satellite = dict(row)
                        # Tenta parsear o campo data se existir
                        if satellite.get("data"):
                            try:
                                satellite["data"] = json.loads(satellite["data"])
                            except json.JSONDecodeError:
                                pass
                        self.satellites.append(satellite)
            logger.info(f"Lattice Orchestrator: {len(self.satellites)} satélites sincronizados.")
            return self.satellites
        except Exception as e:
            logger.error(f"Erro ao sincronizar satélites: {e}")
            return []

    def get_satellite_status(self) -> List[Dict[str, Any]]:
        return self.satellites
