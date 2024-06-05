import json
from typing import Annotated
from aiokafka import AIOKafkaConsumer # type: ignore
from aiokafka.errors import KafkaConnectionError # type: ignore
from fastapi import Depends
from app.controllers.crud_user import add_user_in_db, update_user
from app.controllers.kong_controller import create_consumer_in_kong, create_jwt_credential_in_kong
from app.settings import KONG_TOPIC, USER_TOPIC
from app.kafka.user_producers import producer

#===================================================================================================================
async def get_kafka_consumer(topics: str | list[str]):
    consumer_kafka = AIOKafkaConsumer(
        *topics,
        bootstrap_servers="broker:19092",
        auto_offset_reset="earliest",
        # group_id="user",
    )
    print("Creating Kafka Consumer...")
    await consumer_kafka.start()
    return consumer_kafka
#===================================================================================================================


async def user_consumer():
    # consumer_kafka = AIOKafkaConsumer(
    #     "user",
    #     bootstrap_servers="broker:19092",
    #     auto_offset_reset="earliest",
    #     # group_id="user",
    # )
    # print("Creating Kafka Consumer...")
    # await consumer_kafka.start()
    consumer_kafka = await get_kafka_consumer(USER_TOPIC)
    print("Topic Created SuccessFully")
    try:
        async for msg in consumer_kafka:
            print("Listening...")
            value = bytes(msg.value).decode('utf-8')  # type: ignore
            user = add_user_in_db(user_form=json.loads(value))
            await producer(message=user, topic=KONG_TOPIC)
            print(msg.value)
    except KafkaConnectionError as e:
        print(e)
    finally:
        await consumer_kafka.stop()
        return user
    
async def user_update_consumer():
    # consumer_kafka = AIOKafkaConsumer(
    #     "user",
    #     bootstrap_servers="broker:19092",
    #     auto_offset_reset="earliest",
    #     # group_id="user",
    # )
    # print("Creating Kafka Consumer...")
    # await consumer_kafka.start()
    
    consumer_kafka = await get_kafka_consumer(USER_TOPIC)
    print("Topic Created SuccessFully")
    try:
        async for msg in consumer_kafka:
            print("Listening...")
            value = bytes(msg.value).decode('utf-8')  # type: ignore
            user = update_user(user_form=json.loads(value))
            await producer(message=user, topic=KONG_TOPIC)
            print(msg.value)
    except KafkaConnectionError as e:
        print(e)
    finally:
        await consumer_kafka.stop()
        return user

async def kong_consumer():
    consumer_kafka = await get_kafka_consumer(KONG_TOPIC)
    print("Topic Created SuccessFully")
    try:
        async for msg in consumer_kafka:
            print("Listening...")
            value = bytes(msg.value).decode('utf-8')  # type: ignore
            create_consumer_in_kong(value.user_name)
            create_jwt_credential_in_kong(value.user_name, value.kid)
            print(msg.value)
    except KafkaConnectionError as e:
        print(e)
    finally:
        await consumer_kafka.stop()
    