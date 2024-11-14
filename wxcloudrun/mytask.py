from apscheduler.schedulers.background import BackgroundScheduler
import datetime
import holidays
from lunarcalendar import Lunar
import sxtwl
from cozepy import JWTOAuthApp, Coze, TokenAuth, Message, ChatStatus
import config
from cozepy.config import COZE_CN_BASE_URL

# 定义调度器配置

class TaskScheduler:
    def __init__(self, app):
        self.SCHEDULER_API_ENABLED = True
        self.scheduler = BackgroundScheduler()

    def call_holiday_api(self):
        try:
            holiday = HolidaySet()
            response = holiday.holiday()
            print(f"API Response: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Error occurred: {e}")

    def start_scheduler(self):
        self.scheduler.add_job(self.call_holiday_api,
                               'cron', hour=0, minute=30)
        self.scheduler.add_job(self.call_holiday_api, 'interval', seconds=5)
        self.scheduler.start()

    def shutdown_scheduler(self):
        self.scheduler.shutdown()


class HolidaySet:

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


    def get_solar_terms(self, solar_date):
        """
        根据日期返回对应的节气
        """
        day = sxtwl.fromSolar(solar_date.year, solar_date.month, solar_date.day) 

        if day.hasJieQi():
            return day.getJieQi()  # 返回节气名称

        return None


    def get_lunar_words(self, year, month, day):
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


    def get_season(self, month, day):
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


    def holiday(self):

        # 获取今天的日期
        today = datetime.date.today()

        # 判断国家法定节假日（以中国为例）
        cn_holidays = holidays.China()
        holiday_name = cn_holidays.get(today)

        # 判断农历节气和假日
        lunar_date = Lunar(today.year, today.month, today.day)

        # 确定当前农历节气
        term_name = self.get_solar_terms(today)
        # 农历日期
        lunarwords = self.get_lunar_words(today.year, lunar_date.month, lunar_date.day)
        # 季节
        season = self.get_season(lunar_date.month, lunar_date.day)

        holiday_text = ''
        if holiday_name:
            holiday_text = f"{today} {holiday_name}"
        elif term_name:
            holiday_text = f"{lunarwords} {term_name}"
        else:
            holiday_text = f"{lunarwords} {season}"

        return holiday_text


class CozeWithOAuthJWT:
    def __init__(self, client_id, private_key, public_key_id):
        self.client_id = client_id
        self.private_key = private_key
        self.public_key_id = public_key_id
        self.oauth_app = self._create_jwt_oauth_app()
        self.access_token = None
        self.coze_client = self._create_coze_client()
        
    def _create_jwt_oauth_app(self):
        """创建并返回一个JWT OAuth App实例"""
        return JWTOAuthApp(
            client_id=self.client_id,
            private_key=self.private_key,
            public_key_id=self.public_key_id,
            base_url=COZE_CN_BASE_URL
        )

    def _get_access_token(self, ttl=3600):
        """使用JWT OAuth App获取access token"""
        return self.oauth_app.get_access_token(ttl)

    def _create_coze_client(self, ttl=3600):
        self.access_token = self._get_access_token(ttl)
        self.coze_client = Coze(auth=TokenAuth(self.access_token.access_token), base_url=COZE_CN_BASE_URL)
        return self.coze_client
 
    def set_app_context(self):
        """设置应用程序上下文，以确保Coze客户端正确运行"""
        # 这里假设您有一个Flask应用程序实例名为app
        # 请根据您的应用程序框架进行相应的上下文设置
        # 例如，在Flask中，您可能会这样做：
        # with self.app.app_context():
        #     # 在这里执行需要应用程序上下文的操作
        #     pass
        pass

    def _ensure_coze_client_not_expired(self):
        if not self.coze_client :
            self.coze_client = self._create_coze_client()
        elif self.access_token.expires_in < datetime.datetime.now().timestamp() :
            self.coze_client = self._create_coze_client()

    def say_hi(self) :
        self._ensure_coze_client_not_expired()

        holiday_text = '早安祝福图'
        
        holiday_text = HolidaySet().holiday()
        holiday_question = holiday_text + '的祝福图'

        chat_poll = self.coze_client.chat.create_and_poll(
            bot_id = config.coze_bot_id,
            user_id = config.coze_user_id,
            additional_messages=[
                Message.build_user_question_text(holiday_question),
            ],
        )

        for message in chat_poll.messages:
            print(message.content, end="", flush=True)
            #print(message.content.tojson().output.result[0].imageUrl)


        if chat_poll.chat.status == ChatStatus.COMPLETED:
            print()
            print("token usage:", chat_poll.chat.usage.token_count)


