import grpc
from concurrent import futures
import servico_pb2, servico_pb2_grpc

class CalculadoraServicer(servico_pb2_grpc.calculadoraServicer):
    def Somar(self, request, context):
        return servico_pb2.Resultado(valor=request.a + request.b)


servidor = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

servico_pb2_grpc.add_calculadoraServicer_to_server(CalculadoraServicer(), servidor)

servidor.add_insecure_port("127.0.0.1:50051")

servidor.start()

print("[servidor gRPC] ouvindo em 127.0.0.1:50051", flush=True)

servidor.wait_for_termination()