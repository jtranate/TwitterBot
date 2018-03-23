# Create the Docker

sudo docker build -t "twitter_bot" .
sudo docker run --name=<name> -d -v <path_to_data>:/config twitter_bot
