# encoding: utf-8
# @author: John
# @contact: BoHongtao@yeah.net
# @software: PyCharm
# @time: 2019/9/14 23:43
import time
class Holiday:
    def __init__(self):
        self.pingnian_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        self.runnian_month = [0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        self.cur_month = int(time.strftime("%m", time.localtime()))
        self.cur_day = int(time.strftime("%d", time.localtime()))
        self.year = int(time.strftime("%Y", time.localtime()))
        self.weekday = int(time.strftime("%w", time.localtime()))
        self.holiday_arr = []
        self.add_arr = []
        self.__genHoliday(self.year)

    def __readHoliday(self, year):
        # 读取卡片列表
        day_arr = []
        with open("./data/"+"{}.txt".format(year), "r",encoding='utf-8') as file:
            while 1:
                line = file.readline().strip()
                if not line:
                    break
                if line[0] == '#':  # 过滤注释掉的卡号
                    continue
                if line[:3] == 'add':  # 补假
                    self.add_arr += (line[4:].split(','))
                else:
                    day_arr.append(line.split('#')[0].strip())  # 过滤注释
            return day_arr

    def __dayBetween(self, day, year):
        # 对期间日期进行解析
        days = day.split('-')
        if len(days) == 1:
            return days
        begin = int(days[0].split('.')[1])  # 开始时间
        end = int(days[1].split('.')[1])  # 结束时间
        mon = int(days[0].split('.')[0])
        if begin < end:
            # 添加系列
            while (begin < end - 1):
                begin = begin + 1
                days.append('{}.{}'.format(mon, begin))
        elif begin > end:
            isRunNian = False
            # 判断是否是闰年
            if year % 4 == 0 and year % 100 != 0 and year % 400 == 0:
                isRunNian = True
            max_day = self.pingnian_month[mon]
            if mon == 2:
                if isRunNian:
                    max_day = self.runnian_month[mon]
                else:
                    max_day = self.pingnian_month[mon]
            while (begin < max_day):
                begin = begin + 1
                days.append('{}.{}'.format(mon, begin))
            begin = 1
            while (begin < end):
                days.append('{}.{}'.format(mon + 1, begin))
                begin = begin + 1
        return sorted(days)

    def __genHoliday(self, year):
        day_arr = self.__readHoliday(year)
        for day in day_arr:
            days = self.__dayBetween(day, year)
            self.holiday_arr += days

    def isHoliday(self):
        cur_month_day = '{}.{}'.format(self.cur_month, self.cur_day)
        if cur_month_day in self.holiday_arr:
            return True
        else:
            if cur_month_day not in self.add_arr and (self.weekday == 0 or self.weekday == 6):
                return True
        return False
