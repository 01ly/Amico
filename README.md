# Amipy
 Python微型异步爬虫框架(A micro  asynchronous Python website crawler framework)

> 基于Python 3.5 + 的异步async-await 框架，搭建一个模块化的微型异步爬虫。可以根据需求控制异步队列的长度和延迟时间等。配置了可以去重的布隆过滤器，网页内容正文过滤等，完全自主配置使用。


## 适用环境
* windows 7 + 
* Python 3.5 +

## 安装
直接使用pip安装即可:
```
pip install amipy
```
## 基础命令
* 1.查看当前路径下的可用命令，在DOS命令行下输入：

```> amipy```

会出现命令帮助界面。

* 2.创建一个新的项目，在DOS命令行下输入：
```
> amipy cproject myproject
```
会在当前路径下创建一个Amipy爬虫项目myproject。如果想要创建在指定目录下，可以加上附加参数,-d,如：
```
> amipy cproject myproject -d  D:\somefolder
```
项目myproject便会在路径**D:\somefolder**下创建。
项目的目录结构应该如下:
```text
--myproject
    |-spiders
    |   |-__init__.py
    |-__init__.py
    |-settings.py
```
其中：
> settings.py 为整个项目的配置文件，可以为整个项目下的爬虫安装共有的中间件，控制整个项目的请求并发数，设置日志级别、文件路径等。
* 3.进入项目路径，创建一个新的爬虫，在DOS命令行下输入:
``` 
> amipy cspider myspider
```
此时在项目myproject目录下的spiders文件夹中会创建一个爬虫目录myspider，此时的项目结构为：
```text
--myproject
    |-spiders
    |   |-__init__.py
    |   |-myspider
    |   |    |-__init__.py
    |   |    |-cookies.info
    |   |    |-item.py
    |   |    |-settings.py
    |   |    |-site_record.info
    |   |    |-spider.py
    |   |    |-url_record.info
    |-__init__.py
    |-settings.py
    |-log.log
```
其中：
> * 位于myspider文件夹下的settings.py为爬虫myspider的配置文件，该配置只对当前爬虫有效。可以对该爬虫的布隆过滤器进行配置，安装中间件等。
> * cookies.info 为爬虫的请求cookie保存文件，该爬虫爬过的所有网站的cookie会保存进该文件。可以通过爬虫配置文件settings.py进行路径加载和保存。
> * site_record.info 为爬虫爬取过的网站内容的布隆过滤器记录文件，方便下次爬取的时候加载，会把爬取过相同内容的网站自动去掉。防止重复爬取正文内容相同的网页。
> * url_record.info 为该爬虫发出的请求url+headers+method+数据的去重后集合，爬虫结束运行时，如果配置保存去重url集合。下次爬取时加载该文件可以自动过滤爬取过的所有url+headers+method+数据。
> * item.py 为ORM的MongoDB数据集合对象，对应的类属性可以映射到数据库集合中的字段，类名为数据表名。
> * spider.py 为当前爬虫的主要文件，自己编写爬取逻辑，提取规则和数据保存脚本等。

* 4.运行项目下的所有爬虫，进入项目路径，在DOS命令行下输入：
```text
> amipy runproject
```
则该项目下的所有爬虫会开始运行，如果不想运行某个爬虫，只需要加上参数 -e，如：
```text
> amipy runproject -e No1spider No2spider
```
则名为“No1spider”、“No2spider”的爬虫均不会运行。
* 5.运行指定的爬虫，进入项目路径，在DOS命令行下输入：
```text
> amipy runspider myspider01 
```
则名为“myspider01”的爬虫便会被启动。可以加上多个爬虫名称，用空格隔开即可。

* 6.列出当前项目下的所有爬虫信息。在DOS命令行下输入：
```text
> amipy list
```
便会将当前项目下的所有爬虫信息列出。

## 使用

### Amipy爬虫编写流程
编写自己的爬虫。【假设你已经安装前面"基础命令"创建了一个项目，并且创建了一个爬虫名为myspider】只需要进入myspider文件夹，按照需求修改当前爬虫的配置settings.py 以及数据存储需要用到的表模型item.py编写,编辑文件spider.py，加入爬取规则逻辑等。


### **Url**类对象
Url类对象是一个规则匹配类，它提供了许多种模式的url规则匹配。
比如：
```python
from amipy import Url
# 表示匹配到正则模式'http://www.170mv.com/song.*'的所有链接
Url(re='http://www.170mv.com/song.*')
# 表示匹配到正则模式'http://www.170mv.com/song.*'的所有链接其回调函数为'getmp3'
Url(re='http://www.170mv.com/song/.*',callback='getmp3')
# 表示匹配到地址为http协议,且路径为‘/novel/chapter1’,参数number=2的所有链接
Url(scheme='http',path='/novel/chapter1',params='number=2')
# 表示匹配到域名为www.baidu.com的所有链接,为该链接请求设置代理为'127.0.0.1:1080'
Url(domain='www.baidu.com',proxy='127.0.0.1:1080')
# 表示匹配到域名为www.baidu.com的所有链接，直接扔掉这些链接。
Url(domain='www.baidu.com',drop=True)
```
Url类应用的还在于黑白名单属性中，如在爬虫类中的属性：
```python
whitelist = [
        Url(re='http://www.170mv.com/song.*'),
        Url(re='http.*.sycdn.kuwo.cn.*'),]
blacklist = [
        Url(re='http://www.170mv.com/song.*'),
        Url(re='http.*.sycdn.kuwo.cn.*'),]      
```
表示爬虫请求的url黑白名单匹配规则。

### 必要属性

打开spider.py ，可以看到有两个默认的必要属性：
* name 爬虫的唯一标识，项目下不能有该属性重名的爬虫。
* urls 起始链接种子，爬虫开始的url列表

这两个属性是必须的。

### 回调函数

整个项目的主要实现在于回调函数的使用，利用异步请求得到响应后马上调用其请求绑定的回调函数来实现爬虫的异步爬取。
请求后响应的回调函数(类方法)有：
* parse   返回状态200，请求正常响应正常，可以编写正常的规则提取、数据保存等。
* error   状态码非200，出现异常状态码，编写错误处理逻辑等。
* exception 请求出现异常，异常自定义处理。

###  数据存储
Amipy目前只支持MongoDB数据库，默认的数据库设置在爬虫配置文件settings.py中。
对于爬取的数据进行保存，默认只使用MongoDB进行数据存储（后续可以自己扩展编写ORM）。只需要打开item.py,修改其中的示例类，原先为：
```python
from amipy.BaseClass.orm import Model,Field
class DataItemName(Model):
    ...
```
修改其内容为：
```python
from amipy.BaseClass.orm import Model,Field
class MyTableName(Model):
    ID = Field('索引')
    content = Field('内容')
```
则类名 **MyTableName**为保存在指定数据库中的数据集合名称，ID为列对象，名称为“索引”，以此类推，content也为列对象，名称为“内容”。
可以按照自己的需求进行添加删减列。

数据的保存只需要在回调函数中对对应的列对象进行赋值，而后调用ORM对象的save函数即可。比如在spider.py的爬虫类中的成功回调函数parse中保存爬取到的数据：
```python
    ...
    def parse(self,response):
        self.item.ID = 200
        self.item.content = '这是内容'
        self.item.save()
        ...
```
则 数据集合 **MyTableName**中会自动保存一行数据：列“索引”为200，列“内容”为“这是内容”的数据行。引用orm数据模型对象只需要调用爬虫类的item属性，如上面示例中的**self.item**即是。
获取其数据库对象可以使用：**self.item.db**来获得当前爬虫连接的MongoDB数据库对象。
可以通过
```python
self.item.db.save()
self.item.db.delete()
self.item.db.update()
...
````
等api来实现数据库操作。

### 事件循环loop
Amipy爬虫的异步请求基于python3的协程async框架，所以项目全程只有一个事件循环运行，如果需要添加更多的爬虫请求，可以通过回调函数传进事件循环，加入请求队列。
具体做法便是通过在爬虫类的回调函数中使用**send**函数来传递请求Request对象：
```python
import amipy
from amipy import Request,send

class MySpider(amipy.Spider):
    ...
    
    def parse(self,response):
        ...
        # 加入新的爬虫请求
        url = 'http://www.170mv.com/download/'
        send(Request(self,url))
        ...
```
可以在项目配置文件settings.py中设置整个项目最大的协程并发数CONCURRENCY，以及协程请求的延时等。

### Telnet连接
Amipy爬虫内置一个服务线程，可以通过Telnet进行连接来查看操作当前项目的爬虫，在启动爬虫后，可以通过新开一个DOS命令窗口，
输入：
```text
>telnet 127.0.0.1 2232
```
进行Telnet连接至项目服务线程，可以使用的命令有:
```text

   show spiders         show all running spiders and their conditions.
   list                 list a general situation of all spiders.
   echo                 echo a running spider and its attributes.
   pause                pause a running spider by a give name.
   stop                 stop a running/paused spider by a give name.
   close                close a spider by a give name.
   restart              restart a stopped spider by a give name.
   resume               resume a paused spider by a give name.
   quit                 quit the Spider-Client.
   help                 show all the available commands usage.
```
举例，假设当前爬虫唯一标识名称为lianjia，则可以通过：
```text
$amipy> pause lianjia
```
来暂停爬虫lianjia的爬取进度，在爬虫将当前请求队列清空后会一直暂停，直到收到Telnet端发出的其他命令。恢复爬虫使用：
```text
$amipy> resume lianjia
```
查看当前项目下所有爬虫：
```text
$amipy> list
```
详细查看则使用：
```text
$amipy> show spiders
```
开启关闭Telnet在项目的配置文件settings.py中设置SPIDER_SERVER_ENABLE。

### 爬取去重
Amipy的爬取去重可以分为两种：
* url去重
* 网页内容正文去重

两者皆使用了布隆过滤器去重，对于url去重，则是使用url+method+params+data的方式生成摘要进行布隆过滤器去重。
对于网页正文去重则是按照配置文件指定的正文检测参数来检测每个网页的正文内容生成摘要存进布隆过滤器，可以在爬虫的配置文件
settings.py中对以下几项进行配置来检测网页内容正文:
```text
# 网页内容剔除掉哪些标签后再识别正文
BLOOMFILTER_HTML_EXTRACTS = ['script','style','head']
# 允许一个正文内容块中至多空行数
BLOOMFILTER_HTML_GAP = 3
# 连续多少行有正文则认为是一个正文块
BLOOMFILTER_HTML_THRESHOLD = 5
# 每一行正文的字密度
BLOOMFILTER_HTML_DENSITY =45
```
上面两种是默认的去重方式，还可以指定请求返回的网页内容的某一部分作为响应指纹来进行针对性的去重。
如果想要自己指定哪个响应内容部分作为去重的指纹，可以在将请求Request送进协程队列时指定指纹函数，如：
```python
    ...
    def parse(self,response):
        ...
        send(Request(self,url,fingerprint=self.fingerprint))
        ...
    
    def fingerprint(self,response):
        ...
        # 返回需要作为指纹的文本字符等
        return something
```
## 例子
### 1. **使用Amipy创建链家网爬虫（LianJiaSpider）**

> 爬虫目的：爬取链家网上北京当前最新的租房信息，包含“价格”，“房屋基本信息”、“配套设施”、“房源描述”、“联系经纪人”、“地址和交通”存入MongoDB数据库中

 * 创建项目
 
 进入到D:\LianJia路径，创建Amipy项目LJproject：
 ```text
D:\LianJia> amipy cproject LJproject
```
 * 创建爬虫
 
 进入到项目路径D:\LianJia\LJproject，创建Amipy爬虫lianjia:
 ```text
D:\LianJia\LJproject> amipy cspider lianjia
```
* 编写数据库模型

打开D:\LianJia\LJproject\spiders\Lianjia\item.py，编写数据保存模型：
```python
#coding:utf-8

from amipy.BaseClass.orm import Model,Field

class LianJiaRenting(Model):
    price = Field('价格')
    infos = Field('房屋基本信息')
    facility = Field('配套设施')
    desc = Field('房源描述')
    agent = Field('联系经纪人')
    addr = Field('地址与交通')
```

* 设置数据库连接

打开 D:\LianJia\LJproject\spiders\Lianjia\settings.py，找到MongoDB数据库连接设置，进行设置：
```python
# MongoDB settings for data saving.
DATABASE_SETTINGS = {
    'host':'127.0.0.1',
    'port':27017,
    'user':'',
    'password':'',
    'database':'LianJiaDB',
}
```
要先确保系统安装好MongoDB数据库并已经开启了服务。

 * 编写爬虫脚本
 
 打开 D:\LianJia\LJproject\spiders\Lianjia\spider.py，编写爬虫采集脚本：
 ```python
import amipy,re
from amipy import send,Request,Url
from bs4 import BeautifulSoup as bs 

class LianjiaSpider(amipy.Spider):

    name = 'lianjia'
    # 设置爬取初始链接
    urls = ['https://bj.lianjia.com/zufang/']
    # 设置爬虫白名单，只允许爬取匹配的链接
    whitelist = [
    	Url(re='https://bj.lianjia.com/zufang/.*'),
    ]
    # 自定义的属性
    host ='https://bj.lianjia.com'
    page = 1
    
    # 请求成功回调函数
    def parse(self,response):
        soup = bs(response.text(),'lxml')
        item_list = soup('div',class_='content__list--item')
        for i in item_list:
        # 获取详情页链接 并发送至爬虫请求队列
            url = self.host+i.a['href']
            send(Request(self,url,callback=self.details))
        # 添加下一页
        totalpage = soup('div',class_='content__pg')[0]['data-totalpage']
        if self.page>=int(totalpage):
            return
        self.page +=1
        send(Request(self,self.host+'/zufang/pg{}/'.format(self.page)))
        
    def details(self,response):
        infos = {}
        agent = {}
        facility = []
        soup = bs(response.text(),'lxml')
        infos_li = soup('div',class_='content__article__info')[0].ul('li')
        facility_li = soup('ul',class_='content__article__info2')[0]('li')
        agent_ul = soup('ul',id='agentList')[0]
        addr_li = soup('div',id='around')[0].ul.li
        desc_li = soup('div',id='desc')[0].li
        desc_li.div.extract()
        desc = desc_li.p['data-desc'] if desc_li.p else ''
        for i in infos_li:
            text = i.text
            if '：' in text:
                infos.update({text.split('：')[0]:text.split('：')[1]})
        for i in facility_li[1:]:
            if '_no' not in i['class'][-2]:
                facility.append(i.text)
        for div in agent_ul('div',class_='desc'):
            name = div.a.text
            phone = div('div',class_='phone')[0].text
            agent[name]=phone
        # 数据模型对应并保存
        self.item.desc = desc
        self.item.addr = re.sub(r'[\r\n ]','',addr_li.text) if addr_li else ''
        self.item.price = soup('p',class_='content__aside--title')[0].text
        self.item.infos = infos
        self.item.agent = agent
        self.item.facility = facility
        self.item.save()
```
> 如果在爬虫配置文件settings.py中设置遵守目标网站机器人协议可能会被禁止采集，可以自行关闭设置。
另外，开启网页内容相似过滤**BLOOMFILTER_HTML_ON**可能会使爬取的结果数较少，爬虫只会采集相似度不同的网页内容的链接，
如果需要大批量采集，而网页正文较少的，可以关闭这个设置。

代码比较粗糙，但可以知道Amipy爬虫基本的实现流程。

* 运行爬虫

在项目根路径下，输入：
```text
D:\LianJia\LJproject> amipy runspider
```
* 查看数据库

进入MongoDB数据库：可以看到在数据库‘LianJiaDB’下的集合“LianJiaRenting”中已经保存有我们爬取的数据，格式如下：
```json
{
    "_id" : ObjectId("5c6541b065b2fd1cf002c565"),
    "价格" : "7500元/月 (季付价)",
    "房屋基本信息" : {
        "发布" : "20天前",
        "入住" : "随时入住",
        "租期" : "2~3年",
        "看房" : "暂无数据",
        "楼层" : "中楼层/6层",
        "电梯" : "无",
        "车位" : "暂无数据",
        "用水" : "民水",
        "用电" : "民电",
        "燃气" : "有",
        "采暖" : "集中供暖"
    },
    "配套设施" : [ 
        "电视", 
        "冰箱", 
        "洗衣机", 
        "空调", 
        "热水器", 
        "床", 
        "暖气", 
        "宽带", 
        "衣柜", 
        "天然气"
    ],
    "房源描述" : "【交通出行】 小区门口为八里庄南里公交车站，75，675等多路公交经过。地铁6号线十里堡站D口，距离地铁口400米，交通十分方便，便于出行。<br />\n【周边配套】 此房位置棒棒哒，有建设银行，中国银行，交通银行，邮政储蓄，果多美水果超市，购物，金旭菜市场，娱乐，休闲,便利。旁边首航超市，姥姥家春饼，味多美蛋糕店，生活方便。<br />\n【小区介绍】 该小区中此楼是1981建成，安全舒适，小区内主力楼盘为6层板楼，前后无遮挡，此楼是多见的板楼，楼层高视野好。<br />\n",
    "联系经纪人" : {
        "宋玉恒" : "4000124028转7907"
    },
    "地址与交通" : "距离6号线-十里堡192m"
}
```


* 查看当前爬取进度

新开一个DOS端口，输入：
```text
> telnet 127.0.0.1 2232
```
进行Telnet连接，可以使用命令操作查看当前爬虫的爬取状态。例如使用echo命令:
```text
$amipy> echo lianjia
```
可以查看当前爬虫的状态：
```text
----------------Spider-lianjia-------------------
- Name:lianjia  Status:RUNNING
- Class:LianjiaSpider
- Success:25    Fail:0     Exception:0
- Priority:0
- SeedUrls:['https://bj.lianjia.com/zufang/']
- Path:D:\LianJia\LJproject\spiders\Lianjia
- Session:<aiohttp.client.ClientSession object at  0x000000000386FE10>
- StartAt:Thu Feb 14 20:30:21 2019
- PausedAt:None
- ResumeAt:None
- StopAt:None
- RestartAt:None
- CloseAt:None
--------------------------------------------------
```





