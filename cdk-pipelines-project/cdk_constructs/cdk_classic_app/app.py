#!/usr/bin/env python3

import aws_cdk as cdk

from cdk_classic_app.cdk_classic_app_stack import CdkClassicAppStack


app = cdk.App()
CdkClassicAppStack(app, "cdk-classic-app")

app.synth()
