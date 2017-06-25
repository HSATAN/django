from email.mime.text import MIMEText
import smtplib

def sendemail(data):
    try:
        msg = MIMEText(data, _subtype='html', _charset='utf-8')
        # msg = MIMEMultipart('alternative')
        msg['Subject'] = u'爬虫价格异常报警'
        msg['From'] = 'mfashion <buddy@mfashion.com.cn>'
        msg['To'] = 'kaijie.huang@mfashion.com.cn'

        server = smtplib.SMTP_SSL('smtp.exmail.qq.com', 465)
        server.login('buddy@mfashion.com.cn', 'rose123')
        server.sendmail('buddy@mfashion.com.cn',['2499090390@qq.com'], msg.as_string())
        server.quit()
    except Exception as e:print(e)