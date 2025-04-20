#!/usr/bin/env python3
import os
import aws_cdk as cdk
from aws2.aws2_stack import Aws2Stack

app = cdk.App()
Aws2Stack(
    app, "Aws2Stack",
    env=cdk.Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"),
        region=os.getenv("CDK_DEFAULT_REGION", "us-east-1")
    )
)
app.synth()
