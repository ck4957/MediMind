"""
Script to test Kafka connectivity
"""

from confluent_kafka import Producer
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.kafka_config import KafkaConfig


def test_connection():
    """Test connection to Kafka cluster"""
    print("Testing Kafka connection...")
    print(f"Bootstrap servers: {KafkaConfig.BOOTSTRAP_SERVERS}")
    
    try:
        config = KafkaConfig.get_producer_config()
        producer = Producer(config)
        
        # Get cluster metadata
        metadata = producer.list_topics(timeout=10)
        
        print("\n✓ Connection successful!")
        print(f"\nCluster metadata:")
        print(f"  Cluster ID: {metadata.cluster_id}")
        print(f"  Number of brokers: {len(metadata.brokers)}")
        print(f"\nAvailable topics:")
        for topic in metadata.topics:
            print(f"  - {topic}")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Connection failed: {e}")
        return False


if __name__ == '__main__':
    test_connection()
