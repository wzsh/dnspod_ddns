# Update DDNS record of dnspod （Python 2.x）
As an user of dnspod.com (international), updating sub-domain's ip address is a common operation.

This script can upate ip address of your sub-domain automatically.


## Usage
You need to change the variables as shown on below:


```python
    domain = 'yourdomain.com'
    record = 'your subdomain like (www)'
    email = 'your ddns account'
    password = 'your ddns password'
```
### A cron job example
if you wanna execute this script per hour:

$ crontab -e

1 */1 * * * /usr/bin/python /home/pi/update_ip.py >> /home/pi/update_ip.log


## Notice
如果你使用的是国内版DNSOD, 请尝试BASE_URL替换为国内版api地址(https://dnsapi.cn)
