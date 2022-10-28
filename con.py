
import pika
import sys
import atuadores_def_pb2

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='ambient', exchange_type='direct')

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue


channel.queue_bind(
    exchange='ambient', queue=queue_name, routing_key='lightness')

print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    light = atuadores_def_pb2.Lightness(value=0.0)
    light.ParseFromString(body)

    print(" [x] %r" % (method.routing_key))
    print(light)


channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()