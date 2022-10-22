import sprinkler
import retractable_roof
import lamp

import atuadores_def_pb2_grpc

import logging
import grpc
from concurrent import futures

def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  atuadores_def_pb2_grpc.add_SprinklerServicer_to_server(
      sprinkler.SprinklerServicer(), server)
  atuadores_def_pb2_grpc.add_RetractableRoofServicer_to_server(
      retractable_roof.RetractableRoofServicer(), server)
  atuadores_def_pb2_grpc.add_LampServicer_to_server(lamp.LampServicer(), server)  
  server.add_insecure_port('[::]:50051')
  server.start()
  server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()