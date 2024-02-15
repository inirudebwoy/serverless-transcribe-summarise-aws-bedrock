import aws_cdk as core
import aws_cdk.assertions as assertions

from cdk_llm_serverless.cdk_llm_serverless_stack import CdkLlmServerlessStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cdk_llm_serverless/cdk_llm_serverless_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CdkLlmServerlessStack(app, "cdk-llm-serverless")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
