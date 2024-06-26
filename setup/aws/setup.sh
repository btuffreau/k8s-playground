#!/usr/bin/env bash

set -euo pipefail
cd "$(dirname -- "$0")" || exit 1

export AWS_REGION=eu-west-3
export AWS_PROFILE=dev

NAME=${1:-}

if [ -z "$NAME" ]; then
  echo "Please provide a candidate's name for the instance"
  exit 1
fi

key="${HOME}"/interview-rsa.pem

aws secretsmanager get-secret-value --secret-id interview-rsa --query SecretString --output text > "$key"
chmod 600 "$key"

instanceId=$(aws ec2 run-instances --key-name interview --instance-type t2.large  \
  --image-id ami-07bc135c11aeb2d65 --region eu-west-3 --subnet-id subnet-03846ca7b4b85febc \
  --associate-public-ip-address \
  --user-data file://"$(pwd)"/cloud-init.yaml \
  --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=interview-${NAME}},{Key=Owner,Value=fuji}]" | jq -r .Instances[0].InstanceId)

echo "Waiting for ec2 instance..."
sleep 10

echo "aws profile: ${AWS_PROFILE}"
echo "region: ${AWS_REGION}"
echo "instance ID: ${instanceId}"
echo
echo "ssh -i ${key} ec2-user@$(aws ec2 describe-instances --instance-ids "${instanceId}" --query 'Reservations[*].Instances[*].PublicDnsName' --output text)"
echo
echo -e "remember to terminate the instance when finished:\n\t aws ec2 --profile $AWS_PROFILE --region $AWS_REGION terminate-instances --instance-ids ${instanceId}"