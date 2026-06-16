import json
import boto3
import time

ssm = boto3.client('ssm')

INSTANCE_ID = 'i-07dfefe4c3e028fea'
BUCKET = 'bis202-images-alif240341'

def lambda_handler(event, context):
    try:
        body = json.loads(event.get('body') or '{}')
        image_name = body.get('image')
    except Exception:
        image_name = None

    if not image_name:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Provide "image" in the request body'})
        }

    command = (
        f"sudo -u ssm-user bash -c 'cd /home/ssm-user/yolov5 && "
        f"aws s3 cp s3://{BUCKET}/uploads/{image_name} input.jpg && "
        f"python3 detect.py --weights yolov5s.pt --source input.jpg "
        f"--project /tmp --name out --exist-ok && "
        f"aws s3 cp /tmp/out/input.jpg s3://{BUCKET}/output/{image_name}'"
    )

    resp = ssm.send_command(
        InstanceIds=[INSTANCE_ID],
        DocumentName='AWS-RunShellScript',
        Parameters={'commands': [command]}
    )
    command_id = resp['Command']['CommandId']

    for _ in range(25):
        time.sleep(2)
        inv = ssm.get_command_invocation(
            CommandId=command_id, InstanceId=INSTANCE_ID)
        if inv['Status'] in ('Success', 'Failed', 'Cancelled', 'TimedOut'):
            break

    return {
        'statusCode': 200 if inv['Status'] == 'Success' else 500,
        'body': json.dumps({
            'status': inv['Status'],
            'output_image': f's3://{BUCKET}/output/{image_name}',
            'log': inv['StandardOutputContent'][-500:],
            'error': inv['StandardErrorContent'][-500:]
        })
    }
