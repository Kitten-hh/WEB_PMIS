import poplib
import email
from email.parser import Parser
from datetime import datetime, timedelta
import chardet

# POP3 服务器信息
username = 'hb@artemishome.com'
password = 'shingwaihb11'

# 连接到 POP3 服务器
mail = poplib.POP3("192.168.0.65", 110)
mail.user(username)
mail.pass_(password)

# 获取邮件统计信息
num_messages = len(mail.list()[1])

# 定义 7 天前的日期
seven_days_ago = datetime.now() - timedelta(days=7)

def custom_decode_header(encoded_str):
    decoded_header = email.header.decode_header(encoded_str)[0]

    # 检查解码后的内容类型，并适当地处理
    if isinstance(decoded_header[0], bytes):
        # 如果是字节串，根据其字符集解码成字符串
        encoding = decoded_header[1] if decoded_header[1] else 'utf-8'
        # 替换gb2312为更广泛的gb18030
        if encoding.lower() == 'gb2312':
            encoding = 'gb18030'
        try:
            decoded_str = decoded_header[0].decode(encoding)
        except UnicodeDecodeError:
            decoded_str = decoded_header[0].decode('utf-8', errors='replace')
    else:
        decoded_str = decoded_header[0]

    return decoded_str

# 读取邮件
for i in range(max(1, num_messages - 100), num_messages + 1):  # 示例仅检查最新的100封邮件
    resp, lines, octets = mail.retr(i)
    msg_content = b'\r\n'.join(lines)

    # 使用 chardet 检测编码
    detected = chardet.detect(msg_content)
    encoding = detected['encoding'] if detected['encoding'] else 'utf-8'

    try:
        msg_content = msg_content.decode(encoding)
    except UnicodeDecodeError:
        msg_content = msg_content.decode('utf-8', errors='replace')

    message = Parser().parsestr(msg_content)

    # 解析邮件日期
    date = message.get('Date')
    mail_date = email.utils.parsedate_to_datetime(date)
    mail_date = mail_date.replace(tzinfo=None)

    if mail_date > seven_days_ago:
        subject = message.get('Subject')
        subject = custom_decode_header(subject) if subject else ""
        print(f"Date: {mail_date}")
        print(f"Subject: {subject}")

        # 获取并解码发件人和收件人信息
        print("From:", custom_decode_header(message.get('From')))

        # 遍历邮件各部分提取附件名
        for part in message.walk():
            if part.get_content_maintype() == 'multipart' or part.get('Content-Disposition') is None:
                continue
            
            filename = part.get_filename()
            if filename:
                filename = custom_decode_header(filename)
                print("Found attachment:", filename)

        print("---\n")

# 断开连接
mail.quit()
