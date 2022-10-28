import atuadores_def_pb2_grpc
import atuadores_def_pb2
import grpc
import pika
from concurrent import futures
from channel_utils import Channel
from threading import Thread


channel = grpc.insecure_channel('localhost:50053')

stub_home_assistant = atuadores_def_pb2_grpc.HomeAssistantStub(channel)


while (True):

    actuators = stub_home_assistant.ListActuators(atuadores_def_pb2.Void())
    sensors = stub_home_assistant.ListSensors(atuadores_def_pb2.Void())

    print("Actuators: ")
    print("[1] --- Sprinkler --- ")
    print("[2] --- Lamp --- ")
    print("[3] --- Roof --- ")

    print("Sensors: ")
    print("[4] --- Temperature Sensor --- ")
    print("[5] --- Lightness Sensor --- ")
    print("[6] --- Rain Sensor --- ")
    

    option = input("Select a Actuator: ")

    if (option == "1"):
        print("------- SPRINKLER -------")
        print("State: ", "On" if actuators.sprinkler.state == True else "Off")
        print("Manual Action: ", "Yes" if actuators.sprinkler.manual_action == True else "No")
        print("-------  -------\n")

    elif (option == "2"):
        print("------- LAMP -------")
        print("State: ", "On" if actuators.lamp.is_on == True else "Off")
        print("Manual Action: ", "Yes" if actuators.lamp.manual_action == True else "No")
        print("Color: ", actuators.lamp.color)
        print("-------  -------\n")

    elif (option == "3"):
        print("------- ROOF -------")
        print("State: ", "Open" if actuators.roof.is_open == True else "Closed")
        print("-------  -------\n")

    elif (option == "4"):
        print("------- TEMPERATURE SENSOR-------")
        print("Temperature: ", sensors.temperature.value)
        print("-------  -------\n")

    elif (option == "5"):
        print("------- LIGHTNESS SENSOR -------")
        print("Lightness: ", sensors.lightness.value)
        print("-------  -------\n")

    elif (option == "6"):
        print("------- RAIN SENSOR -------")
        print("Is raining: ", sensors.rain_presence.value)
        print("-------  -------\n")
    else:
        print("Invalid object")