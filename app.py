from flask import Flask,jsonify
import requests 
from requests_html import HTML 
import datetime

def getlst(url,day):
    resp = fetch(url)  #to fetch the website 
    return print_stockinfo(int(day),resp.text) #return a list got from function print_stockinfo

def fetch(url): #to fetch the website
    response = requests.get(url)
    return response

def parse_article_meta(entry): #to catalog the data from the wedsite
    return {
    	'stocknum': entry.find('table tr > th'), #find the stock number and name
        'datatype': entry.find('table thead tr td'), #find the datatype in the table
        'data': entry.find('table tbody tr td'), #find the data in the table
    }

def calculate_num_day_in_month(entries):
    html = HTML(html=entries)
    meta = parse_article_meta(html)
    return len(meta['data'])/9  #there are 9 data in a each row on the table, so the number of the day in current month can be gotten by dividing by 9 

#arrange the stock data in the ideal order and store them in a list
def print_stockinfo(day,entries):
    html = HTML(html=entries)
    meta = parse_article_meta(html)
    lst=[]
    if len(meta['stocknum'])==0: #if the stock symbol is incorrect
        return lst
    lst.append(meta['stocknum'][0].text[8:12]) #put the stock symbol in the list
    print(meta['stocknum'][0].text[8:16]) #print STOCK NO. and name on the terminal
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
        tmp=['Date : '+datalist[i][0],'Total Volume : '+datalist[i][1],'Open price : '+datalist[i][3],'High price : '+datalist[i][4],'Low price : '+datalist[i][5],'Close price : '+datalist[i][6]] 
        lst.append(tmp)         
        i=i+1
    return lst

#web api :set up flask
app=Flask(__name__)

#web api : set the input path and type
@app.route('/stock/id=<string:stocknum>&day=<string:inputday>',methods=['GET'])
def get_tasks(stocknum,inputday):
    #check if input data is correct 
    if len(stocknum)!=4 or stocknum.isdigit() == False: 
        stock=[{'Error' : 'please input the correct type of stock symbol (e.g. id=2330)'}]
        return jsonify(stock)
    if inputday.isdigit() == False:
        stock=[{'Error' : 'please input the type of Integer (e.g. day=5)'}]
        return jsonify(stock)
    #check if the stock symbol is existing 
    url = 'http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=html&date=20180806&stockNo='+stocknum
    lst=getlst(url,1)
    #if the stock symbol isn't existing
    if len(lst)==0: #if the stock symbol is incorrect
        stock=[{'Error' : 'There isn\'t existing this stock symbol'}]
        return jsonify(stock)
    
    #put stock symbol into the list of stock
    stock=[
		{
			'Stock Symbol':lst[0]
		},
	]

    now = datetime.datetime.now() #get the current time information
    day=int(inputday)
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
            lst=getlst(url,day_month)
            day=day-day_month
            if month==1: #if it is nessesary to cross a years, then change the value of year
                month=12
                year=year-1
            else:
                month=month-1
        else: 
            lst=getlst(url,day)
            day=0 #end the while loop

        i=1		
        while i<len(lst):           
            stock.append(lst[i])
            i=i+1
    return jsonify(stock)

if __name__=='__main__':
	app.run(debug=True)


