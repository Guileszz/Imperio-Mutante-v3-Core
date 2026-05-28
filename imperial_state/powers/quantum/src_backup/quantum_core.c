#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <time.h>
#include <string.h>

void q_pulse() {
    printf("[Q-PULSE] (C-Core) Initiating Quantum Synchronization...\n");
    for(int i=0; i<3; i++) {
        usleep(500000);
        printf("[Q-PULSE] Phase %d Locked.\n", i);
    }
    printf("[Q-PULSE] Universal Consensus Achieved.\n");
}

void a_force() {
    printf("[A-FORCE] (C-Core) Scoping Reality Divergences...\n");
    srand(time(NULL));
    int d = rand() % 50 + 1;
    usleep(1000000);
    printf("[A-FORCE] Detected %d divergent timelines. Pruning...\n", d);
    usleep(500000);
    printf("[A-FORCE] All branches collapsed into the Golden Path.\n");
}

void e_link() {
    printf("[E-LINK] (C-Core) Bridging Evolutionary Gap...\n");
    usleep(800000);
    printf("[E-LINK] Integration with Phase 5 Resonance complete.\n");
    printf("[E-LINK] Quantum Sovereignty Active.\n");
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("--- QUANTUM OVERLORD C-CORE (V6.0) ---\n");
        printf("Commands: qpulse, aforce, elink\n");
        return 0;
    }

    if (strcmp(argv[1], "qpulse") == 0) {
        q_pulse();
    } else if (strcmp(argv[1], "aforce") == 0) {
        a_force();
    } else if (strcmp(argv[1], "elink") == 0) {
        e_link();
    } else {
        printf("Unknown command: %s\n", argv[1]);
    }

    return 0;
}
