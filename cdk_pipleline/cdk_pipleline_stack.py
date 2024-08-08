import aws_cdk as cdk
from constructs import Construct
from aws_cdk.pipelines import CodePipeline, CodePipelineSource, ShellStep
from cdk_pipleline.cdk_pipleline_app_stage import MyPipelineAppStage

class CdkPipelineStack(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        pipeline =  CodePipeline(self, "Pipeline",
                        pipeline_name="testCdkPipelineCrossAccount",
                        synth=ShellStep("Synth",
                            input=CodePipelineSource.connection("bhmangroliya/cdk-pipleline", "main", connection_arn='arn:aws:codeconnections:us-east-1:043037169024:connection/1fa5c7b0-2503-4dc2-b9cc-3501447864cb'),
                            commands=["npm install -g aws-cdk",
                                "python -m pip install -r requirements.txt",
                                "cdk synth"]
                        ),
                        cross_account_keys=True,
                        publish_assets_in_parallel=False
                    )
        
        deploy_to_dev= pipeline.add_stage(
                        MyPipelineAppStage(
                            self, "deployToDev",
                            env=cdk.Environment(account="043037169024", region="us-east-1")))
        
        deploy_to_test = pipeline.add_stage(
            MyPipelineAppStage(
                self,
                "deployToTest",
                env=cdk.Environment(account="451949150028", region="us-east-1"),
            ),
            pre=[cdk.pipelines.ManualApprovalStep("approval")],
        )