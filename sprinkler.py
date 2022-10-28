import atuadores_def_pb2_grpc
import atuadores_def_pb2

class SprinklerServicer(atuadores_def_pb2_grpc.SprinklerServicer):

    def __init__(self) -> None:
        super().__init__()
        self.sprinkler_data = atuadores_def_pb2.SprinklerReply(state=False, manual_action=False)

    def Notify(self, request, context):
        temperature = request.value
        if temperature > 80:
            self.sprinkler_data = atuadores_def_pb2.SprinklerReply(state=True, manual_action=False)
        else:
            self.sprinkler_data = atuadores_def_pb2.SprinklerReply(state=False, manual_action=False)

        return self.sprinkler_data

    def ActivateAlarm(self, request, context):
        self.sprinkler_data = atuadores_def_pb2.SprinklerReply(state=True, manual_action=True)
        return self.sprinkler_data
    
    def DeactivateAlarm(self, request, context):
        self.sprinkler_data = atuadores_def_pb2.SprinklerReply(state=False, manual_action=False)
        return self.sprinkler_data
