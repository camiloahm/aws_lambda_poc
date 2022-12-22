# PowerShell
Get-S3Bucket

New-S3Bucket -BucketName demo-bucket-123454321

Write-S3Object -Folder D:\Training\dogs -BucketName demo-bucket-123454321 -KeyPrefix /

Get-S3Object -BucketName demo-bucket-123454321 | Format-Table LastModified,Key,Size

Remove-S3Bucket -BucketName demo-bucket-123454321 -DeleteBucketContent -Force

# AWS Cli from bash or PowerShell (not WSL)
aws s3 ls

aws s3 mb s3://demo-bucket-123454321 --region us-east-1

aws s3 cp d:/training/dogs s3://demo-bucket-123454321/ --recursive

aws s3 ls demo-bucket-123454321

aws s3 rb s3://demo-bucket-123454321 --force 