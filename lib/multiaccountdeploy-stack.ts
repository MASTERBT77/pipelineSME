import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { CodePipeline, CodePipelineSource, ShellStep } from 'aws-cdk-lib/pipelines';
import { DemopipelineAppStage } from './demo-app-stage';

// import * as sqs from 'aws-cdk-lib/aws-sqs';

export class MultiaccountdeployStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const pipeline = new CodePipeline(this, 'Pipeline', {
      pipelineName: 'Sme-Demo',
      crossAccountKeys: true,
      synth: new ShellStep('Synth', {
        installCommands: ['npm i -g npm@latest'],
        input: CodePipelineSource.gitHub('MASTERBT77/pipelineSME', 'main'),
        commands: ['npm ci', 'npm run build', 'npx cdk synth']
      })
    });

    pipeline.addStage(
      new DemopipelineAppStage(this, "DEV", {
        env: {account: "268050465834", region:"us-east-1"}
      }
      
      
      
      
      )


    )
  }
}
