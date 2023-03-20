import pika, sys, os, time, json, base64

from modelCreator import ModelCreator

class ModelServer:
    def __init__(self, mqHost, rpcQName) -> None:
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=mqHost))
        self.channel = self.connection.channel()
        self.rpcQName = rpcQName

        self.channel.queue_declare(queue=self.rpcQName)
        self.model_creator = ModelCreator()

    def start(self):
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=self.rpcQName, on_message_callback=self._callback)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

    def _callback(self, ch, method, properties, body):
        msg = json.loads(body)
        # f = open('testRU.ogg', 'wb')
        # f.write(base64.b64decode(msg["audio"]))
        # f.close()
        print("start")
        start = time.time()
        recognizer = self.model_creator.get_model({"lang": msg["lang"]})
        res = recognizer.predict(base64.b64decode(msg["audio"]))
        ch.basic_publish(exchange='',
                     routing_key=properties.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         properties.correlation_id),
                     body=res)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print("stop")
        print(time.time() - start)

if __name__ == '__main__':
    try:
        ms = ModelServer('localhost', 'rpc_queue')
        ms.start()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)