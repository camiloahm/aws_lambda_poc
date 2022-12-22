# AWS CLI
aws help

# Install AWS Tools for PowerShell
Find-Module AWS.Tools.*

# This is just an example. Add as many of the tools as you think you may need S3, EC2 and Common are just a few
# Use the Find-Module command to determine which you want
Install-Module AWS.Tools.S3,AWS.Tools.EC2,AWS.Tools.Common

Get-Module AWS.Tools* -ListAvailable

# Most modules auto-load by default when you call a command from the module
# Rarely, you may need to pre-load a module for data types to be available
# Try this command
New-Object Amazon.EC2.Model.TagSpecification
# If it doesn't work, you need to import the EC2 module, or run at least one command
# from the EC2 module to force it to auto-load.
Import-Module AWS.Tools.EC2
New-Object Amazon.EC2.Model.TagSpecification

#############
# EC2
############

# PowerShell
Get-EC2Instance | Select-Object -ExpandProperty Instances

(Get-EC2Instance).Instances

(Get-EC2Instance).Instances | Format-List

(Get-EC2Instance).Instances | Select-Object InstanceID, Architecture, VPCID

(Get-EC2Instance).Instances | Select-Object -ExpandProperty InstanceID

(Get-EC2Instance).Instances | Where-Object {$_.Tags.Value -Like "Demo*"}

(Get-EC2Instance).Instances | Where-Object {$_.Tags.Value -eq "Demo Server 2019"}

$InstanceID = ((Get-EC2Instance).Instances | Where-Object {$_.Tags.Value -eq "Demo Server 2019"}).InstanceID

$InstanceID

(Get-EC2Instance).Instances[0].InstanceID

$InstanceID = (Get-EC2Instance).Instances[0].InstanceID

$InstanceID

(Get-EC2Instance).Instances | Where-Object {$_.State.Name -eq "running"}

(Get-EC2Instance).Instances | Where-Object {$_.State.Name -eq "running"} | Select-Object -ExpandProperty InstanceId

# AWS Cli from bash or PowerShell
aws ec2 describe-instances

aws ec2 describe-instances --filter "Name=instance-type,Values=t2.micro"

aws ec2 describe-instances --filter "Name=instance-type,Values=t2.micro" --query "Reservations[*].Instances[*].InstanceId"

aws ec2 describe-instances --filter "Name=tag:Name,Values=Demo Server 2019" --query "Reservations[*].Instances[*].InstanceId" --output text

$instanceid = aws ec2 describe-instances --filter "Name=tag:Name,Values=Demo Server 2019" --query "Reservations[*].Instances[*].InstanceId" --output text

# Bash Only
instanceid=$(aws ec2 describe-instances --filter "Name=tag:Name,Values=Demo Server 2019" --query "Reservations[*].Instances[*].InstanceId" --output text)

echo $instanceid