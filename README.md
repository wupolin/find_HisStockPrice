# find_HisStockPrice

find_HisStockPrice is a tool to help people search and realize the history of stock price. 

## Installation

### Requirements
* Linux
* Python 3.6
* Requests
* Requests_html
* Flask
* Git


## Usage

There are two Python scripts in the repository and three methods to implement the purpose of searching the history of stock price.

### 1. Use the AWS server 

>#### Download the permission keypair from Github

```
$git clone 'https://Github.com/wupolin/wupolin_keypair.pem'
```

>#### Connect to the server built on the AWS

```
$cd ~/wupolin_keypair
$chmod 400 wupolin_keypair.pem
$ssh -i wupolin_keypair.pem ubuntu@18.236.161.160
```

>#### Use web API to query the stock information

```
$curl 'http://127.0.0.1:5000/stock/id=2330&day=2'
[
 {
   "Stock Symbol": "2330"
 },
 [
   "Date : 107/07/18",
   "Total Volume: 45,802,658",
   "Open price : 223.00",
   "High price : 224.00",
   "Low price : 222.00",
   "Close price : 223.00",
 ],
 [
   "Date : 107/07/17",
   "Total Volume: 22,554,436",
   "Open price : 222.50",
   "High price : 223.50",
   "Low price : 221.00",
   "Close price : 221.50",
 ]
```
### 2. Use the private server

>#### Download the python script from Github

```
$git clone 'https://Github.com/wupolin/find_HisStockPrice.git'
```

>#### Keep the web server running on backend
##### (In the case that there is just one terminal in the server ) 

```
$nohup python3.6 ~/find_HisStockPrice/app.py &
```
#####      Now, please restart the terminal.


>#### Use web API to query the stock information

```
$curl 'http://127.0.0.1:5000/stock/id=2330&day=2'
[
 {
   "Stock Symbol": "2330"
 },
 [
   "Date : 107/07/18",
   "Total Volume: 45,802,658",
   "Open price : 223.00",
   "High price : 224.00",
   "Low price : 222.00",
   "Close price : 223.00",
 ],
 [
   "Date : 107/07/17",
   "Total Volume: 22,554,436",
   "Open price : 222.50",
   "High price : 223.50",
   "Low price : 221.00",
   "Close price : 221.50",
 ]
```

### 3. Serverless method

>#### Download the python script from Github

```
$git clone 'https://Github.com/wupolin/find_HisStockPrice.git'
```

>#### Use python3\.6 to run stock.py

```
$python3.6 ~/find_HisStockPrice/stock.py
```
>#### Input the stock symbol and number of days 

```
please input the stock symbol (e.g. 2330) :2330
please input the number of output days (e.g. 5) :2
2330 台積電
日期 : 107/07/18
成交股數 : 45,802,658
開盤價 : 223.00
最高價 : 224.00
最低價 : 222.00
收盤價 : 223.00

日期 : 107/07/17
成交股數 : 22,554,436
開盤價 : 222.50
最高價 : 223.50
最低價 : 221.00
收盤價 : 221.50

Do you want to get the information of another stock? Y/n:
```
