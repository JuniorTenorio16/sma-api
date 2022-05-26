# sma-api
Simple Moving Average API

This API returns the simple moving average for intervals of 20, 50, and 200 days, for consecutive dates up to 365 days before the start date.

How to use this API:

1. clone the repository to a local machine 
2. build the image using the docker-compose build command 
3. set up the Docker environment using docker-compose up 
4. access this API using localhost:8000.

The database URL and coin tags must be manually set as environment variables in an .env file, which must be created by the user as an additional security measure.
