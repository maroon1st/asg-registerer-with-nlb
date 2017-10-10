asg-registerer-with-nlb
====

asg-registerer-with-nlbはAuto Scaling GroupをIPアドレスでNetwork Load Balancerに自動で登録するツールです。

## Description

本ツールの詳細は、以下のブログに記載しています。

https://dev.classmethod.jp/cloud/aws/register-private-auto-scaling-group-with-nlb

## Requirements

- [Serverless Framework](https://github.com/serverless/serverless)

## Install

/conf/environment.yml に設定情報を入力します。

```markdown:/conf/environment.yml
STAGE: dev
AWS_REGION: ap-northeast-1
ASG_NAME: ASG-NAME
TARGET_GROUP: arn:aws:elasticloadbalancing:ap-northeast-1:123456789012:targetgroup/nlb-target/a1b2c3d4e5f6g7h8
```

- STAGE : Serverless FrameworkのStageです。`dev`や`prd`など。
- AWS_REGION : デプロイするAWSのリージョンです。
- ASG_NAME : NLBに登録するAuto Scaling Groupです。
- TARGET_GROUP : 登録するNLBのターゲットグループのARNです。

Serverless FrameworkでDeployします。

```
$ sls deploy
```

