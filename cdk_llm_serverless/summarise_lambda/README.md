# Architecture

![Architecture](./serverless_audio_summarisation.png "Architecture")

# Prerequisites:

- AWS CLI, install
- AWS CDK, install
- Python 3.11 or later
- Node.js LTS, install
- Docker, install
- Access to model `amazon.titan-text-express-v1`. Before [use request access](  
https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html#add-model-access).


# Deployment

1. clone the repository
2. cd into root directory
3. create ptyhon virtual environment
4. activate virtual environment
5. install dependencies, `pip install -r requirements.txt`
6. cdk deploy