"""
このFunctionはCloudWatch EvemtsからAuto ScalingでEC2 Instance Launch Successfulのイベントがあった場合に起動される。
"""
import os
import boto3

print('Loading function')

def lambda_handler(event, context):
    """
    イベントのEC2 InstanceをNLBにIPアドレスで登録する。
    """

    target_group_arn = os.environ['TARGET_GROUP']
    instance_id = event['detail']['EC2InstanceId']

    print('target_group_arn : ' + target_group_arn)
    print('instance_id : ' + instance_id)

    elbv2_client = boto3.client('elbv2')
    ec2_client = boto3.client('ec2')

    response = ec2_client.describe_instances(
        InstanceIds=[
            instance_id
        ],
    )
    private_ip_address = response['Reservations'][0]['Instances'][0]['PrivateIpAddress']

    response = elbv2_client.register_targets(
        TargetGroupArn=target_group_arn,
        Targets=[
            {
                'Id': private_ip_address
            }
        ]
    )

    return instance_id
