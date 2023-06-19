from constructs import Construct
from aws_cdk import (
    Stack
)
# Imports the Network App Construrct
from cdk_constructs.cdk_network.lib.cdk_network import CdkNetwork
# Definition to deploy the Network Construct as a Stack class.
class NetworkStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self._my_network_construct = CdkNetwork(self, 'MyVpc')

    @property
    def target_vpc(self):
        # Returns the VPC id 
        return self._my_network_construct.target_vpc
