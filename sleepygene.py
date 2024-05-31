#X-Ray role update

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AWSXrayFullAccess",
            "Effect": "Allow",
            "Action": [
                "xray:*"
            ],
            "Resource": [
                "*"
            ]
        }
    ]
}

{
    "family": "web",
    "taskRoleArn": "arn:aws:iam::433427046236:role/studypalapplication-iam-1DRSDMMAOOF1-webEcsTaskRole-gJMgLZaHYAQK",
    "executionRoleArn": "arn:aws:iam::433427046236:role/studypalapplication-iam-1DRSDMM-webEcsExecutionRole-np0PYeclQvZF",
    "networkMode": "awsvpc",
    "containerDefinitions": [
        {
            "name": "web",
            "image": "tonnykioko/studypal:latest",
            "cpu": 128,
            "memory": 256,
            "essential": true,
            "portMappings": [
                {
                    "containerPort": 8000,
                    "protocol": "tcp"
                }
            ],
            "environment": [
                {
                    "name": "DATABASE_URL",
                    "value": "postgres://postgres:c3po@db:5432/studypal"
                },
                {
                    "name": "AWS_XRAY_DAEMON_ADDRESS",
                    "value": "127.0.0.1:2000"
                }
            ],
            "command": [
                "bash",
                "-c",
                "python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"
            ],
            "logConfiguration": {
                "logDriver": "awslogs",
                "options": {
                    "awslogs-group": "studypalapplication/svc/ecs/studypalapplication/web",
                    "awslogs-region": "us-east-1",
                    "awslogs-stream-prefix": "web"
                }
            }
        },
        {
            "name": "xray-daemon",
            "image": "amazon/aws-xray-daemon",
            "cpu": 128,
            "memory": 256,
            "essential": true,
            "portMappings": [
                {
                    "containerPort": 2000,
                    "protocol": "udp"
                }
            ],
            "logConfiguration": {
                "logDriver": "awslogs",
                "options": {
                    "awslogs-group": "studypalapplication/svc/ecs/studypalapplication/xray",
                    "awslogs-region": "us-east-1",
                    "awslogs-stream-prefix": "xray"
                }
            }
        }
    ],
    "requiresCompatibilities": [
        "FARGATE"
    ],
    "cpu": "256",
    "memory": "512",
    "runtimePlatform": {
        "cpuArchitecture": "X86_64",
        "operatingSystemFamily": "LINUX"
    },
    "tags": [
        {
            "key": "compose-x::logical_name",
            "value": "web"
        },
        {
            "key": "Environment",
            "value": "studypalapplication-web-16H68UFJS6D6G"
        },
        {
            "key": "compose-x:version",
            "value": "1.1.2"
        },
        {
            "key": "CreatedByComposeX",
            "value": "true"
        },
        {
            "key": "compose-x::family",
            "value": "web"
        },
        {
            "key": "Name",
            "value": "web"
        }
    ]
}

##AmazonECSTaskExecutionRolePolicy
##AWSXRayDaemonWriteAccess
##CloudWatchLogsFullAccess