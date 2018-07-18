from flask import Flask,jsonify
import requests 
from requests_html import HTML 

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

#arrange the stock data in the ideal order and store them in a list
def print_stockinfo(day,pentries):
    html = HTML(html=pentries)
    meta = parse_article_meta(html)
    lst=[]
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
        if i==10:
            print('The system is just storing the information of the stock in 10 days,\nso it\'s just shown the information in 10 days')
            break
        tmp=['Date : '+datalist[i][0],'Total Volume : '+datalist[i][1],'Open price : '+datalist[i][3],'High price : '+datalist[i][4],'Low price : '+datalist[i][5],'Close price : '+datalist[i][6]] 
        lst.append(tmp)         
        i=i+1
    return lst

#web api :set up flask
app=Flask(__name__)

#web api : set the input path and type
@app.route('/stock/id=<string:stocknum>&day=<string:day>',methods=['GET'])
def get_tasks(stocknum,day):
    #check if input data is correct 
    if len(stocknum)!=4 or stocknum.isdigit() == False: 
        stock=[{'Error' : 'please input the correct type of stock symbol (e.g. id=2330)'}]
        return jsonify(stock)
    if day.isdigit() == False:
        stock=[{'Error' : 'please input the type of Integer (e.g. day=5)'}]
        return jsonify(stock)
    url = 'http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=html&date=20180715&stockNo='+stocknum
    lst=getlst(url,day)
    #if the stock symbol isn't existing
    if lst==None:
        stock=[{'Error' : 'There isn\'t existing this stock symbol'}]
        return jsonify(stock)
    stock=[
		{
			'Stock Symbol':lst[0]
		},
	]
    i=1		
    while i<len(lst):			
        stock.append(lst[i])
        i=i+1
    #if requested to output over 10 days, then output the reason that we can just output 10 days 
    if int(day)>10:
        stock.append('Notice:')
        stock.append('There are just shown the information in 10 days')
        stock.append('Becauese the system just store the stock information in the past 10 days')
    return jsonify(stock)

if __name__=='__main__':
	app.run(debug=True)


