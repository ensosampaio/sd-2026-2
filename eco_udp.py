import socket

HOST, PORT = "127.0.0.1", 5000

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("Conectado. Digite uma mensagem (ou 'sair)")
while True:
    msg = input("> ")
    if msg == "sair":
        break
    s.sendto(msg.encode(), (HOST, PORT))
    eco, endereco = s.recvfrom(1024)
    print("eco: ", eco.decode())
s.close()