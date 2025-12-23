import asyncio
import json
import logging
import os
from confluent_kafka import Consumer, KafkaException
from config.kafka_config import KafkaConfig
from api.mock_service import MockDataService

logger = logging.getLogger("consumer_service")

class KafkaConsumerService:
    def __init__(self):
        self.running = False
        self.consumer = None
        self.mock_service = MockDataService()
        self.use_mock = False

    def _init_consumer(self):
        try:
            conf = KafkaConfig.get_consumer_config('cancer-risk-dashboard-group')
            self.consumer = Consumer(conf)
            topics = [
                KafkaConfig.TOPIC_IMAGING,
                KafkaConfig.TOPIC_LAB_RESULTS,
                KafkaConfig.TOPIC_CLINICAL_NOTES,
                KafkaConfig.TOPIC_PREDICTIONS,
                KafkaConfig.TOPIC_ALERTS,
                getattr(KafkaConfig, 'TOPIC_PATIENT_PROFILES', 'patient-profiles-stream')
            ]
            self.consumer.subscribe(topics)
            logger.info(f"Subscribed to topics: {topics}")
            self.use_mock = False
        except Exception as e:
            logger.error(f"Failed to initialize Kafka consumer: {e}")
            logger.warning("Falling back to Mock Data Service")
            self.use_mock = True

    async def start(self, message_callback):
        self.running = True
        self._init_consumer()

        if self.use_mock:
            await self.mock_service.start(message_callback)
            return

        # Run Kafka consumption loop
        try:
            while self.running:
                # We use a small timeout to allow the loop to check self.running
                msg = self.consumer.poll(0.5)

                if msg is None:
                    continue
                if msg.error():
                    logger.error(f"Consumer error: {msg.error()}")
                    continue

                try:
                    value = msg.value().decode('utf-8')
                    topic = msg.topic()
                    data = json.loads(value)
                    
                    # Envelope for frontend
                    payload = json.dumps({
                        "type": topic,
                        "data": data
                    })
                    
                    await message_callback(payload)
                except Exception as e:
                    logger.error(f"Error processing message: {e}")
                
                # Yield control to event loop
                await asyncio.sleep(0.01)
                
        except Exception as e:
            logger.error(f"Consumer loop error: {e}")
        finally:
            self.close()

    async def stop(self):
        self.running = False
        if self.use_mock:
            await self.mock_service.stop()

    def close(self):
        if self.consumer:
            self.consumer.close()
