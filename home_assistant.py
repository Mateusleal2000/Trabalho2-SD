import atuadores_def_pb2_grpc
import atuadores_def_pb2
import grpc
import pika

class HomeAssistant:

    def __init__(self):
        self.channel = grpc.insecure_channel('localhost:50051')
        self.stub_sprinkler = atuadores_def_pb2_grpc.SprinklerStub(self.channel)
        self.stub_lamp = atuadores_def_pb2_grpc.LampStub(self.channel)
        self.stub_retractable_roof = atuadores_def_pb2_grpc.RetractableRoofStub(self.channel)

    def read_queues(self):
        self.subscribe_lamp_queue()
        self.subscribe_sprinkler_queue()
        self.subscribe_retractable_roof_queue()
        pass

    def list_actuators(self):
        pass

    def subscribe_lamp_queue(self):
        pass

    def subscribe_sprinkler_queue(self):
        pass

    def subscribe_retractable_roof_queue(self):
        pass




# channel = grpc.insecure_channel('localhost:50051')
# stub_sprinkler = atuadores_def_pb2_grpc.SprinklerStub(channel)

# stub_lamp = atuadores_def_pb2_grpc.LampStub(channel)

# stub_retractable_roof = atuadores_def_pb2_grpc.RetractableRoofStub(channel)

# response = stub_sprinkler.Notify(atuadores_def_pb2.Temperature(value = 51))
# print("Sprinkler state: " + str(response.state))
# print("Sprinkler manual activation: " + str(response.manual_action))

# response = stub_sprinkler.ActivateAlarm(atuadores_def_pb2.Void())
# print("Sprinkler state: " + str(response.state))
# print("Sprinkler manual activation: " + str(response.manual_action))

# response = stub_sprinkler.DeactivateAlarm(atuadores_def_pb2.Void())
# print("Sprinkler state: " + str(response.state))
# print("Sprinkler manual activation: " + str(response.manual_action))

# # response = stub_lamp.Notify(atuadores_def_pb2.Lightness(value = 0.4))
# # print("Lamp: " + response.message)


# response = stub_retractable_roof.Notify(atuadores_def_pb2.RainPresence(value = True))
# print("Is Roof open: " + str(response.is_open))

# response = stub_retractable_roof.Open(atuadores_def_pb2.Void())
# print("Is Roof open: " + str(response.is_open))

# response = stub_retractable_roof.Close(atuadores_def_pb2.Void())
# print("Is Roof open: " + str(response.is_open))


# response = stub_lamp.Notify(atuadores_def_pb2.Lightness(value = 0.4))
# print("Lamp is  on?: " + str(response.is_on))
# print("Lamp manual activation: " + str(response.manual_action))
# print("Lamp color: " + str(response.color.color))

# response = stub_lamp.TurnOn(atuadores_def_pb2.Void())
# print("Lamp is  on?: " + str(response.is_on))
# print("Lamp manual activation: " + str(response.manual_action))
# print("Lamp color: " + str(response.color.color))

# response = stub_lamp.Notify(atuadores_def_pb2.Lightness(value = 0.8))
# print("Lamp is  on?: " + str(response.is_on))
# print("Lamp manual activation: " + str(response.manual_action))
# print("Lamp color: " + str(response.color.color))

# response = stub_lamp.TurnOff(atuadores_def_pb2.Void())
# print("Lamp is  on?: " + str(response.is_on))
# print("Lamp manual activation: " + str(response.manual_action))
# print("Lamp color: " + str(response.color.color))

# response = stub_lamp.ChangeColor(atuadores_def_pb2.Color(color="Red"))
# print("Lamp is  on?: " + str(response.is_on))
# print("Lamp manual activation: " + str(response.manual_action))
# print("Lamp color: " + str(response.color.color))
