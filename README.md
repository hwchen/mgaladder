# MGA ladder software

## setup for dynamoDB

```
    pip install pynamodb
    pip install flask
```

Also, boto is installed as a dependency of pynamodb.

for now, for local development:
Create ~/.boto
Add these lines:

```
    [Credentials]
    aws_access_key_id = foo
    aws_secret_access_key = bar
    dynamo_enable_local = true
    dynamo_local_host = localhost
    dynamo_local_port = 8000
```
