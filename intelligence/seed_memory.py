import asyncio
import os
import sys

# Adiciona o diretório atual ao path para permitir importações
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from intelligence.brain_drain import BrainDrain
from intelligence.alquimia_processing import AlquimiaProcessor

async def seed_memory():
    print("Iniciando seeding da Memória Ancestral...")
    
    # Instancia o processador Alquimia (que inicializa a AncestralMemory)
    processor = AlquimiaProcessor()
    
    # Instancia o BrainDrain
    drain = BrainDrain(legacy_dir="legacy")
    
    # 1. Escanear arquivos legados
    files = drain.scan_legacy_files()
    print(f"Arquivos encontrados: {files}")
    
    for file_path in files:
        print(f"Processando {file_path}...")
        # Destila a ideia usando Gemini (se disponível) ou apenas lê o conteúdo
        plan = await drain.distill_idea(file_path)
        
        if plan:
            content = plan.get("plan", "")
            source = f"legacy:{plan.get('file', 'unknown')}"
        else:
            # Fallback se o Gemini falhar ou não estiver configurado
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            source = f"legacy:{os.path.basename(file_path)}"
            
        # 2. Injetar diretamente via AlquimiaProcessor (evitando dependência de API rodando)
        await processor.process_and_store(
            raw_data=[{"raw_text": content}],
            source=source
        )
        print(f"Injetado: {source}")

    processor.stop()
    print("Seeding concluído.")

if __name__ == "__main__":
    asyncio.run(seed_memory())
