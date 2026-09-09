import socket
import threading
import time
import statistics

HOST, PORT = "127.0.0.1", 5000
MENSAGENS_POR_CLIENTE = 5
CARGAS = [10, 50, 100]

def executar_cliente(cid, barreira, tempos):
    barreira.wait()
    t_inicio = time.perf_counter()
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            for i in range(MENSAGENS_POR_CLIENTE):
                s.sendall(f"C{cid}-M{i}".encode("utf-8"))
                s.recv(1024)
                time.sleep(0.01) # Simula pequeno intervalo/processamento
        t_fim = time.perf_counter()
        tempos.append(t_fim - t_inicio)
    except Exception as e:
        print(f"[Cliente {cid}] Erro: {e}")

def rodar_teste(n_clientes):
    barreira = threading.Barrier(n_clientes)
    tempos_individuais = []
    threads = []
    
    t_global_inicio = time.perf_counter()
    for cid in range(n_clientes):
        t = threading.Thread(target=executar_cliente, args=(cid, barreira, tempos_individuais))
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
        
    t_global_fim = time.perf_counter()
    
    tempo_total = t_global_fim - t_global_inicio
    tempo_medio = statistics.mean(tempos_individuais) if tempos_individuais else 0
    return tempo_total, tempo_medio

if __name__ == "__main__":
    print(f"{'N Clientes':<12} | {'Tempo Total (s)':<16} | {'Tempo Médio/Cli (s)':<20}")
    print("-" * 54)
    for n in CARGAS:
        total, medio = rodar_teste(n)
        print(f"{n:<12} | {total:<16.4f} | {medio:<20.4f}")
        time.sleep(1)