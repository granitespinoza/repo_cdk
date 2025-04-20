import aws_cdk as cdk
import pytest
from aws2.aws2_stack import Aws2Stack

def test_synth_snapshot(snapshot):
    app = cdk.App()
    stack = Aws2Stack(app, "TestStack",
                      env=cdk.Environment(account="123", region="us-east-1"))
    template = app.synth().get_stack_by_name("TestStack").template
    snapshot.assert_match(template, "stack.template.json")
