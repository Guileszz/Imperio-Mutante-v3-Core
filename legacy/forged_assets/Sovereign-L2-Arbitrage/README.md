# Sovereign L2 Arbitrage Bot

High-performance arbitrage bot designed for exploiting price discrepancies between Solana and Base (L2).

## Features
- Real-time price monitoring via WebSockets.
- FastAPI interface for monitoring and stats.
- Dockerized for easy deployment.
- Low-latency spread calculation and execution logic.

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the bot:
   ```bash
   uvicorn main:app --reload
   ```

## Docker
Build and run with Docker:
```bash
docker build -t sovereign-l2-arbitrage .
docker run -p 8000:8000 sovereign-l2-arbitrage
```

## Disclaimer
This is for educational purposes only. Cryptocurrency trading involves significant risk.
