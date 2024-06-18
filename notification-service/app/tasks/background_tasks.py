import asyncio
from app.kafka.notification_consumers import user_consumer, order_consumer, payment_consumer

async def notification_tasks():
    asyncio.create_task(user_consumer)
    asyncio.create_task(order_consumer)
    asyncio.create_task(payment_consumer)