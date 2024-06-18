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
    notification_func_map = {
        "welcome_user": user_notification.welcome_notification_func,
        "user_verification": user_notification.verified_notification_func,
        "update_user_notification": user_notification.user_update_notification_func,
    }
    await process_messages(consumer_kafka, notification_func_map)

async def order_consumer():
    consumer_kafka = await get_kafka_consumer(ORDER_TOPIC)
    notification_func_map = {
        "order_create_notification": order_notification.order_create_notification_func,
        "order_on_ship_notification": order_notification.order_on_ship_notification_func,
        "order_on_way_notification": order_notification.order_on_way_notification_func,
        "order_cancelled_notification": order_notification.order_cancelled_notification_func,
        "back_order_notification": order_notification.back_order_notification_func,
        "order_arrive_notification": order_notification.order_arrive_notification_func,
    }
    await process_messages(consumer_kafka, notification_func_map)

async def payment_consumer():
    consumer_kafka = await get_kafka_consumer(PAYMENT_TOPIC)
    notification_func_map = {
        "payment_received_notification": payment_notification.payment_received_notification_func,
        "payment_success_notification": payment_notification.payment_success_notification_func,
        "payment_failed_notification": payment_notification.payment_failed_notification_func,
    }
    await process_messages(consumer_kafka, notification_func_map)
