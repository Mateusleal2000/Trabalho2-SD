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

        self.sprinkler_reply = atuadores_def_pb2.SprinklerReply(state=False, manual_action=False)
        self.roof_reply = atuadores_def_pb2.RetractableRoofReply(is_open=True)
        self.lamp_reply = atuadores_def_pb2.LampReply(is_on=False, manual_action=False, color=atuadores_def_pb2.Color(color="White"))

        self.sprinkler_channel = Channel()
        self.roof_channel = Channel()
        self.lamp_channel = Channel()
        self.read_queues()
        self.serve()
        print("HERE")
        
    def ListActuators(self, request, context):
        actuators = atuadores_def_pb2.Actuators(
            sprinkler = self.sprinkler_reply, 
            roof = self.roof_reply, 
            lamp = self.lamp_reply
            )
        return actuators

    def ListSensors(self, request, context):
        sensors = atuadores_def_pb2.Sensors(temperature = self.temperature, rain_presence = self.rainning, lightness = self.lightness)
        return sensors

    def CallMethod(self, request, context):

        void = atuadores_def_pb2.Void()

        actuator = request.actuator
        method = request.method
        args = request.args

        if actuator == 1:
            if method == 1:
                self.sprinkler_reply = self.stub_sprinkler.ActivateAlarm(void)
            elif method == 2:
                self.sprinkler_reply = self.stub_sprinkler.DeactivateAlarm(void)

        elif actuator == 2:
            if method == 1:
                self.lamp_reply = self.stub_lamp.TurnOn(void)
            elif method == 2:
                self.lamp_reply = self.stub_lamp.TurnOff(void)
            elif method == 3:
                self.lamp_reply = self.stub_lamp.ChangeColor(atuadores_def_pb2.Color(color=args[0]))

        elif actuator == 3:
            if method == 1:
                self.roof_reply = self.stub_retractable_roof.Open(void)
            elif method == 2:
                self.roof_reply = self.stub_retractable_roof.Close(void)

        return void

    def read_queues(self):
        Thread(target = self.subscribe_lamp_queue, args=()).start()
        Thread(target = self.subscribe_sprinkler_queue, args=()).start()
        Thread(target = self.subscribe_retractable_roof_queue, args=()).start()
        pass

    def subscribe_lamp_queue(self):
        self.create_queue(self.callback_lamp, 'lightness', self.lamp_channel)

    def subscribe_sprinkler_queue(self):
        self.create_queue(self.callback_sprinkler, 'temperature', self.sprinkler_channel)

    def subscribe_retractable_roof_queue(self):
        self.create_queue(self.callback_roof, 'rain', self.roof_channel)

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

        server.add_insecure_port('[::]:3000')
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