import atuadores_def_pb2_grpc
import atuadores_def_pb2

class LampServicer(atuadores_def_pb2_grpc.LampServicer):


    def __init__(self) -> None:
        super().__init__()
        self.lamp_data = atuadores_def_pb2.LampReply(
            is_on=False, 
            manual_action=False,
            color=atuadores_def_pb2.Color(color="White")
            )

    def Notify(self, request, context):
        lightness = request.value
        if lightness < 0.5 and not self.lamp_data.manual_action:
            self.lamp_data = atuadores_def_pb2.LampReply(
                                is_on=True, 
                                manual_action=False,
                                color = self.lamp_data.color)
 
        elif lightness >= 0.5 and not self.lamp_data.manual_action:
            self.lamp_data = atuadores_def_pb2.LampReply(
                                is_on=False, 
                                manual_action=False,
                                color = self.lamp_data.color)
        return self.lamp_data

    def TurnOn(self, request, context):
        self.lamp_data = atuadores_def_pb2.LampReply(is_on=True, manual_action=True, color = self.lamp_data.color)
        return self.lamp_data

    def TurnOff(self, request, context):
        self.lamp_data = atuadores_def_pb2.LampReply(is_on=False, manual_action=False, color = self.lamp_data.color)
        return self.lamp_data
    
    def ChangeColor(self, request, context):
        self.lamp_data = atuadores_def_pb2.LampReply(
                                    is_on=self.lamp_data.is_on,
                                    manual_action=self.lamp_data.manual_action, 
                                    color=request)
        return self.lamp_data