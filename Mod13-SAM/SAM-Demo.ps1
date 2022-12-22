# Copy files to the D:\Training folder
md D:\Training\SAM
copy 'W:\My Documents\aws\demos\DevOnAWS\SAM\*.*' D:\Training\SAM
cd D:\Training\SAM

# Run the sam deploy command
sam deploy --guided