#!/usr/bin/env python
import atuadores_def_pb2
from threading import Timer
import random
from channel_utils import Channel

temperature_channel = Channel()

def notify(channel, exchange):
    Timer(2.0, notify, args=(channel, exchange)).start()
    temperature_value = int(random.random()*620)
    temperature = atuadores_def_pb2.Temperature(value=temperature_value)

    channel.basic_publish(
    exchange=exchange, routing_key='temperature', body=temperature.SerializeToString())
    print(f" [x] Sent Message:Temperature:{temperature_value}")


def notify_temperature():
    notify(temperature_channel.channel, 'ambient')
