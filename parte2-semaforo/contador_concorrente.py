import threading
import time
import sys

sys.setswitchinterval(0.000001)

T = 8
M = 200_000

count = 0
sem = threading.Semaphore(1)


def tarefa_sem_sincronizacao():
    global count
    for i in range(M):
        atual = count
        # Serve para forçar a troca de contexto no meio da operação (leitura -> escrita)
        if i % 200 == 0:
            time.sleep(0)
        count = atual + 1


def tarefa_com_semaforo():
    global count
    for i in range(M):
        sem.acquire()
        try:
            atual = count
            if i % 200 == 0:
                time.sleep(0)
            count = atual + 1
        finally:
            sem.release()


def iniciar_teste(funcao_alvo, descricao, rodadas=3):
    esperado = T * M
    print(f"=== {descricao} (T={T}, M={M}) ===")
    for r in range(1, rodadas + 1):
        global count
        count = 0
        threads = [threading.Thread(target=funcao_alvo) for _ in range(T)]

        inicio = time.perf_counter()
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        fim = time.perf_counter()

        tempo_gasto = fim - inicio
        perda = esperado - count
        print(f"Execucao {r}: Esperado = {esperado} | Obtido = {count} (Perda: {perda}) | Tempo = {tempo_gasto:.4f} s")
    print()

if __name__ == "__main__":
    iniciar_teste(tarefa_sem_sincronizacao, "| v.1: Sem Sincronização - Condição de Corrida |")
    iniciar_teste(tarefa_com_semaforo, "| v.2: Com Semaforo Binário - Exclusão Mútua |")