from aws_cdk import(
    App,
    Stack,
    assertions, 
    Environment
)
from lib.deployment_pipeline_stack import DeploymentPipelineStack


def test_pipelines_created():
    app = App()
    stack = Stack(app, "MyStack")
    env_dev = Environment(account="12312312341234", region="us-east-1")
    env_qa = Environment(account="12312312341234", region="us-east-1")
    env_prod = Environment(account="12312312341234", region="us-east-1")

    stack = DeploymentPipelineStack(stack, "pipeline_artifact", env_dev, "MyRepo", env_dev, env_qa, env_prod)
    template = assertions.Template.from_stack(stack)
    template.resource_count_is("AWS::CodePipeline::Pipeline", 1)