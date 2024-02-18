from pathlib import Path

import aws_cdk.aws_iam as iam
import aws_cdk.aws_lambda as lambda_
import aws_cdk.aws_s3 as s3
from aws_cdk import Duration, RemovalPolicy, Stack
from aws_cdk.aws_lambda_event_sources import S3EventSourceV2
from aws_cdk.aws_lambda_python_alpha import PythonLayerVersion
from constructs import Construct


class CdkLlmServerlessStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # create s3 bucket
        transcriptions_bucket = s3.Bucket(self, "transcriptions-bucket-llm-klichx")
        recordings_bucket = s3.Bucket(self, "recordings-bucket-llm-klichx")

        # create lambda function
        my_role = iam.Role(
            self, "My Role", assumed_by=iam.ServicePrincipal("lambda.amazonaws.com")
        )

        layer = PythonLayerVersion(
            self,
            "LLMSummariseLayer",
            entry="./cdk_llm_serverless/build",
            compatible_runtimes=[lambda_.Runtime.PYTHON_3_12],
            removal_policy=RemovalPolicy.DESTROY,
        )
        transcribe_fn = lambda_.Function(
            self,
            "TranscribeFunction",
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler="index.handler",
            code=lambda_.Code.from_asset(
                str(Path(".", "cdk_llm_serverless", "transcribe_lambda"))
            ),
            role=my_role,
            environment={
                "S3BUCKETNAMETEXT": transcriptions_bucket.bucket_name,
            },
        )

        summarise_fn = lambda_.Function(
            self,
            "SummariseFunction",
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler="index.handler",
            code=lambda_.Code.from_asset(
                str(Path(".", "cdk_llm_serverless", "summarise_lambda"))
            ),
            role=my_role,
            layers=[layer],
            timeout=Duration.seconds(30),
        )

        my_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                "service-role/AWSLambdaBasicExecutionRole"
            )
        )
        my_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess")
        )
        my_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonTranscribeFullAccess")
        )
        my_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonBedrockFullAccess")
        )

        # trigger lambda function with s3 bucket
        summarise_fn.add_event_source(
            S3EventSourceV2(
                transcriptions_bucket,
                events=[s3.EventType.OBJECT_CREATED],
            )
        )
        transcribe_fn.add_event_source(
            S3EventSourceV2(
                recordings_bucket,
                events=[s3.EventType.OBJECT_CREATED],
            )
        )
