from aws_cdk import(
    assertions,
    Stack
)
from cdk_constructs.cdk_network.lib.cdk_network import CdkNetwork

def test_subnets_created():
    stack = Stack()
    CdkNetwork(stack, "cdk_network_layer")
    template = assertions.Template.from_stack(stack)
    template.has_resource_properties("AWS::EC2::Subnet", {
        "MapPublicIpOnLaunch": False
    })
    print(f"TEMPLATE: {template.to_json()}")
    template.has_resource("AWS::EC2::Subnet",3)


def test_vpc_created():
    stack = Stack()
    CdkNetwork(stack, "cdk_network_layer")
    template = assertions.Template.from_stack(stack)
    template.resource_count_is("AWS::EC2::VPC", 1)