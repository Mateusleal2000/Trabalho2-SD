import atuadores_def_pb2_grpc
import atuadores_def_pb2
import grpc
import pika
from concurrent import futures
from channel_utils import Channel
from threading import Thread
class HomeAssistant(atuadores_def_pb2_grpc.HomeAssistantServicer):

    def __init__(self):
        self.channel = grpc.insecure_channel('localhost:50051')

        self.stub_sprinkler = atuadores_def_pb2_grpc.SprinklerStub(self.channel)
        self.stub_lamp = atuadores_def_pb2_grpc.LampStub(self.channel)
        self.stub_retractable_roof = atuadores_def_pb2_grpc.RetractableRoofStub(self.channel)

        self.lightness = atuadores_def_pb2.Lightness()
        self.rainning = atuadores_def_pb2.RainPresence()
        self.temperature = atuadores_def_pb2.Temperature()

        self.sprinkler_reply = atuadores_def_pb2.SprinklerReply()
        self.roof_reply = atuadores_def_pb2.RetractableRoofReply()
        self.lamp_reply = atuadores_def_pb2.LampReply()

        self.sprinkler_channel = Channel()
        self.roof_channel = Channel()
        self.lamp_channel = Channel()
        self.read_queues()
        self.serve()
        
    def ListActuators(self, request, context):
        actuators = atuadores_def_pb2.Actuators(sprinkler = self.sprinkler_reply, roof = self.roof_reply, lamp = self.lamp_reply)
        return actuators

    def ListSensors(self, request, context):
        sensors = atuadores_def_pb2.Sensors(temperature = self.temperature, rain_presence = self.rainning, lightness = self.lightness)
        return sensors

    def CallMethod(self, request, context):
        return super().CallMethod(request, context)

    def read_queues(self):
        Thread(target = self.subscribe_lamp_queue, args=()).start()
        Thread(target = self.subscribe_sprinkler_queue, args=()).start()
        Thread(target = self.subscribe_retractable_roof_queue, args=()).start()
        
        # self.subscribe_lamp_queue()
        # self.subscribe_sprinkler_queue()
        # self.subscribe_retractable_roof_queue()
        pass

    def list_actuators(self):
        pass

    def subscribe_lamp_queue(self):
        self.create_queue(self.callback_lamp, 'lightness', self.lamp_channel)
    
    def subscribe_sprinkler_queue(self):
        self.create_queue(self.callback_sprinkler, 'temperature', self.sprinkler_channel)

    def subscribe_retractable_roof_queue(self):
        self.create_queue( self.callback_roof, 'rain', self.roof_channel)

    def callback_lamp(self, ch, method, properties, body):
        light = atuadores_def_pb2.Lightness(value=0.0)
        light.ParseFromString(body)
        self.lightness = light

        self.lamp_reply = self.stub_lamp.Notify(light)
        print("Lamp is  on?: " + str(self.lamp_reply.is_on))
        print("Lamp manual activation: " + str(self.lamp_reply.manual_action))
        print("Lamp color: " + str(self.lamp_reply.color.color))
        
    def callback_sprinkler(self, ch, method, properties, body):
        
        temperature = atuadores_def_pb2.Temperature(value=0)
        temperature.ParseFromString(body)
        self.temperature = temperature

        self.sprinkler_reply = self.stub_sprinkler.Notify(temperature)
        print("Sprinkler state: " + str(self.sprinkler_reply.state))
        print("Sprinkler manual activation: " + str(self.sprinkler_reply.manual_action))
        
    def callback_roof(self, ch, method, properties, body):
        rain = atuadores_def_pb2.RainPresence(value=False)
        rain.ParseFromString(body)
        self.rainning = rain

        self.roof_reply = self.stub_retractable_roof.Notify(rain) 
        print("Is Roof open: " + str(self.roof_reply.is_open))
        
    def create_queue(self, callback, route, channel):
        queue = channel.create_queue()
        channel.bind(queue, route)
        channel.consume(queue, callback)
        channel.start()

    def serve(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        atuadores_def_pb2_grpc.add_HomeAssistantServicer_to_server(
            self, server)
          
        server.add_insecure_port('[::]:50053')
        server.start()
        server.wait_for_termination()

    def cli(self):
        print("Sala Inteligente: ")

        while (True):
            print("Intelligent Objects: ")
            print("[1] Roof")
            print("[2] Lamp")
            print("[3] Sprinkler")




            

home = HomeAssistant()
#home.cli()
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
