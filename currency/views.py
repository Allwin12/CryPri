from django.shortcuts import HttpResponse,render
from .models import Table,Price, Marketdata, converter, MainTable
import requests
import json
# Create your views here.
def maintable(request):
    num=1
    for i in range (1,5):
        url='https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&order=market_cap_rank_asc&per_page=250&page='+str(i)+'&sparkline=false&price_change_percentage=1h%2C24h%2C7d'
        response = requests.get(url)
        todos = json.loads(response.text)
        for i in todos:
            try:
                name = i.get('name')
                rank = i.get('market_cap_rank')
                symbol = i.get('symbol')
                id = i.get('id')
                image = i.get('image')
                market_cap = i.get('market_cap')
                toal_volume = i.get('total_supply')
                price_change = i.get('price_change_24h')
                price_change_percentage_24h=i.get('price_change_percentage_24h')
                if (type(price_change_percentage_24h) == float):
                    price_change_percentage_24h=round(price_change_percentage_24h,1)
                price_change_percentage_1h=i.get('price_change_percentage_1h_in_currency')
                if (type(price_change_percentage_1h) == float):
                    price_change_percentage_1h=round(price_change_percentage_1h,1)
                price_change_percentage_7d = i.get('price_change_percentage_7d_in_currency')
                if (type(price_change_percentage_7d) == float):
                    price_change_percentage_7d=round(price_change_percentage_7d,1)
                circulating=i.get('circulating_supply')
                circulating=round(circulating,1)
                ob = MainTable(coinid=id,rank=rank,symbol=symbol,name=name,thumbimg=image,marketcap=market_cap,totalvolume=toal_volume,price_change=price_change,pricechangepercentage=price_change_percentage_24h,circulating_supply=circulating,onehourchange=price_change_percentage_1h,sevendaychange=price_change_percentage_7d)
                ob.save()
                print(num)
                num = num+1
            except Exception as e:
                print(e)

def conv(request):
    ip = request.GET['ip']
    ip1 = request.GET['ip2']
    coins = request.GET['coins']
    target = request.GET['target']
    url = 'https://api.coingecko.com/api/v3/simple/price?ids=' + coins + '&vs_currencies=' + target
    response = requests.get(url)
    todos = json.loads(response.text)
    result = float(todos.get(coins).get(target))
    if(ip=='') and (ip1==''):
        return HttpResponse("both empty")
    elif(ip==''):
        ip1 = float(ip1)
        result = float(todos.get(coins).get(target))
        result = ip1 / result
        return HttpResponse(result)

    elif(ip1==''):
        ip = float(ip)
        result = float(todos.get(coins).get(target))
        result = result * ip
        return HttpResponse(result)


def details(request,name):
    url = 'https://api.coingecko.com/api/v3/coins/' + name
    print(url)
    response = requests.get(url)
    todos = json.loads(response.text)
    desc = todos.get('description')
    en = desc.get('en')
    desc = en.split('\r')[0]
    md = todos.get('market_data')
    h24 = md.get('price_change_24h')
    h24perc = md.get('price_change_24h')
    pcp7d = md.get('price_change_percentage_7d')
    pcp14d = md.get('price_change_percentage_14d')
    pcp30d = md.get('price_change_percentage_30d')
    pcp60d = md.get('price_change_percentage_60d')
    pcp200d = md.get('price_change_percentage_200d')
    pcp1year = md.get('price_change_percentage_1y')
    url = todos.get('links')
    homepage = url.get('homepage')[0]
    desc = todos.get('description')
    english = desc.get('en')
    homepage_url = url.get('homepage')[0]
    repos_url=url.get('repos_url')
    repos_url=repos_url.get('github')[0]
    redditurl = url.get('subreddit_url')
    print(redditurl)
    twitter_screen_name = url.get('twitter_screen_name')
    facebook_username = url.get('facebook_username')
    id = todos.get('id')
    symbol = todos.get('symbol')
    name = todos.get('name')
    img = todos.get('image')
    img_src = img.get('large')
    coingecko_rank = todos.get('coingecko_rank')
    market_data = todos.get('market_data')
    curprice = market_data.get('current_price')
    price = curprice.get('inr')  # can be input from the user
    currency_list = []
    coins_list=[]
    coin_list = Table.objects.all()
    for i in coin_list:
        coins_list.append(i.coinid)
    curr_list = converter.objects.all()
    for i in curr_list:
        name = i.name
        currency_list.append(name)
    url='https://newsapi.org/v2/everything?q='+name+'&apiKey=a01a07bc9ade4fb6a9caa52431f5641f'
    response = requests.get(url)
    todos = json.loads(response.text)
    articles = todos.get('articles')
    news = articles[0].get('content')
    news_image_url = articles[0].get('urlToImage')

    context = {'id': id,
               'news':news,
               'newsimage':news_image_url,
               'homepage':homepage_url,
               'repos':repos_url,
               'reddit':redditurl,
               'name': name,
               'symbol': symbol,
               'img_src': img_src,
               'coingecko_rank': coingecko_rank,
               'price': price,
               'urls': [facebook_username, twitter_screen_name, homepage_url],
               'description':desc,
               'h24':h24,
               'h24p':h24perc,
               'pcp7d':pcp7d,
                'pcp14d':pcp14d,
                'pcp30d':pcp30d,
                'pcp60d': pcp60d,
                'pcp200d':pcp200d,
             'pcp1year':pcp1year,
               'desc':english,
               'list':currency_list,
               'coinslist':coins_list,

    }
    return render(request, 'hello.html', context)

def homepage(request):
    li = []
    data = MainTable.objects.all()
    for i in data:
        pcp1h = i.onehourchange
        pcp7d = i.sevendaychange
        pcp = i.pricechangepercentage
        if (type(pcp) == float):
            if pcp < 0:
                pcpercent = {"red24": pcp, "downward24": '↓'}
            elif pcp > 0:
                pcpercent = {"green24": pcp, "upward24": '↑'}
        else:
            pcpercent = {"None24": 'None24'}

        if (type(pcp1h) == float):
            if pcp1h < 0:
                pcpercent1 = {"red1": pcp1h, "downward1": '↓'}
            elif pcp1h > 0:
                pcpercent1 = {"green1": pcp1h, "upward1": '↑'}
        else:
            pcpercent1 = {"None1": 'None1'}

        if (type(pcp7d) == float):
            if pcp7d < 0:
                pcpercent7 = {"red7": pcp7d, "downward7": '↓'}
            elif pcp7d > 0:
                pcpercent7 = {"green7": pcp7d, "upward7": '↑'}
        else:
            pcpercent7 = {"None7": 'None7'}
        info={
            'id':i.coinid,
            'rank':i.rank,
            'symbol':i.symbol,
            'name':i.name,
            'image':i.thumbimg,
            'marketcap':i.marketcap,
            'totalvolume':i.totalvolume,
            'pricechange':i.price_change,
            'csupply':i.circulating_supply,
        }
        info.update(pcpercent)
        info.update(pcpercent1)
        info.update(pcpercent7)
        print(info)
        li.append(info)
    return render(request,'homepage.html',{'links': li})

def home(request):
    li = []
    id = 1
    li1=[]
    list3=[]
    marketdata = Marketdata.objects.all()
    for i in marketdata:
        info={
            "pricechange":i.price_change_24h,
            "pricechangepercentage":i.price_change_percentage_24h,
        }
        list3.append(info)
    price = Price.objects.all()
    for i in price:
        pri = i.price
        li1.append(pri)
    for i in Table.objects.all():
        info = {
            "serialno":i.id,
            "name": i.name,
            "id": i.coinid,
            "img": i.img,
            "symbol": i.symbol,
            "image":i.image,
        }
        li.append(info)
    li.append(li1)
    for i in range(0,500):
        nk = {"price":li1[i]}
        pc = {"pricechange":list3[i].get('pricechange')}
        pcpercentage=list3[i].get('pricechangepercentage')
        if(type(pcpercentage)==float):
            if pcpercentage < 0:
                pcp = {"red": pcpercentage , "downward":'↓'}
            elif pcpercentage > 0:
                pcp = {"green": pcpercentage,"upward":'↑' }
        else:
            pcp={"None":'None'}
        li[i].update(nk)
        li[i].update(pc)
        li[i].update(pcp)
        '''li[i].update(pcp)'''
    return render(request,'homepage.html',{'links': li})

def add(request):
    url = 'https://api.coingecko.com/api/v3/coins/list'
    cryptos = json.loads(response.text)
    num=1
    for i in range(2500,2600):
        data = cryptos[i]
        name = data.get('name')
        coin_id =data.get('id')
        symbol = data.get('symbol')
        url = 'https://api.coingecko.com/api/v3/coins/' + coin_id
        response = requests.get(url)
        todos = json.loads(response.text)
        img = todos.get('image')
        img_src = img.get('thumb')
        img = img_src
        print(num)
        ob = Table(name=name,coinid=coin_id,symbol=symbol,img=img)
        ob.save()
        num=num+1
    return HttpResponse(cryptos)

'''def imageadd(request):
    url = 'https://api.coingecko.com/api/v3/coins/list'
    response = requests.get(url)
    cryptos = json.loads(response.text)
    num = 1
    for i in range(10,20):
        data = cryptos[i]
        coin_id = data.get('id')
        des = data.get('description')
        print(des)
        url = 'https://api.coingecko.com/api/v3/coins/' + coin_id
        response = requests.get(url)
        todos = json.loads(response.text)
        for i in todos:
            print(type(i))
        img = todos.get('image')
        img_src = img.get('large')
        print(num)
        num=num+1
        ob = Additional(image_source = img_src)
        ob.save()'''

def imageadd(request):

    for i in Table.objects.all():
        url = 'https://api.coingecko.com/api/v3/coins/' +i.coinid
        response = requests.get(url)
        todos = json.loads(response.text)
        img = todos.get('image')
        img_src = img.get('large')
        img = img_src
        i.image = img
        i.save()
    return HttpResponse("done")

def addprice(request):
    url = 'https://api.coingecko.com/api/v3/coins/list'
    response = requests.get(url)
    cryptos = json.loads(response.text)
    num = 1
    itr = 1328
    for i in cryptos:
        id = i.get('id')
        url='https://api.coingecko.com/api/v3/simple/price?ids='+id+'&vs_currencies=inr'
        try:
            response = requests.get(url)
            todos = json.loads(response.text)
            print(todos)
            price = todos.get(id)
            price = price.get('inr')
            num=num+1
            ob = Price.objects.get(pk=itr)
            ob.price = price
            ob.save()
            print('saved')
            itr=itr+1
        except Exception as e:
            print(e)

def addmarketdata(request):
    url = 'https://api.coingecko.com/api/v3/coins/list'
    response = requests.get(url)
    cryptos = json.loads(response.text)
    for i in cryptos:
        id = i.get('id')
        url = 'https://api.coingecko.com/api/v3/coins/'+id
        try:
            response = requests.get(url)
            todos = json.loads(response.text)
            md = todos.get('market_data')
            price_change_24h = md.get('price_change_24h')
            price_change_percentage_24h = md.get('price_change_percentage_24h')
            ob = Marketdata(price_change_24h=price_change_24h,price_change_percentage_24h=price_change_percentage_24h)
            ob.save()
        except Exception as e:
            print(e)
