# Create the Docker

sudo docker build --build_arg config_path="<path_to_config>" -t "twitter_bot" .
sudo docker run --name=<name> -d -v <path_to_data>:<path_to_config> twitter_bot
