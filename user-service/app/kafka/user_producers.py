from typing import Annotated, Any, Generator
from aiokafka import AIOKafkaProducer # type: ignore
from fastapi import Depends


#========================================= Dependency Injection ========================================================
async def get_kafka_producer():
    producer = AIOKafkaProducer(bootstrap_servers='broker:19092')
    await producer.start()
    print("Producer Starting....!")
    try:
        yield producer
    finally:
        print("Producer is stopped....!")
        await producer.stop()
        

#=========================================================================================================================
async def producer(message:Any, topic: str, aio_producer:AIOKafkaProducer = Depends(get_kafka_producer)):
    try:
        result = await aio_producer.send_and_wait(topic , message.encode("utf-8"))
    except:
        print(f"Error In Print message...!")
    finally:
        await aio_producer.stop()
        return result
