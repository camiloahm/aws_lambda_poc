# Invoke the Lambda function from PowerShell
# Copy and paste this into a PS prompt

$InputData = '{"message_body": "Lambda Function triggered from PowerShell"}'

Invoke-LMFunction -FunctionName testsns -Payload $InputData

# Or, run this from bash or WSL
aws lambda invoke \
    --function-name testsns \
    --payload '{"message_body": "Lambda Function triggered from CLI"}' \
    response.json