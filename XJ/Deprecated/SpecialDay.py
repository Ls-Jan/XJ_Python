

'''
	不过是娱乐性质的代码。
    
    获取指定年份下的“特别日”，
    所谓“特别日”指的是“日”的个位数与“星期数”恰好一致的日期
	例如：2022年8月4号-星期四、2022年7月15日-星期五
'''

def IsLeapYear(year):#判断闰年
    if(year%400==0):
        return True
    elif(year%4==0 and year%100!=0):
        return True
    else:
        return False

def GetSpecialDay_Month(days,weekNum):#传入月的天数，以及月的第一天对应的星期数。返回列表[day,day,...]
    if(weekNum==1):
        return list(range(1,8))
    elif(weekNum==5):
        return list(range(11,18))
    elif(weekNum==2):
        return list(range(21,28))
    elif(weekNum==6 and days>30):
        return [31]
    else:
        return []

def GetSpecialDay_Year(year,weekNum):#传入年号，以及元旦(1月1日)对应的星期数。返回字典{month:[day,day,...],...}
    monthDays=[31,28,31,30,31,30,31,31,30,31,30,31]
    monthDays[1]=29 if IsLeapYear(year) else 28
    rst=dict()
    for month in range(12):
        days=monthDays[month]
        lst=GetSpecialDay_Month(days,weekNum)
        if(len(lst)):
            rst[month+1]=lst
        weekNum+=days-28
        if(weekNum>7):
            weekNum-=7
    return rst
    
def GetSpecialDay(year):#传入年号。返回字典{month:[day,day,...],...}
    from datetime import date
    weekNum=date(year,1,1).weekday()+1
    return GetSpecialDay_Year(year,weekNum)




year=2021
rst=GetSpecialDay(year)
print(f'【{year}】\n')
for i in rst:
    print(f'{i:2}  {rst[i]}')

print("\n\n")








