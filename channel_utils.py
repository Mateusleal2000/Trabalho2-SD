import pika
import atuadores_def_pb2


class Channel:

    def __init__(self) -> None:
        self.connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()

        self.channel.exchange_declare(exchange='ambient', exchange_type='direct')

    def bind(self,queue_name, key_of_routing):

        self.channel.queue_bind(
            exchange='ambient', queue=queue_name, routing_key=key_of_routing)

    def create_queue(self):
        result = self.channel.queue_declare(queue='', exclusive=True)
        return result.method.queue

    def consume(self, queue_name, callback):
        
        self.channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)

    def start(self):
        self.channel.start_consuming()