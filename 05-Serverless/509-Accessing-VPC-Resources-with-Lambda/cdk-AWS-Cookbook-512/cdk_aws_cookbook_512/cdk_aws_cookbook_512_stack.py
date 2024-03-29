from aws_cdk import (
    aws_ec2 as ec2,
    aws_s3 as s3,
    aws_s3_deployment,
    aws_iam as iam,
    aws_rds as rds,
    aws_logs as logs,
    aws_lambda,
    custom_resources,
    core,
)


class CdkAwsCookbook512Stack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        isolated_subnets = ec2.SubnetConfiguration(
            name="ISOLATED",
            subnet_type=ec2.SubnetType.ISOLATED,
            cidr_mask=24
        )

        # create VPC
        vpc = ec2.Vpc(
            self,
            'AWS-Cookbook-VPC',
            cidr='10.10.0.0/23',
            subnet_configuration=[isolated_subnets]
        )

        cache_security_group = ec2.SecurityGroup(
            self,
            'cache_security_group',
            description='Security Group for the ElastiCache cluster',
            allow_all_outbound=True,
            vpc=vpc
        )

        # outputs

        core.CfnOutput(
            self,
            'VPCId',
            value=vpc.vpc_id
        )

        core.CfnOutput(
            self,
            'CacheSecurityGroup',
            value=cache_security_group.security_group_id
        )

        isolated_subnets = vpc.select_subnets(subnet_type=ec2.SubnetType.ISOLATED)

        core.CfnOutput(
            self,
            'IsolatedSubnets',
            value=', '.join(map(str, isolated_subnets.subnet_ids))
        )
