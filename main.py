import pulsar
from _pulsar import ConsumerType

from schemas import event_pb2


def emit_event():
    client = pulsar.Client('pulsar://localhost:6650')

    producer = client.create_producer('my-topic')

    event = event_pb2.MyEvent()
    event.id = "value1"
    event.name = "value2"
    event.count = 1

    event_bytes = event.SerializeToString()

    producer.send(event_bytes)

    producer.close()
    client.close()


def consume_event():
    client = pulsar.Client('pulsar://localhost:6650')

    consumer = client.subscribe(
        topic="my-topic",
        subscription_name="my-subscription",
        consumer_type=ConsumerType.Shared
    )

    while True:
        msg = consumer.receive()
        try:
            my_message = event_pb2.MyEvent()
            my_message.ParseFromString(msg.data())
            print("Received message with ID %s: %s" % (msg.message_id(), my_message))
            consumer.acknowledge(msg)
        except Exception as e:
            print("Failed to process message with ID %s: %s" % (msg.message_id(), e))
            consumer.negative_acknowledge(msg)
        client.close()

if __name__ == '__main__':
    #emit_event()
    consume_event()
