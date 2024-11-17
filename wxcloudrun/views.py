from datetime import datetime
from flask import render_template, request, jsonify
from run import app
from wxcloudrun.dao import delete_counterbyid, query_counterbyid, insert_counter, update_counterbyid
from wxcloudrun.model import Counters
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response
import os,requests
from wxcloudrun import coze

# 从环境变量中获取微信小程序的 AppID 和 AppSecret
APPID = os.getenv('WECHAT_APPID')
APPSECRET = os.getenv('WECHAT_APPSECRET')

@app.route('/')
def index():
    """
    :return: 返回index页面
    """
    return render_template('index.html')

# 微信小程序登录的路由
@app.route('/wechat/login', methods=['POST'])
def wechat_login():
    # 从请求中获取 code
    data = request.json
    code = data.get('code')
    
    if not code:
        return jsonify({'error': 'missing code'}), 400

    # 向微信服务器请求 session_key 和 openid
    url = f'https://api.weixin.qq.com/sns/jscode2session?appid={APPID}&secret={APPSECRET}&js_code={code}&grant_type=authorization_code'
    response = requests.get(url)
    
    if response.status_code != 200:
        return jsonify({'error': 'failed to get session'}), 500
    
    # 解析响应数据
    result = response.json()
    openid = result.get('openid')
    session_key = result.get('session_key')
    
    if not openid:
        return jsonify({'error': 'failed to get openid'}), 500
    
    # TODO: 将 openid 和 session_key 保存到数据库，并创建会话或令牌
    # 例如，你可以创建一个 JWT 令牌或使用其他会话管理机制
    
    # 返回成功响应，实际应用中可能需要返回一个令牌
    return jsonify({'message': 'login successful', 'openid': openid})

# 健康检查路由
@app.route('/healthz')
def health_check():
    return 'OK'

@app.route('/api/count', methods=['POST'])
def count():
    """
    :return:计数结果/清除结果
    """

    # 获取请求体参数
    params = request.get_json()

    # 检查action参数
    if 'action' not in params:
        return make_err_response('缺少action参数')

    # 按照不同的action的值，进行不同的操作
    action = params['action']

    # 执行自增操作
    if action == 'inc':
        counter = query_counterbyid(1)
        if counter is None:
            counter = Counters()
            counter.id = 1
            counter.count = 1
            counter.created_at = datetime.now()
            counter.updated_at = datetime.now()
            insert_counter(counter)
        else:
            counter.id = 1
            counter.count += 10
            counter.updated_at = datetime.now()
            update_counterbyid(counter)
        return make_succ_response(counter.count)

    # 执行清0操作
    elif action == 'clear':
        delete_counterbyid(1)
        return make_succ_empty_response()

    # action参数错误
    else:
        return make_err_response('action参数错误')


@app.route('/api/count', methods=['GET'])
def get_count():
    """
    :return: 计数的值
    """
    counter = Counters.query.filter(Counters.id == 1).first()
    return make_succ_response(0) if counter is None else make_succ_response(counter.count)

@app.route('/api/greetings', methods=['GET'])
def get_greetings():

     return coze.say_hi() 