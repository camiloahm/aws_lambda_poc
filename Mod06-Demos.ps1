# ----------------------
# Pre-Signed URL from PowerShell
# ----------------------
Get-S3PreSignedURL -Bucket markbucket20211027 `
                   -Key SysopsDemos.zip `
                   -Expires 2018-07-13
