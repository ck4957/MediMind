"""
Script to create Kafka topics for the cancer risk assessment system
"""

from confluent_kafka.admin import AdminClient, NewTopic
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.kafka_config import KafkaConfig, TOPIC_CONFIGS


def create_topics():
    """Create all required Kafka topics"""
    
    # Initialize admin client
    admin_client = AdminClient(KafkaConfig.get_producer_config())
    
    # Create topic configurations
    topics = []
    for topic_name, config in TOPIC_CONFIGS.items():
        topics.append(NewTopic(
            topic_name,
            num_partitions=config['num_partitions'],
            replication_factor=config['replication_factor'],
            config=config['config']
        ))
    
    # Create topics
    print("Creating topics...")
    fs = admin_client.create_topics(topics)
    
    # Wait for operation to finish
    for topic, f in fs.items():
        try:
            f.result()  # The result itself is None
            print(f"✓ Topic {topic} created successfully")
        except Exception as e:
            print(f"✗ Failed to create topic {topic}: {e}")


if __name__ == '__main__':
    print("Kafka Topic Creation Script")
    print("=" * 50)
    create_topics()
    print("=" * 50)
    print("Done!")
