import pika, sys, os

from recognizer import recognize

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='rpc_queue')

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
        f = open('test.ogg', 'wb')
        f.write(body)
        f.close()
        res = recognize(body)
        ch.basic_publish(exchange='',
                     routing_key=properties.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         properties.correlation_id),
                     body=res)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print("123")
        print(res)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='rpc_queue', on_message_callback=callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
