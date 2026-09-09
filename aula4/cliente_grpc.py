import grpc
import servico_pb2, servico_pb2_grpc

with grpc.insecure_channel("127.0.0.1:50051") as canal:
    stub = servico_pb2_grpc.calculadoraStub(canal)
    resposta = stub.Somar(servico_pb2.Operandos(a=2, b=3))   # parece local!
    print("2 + 3 =", resposta.valor)
    resposta_mult = stub.Multiplicar(servico_pb2.Operandos(a=2,b=3))
    print("2 * 3 =", resposta_mult.valor)
    resposta_div = stub.Dividir(servico_pb2.Operandos(a=4,b=2))
    print("4 / 2 =", resposta_div.valor)
    resposta_sub = stub.Diminuir(servico_pb2.Operandos(a=4,b=2))
    print("4 - 2 =", resposta_sub.valor)