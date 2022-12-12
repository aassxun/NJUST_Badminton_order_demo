import requests
import pandas as pd
import os
import json
import datetime
import time
os.environ['NO_PROXY'] = 'stackoverflow.com'


def getHTMLText(url, cookies, siteID):
    try:
        headers = {
            'Host': 'wechat.njust.edu.cn',
            'Content-Length': '69',
            'Accept': 'application/json, text/plain, */*',
            'Origin': 'http://wechat.njust.edu.cn',
            'User-Agent': 'MicroMessenger/6.8.0',#最好自己改改
            'Content-Type': 'application/json',
            'cookie': 'JSESSIONID=' + cookies['JSESSIONID'] + ';lxwxuserid=' + cookies['lxwxuserid'],
            'Referer': 'http://wechat.njust.edu.cn/gymBooking/venueBooking.html',
            'Accept-Encoding': 'gzip,deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        }
        
        bookDate = str(datetime.date.today()+datetime.timedelta(days=1))
        data = {
            'siteId': siteID, 
            'bookDate': bookDate, 
        }
        
        r = requests.post(url, headers=headers, data=json.dumps(data), timeout=30)
        return r
    except:
        return ""

def get_Area_List(data):
    Area_List = []
    for i in range(len(data)):
        _id = data[i]['id']
        timeTemplateID = data[i]['timeTemplateId']
        startTime = data[i]['startTime']
        endTime = data[i]['endTime']
        AreaPrice = data[i]['listAreaPrice']
        totalCount = data[i]['totalCount']
        for j in range(17):
            Area_List.append(AreaPrice[j])
    return Area_List

def get_order_list(Area_List):
    max_order = 1
    flag = 0
    need_order_list = []

    for i in range(len(Area_List)):
        if Area_List[i]['use'] == None and Area_List[i]['price'] != -1:
            need_order_list.append(Area_List[i])
            flag += 1
        if flag == max_order:
            break
    return need_order_list


def sku_order_submet(need_order, cookies, siteID, bookingDate):

    url = 'http://wechat.njust.edu.cn/api/v2/appGym/submitAreaOrder'

    areaId = need_order['areaId']
    areaName = need_order['areaName']
    timeId = need_order['timeId']
    price = need_order['price']
    areaPriceId = need_order['areaPriceId']

    headers = {
        'Host': 'wechat.njust.edu.cn',
        'Content-Length': '398',
        'Accept': 'application/json, text/plain, */*',
        'Origin': 'http://wechat.njust.edu.cn',
        'User-Agent': 'MicroMessenger/6.8.0',#最好自己改改
        'Content-Type': 'application/json',
        'cookie': 'JSESSIONID=' + cookies['JSESSIONID'] + ';lxwxuserid=' + cookies['lxwxuserid'],
        'Referer': 'http://wechat.njust.edu.cn/gymBooking/venueBooking.html',
        'Accept-Encoding': 'gzip,deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    data = {
        'siteId': siteID,
        'gymId': '790c8055a06311e8a69022faa7560813',
        'payAmount': price,
        'payDuration': '60',
        'areaRecordList':[{
            'areaId': areaId,
            'areaName': areaName,
            'bookingType': 'null',
            'bookingDate': bookingDate,
            'timeId': timeId,
            #'time': '14:00~15:00',
            'userType': '1',
            'price': price,
            'areaPriceId': areaPriceId,
        }],
        'bookTimes': '1'
    }
    
    order_req = requests.post(url, headers=headers, data=json.dumps(data), timeout=30)
    return order_req


def main():
    url = 'http://wechat.njust.edu.cn/api/v2/appGym/listAreaPriceBySiteIdAndTime'
    
    #请设置为自己的cookie
    cookies = {
        'JSESSIONID': '',
        'lxwxuserid': ''
    }
    siteID = 'e1f5c85e86c34c46a2d0935452094b77'  #不知道以后会不会变

    html = getHTMLText(url, cookies, siteID)
    df = html.json()
    data = df['data']

    Area_List = get_Area_List(data=data)
    need_order_list = get_order_list(Area_List)
    
    bookingDate = str(datetime.date.today()+datetime.timedelta(days=1))
    order_req = sku_order_submet(need_order=need_order_list[0], cookies=cookies, siteID=siteID, bookingDate=bookingDate)
    ood = order_req.json()
    print(ood['message'])
    
main()