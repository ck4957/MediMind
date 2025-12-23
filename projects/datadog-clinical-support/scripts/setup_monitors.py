"""
Script to set up Datadog monitors
"""

import os
import sys
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v1.api.monitors_api import MonitorsApi
from datadog_api_client.v1.model.monitor import Monitor

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.datadog_config import DatadogConfig
from config.monitor_definitions import MONITOR_DEFINITIONS


def create_monitors():
    """Create all monitors in Datadog"""
    
    if not DatadogConfig.DD_API_KEY or not DatadogConfig.DD_APP_KEY:
        print("Error: DD_API_KEY and DD_APP_KEY must be set")
        print("Please configure your .env file")
        return
    
    configuration = Configuration()
    configuration.api_key['apiKeyAuth'] = DatadogConfig.DD_API_KEY
    configuration.api_key['appKeyAuth'] = DatadogConfig.DD_APP_KEY
    configuration.server_variables['site'] = DatadogConfig.DD_SITE
    
    with ApiClient(configuration) as api_client:
        api_instance = MonitorsApi(api_client)
        
        print("Creating Datadog monitors...")
        print("=" * 60)
        
        for monitor_def in MONITOR_DEFINITIONS:
            try:
                monitor = Monitor(
                    name=monitor_def['name'],
                    type=monitor_def['type'],
                    query=monitor_def['query'],
                    message=monitor_def['message'],
                    tags=monitor_def.get('tags', []),
                    priority=monitor_def.get('priority'),
                    options=monitor_def.get('options', {}),
                )
                
                response = api_instance.create_monitor(body=monitor)
                print(f"✓ Created: {monitor_def['name']}")
                print(f"  ID: {response.id}")
                
            except Exception as e:
                print(f"✗ Failed to create: {monitor_def['name']}")
                print(f"  Error: {str(e)}")
        
        print("=" * 60)
        print("Monitor setup complete!")


if __name__ == '__main__':
    create_monitors()
