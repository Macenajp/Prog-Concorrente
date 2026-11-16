import threading
import time

lock_a = threading.Lock()
lock_b = threading.Lock()


def executar_com_hierarquia(nome_thread):
    print(f"[{nome_thread}] Tentando adquirir LOCK_A...", flush=True)
    lock_a.acquire()
    print(f"[{nome_thread}] Adquiriu LOCK_A. Dormindo 50ms...", flush=True)

    time.sleep(0.05)

    print(f"[{nome_thread}] Tentando adquirir LOCK_B...", flush=True)
    lock_b.acquire()
    try:
        print(f"[{nome_thread}] Adquiriu LOCK_B e concluiu a secao critica com sucesso!", flush=True)
    finally:
        lock_b.release()
        print(f"[{nome_thread}] Liberou LOCK_B.", flush=True)
        lock_a.release()
        print(f"[{nome_thread}] Liberou LOCK_A.", flush=True)


if __name__ == "__main__":
    print("===========================================================================")
    print("| Iniciando Execucao Corrigida (Hierarquia Global: LOCK_A -> LOCK_B) |\n")

    t1 = threading.Thread(target=executar_com_hierarquia, args=("Thread-1",), name="Thread-1")
    t2 = threading.Thread(target=executar_com_hierarquia, args=("Thread-2",), name="Thread-2")

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print("\nTodas as threads finalizaram sem qualquer deadlock.")