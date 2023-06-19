from aws_cdk import(
    aws_ec2 as ec2,
    App,
    Stack,
    assertions,
    Environment
)
from cdk_constructs.cdk_classic_app.lib.cdk_classic_app import CdkClassicApp

def create_vpc(scope):
 # VPC CIDR that will be used to create a new VPC
    VPC_CIDR = "10.10.0.0/20"
    # Subnet size for subnets
    SUBNET_MASK = 24
    # Max number of AZs
    AZS = 2
    my_vpc = ec2.Vpc(
        scope, "MyVpc",
        cidr = VPC_CIDR,
        max_azs = AZS,
        # configuration will create 3 groups in 2 AZs = 6 subnets.
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
    return my_vpc

def test_asg_created():
    app = App()
    stack = Stack(app, "MyStack")
    CdkClassicApp(stack, 'MyClassic', vpc = create_vpc(stack), environment="test")
    template = assertions.Template.from_stack(stack)
    template.resource_count_is("AWS::AutoScaling::AutoScalingGroup", 1)

def test_launch_configuration_created():
    app = App()
    stack = Stack(app, "MyStack")
    CdkClassicApp(stack, 'MyClassic', vpc = create_vpc(stack), environment="test")
    template = assertions.Template.from_stack(stack)
    template.resource_count_is("AWS::AutoScaling::LaunchConfiguration", 1)

def test_elb_created():
    app = App()
    stack = Stack(app, "MyStack")
    CdkClassicApp(stack, 'MyClassic', vpc = create_vpc(stack), environment="test")
    template = assertions.Template.from_stack(stack)
    template.resource_count_is("AWS::ElasticLoadBalancingV2::LoadBalancer", 1)

def test_bucket_created():
    app = App()
    stack = Stack(app, "MyStack")
    CdkClassicApp(stack, 'MyClassic', vpc = create_vpc(stack), environment="test")
    template = assertions.Template.from_stack(stack)
    template.resource_count_is("AWS::S3::Bucket", 1)

