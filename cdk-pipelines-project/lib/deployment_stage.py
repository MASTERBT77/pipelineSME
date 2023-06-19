import aws_cdk as cdk
from constructs import Construct
from .network_stack import NetworkStack
from .classic_app_stack import ClassicAppStack


# Definition to deploy the Classic App and Network Stacks.
class DeploymentStage(cdk.Stage):

    def __init__(self, scope: Construct, construct_id: str, environment: str, env, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        # Stacks Deployment definition
        network_stack = NetworkStack(self, 'MyNetwork', env=env) # do not put down
        classic_stack = ClassicAppStack(self, "MyClassic", env=env, environment=environment, vpc=network_stack.target_vpc)
        classic_stack.add_dependency(network_stack)
