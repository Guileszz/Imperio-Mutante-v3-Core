#!/usr/bin/env python3
import sys
import os
import json
from collections import defaultdict

"""
🔱 NEXUS CONSOLIDATOR (V1.0)
Developed by OMNI-SOVEREIGN.
Identifies redundant insights in the Memory Nexus and consolidates them.
Ensures the 'Pure Gold' standard for collective memory.
"""

class NexusConsolidator:
    def __init__(self, nexus_path: str = "/home/team/shared/powers/memory_nexus_db.json"):
        self.nexus_path = nexus_path
        print("[CONSOLIDATOR] Nexus Consolidator Active.")

    def consolidate(self):
        if not os.path.exists(self.nexus_path):
            print("[CONSOLIDATOR] Nexus not found.")
            return

        with open(self.nexus_path, 'r') as f:
            data = json.load(f)

        original_count = len(data)
        unique_insights = {}
        
        for entry in data:
            content = entry['content'].strip()
            # Use a simplified key for matching (lowercased, stripped)
            key = content.lower()
            
            if key not in unique_insights:
                unique_insights[key] = entry
            else:
                # Merge logic: keep the one with more metadata or the later one
                # For now, just keep the existing one but record the merge
                pass

        consolidated_data = list(unique_insights.values())
        new_count = len(consolidated_data)

        with open(self.nexus_path, 'w') as f:
            json.dump(consolidated_data, f, indent=2)

        print(f"[CONSOLIDATOR] Consolidation complete. Reduced {original_count} -> {new_count} units.")
        print(f"[CONSOLIDATOR] Memory Purity increased by {((original_count - new_count)/original_count)*100:.2f}%" if original_count > 0 else "")

if __name__ == "__main__":
    consolidator = NexusConsolidator()
    consolidator.consolidate()
