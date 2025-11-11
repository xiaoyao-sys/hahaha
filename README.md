# 系统

这是一个

## 功能特点


## 配置说明

在 `config.ini` 文件中配置以下参数：

```ini
[WeChat]
webhook_url = https://qyapi.weixin.qq.com/cgi-bin/webhook/send
webhook_key = your_webhook_key

[FundAlert]
# 溢价率阈值，超过此值的基金会触发企业微信通知
premium_threshold = 5.0
```

## 定时执行


系统通过GitHub Actions每天自动执行，无需人工干预。
