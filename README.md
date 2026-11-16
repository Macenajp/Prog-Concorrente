# Programação Concorrente: Filósofos, Semáforos e Deadlock

- **Autor:** João Pedro Macena Correa
- **Linguagem:** Python 3
- **Apresentação (YouTube):** [Clique aqui para assistir ao vídeo](https://youtu.be/k7UZCHLKWuY)
- **Prints e Histórico de Execuções:** [CHANGELOG.md](./CHANGELOG.md)

---

## Estrutura e Execução

Requer **Python 3.10 (ou superior)** - (bibliotecas usadas: `threading`, `time`, `sys`, `random`; Todas são bibliotecas padrão).

```bash
python parte1-filosofos/filosofos_ingenuo.py
python parte1-filosofos/filosofos_hierarquia.py
python parte2-semaforo/contador_concorrente.py
python parte3-deadlock/deadlock_reproducao.py
python parte3-deadlock/deadlock_corrigido.py
```

---

## Parte 1 — Jantar dos Filósofos

- **Dinâmica e Impasse:** Cinco filósofos compartilham 5 garfos em uma mesa circular e precisam de 2 garfos adjacentes para comer. No protocolo ingênuo (`filosofos_ingenuo.py`), todos pegam o garfo da esquerda simultaneamente e aguardam indefinidamente pelo da direita, gerando **deadlock**.
- **Solução e Condição de Coffman Negada:** Em `filosofos_hierarquia.py`, aplicamos **Hierarquia de Recursos**. Cada filósofo adquire sempre o garfo de **menor índice** primeiro (`min(esq, dir)`) e o de **maior índice** depois (`max(esq, dir)`). Isso nega a condição de **Espera Circular**, pois o Filósofo 4 disputa inicialmente o garfo `0` em vez do `4`, impedindo o ciclo fechado.
- **Progresso e Justiça:** Sem espera circular, ao menos um filósofo sempre consegue comer, liberando os garfos em seguida e permitindo que os vizinhos bloqueados avancem sem inanição (*starvation*). No log da versão corrigida, todos os 5 filósofos concluíram as 3 refeições.
- **Evidências de Execução:** [Log do protocolo ingênuo (travamento)](https://github.com/Macenajp/Prog-Concorrente/issues/1) | [Log da hierarquia de recursos](https://github.com/Macenajp/Prog-Concorrente/issues/2)

**Fluxo do Protocolo Corrigido:**
```text
Para cada filósofo p (0..4):
  primeiro = min(p, (p + 1) % 5)  |  segundo = max(p, (p + 1) % 5)
  [PENSANDO] -> [COM FOME] -> acquire(primeiro) -> acquire(segundo) -> [COMENDO] -> release(segundo) -> release(primeiro)
```

---

## Parte 2 — Threads e Semáforos (Contador Concorrente)

Experimento executado com T = 8 threads e M = 200.000 incrementos por thread (valor esperado: `1.600.000`).

| Versão | Execução | Esperado | Obtido | Incrementos Perdidos | Tempo (s) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **v.1 Sem Sincronização** | 1 | 1.600.000 | 567.695 | 1.032.305 | 0.1215 s |
| **v.1 Sem Sincronização** | 2 | 1.600.000 | 599.710 | 1.000.290 | 0.1187 s |
| **v.1 Sem Sincronização** | 3 | 1.600.000 | 586.211 | 1.013.789 | 0.1342 s |
| **v.2 Com Semáforo Binário** | 1 | 1.600.000 | 1.600.000 | 0 | 8.0560 s |
| **v.2 Com Semáforo Binário** | 2 | 1.600.000 | 1.600.000 | 0 | 7.1059 s |
| **v.2 Com Semáforo Binário** | 3 | 1.600.000 | 1.600.000 | 0 | 7.2737 s |

- **Perda de Incrementos (v.1):** A operação `count = atual + 1` não é atômica (envolve leitura, soma e escrita). Quando ocorre troca de contexto entre a leitura e a escrita, threads sobrescrevem o valor com estados desatualizados.
- **Exclusão Mútua (v.2):** O `threading.Semaphore(1)` serializa o acesso à seção crítica, garantindo que apenas uma thread leia e atualize `count` por vez.
- **Trade-off de Throughput:** O tempo sobe de `~0.12 s – 0.13 s` para `7.1 s – 8.1 s` devido à serialização das threads, contenção do semáforo e overhead de trocas de contexto no SO.
- **Visibilidade e Ordenação:** O par `release()` / `acquire()` garante sincronização de memória (equivalente ao *happens-before*), assegurando que toda escrita feita antes de `release()` seja visível para a próxima thread que adquirir o semáforo, mesmo sob trocas de contexto do GIL no Python.
- **Evidência de Execução:** [Log do contador concorrente](https://github.com/Macenajp/Prog-Concorrente/issues/3)


---

## Parte 3 — Deadlock

- **Cenário Reproduzido (`deadlock_reproducao.py`):** `Thread-1` adquire `LOCK_A` e aguarda `LOCK_B`, enquanto `Thread-2` adquire `LOCK_B` e aguarda `LOCK_A`.
- **Condições de Coffman Presentes:**
  1. *Exclusão Mútua:* `LOCK_A` e `LOCK_B` permitem apenas uma thread por vez.
  2. *Manter-e-Esperar:* Ambas seguram um lock enquanto solicitam o segundo.
  3. *Não Preempção:* Os locks não são tomados à força pelo sistema.
  4. *Espera Circular:* Ciclo fechado `Thread-1 -> LOCK_B -> Thread-2 -> LOCK_A -> Thread-1`.
- **Correção (`deadlock_corrigido.py`):** Imposição de **ordem global de aquisição** (`LOCK_A` sempre antes de `LOCK_B` em todas as threads), eliminando a **Espera Circular**.
- **Evidências de Execução:** [Log do deadlock reproduzido](https://github.com/Macenajp/Prog-Concorrente/issues/5) | [Log da versão corrigida](https://github.com/Macenajp/Prog-Concorrente/issues/4)

**Diagnóstico de Travamento (`threading.enumerate()`):**
```text
| DEADLOCK DETECTADO |
As threads nao terminaram apos o tempo limite. Estado atual (threading.enumerate()):
  -> Nome: MainThread | Ativa (bloqueada se 'worker'): True | ID: 15000
  -> Nome: Thread-1 | Ativa (bloqueada se 'worker'): True | ID: 25432
  -> Nome: Thread-2 | Ativa (bloqueada se 'worker'): True | ID: 25276
```
