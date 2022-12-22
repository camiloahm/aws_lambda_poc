# Run these commands in bash or WSL

aws dynamodb list-tables

aws dynamodb create-table --table-name MusicCollection \
                          --attribute-definitions AttributeName=Artist,AttributeType=S AttributeName=SongTitle,AttributeType=S \
                          --key-schema AttributeName=Artist,KeyType=HASH AttributeName=SongTitle,KeyType=RANGE \
                          --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5

aws dynamodb put-item --table-name MusicCollection \
                      --item '{"Artist": {"S":"Pink Floyd"}, "SongTitle": {"S":"Breathe"}, "AlbumTitle": {"S":"The Dark Side of the Moon"}}'

aws dynamodb scan --table-name MusicCollection
                  
aws dynamodb delete-table --table-name MusicCollection


                      