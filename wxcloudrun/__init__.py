from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from wxcloudrun.mytask import CozeWithOAuthJWT
import pymysql
import config

# 因MySQLDB不支持Python3，使用pymysql扩展库代替MySQLDB库
pymysql.install_as_MySQLdb()

# 初始化web应用
app = Flask(__name__, instance_relative_config=True)
app.config['DEBUG'] = config.DEBUG

# 设定数据库链接
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{}:{}@{}/flask_demo'.format(config.username, config.password,
                                                                             config.db_address)
# 初始化DB操作对象
db = SQLAlchemy(app)

# 启动定时任务
#tsk = TaskScheduler(app)
#tsk.start_scheduler()

# CozeWithOAuthJWT
coze = CozeWithOAuthJWT(config.coze_client_id,config.coze_private_key,config.coze_public_key_id)
coze.set_app_context()
#coze.say_hi()

# 加载控制器
from wxcloudrun import views

# 加载配置
app.config.from_object('config')
