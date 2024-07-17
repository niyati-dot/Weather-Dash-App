# weather-app
This is the repo of the Weather app 

# Project structure
In this project I build a end-to-end pipeline from requesting weather data from an API to visualizing the results on a Dashboard.
As tools I use the weather API, Docker, AWS Elastic container registry, AWS Lambda, AWS EventBridge and Grafana as the dashboard solution.

# What to do in the right order
- Created account on [weatherapi.com](https://www.weatherapi.com) and generate a token
- Setup the TDengine cloud database on [tdengine.com](https://cloud.tdengine.com/login)
- Create the weather database, stable and tables berlin and sanfrancisco
- Install TDengine connector for python with `pip install taospy`
- Build the docker container using `docker build -f dockerfile-user -t weather-data .`
- installed the AWS cli
- Created a development user and role in IAM with full rights to ecr, create keys for that user
- `aws configure` and enter key and secret key
- Created ECR, tag the image and push the image up to ECR 
- Created Lambda that uses the image
- Created EventBridge schedule that triggers the Lambda function
- Pull the [Grafana image](https://hub.docker.com/r/grafana/grafana) from docker hub `docker pull grafana/grafana`
- Start grafana with `docker run --name=grafana -p 3000:3000 grafana/grafana`
- Go to localhost:3000 to access Grafana, connect the TDengine datasource and create yourself a Dashboard

