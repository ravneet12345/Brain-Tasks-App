import boto3
import subprocess
import os

def handler(event, context):
    job_id = event['CodePipeline.job']['id']
    try:
        subprocess.run([
            "aws", "eks", "update-kubeconfig",
            "--name", os.environ['CLUSTER_NAME'],
            "--region", os.environ['AWS_REGION']
        ], check=True)

        subprocess.run([
            "kubectl", "set", "image",
            f"deployment/{os.environ['DEPLOYMENT_NAME']}",
            f"{os.environ['CONTAINER_NAME']}={os.environ['ECR_IMAGE_URI']}"
        ], check=True)

        boto3.client('codepipeline').put_job_success_result(jobId=job_id)
    except Exception as e:
        boto3.client('codepipeline').put_job_failure_result(
            jobId=job_id,
            failureDetails={'message': str(e), 'type': 'JobFailed'}
        )
        raise
