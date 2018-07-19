import requests #step1
from requests_html import HTML #step2


def fetch(url): #to fetch the website 
    response = requests.get(url)
    return response

def parse_article_meta(entry): #to catalog the data from the wedsite
    return {
    	'stocknum': entry.find('table tr > th'), #find the stock number and name
        'datatype': entry.find('table thead tr td'), #find the datatype in the table
        'data': entry.find('tbody tr td'), #find the data in the table
    }

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
        if i==10:
            print('There are just shown the information in 10 days')
            print('Becauese the system just store the stock information in the past 10 days')
            break
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
    url = 'http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=html&date=20180715&stockNo='+stocknum
    day=input('please input the number of output days (e.g. 5) :')
    while day.isdigit() == False:
        day=input('Sorry, please input the type of Integer (e.g. 5) :')
    resp = fetch(url)  #to fetch the website
    print_stockinfo(int(day),resp.text)
    check=input('Do you want to get the information of another stock? Y/n: ')
    if(check!='Y' and check!='y'):
        break



    
