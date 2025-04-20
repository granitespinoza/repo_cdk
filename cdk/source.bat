@echo off
REM Activar entorno y desplegar en Windows CMD
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
set AWS_EC2_METADATA_DISABLED=true
set AWS_PROFILE=default
for /f "usebackq tokens=*" %%a in (`aws sts get-caller-identity --query Account --output text`) do set CDK_DEFAULT_ACCOUNT=%%a
set CDK_DEFAULT_REGION=us-east-1
cdk synth
cdk deploy --require-approval never --role-arn arn:aws:iam::%CDK_DEFAULT_ACCOUNT%:role/LabRole

