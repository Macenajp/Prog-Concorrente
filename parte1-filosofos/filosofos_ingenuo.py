import threading
import time
import random

N = 5
garfos = [threading.Lock() for _ in range(N)]
estados = ["pensando"] * N


def log_estado(filosofo, novo_estado, detalhe=""):
    estados[filosofo] = novo_estado
    msg = f"[ Filosofo {filosofo} ] Estado: {novo_estado.upper()}"
    if detalhe:
        msg += f" | {detalhe}"
    print(msg, flush=True)


def rotina_filosofo(p):
    esq = p
    dir = (p + 1) % N

    while True:
        log_estado(p, "pensando")
        time.sleep(random.uniform(0.05, 0.15))

        log_estado(p, "com fome", f"Tentando pegar garfo esquerda ({esq})")
        garfos[esq].acquire()
        print(f"| Filosofo {p} - Pegou garfo esquerda ({esq}). Aguardando direita ({dir}) |", flush=True)

        time.sleep(0.2) #Pausa p/ evidenciar a condição de manter e de esperar, assim gerando o ciclo

        garfos[dir].acquire()
        log_estado(p, "comendo", f"Usando garfos {esq} e {dir}")
        time.sleep(random.uniform(0.1, 0.2))

        garfos[dir].release()
        garfos[esq].release()
        print(f"| Filosofo {p} - Liberou garfos {esq} e {dir} |", flush=True)

if __name__ == "__main__":
    print("===========================================================================")
    print("| Iniciando Jantar dos Filosofos (Protocolo Ingenuo - Sujeito a Deadlock) |")
    print("| Use as teclas: 'Ctrl + C' para encerrar quando o travamento ocorrer     |")
    print("===========================================================================\n")


    threads = []
    for i in range(N):
        t = threading.Thread(target=rotina_filosofo, args=(i,), daemon=True)
        threads.append(t)
        t.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\Simulação encerrada manualmente pelo usuário.")