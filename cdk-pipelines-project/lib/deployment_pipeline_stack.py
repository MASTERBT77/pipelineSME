from constructs import Construct
from aws_cdk import (
    Stack,
    StackProps,
    aws_codecommit as codecommit
)
from aws_cdk.pipelines import (
    CodePipeline,
    CodePipelineSource,
    ShellStep,
    ManualApprovalStep
)

from .deployment_stage import DeploymentStage
from .security_validations import SecurityValidations
from cdk_nag import NagSuppressions 

"""
 The stack that defines the application pipeline
"""
class DeploymentPipelineStack(Stack): 
    @property
    def repository_name(self):
        return self._repository_name

    def __init__(self, scope: Construct, construct_id: str, env, repository_name: str, dev_env, qa_env, prod_env, **kwargs) -> None:
        super().__init__(scope, construct_id,env=env)
        """
        """
        self._repository_name=repository_name
        repository=codecommit.Repository.from_repository_name(self, "CodeCommitRepo",repository_name)
        pipeline=CodePipeline(self, "Pipeline",
            pipeline_name='infra-deployment-pipeline', cross_account_keys=True,enable_key_rotation=True,
            synth=ShellStep("Synth",
                input=CodePipelineSource.code_commit(repository,"master"),
                install_commands=[
                    "npm install -g aws-cdk",
                    "pip install -r requirements.txt"
                    ],
                commands=[
                    "ls -lstra 2>&1",
                    "cdk synth >>synth.out 2>&1", 
                    "cat synth.out"
                    ],
                    ))
        """ 
        This is where we add the application stages.
        Each stage point to deploy the application in a different account
        """
        deploy_dev=pipeline.add_stage(DeploymentStage(self, 'Development', environment='dev', env=dev_env))
        """
        This is where we add security validations
        """
        deploy_dev.add_pre(SecurityValidations().linting, SecurityValidations().unit_tests)
        deploy_qa=pipeline.add_stage(DeploymentStage(self, 'Quality', environment='qa', env=qa_env))
        deploy_prod=pipeline.add_stage(DeploymentStage(self, 'production', environment='prod', env=prod_env))
        """
        This is where we add the tests and manual approval steps
        """
        deploy_qa.add_pre(ManualApprovalStep("PromoteToQA"))
        deploy_prod.add_pre(ManualApprovalStep("PromoteToProduction"))
        pipeline.build_pipeline()