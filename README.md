# Twitter Bot
Just an attempt to win things on Twitter...  


### Setup
Alter the [settings.py](https://github.com/tranaj2/TwitterBot/blob/master/contest_bot/settings.py) file to add your API Credentials and to customize the app more.


### Running the Docker Container
```
sudo docker build --build_arg config_path="<path_to_config>" -t "twitter_bot" .  
sudo docker run --name=<name> -d -v <path_to_data>:<path_to_config> twitter_bot
```
