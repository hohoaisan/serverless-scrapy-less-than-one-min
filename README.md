# Serverless Scrapy Project Less Than 1 Minute

Sample scrapy project intergrate with AWS Step Function to trigger all lambdas all at once, then save results to AWS S3 Bucket.

References:
- [Another Way to Trigger a Lambda Function Every 5–10 Seconds](https://zaccharles.medium.com/another-way-to-trigger-a-lambda-function-every-5-10-seconds-41cb5bc3fa80)
- [Serverless Scraping with Scrapy, AWS Lambda and Fargate – a guide](https://blog.vikfand.com/posts/scrapy-fargate-sls-guide/)

With a couple of modifications for scrapy working with AWS Lambda

## Prerequisites

- Docker (Non-linux evironment, for building compatible python package for AWS Lambda environment)
- Python 3.9 
- Pipenv
- NodeJs 16
- AWS cli + AWS profile
- Serverless CLI 3.22

## Local development & testing

### Packages
Python packages is managed by Pipenv. Use Pipenv's `pipenv install` to install required packages and `pipenv shell` to start python development environment with those installed packages.

### Scrapy
This repository is already a scrapy project. Any scrapy command can be used. For example scrape a spider that is already defined:
```
scrapy crawl quotes -o test.json
```

### Lambda Functions
We can test the lambda function by invoke it locally:
```
serverless invoke local -f scrape_quotes
```
## Deploy to AWS

Change the `stage` of the deployment in the `serverless.yml` file.

### Deploy
With configued AWS CLI Profile, serverless deployment can be done by using
```
serverless deploy
```

### Destroy

Defined serverless deployment can be remove by using
```
serverless remove
```
Or Delete corresponding stack on CloudFormation

All of buckets created needs to be empty before removing resources, we can remove again if there's errors

