from datetime import datetime
from flask import render_template, request, jsonify
from run import app
from wxcloudrun.dao import delete_counterbyid, query_counterbyid, insert_counter, update_counterbyid
from wxcloudrun.model import Counters
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response
import os,requests
import datetime
import holidays
from lunarcalendar import Lunar

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

# 定义农历节气
SOLAR_TERMS = {
    "立春": (2, 4),
    "雨水": (2, 19),
    "惊蛰": (3, 5),
    "春分": (3, 20),
    "清明": (4, 4),
    "谷雨": (4, 19),
    "立夏": (5, 5),
    "小满": (5, 21),
    "芒种": (6, 6),
    "夏至": (6, 21),
    "小暑": (7, 7),
    "大暑": (7, 22),
    "立秋": (8, 7),
    "处暑": (8, 23),
    "白露": (9, 8),
    "秋分": (9, 23),
    "寒露": (10, 8),
    "霜降": (10, 23),
    "立冬": (11, 7),
    "小雪": (11, 22),
    "大雪": (12, 7),
    "冬至": (12, 21),
    "小寒": (1, 5),
    "大寒": (1, 20)
}

def get_solar_terms(month, day):
        """
        根据农历日期返回对应的节气
        """
        # 遍历节气字典，寻找符合的节气
        for term, (m, d) in SOLAR_TERMS.items():
            if (month == m and day >= d) or (month > m):
                return term
        return None  # 如果没有找到对应节气

def get_lunar_words(year, month, day):
    """
        返回农历的中文形式，例如“某年 龙 十月初八”
    """
    chinese_months = [
        "正月", "二月", "三月", "四月", "五月", "六月",
        "七月", "八月", "九月", "十月", "冬月", "腊月"
    ]
    
    chinese_days = [
        "初一", "初二", "初三", "初四", "初五",
        "初六", "初七", "初八", "初九", "初十",
        "十一", "十二", "十三", "十四", "十五",
        "十六", "十七", "十八", "十九", "二十",
        "廿一", "廿二", "廿三", "廿四", "廿五",
        "廿六", "廿七", "廿八", "廿九", "三十"
    ]
        
    # 获取对应的月份和日期的中文形式
    month_str = chinese_months[month - 1]
    day_str = chinese_days[day - 1]

    # 定义农历生肖
    ANIMALS = [
        "鼠", "牛", "虎", "兔", "龙", "蛇",
        "马", "羊", "猴", "鸡", "狗", "猪"
    ]
    
    animal_year = ANIMALS[(year - 1900) % 12]
    return f"{year}年 {animal_year} {month_str} {day_str}"

def get_season(month, day):
    """
    根据农历日期返回季节
    """
    if (month == 2 and day >= 4) or (month == 3) or (month == 4 and day < 21):
        return "春季"
    elif (month == 4 and day >= 21) or (month == 5) or (month == 6 and day < 22):
        return "夏季"
    elif (month == 6 and day >= 22) or (month == 7) or (month == 8 and day < 23):
        return "秋季"
    elif (month == 8 and day >= 23) or (month == 9) or (month == 10 and day < 23):
        return "冬季"
    else:
        return "冬季"

@app.route('/api/holiday', methods=['GET'])
def holiday():

    # 获取今天的日期
    today = datetime.date.today()

    # 判断国家法定节假日（以中国为例）
    cn_holidays = holidays.China()
    holiday_name = cn_holidays.get(today)

    # 判断农历节气和假日
    lunar_date = Lunar(today.year, today.month, today.day)
    
    # 确定当前农历节气
    term_name = get_solar_terms(lunar_date.month, lunar_date.day)

    # 汇总节日信息
    result = {
        "date": str(today),
        "holiday": holiday_name if holiday_name else "",
        "solarterm": term_name if term_name else "",
        "lunarwords": get_lunar_words(today.year, lunar_date.month, lunar_date.day),
        "season": get_season(lunar_date.month, lunar_date.day)
    }

    return jsonify(result)