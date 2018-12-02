import boto3
import psutil
import schedule
import time
import re

sts = boto3.client('sts')
cw = boto3.client('cloudwatch', region_name='ap-northeast-1')

def getInstanceId():
    userId = sts.get_caller_identity()['UserId']
    return re.findall(':(mi-.*)$', userId)[0]

def job():
    cpu = psutil.cpu_percent(interval=20)
    memory = psutil.virtual_memory().percent

    instanceId = getInstanceId()
    dimensions = [{'Name':'InstanceId', 'Value':instanceId}]

    PutMetricData = cw.put_metric_data(
        Namespace='RasPi',
        MetricData=[
            {
                'MetricName': 'CpuUsage',
                'Dimensions': dimensions,
                'Value': cpu,
                'Unit': 'Percent'
            },
            {
                'MetricName': 'MemoryUsage',
                'Dimensions': dimensions,
                'Value': memory,
                'Unit': 'Percent'
            }
        ]
    )

if __name__ == '__main__':
    schedule.every().minutes.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)    





