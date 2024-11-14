from apscheduler.schedulers.background import BackgroundScheduler
import datetime
import holidays
from lunarcalendar import Lunar
from flask import render_template, request, jsonify

# 定义调度器配置

class TaskScheduler:
    def __init__(self):
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


    def get_solar_terms(self, month, day):
        """
        根据农历日期返回对应的节气
        """
        # 遍历节气字典，寻找符合的节气
        for term, (m, d) in self.SOLAR_TERMS.items():
            if (month == m and day >= d) or (month > m):
                return term
        return None  # 如果没有找到对应节气


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
        term_name = self.get_solar_terms(lunar_date.month, lunar_date.day)

        # 汇总节日信息
        result = {
            "date": str(today),
            "holiday": holiday_name if holiday_name else "",
            "solarterm": term_name if term_name else "",
            "lunarwords": self.get_lunar_words(today.year, lunar_date.month, lunar_date.day),
            "season": self.get_season(lunar_date.month, lunar_date.day)
        }

        return jsonify(result)
