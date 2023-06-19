from constructs import Construct
from aws_cdk import (
    aws_elasticloadbalancingv2 as elbv2,
    aws_ec2 as ec2,
    aws_autoscaling as asg,
    aws_rds as rds,
    aws_iam as iam,
    Tags as tags, 
    Duration,
    aws_ssm as ssm,
    aws_s3 as s3,
    Aws
)
from dataclasses import dataclass

#User Data file path 
import os 
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'userdata.sh')

# Parameters to define EC2 instance type, Db instance type & subnets for each layer.
# Each parameter type is string

EC2_TYPE = "t3.medium"
DB_TYPE = "t3.medium"
SUBNET_DATABASES_GROUP = "PrivateDatabase"
SUBNET_APP_GROUP = "PrivateApp"

# Read user data file, this file contains the insutructions to excecute on the EC2 instance bootstrap
with open(filename) as f:
    user_data = f.read()

""" Main construct definition """
# S3 bucket to store the artifacts for the app deployment.
# SSM parameters to define diferents paths and names requieres for the app at the deployment stage.
# Security Group to define inbount/outbount rules for the different NICs.
# Load balancer to expose the application and distribute traffic across the diferente EC2 instances of the App layer.
# Auto Scaling group to provision EC2 instances with scaling capacity based on defined metrics. 
# Aurora database to provide the data layer 

class CdkClassicApp(Construct):

    def create_s3(self, s3_name):
        """
        This function deploy an S3 bucket with S3 managed encryption
        and no open public access.
        """
        _bucket = s3.Bucket(
            self, s3_name, 
            bucket_name = s3_name,
            encryption = s3.BucketEncryption.S3_MANAGED,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL)
        """
        The ssm functions store string values requiere for the app deployment
        as parameters in the parameter store service of SSM.
        """
        ssm.StringParameter(self, 'parameterpath',
            parameter_name = "/BluAge/S3_CONF_PATH",
            description = 'path on s3',
            string_value = "artifacts/config/tomcat/conf"
        )

        ssm.StringParameter(self, 'parameterbucketname',
            parameter_name = "/BluAge/BUCKET_NAME",
            description = 'bucket name',
            string_value = s3_name
        )

        ssm.StringParameter(self, 'parameterpathsharedapps',
            parameter_name = "/BluAge/S3_SHAREDAPPS_PATH",
            description = 'path shared app files',
            string_value = "artifacts/config/tomcat/webapps"
        )

        ssm.StringParameter(self, 'parameterpathsharedfile',
            parameter_name = "/BluAge/S3_SHARED_FILE",
            description = 'path shared files',
            string_value = "artifacts/config/tomcat/shared/shared.zip"
        )

        ssm.StringParameter(self, 'parametertomcatfolder',
            parameter_name = "/BluAge/TOMCAT_ROOT_FOLDER",
            description = 'path tomcat',
            string_value = "/usr/share/tomcat9"
        )
        # Returns a single S3 bucket
        return _bucket

    def create_sg(self, vpc, sg_name):
        """
        This function defines a security group linked to a VPC provided. 
        It also allow all outbound traffic.
        """
        _sg = ec2.SecurityGroup(
            self, sg_name,
            security_group_name = sg_name,
            vpc = vpc,
            allow_all_outbound=True
        )
        tags.of(_sg).add("Name", sg_name)
        # Returns a single Security group
        return _sg

    def create_elb(self, vpc, securitygroup, asg, elb_name):
        """
        This function defines an internet facing Application load balancer. 
        The function requiere a VPC, a security group and a elb name (all String Parameters). 
        The ALB is attached to a VPC and linked to a provided Security group.
        The ALB DNS generated name is stored in a parameter store for future reference. 
        The health checks for the web app are configure to the path /gapwalk-application/ through port 8080.
        The targets for the ALB are defined as the EC2 instances of the ASG.
        """
        _elb_dns = ""

        _elb = elbv2.ApplicationLoadBalancer(
            self, elb_name,
            vpc = vpc,
            security_group = securitygroup,
            internet_facing = True
        )
        # call the dns name propertie of the elb
        _elb_dns = _elb.load_balancer_dns_name

        ssm.StringParameter(self, 'parameterdns',
            parameter_name= "/BluAge/APP_DNS",
            description='DNS for app',
            string_value = _elb_dns
        )

        _health_check = elbv2.HealthCheck(path= "/gapwalk-application/", port = "8080", healthy_http_codes = "200")
        _listener = _elb.add_listener("listener8080", port = 8080, open = True)
        _listener.add_targets("target_group_8080", port = 8080, targets = [asg], health_check=_health_check, stickiness_cookie_duration = Duration.hours(1))

        tags.of(_elb).add("Name", elb_name)

        # Returns the Aplication load balancer
        return _elb

    def create_asg(self, vpc, asg_sg, asg_name):
        """
        This function defines the autoscaling group of EC2 instances.
        The function requiere a VPC, a security group and a Autoscaling group name (all String Parameters). 
        The role for each instances is defined as an IAM role with managed policies to provide access to the following AWS services:
            - S3 read access
            - Secret manager read/write access
            - System manager for instance remote access
        """

        _role = iam.Role(
            self, "asgRole",
            assumed_by = iam.ServicePrincipal("ec2.amazonaws.com"),
            description = ""
            )
        _role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3ReadOnlyAccess"))
        _role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("SecretsManagerReadWrite"))
        _role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore"))
        _role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess"))

        _asg = asg.AutoScalingGroup(
            self, asg_name,
            role = _role,
            vpc = vpc,
            security_group = asg_sg,
            vpc_subnets = ec2.SubnetSelection(subnet_group_name = SUBNET_APP_GROUP),
            instance_type = ec2.InstanceType(instance_type_identifier = EC2_TYPE),
            machine_image = ec2.MachineImage.generic_linux({'us-east-1': "ami-00c39f71452c08778",}),
            user_data = ec2.UserData.custom(user_data),
            #desired_capacity = 2,
            min_capacity = 2,
            max_capacity = 2
        )
        tags.of(_asg).add("Name", asg_name)
        # Returns the AutoScalingGroup
        return _asg

    def create_aurora_from_snapshot(self, vpc, aurora_sg, snapshot, aurora_name):
        """
        This function defines the aurora database base on an existend snapshot.
        The function requiere a VPC, a security group, an snapshot and a db name (all String Parameters). 
        To connect to the DB the function generates a aurora_secret, this secret is store in secret manager
        and it is referenced from parameter store. 

        """
        _aurora_secret_arn = None
        _aurora = rds.DatabaseClusterFromSnapshot(self, aurora_name,
            snapshot_identifier = snapshot,
            engine=rds.DatabaseClusterEngine.aurora_postgres(version=rds.AuroraPostgresEngineVersion.VER_14_6),
            snapshot_credentials= rds.SnapshotCredentials.from_generated_secret("postgres"),
            instances = 1,
            instance_props = rds.InstanceProps(
                instance_type = ec2.InstanceType(instance_type_identifier=DB_TYPE),
                vpc_subnets = ec2.SubnetSelection(subnet_group_name=SUBNET_DATABASES_GROUP),
                vpc = vpc,
                security_groups=[aurora_sg],
            )
        )
        #reference the aruora db secret arn
        _aurora_secret_arn = _aurora.secret.secret_arn
        #store the secret arn in parameter store 
        ssm.StringParameter(self, 'parametersecret',
            parameter_name= "/BluAge/DB_SECRET_ARN",
            description='The Secret ARN for aurora',
            string_value = _aurora_secret_arn
        )

        ssm.StringParameter(self, 'parameterdatabase',
            parameter_name= "/BluAge/DB_NAME",
            description='The name of the database',
            string_value = "murach"
        )
        return _aurora


    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc, environment:str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create bucket and related parameters
        self.create_s3("bluage-testing-sme-2023-" + environment)

        # Security group for application load balancer, it opens 8080 port to 0.0.0.0/0
        sg_elb = self.create_sg(vpc, "elb-sg")
        sg_elb.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(8080), 'http from anywhere')

        # Security group for autoscaling group
        sg_asg = self.create_sg(vpc, "asg-sg")
        sg_asg.add_ingress_rule(ec2.Peer.security_group_id(sg_elb.security_group_id), ec2.Port.tcp(8080), 'http from the elb security group')
        sg_asg.add_ingress_rule(ec2.Peer.ipv4("18.206.107.24/29"), ec2.Port.tcp(22), 'ssh access ssm')

        # Security group for aurora
        sg_aurora = self.create_sg(vpc, "aurora-sg")
        sg_aurora.add_ingress_rule(ec2.Peer.security_group_id(sg_asg.security_group_id), ec2.Port.tcp(5432), 'access from asg')

        # Create autoscaling group
        asg = self.create_asg(vpc, sg_asg, "myasg")

        # Create Load balancer
        self.create_elb(vpc, sg_elb, asg, "myelb")

        # Create Aurora Database
        self.create_aurora_from_snapshot(vpc, sg_aurora, "sme-project-db-snapshot2", "myaurora")

# https://apg-library.amazonaws.com/content/84f3b20a-6520-4ded-8c0b-eadbb4cc5020