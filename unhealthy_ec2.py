"""
このFunctionはCloudWatch Evemtsから1分ごとに起動される。
"""
import os
import boto3

print('Loading function')

def lambda_handler(event, context):
    """
    環境変数で定義されたターゲットグループでUnhealthyのIPアドレスの登録を解除して、同じIPアドレスのEC2 Instanceを削除する。
    """

    target_group_arn = os.environ['TARGET_GROUP']

    elbv2_client = boto3.client('elbv2')

    target_group = elbv2_client.describe_target_groups(
        TargetGroupArns=[
            target_group_arn
        ]
    )

    health_response = elbv2_client.describe_target_health(
        TargetGroupArn=target_group_arn
    )

#    print("health_response:")
#    print(health_response)

    unhealthy_targets = [
        i for i in health_response['TargetHealthDescriptions'] \
        if i['TargetHealth']['State'] == "unhealthy"
    ]

#    print("unhealthy_targets:")
#    print(unhealthy_targets)

    #print('unhealthy_targets: ' + ','.join(unhealthy_targets))

    if not unhealthy_targets:
        print("Unhealthy Instance is nothing.")
        return ""

    unhealthy_ips = [{'Id':t['Target']['Id']} for t in unhealthy_targets]
    print(unhealthy_ips)

    elbv2_client.deregister_targets(
        TargetGroupArn=target_group_arn,
        Targets=unhealthy_ips
    )

    ec2_client = boto3.client('ec2')

    unhealthy_instances = ec2_client.describe_instances(
        Filters=[
            {
                'Name': 'private-ip-address',
                'Values': [t['Target']['Id'] for t in unhealthy_targets]
            },
            {
                'Name': 'vpc-id',
                'Values': [t['VpcId'] for t in target_group['TargetGroups']]
            },
        ],
    )

    print(unhealthy_instances)

    unhealthy_instance_ids = [
        i['Instances'][0]['InstanceId'] for i in unhealthy_instances['Reservations']
    ]
    print('unhealthy_instance_ids: ' + ','.join(unhealthy_instance_ids))

    if unhealthy_instances:
        ec2_client.terminate_instances(
            InstanceIds=unhealthy_instance_ids
        )

    return ','.join([t['Target']['Id'] for t in unhealthy_targets])
