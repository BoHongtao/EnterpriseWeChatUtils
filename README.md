# EnterpriseWeChatUtils
企业微信小助手，工作日发送消息给员工,配合crontab可实现定时推送消息
# Note
1. 必须创建新的企业微信小程序
2. 获取小程序的CORPSECRET，CORPID和AGENTID，通过TOUSER可指定消息接受者
3. 消息推送默认只有工作日推送，及周一至周五，可配置除去法定节假日，可在data/下配置每年的法定节假日
