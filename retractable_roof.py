import atuadores_def_pb2_grpc
import atuadores_def_pb2

class RetractableRoofServicer(atuadores_def_pb2_grpc.RetractableRoofServicer):

    def __init__(self) -> None:
        super().__init__()
        self.roof_data = atuadores_def_pb2.RetractableRoofReply(is_open=True)

    def Notify(self, request, context):
        rain_presence = request.value
        if rain_presence:
            self.roof_data = atuadores_def_pb2.RetractableRoofReply(is_open=False)
        
        return self.roof_data
    
    def Open(self, request, context):
        self.roof_data = atuadores_def_pb2.RetractableRoofReply(is_open=True)
        return self.roof_data

    def Close(self, request, context):
        self.roof_data = atuadores_def_pb2.RetractableRoofReply(is_open=False)
        return self.roof_data
# def serve():
#   server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
#   atuadores_def_pb2_grpc.add_RetractableRoofServicer_to_server(
#       RetractableRoofServicer(), server)
#   server.add_insecure_port('[::]:50051')
#   server.start()
#   server.wait_for_termination()