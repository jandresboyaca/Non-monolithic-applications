from schemas.orden_pb2 import Orden


async def recibir_ordenes(consumer):
    while True:
        try:
            msg = consumer.receive()
            my_message = Orden()
            my_message.ParseFromString(msg.data())
            print("Received message with ID %s: %s" % (msg.message_id(), my_message))
            consumer.acknowledge(msg)
            #ordenes.append(my_message)
            #client.close()
        except Exception as e:
            print("Failed to process message with ID  %s" % (e))
