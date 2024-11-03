#!/bin/bash

# == often change ==
AMI=ami-0d04f0c2f96897faf            # AMI to launch from
TYPE=t2.micro                       # EC2 instance type
TAG_SERVICE=avery-chat-ec2    # Tag: Service Name
TAG_USER=avery                       # Tag: User Name
TAG_ROLE=web                         # Tag: Role

# ==  set it once and seldom change ==
TAG_APPLICATION=yeogi
TAG_NAME=D-${TAG_SERVICE}-001
TAG_REVISION=5.0
TAG_OS=AmazonLinux2
TAG_TEAM=avery
TAG_SVC_TYPE=DEV-${TAG_SERVICE}
TAG_ENVIRIONMENT=development

# ==  set it once and seldom change ==
SUBNET=subnet-05dc43006e33b83b6  # Subnet ID
SG=sg-0219eaa05ed9d6597          # security group ID
KEY=dev@within.co.kr             # EC2 key pair name
COUNT=1                          # how many instances to launch
IAM=AdministratorRole            # EC2 IAM role name
EBS_SIZE=32                      # root EBS volume size (GB)

# == almost never change; just leave it as-is ==
aws ec2 run-instances --image-id $AMI \
    --subnet-id $SUBNET \
    --security-group-ids $SG --count $COUNT \
    --instance-type $TYPE --key-name $KEY \
    --iam-instance-profile Name=$IAM \
    --block-device-mapping DeviceName=/dev/xvda,Ebs={VolumeSize=$EBS_SIZE} \
    --tag-specifications "ResourceType=instance, Tags=[ \
    {Key=Application,Value=$TAG_APPLICATION}, \
    {Key=Name,Value=$TAG_NAME}, \
    {Key=Service,Value=$TAG_SERVICE}, \
    {Key=User,Value=$TAG_USER}, \
    {Key=Revision,Value=$TAG_REVISION}, \
    {Key=os,Value=$TAG_OS}, \
    {Key=Team,Value=$TAG_TEAM}, \
    {Key=svc-type,Value=$TAG_SVC_TYPE}, \
    {Key=Environment,Value=$TAG_ENVIRIONMENT}, \
    {Key=Role,Value=$TAG_ROLE} \
    ]"
