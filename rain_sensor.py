#!/usr/bin/env python
import atuadores_def_pb2
from threading import Timer
import random
from channel_utils import Channel

rain_channel = Channel()

def notify(channel, exchange):
    Timer(10.0, notify, args=(channel, exchange)).start()
    rainning_val = random.random()
    rainning = True if rainning_val < 0.45 else False
    rain_presence = atuadores_def_pb2.RainPresence(value=rainning)

    channel.basic_publish(
    exchange=exchange, routing_key='rain', body=rain_presence.SerializeToString())
    print(f" [x] Sent Message:Rain:{rainning}:{rainning_val}")


def notify_rain():
    notify(rain_channel.channel, 'ambient')

