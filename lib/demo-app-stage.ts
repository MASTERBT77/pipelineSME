import { Stage, StageProps } from "aws-cdk-lib";
import { Construct } from "constructs";
import { DemolambdaStack } from "./demo-lambda-stack";

export class DemopipelineAppStage extends Stage {
  constructor(scope: Construct, id: string, props?: StageProps){
    super(scope, id, props)

    const LambdaStack = new DemolambdaStack( this, "lambdaStack") 

  }  



}