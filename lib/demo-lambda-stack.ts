import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { LambdaRestApi } from 'aws-cdk-lib/aws-apigateway';
import { Code, Function, InlineCode, Runtime } from 'aws-cdk-lib/aws-lambda';

export class DemolambdaStack extends cdk.Stack {
    constructor(scope: Construct, id: string, props?: cdk.StackProps) {
      super(scope, id, props);
  
      const index =  new Function(this, 'LambdaFunction', {
        runtime: Runtime.NODEJS_14_X,
        handler: 'index.handler',
        code: Code.fromAsset("lambda")
      });
    }
}