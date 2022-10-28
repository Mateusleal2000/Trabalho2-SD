import atuadores_def_pb2_grpc
import atuadores_def_pb2
import grpc
import pika
from concurrent import futures
from channel_utils import Channel
from threading import Thread


channel = grpc.insecure_channel('localhost:3000')

stub_home_assistant = atuadores_def_pb2_grpc.HomeAssistantStub(channel)


while (True):

    # actuators = stub_home_assistant.ListActuators(atuadores_def_pb2.Void())
    # sensors = stub_home_assistant.ListSensors(atuadores_def_pb2.Void())

    print("Actuators: ")
    print("[1] --- Sprinkler --- ")
    print("[2] --- Lamp --- ")
    print("[3] --- Roof --- ")

    print("Sensors: ")
    print("[4] --- Temperature Sensor --- ")
    print("[5] --- Lightness Sensor --- ")
    print("[6] --- Rain Sensor --- ")
    

    option = input("Select a Actuator: ")


    actuators = stub_home_assistant.ListActuators(atuadores_def_pb2.Void())
    sensors = stub_home_assistant.ListSensors(atuadores_def_pb2.Void())

    if (option == "1"):
        print("------- SPRINKLER -------")
        print("State: ", "On" if actuators.sprinkler.state == True else "Off")
        print("Manual Action: ", "Yes" if actuators.sprinkler.manual_action == True else "No")
        print(" -- Available operations -- ")
        print("\t[1] Activate Alarm")
        print("\t[2] Deactivate Alarm")
        
        try:
            operation = int(input("\t Enter a action: "))
            params = atuadores_def_pb2.RemoteCallParams(actuator = 1, method = operation)
            stub_home_assistant.CallMethod(params)
        except:
            print("Invalid method")
            continue
        print("-------  -------\n")
        
        
    elif (option == "2"):
        print("------- LAMP -------")
        print("State: ", "On" if actuators.lamp.is_on == True else "Off")
        print("Manual Action: ", "Yes" if actuators.lamp.manual_action == True else "No")
        print("Color: ", actuators.lamp.color)
        
        print("\t[1] Turn on")
        print("\t[2] Turn off")
        print("\t[3] Change color")

        try:
            operation = int(input("\t Enter a action: "))
            params = atuadores_def_pb2.RemoteCallParams(actuator = 2, method = operation)
            if(operation == 3):
                args_s = input("Type a color: ")
                params.args.append(args_s)

            stub_home_assistant.CallMethod(params)

        except:
            print("Invalid method")
            continue
        print("-------  -------\n")

    elif (option == "3"):
        print("------- ROOF -------")
        print("State: ", "Open" if actuators.roof.is_open == True else "Closed")
        print(" -- Available operations -- ")
        print("\t[1] Open Roof")
        print("\t[2] Close Roof")
        
        try:
            operation = int(input("\t Enter a action: "))
            params = atuadores_def_pb2.RemoteCallParams(actuator = 3, method = operation)
            stub_home_assistant.CallMethod(params)
        except:
            print("Invalid method")
            continue
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