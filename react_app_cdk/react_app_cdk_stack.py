from aws_cdk import (
    # Duration,
    Stack,
    aws_s3 as s3,
    aws_s3_deployment as s3_deployment,
    CfnOutput,
)
from constructs import Construct


class ReactAppCdkStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create bucket to store static website
        bucket = s3.Bucket(
            self,
            "AppBucket",
            bucket_name="react-app",
            public_read_access=True,
            block_public_access=s3.BlockPublicAccess(
                block_public_acls=False,
                block_public_policy=False,
                ignore_public_acls=False,
                restrict_public_buckets=False,
            ),
            access_control=s3.BucketAccessControl.BUCKET_OWNER_FULL_CONTROL,
            website_index_document="index.html",
        )

        s3_deployment.BucketDeployment(
            self,
            "StaticWebsite",
            sources=[s3_deployment.Source.asset("./my-app/build")],
            destination_bucket=bucket,
        )

        CfnOutput(
            self,
            id="BucketOutputs",
            value=f"{bucket.bucket_website_url}",
            description="API Gateway endpoint URL for Prod stage for Hello World function",
        )
