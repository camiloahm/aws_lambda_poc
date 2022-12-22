# Invoke the Lambda function from PowerShell
# Copy and paste this into a PS prompt

$InputData = @'
{
    "queryStringParameters": {
      "name": "Mark Morgan - From PowerShell"
    }
  }
'@

Invoke-LMFunction -FunctionName HelloWorld -Payload $InputData
