import requests #step1
from requests_html import HTML #step2
import datetime

now = datetime.datetime.now() #get the current time information

def fetch(url): #to fetch the website 
    response = requests.get(url)
    return response

def parse_article_meta(entry): #to catalog the data from the wedsite
    return {
    	'stocknum': entry.find('table tr > th'), #find the stock number and name
        'datatype': entry.find('table thead tr td'), #find the datatype in the table
        'data': entry.find('tbody tr td'), #find the data in the table
    }

def calculate_num_day_in_month(entries):
    html = HTML(html=entries)
    meta = parse_article_meta(html)
    return len(meta['data'])/9  #there are 9 data in a each row on the table, so the number of the day in current month can be gotten by dividing by 9 

def print_stockinfo(day,entries):
    html = HTML(html=entries)
    meta = parse_article_meta(html)
    if len(meta['stocknum'])==0:
        print('There isn\'t existing this stock symbol')
        return
    print(meta['stocknum'][0].text[8:16]) #print STOCK NO. and name 
    datatype=(meta['datatype'][0].text,meta['datatype'][3].text,meta['datatype'][4].text,meta['datatype'][5].text,meta['datatype'][6].text)
    datalist=[]
    i=0
    while i<len(meta['data']):  #make data be a list cataloged by date, and store in datalist
        tmplist=[]
        tmplist.append(meta['data'][i].text)
        j=1            
        while j<9:
            tmplist.append(meta['data'][i+j].text)                
            j=j+1        
        datalist.append(tmplist)
        i=i+j               
    datalist.reverse()  #make the latest data in the beginning of the datalist
    i=0
    while i<day:  #make the two row's data combine
        print(meta['datatype'][0].text+' : '+datalist[i][0])
        print(meta['datatype'][1].text+' : '+datalist[i][1])
        print(meta['datatype'][3].text+' : '+datalist[i][3])
        print(meta['datatype'][4].text+' : '+datalist[i][4])
        print(meta['datatype'][5].text+' : '+datalist[i][5])
        print(meta['datatype'][6].text+' : '+datalist[i][6]+'\n')
        i=i+1

while 1:
    stocknum=input('please input the stock symbol (e.g. 2330) :')
    while stocknum.isdigit() == False or len(stocknum)!=4:
        stocknum=input('Sorry, please input the correct type of stock symbol (e.g. 2330) :')
    day_str=input('please input the number of output days (e.g. 5) :')
    while day_str.isdigit() == False:
        day_str=input('Sorry, please input the type of Integer (e.g. 5) :')
    day=int(day_str)
    month=now.month
    year=now.year
    while day!=0: #output the data
        if month<=10:
            url = 'http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=html&date='+str(year)+'0'+str(month)+'01&stockNo='+stocknum
        else:
            url = 'http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=html&date='+str(year)+str(month)+'01&stockNo='+stocknum
        resp = fetch(url)  #to fetch the website
        day_month=calculate_num_day_in_month(resp.text)  
        if day>day_month: #check if the current month is enough for desired day 
            print_stockinfo(day_month,resp.text)
            day=day-day_month
            if month==1: #if it is nessesary to cross a years, then change the value of year
                month=12
                year=year-1
            else:
                month=month-1
        else: 
            print_stockinfo(day,resp.text)
            day=0 #end the while loop

    check=input('Do you want to get the information of another stock? Y/n: ')
    if(check!='Y' and check!='y'):
        break



    
