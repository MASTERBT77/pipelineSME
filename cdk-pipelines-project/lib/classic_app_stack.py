from constructs import Construct
from aws_cdk import (
    Stack,
    aws_ec2 as ec2
)
# Imports the classic App Construrct
from cdk_constructs.cdk_classic_app.lib.cdk_classic_app import CdkClassicApp

# Definition to deploy the App Construct as a Stack class.
class ClassicAppStack(Stack):
    # This Function requires an existing VPC and an environment for tag and name purposes.
    def __init__(self, scope: Construct, construct_id: str,
                 vpc: ec2.Vpc, environment:str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        _my_classic_app_construct = CdkClassicApp(self, 'MyClassic', vpc, environment)
