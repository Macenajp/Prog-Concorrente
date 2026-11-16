import threading
import time
import sys

lock_a = threading.Lock()
lock_b = threading.Lock()


def tarefa_thread_1():
    print("[ Thread-1 ] Tentando adquirir LOCK_A...", flush=True)
    lock_a.acquire()
    print("[ Thread-1 ] Adquiriu LOCK_A. Dormindo 50ms...", flush=True)

    time.sleep(0.05)

    print("[ Thread-1 ] Tentando adquirir LOCK_B (aguardando liberacao)...", flush=True)
    lock_b.acquire()
    try:
        print("[ Thread-1 ] Concluiu secao critica!", flush=True)
    finally:
        lock_b.release()
        lock_a.release()


def tarefa_thread_2():
    print("[ Thread-2 ] Tentando adquirir LOCK_B...", flush=True)
    lock_b.acquire()
    print("[ Thread-2 ] Adquiriu LOCK_B. Dormindo 50ms...", flush=True)

    time.sleep(0.05)

    print("[ Thread-2 ] Tentando adquirir LOCK_A (aguardando liberacao)...", flush=True)
    lock_a.acquire()
    try:
        print("[ Thread-2 ] Concluiu secao critica!", flush=True)
    finally:
        lock_a.release()
        lock_b.release()

if __name__ == "__main__":   
    print("===========================================================================")
    print("| Iniciando Simulacao de Deadlock (Ordem Inversa de Locks) |\n")

    t1 = threading.Thread(target=tarefa_thread_1, name="Thread-1", daemon=True)
    t2 = threading.Thread(target=tarefa_thread_2, name="Thread-2", daemon=True)

    t1.start()
    t2.start()
    t1.join(timeout=2.0)
    t2.join(timeout=2.0)

    if t1.is_alive() and t2.is_alive():
        print("\n| DEADLOCK DETECTADO |")
        print("As threads nao terminaram apos o tempo limite. Estado atual (threading.enumerate()):")
        
        for t in threading.enumerate():
            print(f" -> Nome: {t.name} | Ativa (bloqueada se 'worker'): {t.is_alive()} | ID: {t.ident}")
        print("\n[!] O programa permanece travado em espera circular. Use as teclas: 'Ctrl + C' para encerrar [!]")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nEncerrado manualmente pelo usuário.")
            sys.exit(0)