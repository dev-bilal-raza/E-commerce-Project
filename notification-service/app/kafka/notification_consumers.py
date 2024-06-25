from typing import Union, List
import json
from aiokafka import AIOKafkaConsumer
from aiokafka.errors import KafkaConnectionError
from fastapi import HTTPException
from app.settings import USER_TOPIC, ORDER_TOPIC, PAYMENT_TOPIC
from app.controllers import user_notification, order_notification, payment_notification

async def get_kafka_consumer(*topics: Union[str, List[str]]):
    consumer_kafka = AIOKafkaConsumer(
        *topics,
        bootstrap_servers=["broker:19092"],
        auto_offset_reset="earliest"
    )
    print("Creating Kafka Consumer...")
    await consumer_kafka.start()
    return consumer_kafka

async def process_messages(consumer_kafka, notification_func_map):
    try:
        async for message in consumer_kafka:
            try:
                value = json.loads(bytes(message.value).decode("utf-8"))
                notification_type = value.get("notification_type")
                email = value.get("email")
                
                if notification_type and email:
                    notification_func = notification_func_map.get(notification_type)
                    if notification_func:
                        notification_func(email)
                    else:
                        print(f"Unknown notification type: {notification_type}")
                else:
                    print("Invalid message format")
            except json.JSONDecodeError as e:
                print(f"Failed to decode message: {e}")
    except KafkaConnectionError as ke:
        raise HTTPException(status_code=500, detail=f"Kafka connection error: {str(ke)}")
    finally:
        await consumer_kafka.stop()

async def user_consumer():
    consumer_kafka = await get_kafka_consumer(USER_TOPIC)
    await process_messages(consumer_kafka, user_notification.user_notification_func_map)

async def order_consumer():
    consumer_kafka = await get_kafka_consumer(ORDER_TOPIC)
    await process_messages(consumer_kafka, order_notification.order_notification_func_map)

async def payment_consumer():
    consumer_kafka = await get_kafka_consumer(PAYMENT_TOPIC)
    await process_messages(consumer_kafka, payment_notification.payment_notification_func_map)
