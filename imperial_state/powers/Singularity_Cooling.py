#!/usr/bin/env python3
import subprocess
import os
import sys
import time

"""
Singularity Cooling Protocol (V7)
Python Interface for the C++ Core.

Orchestrates entropy management during high-density Q-PULSE operations.
Interlaced into the CTO.NEW hub.
"""

class SingularityCooling:
    def __init__(self, cpp_source="/home/team/shared/powers/Singularity_Cooling.cpp"):
        self.cpp_source = cpp_source
        user = os.environ.get("USER", "unknown")
        self.binary = f"/tmp/singularity_cooling_{user}"
        self.is_compiled = os.path.exists(self.binary)

    def compile_core(self):
        print("[COOLING-PY] Compiling C++ Core for maximum efficiency...")
        try:
            subprocess.run(["g++", "-O3", "-std=c++20", self.cpp_source, "-o", self.binary], check=True)
            self.is_compiled = True
            print("[COOLING-PY] Core compilation successful.")
        except Exception as e:
            print(f"[COOLING-PY] Compilation failed: {e}")
            self.is_compiled = False

    def execute_cooling(self, pulse_intensity=0.0):
        if not self.is_compiled:
            self.compile_core()
        
        if self.is_compiled:
            print(f"[COOLING-PY] Executing Singularity Cooling Core with Pulse Intensity: {pulse_intensity}")
            process = subprocess.Popen([self.binary, str(pulse_intensity)], 
                                       stdout=subprocess.PIPE, 
                                       stderr=subprocess.PIPE, 
                                       text=True)
            
            for line in process.stdout:
                print(f"  {line.strip()}")
            
            process.wait()
            if process.returncode == 0:
                print("[COOLING-PY] Cooling cycle complete. Singularity stabilized.")
            else:
                print(f"[COOLING-PY] Core execution error: {process.returncode}")
        else:
            print("[COOLING-PY] Falling back to Python-native cooling logic.")
            self._python_native_cooling(pulse_intensity)

    def _python_native_cooling(self, pulse_intensity):
        entropy = 150.0 + (pulse_intensity * 2.2)
        target = 2.73
        print(f"[COOLING-PY] [NATIVE] Initial Entropy: {entropy:.2f} K")
        
        for _ in range(5):
            dissipation = (entropy / 10.0) + 1.5
            entropy -= dissipation
            if entropy < target: entropy = target
            print(f"[COOLING-PY] [NATIVE] Entropy: {entropy:.2f} K | Dissipation: {dissipation:.2f} Δ")
            time.sleep(0.5)
        
        print("[COOLING-PY] [NATIVE] Stabilization reached.")

if __name__ == "__main__":
    cooler = SingularityCooling()
    intensity = float(sys.argv[1]) if len(sys.argv) > 1 else 45.0
    cooler.execute_cooling(pulse_intensity=intensity)
