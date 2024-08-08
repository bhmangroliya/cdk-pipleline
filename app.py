#!/usr/bin/env python3
import aws_cdk as cdk
from cdk_pipleline.cdk_pipleline_stack import CdkPipelineStack

app = cdk.App()
CdkPipelineStack(app, "CdkPipelineStack",
    env=cdk.Environment(account="043037169024", region="us-east-1")
)

app.synth()
