# Relatório de análise de desempenho e concorrência

## 1- Dados coletados

N Clientes   | Tempo Total (s)  | Tempo Médio/Cli (s) 
------------------------------------------------------
10           | 0.0588           | 0.0532              
50           | 0.0803           | 0.0617              
100          | 0.1565           | 0.0947  

## 2- Onde o servidor single thread trava

1. O servidor executa `s.accept()` e obtém um descritor de socket para o Cliente A.
2. O servidor entra no laço `while True: dado = conexao.recv(1024)` exclusivo para o Cliente A.
3. Enquanto o Cliente A mantiver o canal TCP aberto (esperando entre envios, processando dados ou com alta latência), a chamada de sistema `recv()` fica em estado de espera bloqueante (**blocking I/O**).
4. O fluxo de execução do servidor nunca retorna para a linha `s.accept()`, impedindo o atendimento dos Clientes B, C e subsequentes.

### Esgotamento da Fila de Backlog (`listen(backlog)`)
* Quando 50 a 100 clientes tentam realizar o *handshake* TCP simultaneamente (disparados pela barreira do cliente de carga), os clientes que ainda não foram aceitos por `accept()` acumulam na fila de conexões pendentes do sistema operacional (gerenciada por `s.listen(backlog)`).
* Assim que essa fila atinge o limite do buffer do SO, novas tentativas de conexão recebem pacotes **TCP RST** ou são descartadas silenciosamente, resultando em:
  * `ConnectionRefusedError: [Errno 111] Connection refused`
  * `TimeoutError` na ponta do cliente.

### Conclusão Técnica
O servidor single-thread falha estruturalmente ao lidar com clientes com estado prolongado (*keep-alive* ou múltiplas mensagens por conexão). Para suportar concorrência real em I/O, a dissociação entre *aceitar conexões* e *processar mensagens* torna-se mandatória — seja via **multi-threading/multi-processing** (uma linha de execução por cliente) ou via **I/O multiplexing não-bloqueante** (`select`, `poll`, `epoll`).



