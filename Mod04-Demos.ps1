##############################################################################
# Configure default security settings:

# PowerShell
# (Provide the AccessKey and SecretKey in quotes.)
Initialize-AWSDefaultConfiguration -AccessKey "" -SecretKey "" -Region us-east-1
Initialize-AWSDefaultConfiguration -ProfileName jane -AccessKey "" -SecretKey "" -Region us-east-1

Get-S3Bucket -ProfileName labdemo2

# AWSCli
aws configure
aws configure --profile jane

aws s3 ls
aws s3 ls --profile jane

# Profile location

# Windows
dir $env:USERPROFILE\.aws

# Linux / Windows
ls ~/.aws