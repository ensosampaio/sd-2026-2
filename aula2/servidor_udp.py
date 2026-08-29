import socket

HOST, PORT = "127.0.0.1", 5000

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))

print(f"[servidor] ouvindo em {HOST}:{PORT}", flush=True)

while True:
    dados, endereco = s.recvfrom(1024)
    print(f"[servidor] recebi de {endereco}: {dados.decode()}", flush=True)
    s.sendto(dados, endereco)