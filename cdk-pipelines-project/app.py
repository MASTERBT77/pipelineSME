#!/usr/bin/env python3
from aws_cdk import (
    App,
    Environment,
    Aspects
)
import os
import json

from cdk_nag import AwsSolutionsChecks
from lib.deployment_pipeline_stack import DeploymentPipelineStack
from cdk_nag import NagSuppressions 

# List of required parameters in parameters.json file.
PARAMETER_LIST = ["CI_CD_ACCOUNT", "CI_CD_REGION", "CI_CD_REPO_NAME", "DEV_ACCOUNT", "DEV_REGION", "QA_ACCOUNT","QA_REGION", "PROD_ACCOUNT", "PROD_REGION"]
FILE_PATH="parameters.json"

print(f"Required parameters {PARAMETER_LIST}")

# Load JSON parameters
with open(FILE_PATH,'r',encoding='utf-8') as r:
    try:
        json_file = json.load(r)
    except Exception as e:
        print(f"ERROR: Unable to load parameters file. {e}")
        os._exit(-1)
    print(f"Parameters: {json_file['params']}")

# Parameter validation
for param in PARAMETER_LIST:
    if param not in json_file['params']:
        print(f"ERROR: parameter {param} is not set in {FILE_PATH}")
        os._exit(-1)

cdk_parameters = json_file['params']
repo_name = cdk_parameters['CI_CD_REPO_NAME']

# Environments Definition, targets accounts (one for each environment) and region.
env_pipeline=Environment(account=cdk_parameters['CI_CD_ACCOUNT'], region=cdk_parameters['CI_CD_REGION'])
dev_env=Environment(account=cdk_parameters['DEV_ACCOUNT'], region=cdk_parameters['DEV_REGION'])
qa_env=Environment(account=cdk_parameters['QA_ACCOUNT'], region=cdk_parameters['QA_REGION'])
prod_env=Environment(account=cdk_parameters['PROD_ACCOUNT'], region=cdk_parameters['PROD_REGION'])

app = App()

# Pipeline definition
deployment = DeploymentPipelineStack(app, 'DeploymentPipelineStack', env=env_pipeline, repository_name=repo_name, dev_env=dev_env, qa_env=qa_env, prod_env=prod_env)
Aspects.of(app).add( AwsSolutionsChecks())
"""
This is where we add Nag Suppression
"""
NagSuppressions.add_resource_suppressions_by_path(deployment,
'/DeploymentPipelineStack/Pipeline/Pipeline/ArtifactsBucket/Resource',
    [
        {
            'id': 'AwsSolutions-S1',
            'reason': 'Because it is the bucket for temporary artifacts',
            },
    ]
        )
NagSuppressions.add_resource_suppressions_by_path(deployment,
'/DeploymentPipelineStack/Pipeline/Pipeline/Role/DefaultPolicy/Resource',
    [
        {
            'id': 'AwsSolutions-IAM5',
            'reason': 'Cross Account permissions needed for multi account deployment to work',
            },
    ]
        )
NagSuppressions.add_resource_suppressions_by_path(deployment,
f'/DeploymentPipelineStack/Pipeline/Pipeline/Source/{repo_name}/CodePipelineActionRole/DefaultPolicy/Resource',
    [
        {
            'id': 'AwsSolutions-IAM5',
            'reason': 'Cross Account permissions needed for multi account deployment to work',
            },
    ]
        )
NagSuppressions.add_resource_suppressions_by_path(deployment,
'/DeploymentPipelineStack/Pipeline/Pipeline/Build/Synth/CdkBuildProject/Role/DefaultPolicy/Resource',
    [
        {
            'id': 'AwsSolutions-IAM5',
            'reason': 'Cross Account permissions needed for multi account deployment to work',
            },
    ]
        )
NagSuppressions.add_resource_suppressions_by_path(deployment,
'/DeploymentPipelineStack/Pipeline/Pipeline/Build/Synth/CdkBuildProject/Role/DefaultPolicy/Resource',
    [
        {
            'id': 'AwsSolutions-IAM5',
            'reason': 'Cross Account permissions needed for multi account deployment to work',
            },
    ]
        )
NagSuppressions.add_resource_suppressions_by_path(deployment,
'/DeploymentPipelineStack/Pipeline/UpdatePipeline/SelfMutation/Role/DefaultPolicy/Resource',
    [
        {
            'id': 'AwsSolutions-IAM5',
            'reason': 'Permissions needed for SelfMutation pipelines',
            },
    ]
        )
NagSuppressions.add_resource_suppressions_by_path(deployment,
'/DeploymentPipelineStack/Pipeline/Pipeline/Development/linting_bandit/linting_bandit/Role/DefaultPolicy/Resource',
    [
        {
            'id': 'AwsSolutions-IAM5',
            'reason': 'Permissions needed for posting reports - Security validation stage',
            },
    ]
        )
NagSuppressions.add_resource_suppressions_by_path(deployment,
'/DeploymentPipelineStack/Pipeline/Pipeline/Development/UnitTest/UnitTest/Role/DefaultPolicy/Resource',
    [
        {
            'id': 'AwsSolutions-IAM5',
            'reason': 'Unit tests suppressions',
            },
    ]
        )
app.synth()