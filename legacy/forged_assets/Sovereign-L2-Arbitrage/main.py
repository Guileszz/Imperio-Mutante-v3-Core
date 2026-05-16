import asyncio
from fastapi import FastAPI
from engine import ArbitrageEngine

app = FastAPI(title="Sovereign L2 Arbitrage Bot")
engine = ArbitrageEngine()

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(engine.start())

@app.on_event("shutdown")
async def shutdown_event():
    await engine.stop()

@app.get("/")
async def root():
    return {
        "status": "active",
        "engine": engine.get_status()
    }

@app.get("/trades")
async def trades():
    return engine.get_trades()

@app.get("/config")
async def config():
    return {
        "threshold": engine.threshold,
        "assets": ["SOL/USDC"],
        "networks": ["Solana", "Base"]
    }
