import os
from constructs import Construct
import aws_cdk as cdk
from aws_cdk import (
    Stack, CfnParameter, CfnOutput,
    aws_ec2 as ec2,
    aws_iam as iam,
)

class Aws2Stack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # 1) Parámetro AMI
        ami = CfnParameter(
            self, "AMI",
            type="String",
            default="ami-0aa28dab1f2852040",
            description="AMI Cloud9 Ubuntu22"
        )

        # 2) VPC + Security Group
        vpc = ec2.Vpc.from_lookup(self, "VPC", is_default=True)
        sg = ec2.SecurityGroup(
            self, "SG",
            vpc=vpc,
            description="SSH (22) y HTTP (80)",
            allow_all_outbound=True
        )
        sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "SSH")
        sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(80), "HTTP")

        # 3) LabRole dinámico
        acct = os.getenv("CDK_DEFAULT_ACCOUNT")
        role_arn = f"arn:aws:iam::{acct}:role/LabRole"
        lab_role = iam.Role.from_role_arn(self, "LabRole", role_arn)

        # 4) EC2 t2.micro
        inst = ec2.Instance(
            self, "Instance",
            vpc=vpc,
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=ec2.MachineImage.generic_linux(
                { self.region: ami.value_as_string }
            ),
            security_group=sg,
            key_name="vockey",
            role=lab_role,
            block_devices=[ ec2.BlockDevice(
                device_name="/dev/sda1",
                volume=ec2.BlockDeviceVolume.ebs(20)
            ) ]
        )

        # 5) User data (Apache + Git + clones)
        inst.add_user_data(
            "#!/bin/bash",
            "yum update -y",
            "yum install -y git httpd",
            "systemctl enable httpd && systemctl start httpd",
            "cd /var/www/html",
            "git clone https://github.com/granitespinoza/websimple.git",
            "git clone https://github.com/granitespinoza/webplantilla.git",
            "chown -R ec2-user:ec2-user /var/www/html"
        )

        # 6) Outputs
        CfnOutput(self, "PublicIP",
                  description="IP pública",
                  value=inst.instance_public_ip)
        CfnOutput(self, "URLwebsimple",
                  description="URL websimple",
                  value=f"http://{inst.instance_public_ip}/websimple")
        CfnOutput(self, "URLwebplantilla",
                  description="URL webplantilla",
                  value=f"http://{inst.instance_public_ip}/webplantilla")
