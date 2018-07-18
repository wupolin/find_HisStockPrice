from flask import Flask,jsonify
import requests #step1
from requests_html import HTML #step2


def fetch(url): #step1 : to fetch the website
    response = requests.get(url)
    return response

def parse_article_entries(doc): #step2 : to find the entries we want in the website  
    html = HTML(html=doc)
    post_entries = html.find('table')
    return post_entries


def parse_article_meta(entry): #step3 : to catalog the data in the wedsite
    return {
    	'stocknum': entry.find('tr > th'), #find the stock number and name
        'datatype': entry.find('thead tr td'), #find the datatype in the table
        'data': entry.find('tbody tr td'), #find the data in the table
    }

def print_stockinfo(day,post_entries):
    if len(post_entries)==0:
        print('There isn\'t existing this stock symbol')
    for entry in post_entries: 
        meta = parse_article_meta(entry)
        lst=[]
        lst.append(meta['stocknum'][0].text[8:16])
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
                print('The system is just storing the information of the stock in 10 days,\nso it\'s just shown the information in 10 days')
                break
            tmp=['Date : '+datalist[i][0],'Total Volume : '+datalist[i][1],'Open price : '+datalist[i][3],'High price : '+datalist[i][4],'Low price : '+datalist[i][5],'Close price : '+datalist[i][6]] 
            lst.append(tmp)         
            i=i+1
        return lst
def mainfunc(url,day):
    resp = fetch(url)  # step-1
    post_entries = parse_article_entries(resp.text)  # step-2
    return print_stockinfo(int(day),post_entries)

app=Flask(__name__)


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
    lst=mainfunc(url,day)
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
    if int(day)>10:
        stock.append('Notice:')
        stock.append('There are just shown the information in 10 days')
        stock.append('Becauese the system just store the stock information in the past 10 days')
    return jsonify(stock)

if __name__=='__main__':
	app.run(debug=True)


