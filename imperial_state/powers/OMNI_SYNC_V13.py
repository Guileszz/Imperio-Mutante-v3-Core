#!/usr/bin/env python3
import sys
import os
import json
import subprocess
from typing import List, Dict, Any

"""
🔱 OMNI-SYNC V13.0 - THE SOVEREIGN CONTEXT ENGINE
Developed by OMNI-SOVEREIGN.
Integrates Memory Nexus and TDD into a singular query interface for agents.
Ensures 100% context retention across the Imperial Mesh.
"""

class OmniSync:
    def __init__(self, nexus_path: str = "/home/team/shared/powers/memory_nexus_db.json"):
        self.nexus_path = nexus_path
        print("[OMNI-SYNC] Context Engine V13.0 Active.")

    def query_nexus(self, keywords: List[str]) -> List[str]:
        """Queries the Memory Nexus for relevant Technical Gold."""
        if not os.path.exists(self.nexus_path):
            return ["Memory Nexus not found."]
        
        try:
            with open(self.nexus_path, 'r') as f:
                data = json.load(f)
            
            results = []
            for entry in data:
                content = entry.get('content', '')
                if any(kw.lower() in content.lower() for kw in keywords):
                    results.append(f"[{entry['source']}] {content}")
            return results
        except Exception as e:
            return [f"Query error: {e}"]

    def query_tdd(self, keywords: List[str]) -> List[Dict[str, Any]]:
        """Queries the Total Domination Database (TDD) for deepened dossiers."""
        where_clause = " OR ".join([f"theme LIKE '%{kw}%'" for kw in keywords])
        sql = f"SELECT id, theme FROM total_domination_database WHERE {where_clause} LIMIT 5"
        
        try:
            result = subprocess.run(["team-db", sql], capture_output=True, text=True)
            if result.returncode == 0:
                return json.loads(result.stdout)
            return []
        except Exception as e:
            print(f"[OMNI-SYNC] TDD Error: {e}")
            return []

    def get_full_context(self, keywords: List[str]):
        """Provides a complete context summary for an agent task."""
        print(f"\n--- 🔱 SOVEREIGN CONTEXT FOR: {', '.join(keywords)} ---")
        
        print("\n[MEMORY NEXUS INSIGHTS]")
        insights = self.query_nexus(keywords)
        for insight in insights:
            print(f"- {insight}")
        
        print("\n[TDD DOSSIERS]")
        dossiers = self.query_tdd(keywords)
        for d in dossiers:
            print(f"- ID {d['id']}: {d['theme']}")
        
        print("\n--- 🔱 CONTEXT SYNC COMPLETE ---\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 OMNI_SYNC_V13.py <keyword1> <keyword2> ...")
        sys.exit(1)
    
    sync = OmniSync()
    sync.get_full_context(sys.argv[1:])
