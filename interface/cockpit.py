from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import httpx
import uvicorn
import asyncio
from datetime import datetime
import os

app = FastAPI(title="NEXUS COCKPIT v4.0.0 Beta")

# URL do Nexus Core para buscar dados reais
NEXUS_URL = os.getenv("NEXUS_URL", "http://localhost:8000")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NEXUS COCKPIT v4.0.0 Beta</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=JetBrains+Mono:wght@300;500&display=swap');
        
        :root {
            --neon-green: #00ff41;
            --neon-blue: #00f2ff;
            --neon-red: #ff003c;
            --dark-bg: #050505;
        }

        body { 
            background-color: var(--dark-bg); 
            color: var(--neon-green); 
            font-family: 'JetBrains Mono', monospace; 
            overflow-x: hidden;
        }

        .orbitron { font-family: 'Orbitron', sans-serif; }

        .cyber-card { 
            border: 1px solid rgba(0, 255, 65, 0.3); 
            background: rgba(0, 255, 65, 0.02); 
            box-shadow: 0 0 15px rgba(0, 255, 65, 0.1);
            backdrop-filter: blur(5px);
            transition: all 0.3s ease;
        }

        .cyber-card:hover {
            border-color: var(--neon-green);
            box-shadow: 0 0 20px rgba(0, 255, 65, 0.2);
        }

        .glitch-text { 
            text-shadow: 2px 2px #ff00ff, -2px -2px #00ffff; 
            animation: glitch 2s infinite;
        }

        @keyframes glitch {
            0% { text-shadow: 2px 2px #ff00ff, -2px -2px #00ffff; }
            25% { text-shadow: -2px 2px #ff00ff, 2px -2px #00ffff; }
            50% { text-shadow: 2px -2px #ff00ff, -2px 2px #00ffff; }
            75% { text-shadow: -2px -2px #ff00ff, 2px 2px #00ffff; }
            100% { text-shadow: 2px 2px #ff00ff, -2px -2px #00ffff; }
        }

        .scanline {
            width: 100%;
            height: 2px;
            background: rgba(0, 255, 65, 0.1);
            position: fixed;
            top: 0;
            left: 0;
            z-index: 100;
            pointer-events: none;
            animation: scanline 6s linear infinite;
        }

        @keyframes scanline {
            0% { top: 0; }
            100% { top: 100%; }
        }

        .stat-value { color: white; text-shadow: 0 0 5px rgba(255,255,255,0.5); }
        
        ::-webkit-scrollbar { width: 4px; }
        ::-webkit-scrollbar-track { background: #050505; }
        ::-webkit-scrollbar-thumb { background: #00ff41; }
    </style>
</head>
<body class="p-4 md:p-8">
    <div class="scanline"></div>

    <header class="mb-8 border-b border-green-900 pb-6 flex flex-col md:flex-row justify-between items-end">
        <div>
            <h1 class="text-3xl md:text-5xl font-bold glitch-text orbitron">🦾 NEXUS COCKPIT v4.0.0 Beta</h1>
            <p class="text-xs md:text-sm tracking-widest opacity-70 mt-2 uppercase">SISTEMA DE IGNIÇÃO OPERACIONAL ATIVADO | CLUSTER: SPECTRUM-NEURO-GLITCH</p>
        </div>
        <div class="text-right mt-4 md:mt-0">
            <div id="clock" class="text-xl font-bold">00:00:00</div>
            <div class="text-[10px] opacity-50 uppercase">Coordinated Universal Time</div>
        </div>
    </header>

    <main class="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <!-- Main Stats -->
        <div class="lg:col-span-1 space-y-6">
            <div class="cyber-card p-6 rounded-none">
                <h2 class="text-xs uppercase opacity-50 mb-1">Status do Sistema</h2>
                <div id="system-status" class="text-2xl font-bold orbitron uppercase tracking-tighter">OFFLINE</div>
                <div class="mt-4 flex items-center gap-2">
                    <div id="status-indicator" class="w-2 h-2 rounded-full bg-red-500 shadow-[0_0_8px_#f00]"></div>
                    <span id="status-text" class="text-[10px] uppercase">Aguardando Conexão...</span>
                </div>
            </div>

            <div class="cyber-card p-6 rounded-none">
                <h2 class="text-xs uppercase opacity-50 mb-1">Lucro de Arbitragem (24h)</h2>
                <div id="arbitrage-profit" class="text-3xl font-bold orbitron text-white">$0.00</div>
                <div class="mt-2 text-[10px] text-green-400" id="profit-change">+0.0% vs last hour</div>
            </div>

            <div class="cyber-card p-6 rounded-none">
                <h2 class="text-xs uppercase opacity-50 mb-1">Sovereignty Score</h2>
                <div id="sovereignty-score" class="text-4xl font-bold orbitron text-white">0.0%</div>
                <div class="w-full bg-green-900 h-1 mt-4">
                    <div id="score-bar" class="bg-green-400 h-full" style="width: 0%"></div>
                </div>
            </div>
        </div>

        <!-- Telemetry & Nodes -->
        <div class="lg:col-span-2 space-y-6">
            <div class="cyber-card p-6 rounded-none">
                <h3 class="text-lg font-bold mb-4 flex justify-between items-center">
                    <span>TELEMETRIA DISTRIBUÍDA</span>
                    <span class="text-[10px] font-normal opacity-50">REAL-TIME DATA FEED</span>
                </h3>
                <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div class="border-l-2 border-green-500 pl-3">
                        <p class="text-[10px] opacity-50 uppercase">CPU Global</p>
                        <div id="cpu-usage" class="stat-value text-xl">0%</div>
                    </div>
                    <div class="border-l-2 border-blue-500 pl-3">
                        <p class="text-[10px] opacity-50 uppercase">RAM Global</p>
                        <div id="ram-usage" class="stat-value text-xl">0%</div>
                    </div>
                    <div class="border-l-2 border-purple-500 pl-3">
                        <p class="text-[10px] opacity-50 uppercase">GPU Load</p>
                        <div id="gpu-load" class="stat-value text-xl">0%</div>
                    </div>
                    <div class="border-l-2 border-red-500 pl-3">
                        <p class="text-[10px] opacity-50 uppercase">GPU Temp</p>
                        <div id="gpu-temp" class="stat-value text-xl">0°C</div>
                    </div>
                </div>
                <div class="mt-8 h-40">
                    <canvas id="telemetryChart"></canvas>
                </div>
            </div>

            <div class="cyber-card p-6 rounded-none">
                <h3 class="text-lg font-bold mb-4">NETWORK CLUSTER NODES</h3>
                <div id="nodes-list" class="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <!-- Nodes will be injected here -->
                </div>
            </div>

            <div class="cyber-card p-6 rounded-none">
                <h3 class="text-lg font-bold mb-4 uppercase text-blue-400">MALHA P2P - O TELHADO</h3>
                <div id="p2p-mesh" class="space-y-4">
                    <div class="flex justify-between items-center text-xs">
                        <span>ESTADO DE CONSENSO:</span>
                        <span id="consensus-status" class="text-green-400">SINCRONIZADO</span>
                    </div>
                    <div class="h-32 bg-black bg-opacity-50 relative overflow-hidden border border-green-900 border-opacity-30" id="mesh-container">
                         <div id="mesh-visual" class="w-full h-full flex justify-around items-center">
                            <!-- P2P Visualization nodes will be here -->
                         </div>
                    </div>
                    <div class="grid grid-cols-2 gap-2 text-[9px] opacity-60">
                        <div>LAST MUTATION: <span id="last-mutation-hash" class="text-white text-bold">-</span></div>
                        <div>ACTIVE PEERS: <span id="active-peers-count" class="text-white">0</span></div>
                    </div>
                </div>
            </div>

            <div class="cyber-card p-6 rounded-none">
                <h3 class="text-lg font-bold mb-4 uppercase">Lattice Satellite Network</h3>
                <div id="satellites-list" class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <!-- Satellites will be injected here -->
                </div>
            </div>
        </div>

        <!-- Console / Logs -->
        <div class="lg:col-span-1">
            <div class="cyber-card p-4 rounded-none h-full flex flex-col">
                <h3 class="text-xs font-bold mb-3 border-b border-green-900 pb-2 uppercase">Neural Link Log</h3>
                <div id="console-logs" class="text-[10px] font-mono space-y-1 overflow-y-auto flex-grow max-h-[600px]">
                    <div>[SYSTEM] Cockpit v4.0.0 Beta Initialized...</div>
                    <div>[SYSTEM] Establishing gRPC Bridge...</div>
                </div>
            </div>
        </div>
    </main>

    <footer class="mt-12 pt-4 border-t border-green-900 flex justify-between items-center text-[10px] opacity-40">
        <div>IMPÉRIO MUTANTE &copy; 2024 - PROTOCOLO DE SOBERANIA TOTAL</div>
        <div id="connection-latency">LATENCY: 0ms</div>
    </footer>

    <script>
        const ctx = document.getElementById('telemetryChart').getContext('2d');
        const telemetryChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: Array(20).fill(''),
                datasets: [{
                    label: 'CPU',
                    borderColor: '#00ff41',
                    borderWidth: 1,
                    data: Array(20).fill(0),
                    tension: 0.4,
                    pointRadius: 0
                }, {
                    label: 'GPU',
                    borderColor: '#ff003c',
                    borderWidth: 1,
                    data: Array(20).fill(0),
                    tension: 0.4,
                    pointRadius: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: { beginAtZero: true, max: 100, grid: { color: '#111' } },
                    x: { grid: { display: false } }
                },
                plugins: { legend: { display: false } }
            }
        });

        function addLog(msg, type = 'INFO') {
            const logs = document.getElementById('console-logs');
            const entry = document.createElement('div');
            const time = new Date().toLocaleTimeString();
            entry.innerHTML = `<span class="opacity-50">[${time}]</span> <span class="${type === 'ERR' ? 'text-red-500' : 'text-green-400'}">[${type}]</span> ${msg}`;
            logs.appendChild(entry);
            logs.scrollTop = logs.scrollHeight;
            if (logs.children.length > 50) logs.removeChild(logs.firstChild);
        }

        async function updateDashboard() {
            const start = Date.now();
            try {
                const response = await fetch('/api/health');
                const data = await response.json();
                const latency = Date.now() - start;
                
                document.getElementById('connection-latency').innerText = `LATENCY: ${latency}ms`;

                if (data.status) {
                    const statusEl = document.getElementById('system-status');
                    statusEl.innerText = data.status;
                    const indicator = document.getElementById('status-indicator');
                    const statusText = document.getElementById('status-text');
                    
                    if (data.status === 'ONLINE' || data.status === 'ACTIVE' || data.status === 'SOVEREIGN_OPERATIONAL') {
                        statusEl.style.color = '#00ff41';
                        indicator.className = 'w-2 h-2 rounded-full bg-green-500 shadow-[0_0_8px_#0f0]';
                        statusText.innerText = 'Sistemas Operacionais';
                    } else {
                        statusEl.style.color = '#ff003c';
                        indicator.className = 'w-2 h-2 rounded-full bg-red-500 shadow-[0_0_8px_#f00]';
                        statusText.innerText = 'Sistema em Alerta';
                    }
                }
                
                const score = (data.sovereignty_score || 0) * 100;
                document.getElementById('sovereignty-score').innerText = score.toFixed(1) + '%';
                document.getElementById('score-bar').style.width = score + '%';
                
                const profit = data.arbitrage_profit || 0;
                document.getElementById('arbitrage-profit').innerText = `${profit.toLocaleString(undefined, {minimumFractionDigits: 2})}`;

                const tel = data.telemetry || {};
                document.getElementById('cpu-usage').innerText = (tel.cpu_percent || 0).toFixed(1) + '%';
                document.getElementById('ram-usage').innerText = (tel.memory?.percent || 0).toFixed(1) + '%';
                
                let gpuLoad = 0;
                let gpuTemp = 0;
                if (tel.gpu && tel.gpu.length > 0) {
                    gpuLoad = tel.gpu[0].utilization;
                    gpuTemp = tel.gpu[0].temperature;
                }

                document.getElementById('gpu-load').innerText = gpuLoad.toFixed(1) + '%';
                document.getElementById('gpu-temp').innerText = gpuTemp.toFixed(1) + '°C';

                // Update Chart
                telemetryChart.data.datasets[0].data.shift();
                telemetryChart.data.datasets[0].data.push(tel.cpu_percent || 0);
                telemetryChart.data.datasets[1].data.shift();
                telemetryChart.data.datasets[1].data.push(gpuLoad || 0);
                telemetryChart.update('none');

                const nodesList = document.getElementById('nodes-list');
                nodesList.innerHTML = '';
                const nodes = data.nodes || {};

                for (const [id, node] of Object.entries(nodes)) {
                    const isOnline = node.status === 'online' || node.status === 'active';
                    const statusColor = isOnline ? 'var(--neon-green)' : 'var(--neon-red)';
                    
                    let specs = "";
                    if (id === "NEURO-TOXIN") specs = "<br><span class='text-[8px] opacity-40'>Ryzen 9 / RTX 3070</span>";
                    if (id === "SPECTRUM") specs = "<br><span class='text-[8px] opacity-40'>RTX 3050</span>";

                    const html = `
                        <div class="p-3 border border-green-900 bg-black bg-opacity-40">
                            <div class="flex justify-between items-center mb-2">
                                <span class="text-[10px] font-bold orbitron">${id} ${specs}</span>
                                <div class="w-1.5 h-1.5 rounded-full ${isOnline ? 'animate-pulse' : ''}" style="background-color: ${statusColor}; box-shadow: 0 0 5px ${statusColor}"></div>
                            </div>
                            <div class="text-[9px] opacity-60 uppercase">Latency</div>
                            <div class="text-xs">${node.latency_ms?.toFixed(2) || 0} ms</div>
                        </div>
                    `;
                    nodesList.innerHTML += html;
                }

                const satellitesList = document.getElementById('satellites-list');
                satellitesList.innerHTML = '';
                const satellites = data.lattice || [];

                satellites.forEach(sat => {
                    const statusColor = sat.status === 'DEPLOYED' ? 'var(--neon-green)' : 'var(--neon-blue)';
                    const html = `
                        <div class="p-3 border border-blue-900 bg-black bg-opacity-40">
                            <div class="flex justify-between items-center mb-2">
                                <span class="text-[10px] font-bold orbitron">${sat.name}</span>
                                <div class="w-1.5 h-1.5 rounded-full" style="background-color: ${statusColor}; box-shadow: 0 0 5px ${statusColor}"></div>
                            </div>
                            <div class="text-[9px] opacity-60 uppercase">Repository</div>
                            <div class="text-[10px] truncate">${sat.repository}</div>
                            <div class="mt-2 text-[8px] opacity-40 italic">Status: ${sat.status}</div>
                        </div>
                    `;
                    satellitesList.innerHTML += html;
                });

                // Update P2P Mesh
                if (data.p2p_mesh) {
                    const mesh = data.p2p_mesh;
                    document.getElementById('last-mutation-hash').innerText = mesh.state.last_mutation_hash || '0x00000000';
                    document.getElementById('active-peers-count').innerText = mesh.state.active_nodes.length;
                    
                    const visual = document.getElementById('mesh-visual');
                    visual.innerHTML = '';
                    
                    // Current node
                    visual.innerHTML += `
                        <div class="flex flex-col items-center">
                            <div class="w-8 h-8 rounded-full border-2 border-green-500 bg-green-900 flex items-center justify-center text-[10px] font-bold">CORE</div>
                            <span class="text-[8px] mt-1">NEXUS</span>
                        </div>
                    `;

                    // Peers
                    mesh.peers.forEach(peer => {
                        const isActive = mesh.state.active_nodes.includes(peer);
                        const color = isActive ? 'green' : 'gray';
                        visual.innerHTML += `
                            <div class="w-4 h-[1px] bg-${color}-500 opacity-50"></div>
                            <div class="flex flex-col items-center">
                                <div class="w-6 h-6 rounded-full border border-${color}-500 bg-${color}-900 flex items-center justify-center text-[8px]">${peer[0]}</div>
                                <span class="text-[6px] mt-1">${peer}</span>
                            </div>
                        `;
                    });

                    const consensusStatus = document.getElementById('consensus-status');
                    if (mesh.is_synchronized) {
                        consensusStatus.innerText = 'SINCRONIZADO';
                        consensusStatus.className = 'text-green-400';
                    } else {
                        consensusStatus.innerText = 'DIVERGENTE';
                        consensusStatus.className = 'text-yellow-400';
                    }
                }

            } catch (error) {
                console.error('Error fetching health:', error);
                document.getElementById('system-status').innerText = 'ERROR';
                document.getElementById('system-status').style.color = '#ff003c';
            }
        }

        setInterval(() => {
            const now = new Date();
            document.getElementById('clock').innerText = now.toTimeString().split(' ')[0];
        }, 1000);

        setInterval(updateDashboard, 2000);
        updateDashboard();
        
        setTimeout(() => addLog("Neural Bridge connected to cluster."), 1500);
        setTimeout(() => addLog("Telemetria dos nós sincronizada via gRPC.", "INFO"), 3000);
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def get_dashboard():
    return HTML_TEMPLATE

@app.get("/api/health")
async def get_api_health():
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(f"{NEXUS_URL}/health", timeout=2.0)
            return resp.json()
        except Exception:
            return {
                "status": "OFFLINE", 
                "sovereignty_score": 0.0,
                "arbitrage_profit": 0.0,
                "telemetry": {
                    "cpu_percent": 0,
                    "memory": {"percent": 0},
                    "gpu": []
                },
                "nodes": {
                    "SPECTRUM": {"status": "offline", "latency_ms": 0},
                    "NEURO-TOXIN": {"status": "offline", "latency_ms": 0},
                    "GLITCH": {"status": "offline", "latency_ms": 0}
                }
            }


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
