import threading
import time
import random

N = 5
REFEICOES_POR_FILOSOFO = 3
garfos = [threading.Lock() for _ in range(N)]
estados = ["pensando"] * N
refeicoes_concluidas = [0] * N


def log_estado(filosofo, novo_estado, detalhe=""):
    estados[filosofo] = novo_estado
    msg = f"[ Filosofo {filosofo} ] Estado: {novo_estado.upper()}"
    if detalhe:
        msg += f" | {detalhe}"
    print(msg, flush=True)


def rotina_filosofo(p):
    garfo_esq = p
    garfo_dir = (p + 1) % N

    # Hierarquia de recursos (sempre adquirir o menor indice primeiro)
    primeiro = min(garfo_esq, garfo_dir)
    segundo = max(garfo_esq, garfo_dir)

    for refeicao in range(1, REFEICOES_POR_FILOSOFO + 1):
        log_estado(p, "pensando")
        time.sleep(random.uniform(0.05, 0.15))

        log_estado(p, "com fome", f"Ordem de aquisicao: garfo {primeiro} -> garfo {segundo}")

        garfos[primeiro].acquire()
        print(f"[ Filosofo {p} ] Adquiriu primeiro garfo ({primeiro})", flush=True)
        time.sleep(0.05)

        garfos[segundo].acquire()
        log_estado(p, "comendo", f"Refeicao {refeicao}/{REFEICOES_POR_FILOSOFO} com garfos {primeiro} e {segundo}")
        time.sleep(random.uniform(0.1, 0.2))
        refeicoes_concluidas[p] += 1

        garfos[segundo].release()
        garfos[primeiro].release()
        print(f"[ Filosofo {p}  Liberou garfos {segundo} e {primeiro}", flush=True)

    log_estado(p, "pensando", "Satisfeito (concluiu todas as refeições)")

if __name__ == "__main__":
    print("===========================================================================")
    print("| Iniciando o Jantar dos Filosofos (Solucao: Hierarquia de Recursos)       |")
    print("===========================================================================\n")


    threads = []
    for i in range(N):
        t = threading.Thread(target=rotina_filosofo, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print("\n\n=======================")
    print("| Resumo da Simulacao |")
    print("=======================\n")
    for i in range(N):
        print(f"Filosofo {i}: comeu {refeicoes_concluidas[i]} vezes.")