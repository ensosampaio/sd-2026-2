import socket
import time

HOST, PORT = "127.0.0.1", 5000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

contador = 1

print("Conectado. Digite uma mensagem (ou 'sair')")
while True:
    msg = input("> ")
    if msg == "sair":
        break

    if msg == "teste":
        tempo_total_inicio = time.time()
        
        while contador <= 100:
            msg_repetida = str(contador)
                
            inicio = time.time()
            s.sendall(msg_repetida.encode())
            eco = s.recv(1024)
            fim = time.time()
                
            rtt = (fim - inicio) * 1000
            print(f"eco: {eco.decode()} | RTT: {rtt:.2f} ms")
                
            contador += 1
            
        tempo_total_fim = time.time()
        tempo_total = (tempo_total_fim - tempo_total_inicio) * 1000
        print(f"\n--- Fim do Teste ---")
        print(f"Tempo total para 100 mensagens: {tempo_total:.2f} ms\n")
    else:
        inicio = time.time()

        s.sendall(msg.encode())
        eco = s.recv(1024)

        fim = time.time()

        rtt = (fim - inicio) * 1000

        print(f"eco: {eco.decode()} || RTT: {rtt:.2f}")

s.close()