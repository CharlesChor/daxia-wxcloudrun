import os

# 是否开启debug模式
DEBUG = True

# 读取数据库环境变量
username = os.environ.get("MYSQL_USERNAME", 'root')
password = os.environ.get("MYSQL_PASSWORD", 'root')
db_address = os.environ.get("MYSQL_ADDRESS", '127.0.0.1:3306')


COZE_DAXIA_DG_CLIENT_ID = '1152109278574'
COZE_DAXIA_DG_PUBLIC_KEY_ID = 'qIQ90o2IHmaT9FCPZg0QoX5qHuB1Q55sCwFBMyIJu8c'
COZE_DAXIA_DG_PRIVATE_KEY = '''-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCoGRy7zqcxrhYZ
x7NUE2repGKQw+SeaFUTUo83/frklB+QGyVQdWS1/8b8Ms2nvIo58ToFcp52zQ5s
6n7v0JYkbQMmF13c/jJ3K1WwIkE9aL6R3n7/JDdftVuVHQz7Y0SGmVPEVz+fgc8K
5+dC8q7zhUn0HdL34kQiBLj+OeDbYfr8ixCjynb4hNPMX3EKDJ/tiwRvCHuxyZh+
1GGXmSlho302KpFII5XUCvX7Kh4s/86KXVN377MDKR1YUemYUjBc8CigFuERtwkF
wL5wvKysJ33sWPfuOKcw6Fmdp3FJdcf+Eb52CgNCooJKKE/dx+n75gg/RVbLFUER
qwKs2S63AgMBAAECggEADJ7qDd27ptq7tQ7N04Ors/Cip9zVVuFdddhugVUz16KZ
Zg/rsslFmPaNwZSs5SmeNTB72znaVPAbY6kNg8Lk6vI2WM9LUFLThif+RH2l6U7q
c/hBD7Xv5GMw75ahSWSQGgz8AZNNZxPvcBGuRtQCt6zruwTcOJlH5Uf2fbvpun7X
GPP1Z1ar5qi4uIfANhBhni14EkvnQ2Vy96lF7zfNVM/oWTRETFbBJJfDC7vvXEKH
Hot/AaDS+5siFDMblHfKziZFUZXyCt3ZqM8kdVJnv+NW4x9+jWRxqUbCgb0SSkqc
/A5hIHY+huQe+zJD3zp0V6DFTp215rA44KAb3DcEdQKBgQDUl3RshRMjYuoIZV/t
ZQVaV0zQ5FKymlTA8cpc/ITxYPV0+IdzN7aSFD6tsla5RsJsL0YCFQFrrexh5eYK
9SrpcrZoYfXXdwe7PXGttaTuXzXyae/QTjdOdEp3mg6HRF8Y70+X7rjFBxUkenkj
KsHey7wllcMtkQgEfYLjd7Fe6wKBgQDKa+at8As1PD3T/+8CUIgHnpAUSSGOi59G
/M6fubXxXqeSjKJw4tI8DPWVs4IzYqSI04CKUuOiH8Xxxae9DL/VKRIOSn9vK9IB
MKjnCGmNboXBl/tyPOtqE47vsoJBOYLVheG/XekPJBSKMzMWCrLSjV1RVHgRHg38
08loNgU0ZQKBgQCzuMZn56hiRgDr0CfknX6E/UCnaB6xdt8nrkERkzkghoN7u49m
zDbAD/VdCmNehn9ezig1ImTtDz/DE4QCx3jbmmqym/4lhS84D53G6MTh8AO/R+fB
Bh6jaJR7v/WATUDH56g2HU5+4pnxGMjH/iGfpEUO0SkLoIxSn3jDrDB6uQKBgHqG
8e1bng0tV+eZxh1Kjey+yEvfMJbOYS1hHdmFWmKufxSwWCuowMVkustRC4D7Nskz
7VzNa8jZHsKIeE5xBzWKVMmdwqGSjt31jGe8qdfYjNJwot21jnJ5QE5LaZj9rPp+
vfVObSKjHmPBNi0jcLcOpuvyC3OhE6p0sDeKa4AZAoGATCGCbTMeXbkXIJ/LEOv5
YjLbPsNCZ+vsE1YUAxFM7rhzf5zD6+iStJ9/VaK/+QDl7uQwFn5+aXPQoa9O+vBC
Ihk6NUXGdgaGepHgdKedcimeia/upLkqoMKdFY/94st2ZbQjyS8O5o3BZZzFoBZr
gr8XpbGonARaEGZWJoIhnZY=
-----END PRIVATE KEY-----'''
COZE_DAXIA_DG_BOT_ID = '7436768424971681827'
COZE_DAXIA_DG_USER_ID = 'daxia'

# 使用环境变量中的值初始化CozeCaller
coze_client_id = os.getenv("COZE_JWT_OAUTH_CLIENT_ID", COZE_DAXIA_DG_CLIENT_ID)
coze_private_key = os.getenv("COZE_JWT_OAUTH_PRIVATE_KEY", COZE_DAXIA_DG_PRIVATE_KEY)
coze_public_key_id = os.getenv("COZE_JWT_OAUTH_PUBLIC_KEY_ID", COZE_DAXIA_DG_PUBLIC_KEY_ID)
coze_bot_id = os.getenv("COZE_BOT_ID", COZE_DAXIA_DG_BOT_ID)
coze_user_id = os.getenv("COZE_USER_ID", COZE_DAXIA_DG_USER_ID)