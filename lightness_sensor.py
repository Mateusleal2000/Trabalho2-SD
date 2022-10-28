#!/usr/bin/env python
import atuadores_def_pb2
from threading import Timer
import random
from channel_utils import Channel

light_channel = Channel()


def notify(channel, exchange):
    Timer(5.0, notify, args=(channel, exchange)).start()
    lightness_value = random.random()
    lightness = atuadores_def_pb2.Lightness(value=lightness_value)

    channel.basic_publish(
    exchange=exchange, routing_key='lightness', body=lightness.SerializeToString())
    print(f" Mensagem:Light:{lightness_value}")


def notify_lightness():
    notify(light_channel.channel, 'ambient')


