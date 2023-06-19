from constructs import Construct
from aws_cdk import (
    aws_elasticloadbalancingv2 as elbv2,
    aws_ec2 as ec2
)

# VPC CIDR that will be used to create a new VPC
VPC_CIDR = "10.10.0.0/20"
# Subnet size for subnets
SUBNET_MASK = 24
# Max number of AZs
AZS = 2
# VPC Name
VPC_NAME = "MyVpc"


""" Main construct definition """
# VPC with 3 different subnets in 2 AZ.

class CdkNetwork(Construct):
   
    def create_VPC(self):
        """
        This function defines a VPC with 3 different layers, 
        each layer have 2 different subnets in 2 AZ. 
        """
        vpc = ec2.Vpc(
            self, "MyVpc", 
            #cidr = VPC_CIDR,
            ip_addresses = ec2.IpAddresses.cidr(VPC_CIDR),
            max_azs = AZS,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                subnet_type = ec2.SubnetType.PUBLIC,
                name = "Public",
                cidr_mask = SUBNET_MASK,
            ), 
                ec2.SubnetConfiguration(
                subnet_type = ec2.SubnetType.PRIVATE_WITH_EGRESS,
                name = "PrivateApp",
                cidr_mask = SUBNET_MASK
            ), 
                ec2.SubnetConfiguration(
                subnet_type = ec2.SubnetType.PRIVATE_ISOLATED,
                name = "PrivateDatabase",
                cidr_mask = SUBNET_MASK
            )
            ]
            )
        # Returns a VPC
        return vpc
    

    @property
    def target_vpc(self):
        return self._target_vpc

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        # VPC creation
        _target_vpc = self.create_VPC()
        self._target_vpc = _target_vpc