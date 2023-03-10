import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { CodePipeline, CodePipelineSource, ShellStep } from 'aws-cdk-lib/pipelines';
// import * as sqs from 'aws-cdk-lib/aws-sqs';

export class MultiaccountdeployStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const pipeline = new CodePipeline(this, 'Pipeline', {
      pipelineName: 'Sme-Demo',
      synth: new ShellStep('Synth', {
        input: CodePipelineSource.gitHub('brayiyandres/pipelineSME', 'main'),
        commands: ['npm ci', 'npm run build', 'npx cdk synth']
      })
    });

  
  }
}
