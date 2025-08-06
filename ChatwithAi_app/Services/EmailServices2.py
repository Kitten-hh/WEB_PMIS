from msal import ConfidentialClientApplication
import imaplib

# Office 365 应用和用户信息
client_id = '25587ff2-118c-4489-bbef-706a48e649b0'
client_secret = 'Rch8Q~_0r9FDsiZAPE-mnE5T.R6DrBjyBWtMqaAT'
authority = 'https://login.microsoftonline.com/3e2d25d0-8a92-4753-9b9e-7c46f5b604ad'
scope = ['https://graph.microsoft.com/.default']

# 创建 MSAL 应用实例
app = ConfidentialClientApplication(
    client_id,
    authority=authority,
    client_credential=client_secret,
)

# 获取令牌
result = app.acquire_token_for_client(scopes=scope)

if 'access_token' in result:
    imap_host = 'outlook.office365.com'
    print(result['access_token'])
    # 使用获得的令牌通过 IMAP 连接
    username = "singchan@shingwai.com"
    mail = imaplib.IMAP4_SSL(imap_host, 993)
    # 准备 OAuth2 认证字符串
    auth_string = f'user={username}\1auth=Bearer {result["access_token"]}\1\1'.encode()
    print(auth_string)
    mail.authenticate('XOAUTH2', lambda x: auth_string)
    mail.select('inbox')
    print("Login successful")
    # 继续处理邮件
    mail.logout()
else:
    print(f"Error obtaining token: {result.get('error')}, {result.get('error_description')}")
