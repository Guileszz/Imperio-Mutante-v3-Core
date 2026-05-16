import asyncio
import json
import logging
import websockets
from typing import Dict, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ArbitrageEngine")

class ArbitrageEngine:
    def __init__(self):
        self.solana_price = 0.0
        self.base_price = 0.0
        self.running = False
        self.trades = []
        self.threshold = 0.005  # 0.5% spread threshold

    async def solana_ws(self):
        """Connects to Solana WebSocket for price updates"""
        uri = "wss://api.mainnet-beta.solana.com"
        while self.running:
            try:
                async with websockets.connect(uri) as websocket:
                    # Solana JSON-RPC subscribe to account or program
                    # For demonstration, we use a mock subscription that updates price
                    subscribe_msg = {
                        "jsonrpc": "2.0",
                        "id": 1,
                        "method": "slotSubscribe",
                        "params": []
                    }
                    await websocket.send(json.dumps(subscribe_msg))
                    while self.running:
                        message = await websocket.recv()
                        # Simulate price movement based on slot updates
                        self.solana_price = 145.0 + (asyncio.get_event_loop().time() % 10) / 10
                        await self.check_arbitrage()
            except Exception as e:
                logger.error(f"Solana WS Error: {e}")
                await asyncio.sleep(5)

    async def base_ws(self):
        """Connects to Base WebSocket (Coinbase L2) for price updates"""
        uri = "wss://ws-feed.exchange.coinbase.com"
        while self.running:
            try:
                async with websockets.connect(uri) as websocket:
                    subscribe_msg = {
                        "type": "subscribe",
                        "product_ids": ["SOL-USD"],
                        "channels": ["ticker"]
                    }
                    await websocket.send(json.dumps(subscribe_msg))
                    while self.running:
                        message = await websocket.recv()
                        data = json.loads(message)
                        if data.get("type") == "ticker":
                            self.base_price = float(data.get("price", 0))
                            # logger.info(f"Base Price Updated: {self.base_price}")
                            await self.check_arbitrage()
            except Exception as e:
                logger.error(f"Base WS Error: {e}")
                await asyncio.sleep(5)

    async def check_arbitrage(self):
        if self.solana_price == 0 or self.base_price == 0:
            return

        spread = abs(self.solana_price - self.base_price) / min(self.solana_price, self.base_price)
        
        if spread > self.threshold:
            direction = "SOL -> BASE" if self.solana_price < self.base_price else "BASE -> SOL"
            await self.execute_trade(direction, spread)

    async def execute_trade(self, direction: str, spread: float):
        trade = {
            "direction": direction,
            "spread": f"{spread:.4%}",
            "solana_price": self.solana_price,
            "base_price": self.base_price,
            "timestamp": asyncio.get_event_loop().time()
        }
        self.trades.append(trade)
        logger.info(f"ARBITRAGE OPPORTUNITY DETECTED: {trade}")
        # Real execution logic would go here

    async def start(self):
        self.running = True
        await asyncio.gather(
            self.solana_ws(),
            self.base_ws()
        )

    async def stop(self):
        self.running = False

    def get_status(self):
        return {
            "running": self.running,
            "solana_price": self.solana_price,
            "base_price": self.base_price,
            "current_spread": abs(self.solana_price - self.base_price) / min(self.solana_price, self.base_price) if self.solana_price and self.base_price else 0,
            "total_trades": len(self.trades)
        }

    def get_trades(self):
        return self.trades[-20:]
