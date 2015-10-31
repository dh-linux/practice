#!/usr/bin/env python
# -*- coding:utf-8 -*- 
'''
1.获取天气信息
2.发送短信
3.api eg: http://www.weather.com.cn/adat/cityinfo/101010100.html
'''

import json
import urllib2
import subprocess
import datetime

Api='http://www.weather.com.cn/adat/cityinfo/'
bjCode='101010100.html'
weatherApi=Api+bjCode
'''
#urllib2方式获取结果不稳定
header={'Accept': 'text/html;q=0.9,*/*;q=0.8',
 'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
 'Accept-Encoding': 'gzip',
 'Connection': 'close',
 'Referer': 'http://www.weather.com.cn',
 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}

req=urllib2.Request(weatherApi,None,header)
weatherHTML=urllib2.urlopen(req).read()
a=json.dumps(weatherHTML,ensure_ascii = False)

curl -X POST \
  -H "X-Bmob-Application-Id: 2e8bab0e2d2e7440f786a05d471f6e89"          \
  -H "X-Bmob-REST-API-Key: 12153d11fc8f25e0d10197e82591977b"        \
  -H "Content-Type: application/json" \
  -d '{"mobilePhoneNumber": "18508425114", "content":" it is just a test sms... "}' \
  https://api.bmob.cn/1/requestSms
'''

cmdApi="curl "+weatherApi
resultApi=subprocess.Popen(cmdApi,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
data=resultApi.communicate()[0]
weatherData=json.loads(data)

#json.loads()输出为unicode
city=weatherData['weatherinfo']['city'].encode('utf-8')
maxTemp=weatherData['weatherinfo']['temp1'].encode('utf-8')
minTemp=weatherData['weatherinfo']['temp2'].encode('utf-8')
weather=weatherData['weatherinfo']['weather'].encode('utf-8')

sms="  今天" + city + weather + "\\n最高温度: " + maxTemp + "\\n最低温度: " + minTemp + "\\n又是新的一天棒棒哒 ^_^ \\n"
cmdSendSms='curl -X POST -H "X-Bmob-Application-Id:2e8bab0e2d2e7440f786a05d471f6e89" -H "X-Bmob-REST-API-Key:12153d11fc8f25e0d10197e82591977b" -H "Content-Type: application/json" -d \'{"mobilePhoneNumber": "18508425114", "content": " ' + sms + ' " }\' https://api.bmob.cn/1/requestSms'

resultSms=subprocess.Popen(cmdSendSms,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
resultSend=resultSms.communicate()[0]
time=str(datetime.datetime.now())
log=time + "  result: " + resultSend + "\n"

with open("/tmp/weatherSmsSendResult.txt","a+") as f:
    f.write(log)

