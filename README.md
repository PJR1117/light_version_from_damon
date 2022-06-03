# 上市公司新闻文本分析与分类预测

 ![image](https://github.com/DemonDamon/Listed-company-news-crawl-and-text-analysis/blob/master/docs/images/FINNEWS-HUNTER.jpg)

-------------------------------

## 简介

上市公司新闻文本分析与分类预测的基本步骤如下：

 - 将原来的改为仅从金融界爬取
 - 从Tushare上获取沪深股票日线数据（开、高、低、收、成交量和持仓量）和基本信息（包括股票代码、股票名称、所属行业、所属地区、PE值、
   总资产、流动资产、固定资产、留存资产等）
 - 对抓取的新闻文本按照，去停用词、加载新词、分词的顺序进行处理
 - 利用前两步中所获取的股票名称和分词后的结果，抽取出每条新闻里1所包含的（0支、支或多支）股票名称，并将所对应的所有股票代码，组合成与该条新闻相关
   的股票代码列表，并在历史数据表中增加一列相关股票代码数据
 - 从历史新闻数据库中抽取与某支股票相关的所有新闻文本，利用该支股票的日线数据（比如某一天发布的消息，
   在设定N天后如果价格上涨则认为是利好消息，反之则是利空消息）给每条新闻贴上“利好”和“利空”的标签，并存储到新的数据库中（或导出到CSV文件）
 - 实时抓取新闻数据，判断与该新闻相关的股票有哪些，利用上一步的结果，对与某支股票相关的所有历史新闻文本（已贴标签）进行文本分析（构建新的特征集），
   然后利用SVM（或随机森林）分类器对文本分析结果进行训练（如果已保存训练模型，可选择重新训练或直接加载模型），最后利用训练模型对实时抓取的新闻数据进行分类预测

开发环境`Python-v3(3.6)`：

 - gensim==3.2.0
 - jieba==0.39
 - scikit-learn==0.19.1
 - pandas==0.20.0
 - numpy==1.13.3+mkl
 - scipy==0.19.0
 - pymongo==3.6.0 #我可以用pymysql来替代
 - beautifulsoup4==4.6.0
 - tushare==1.1.1
 - requests==2.18.4
 - gevent==1.2.1

## 文本处理 -> [text_processing.py](https://github.com/DemonDamon/Listed-company-news-crawl-and-text-analysis/blob/master/Text_Analysis/text_processing.py)

 - 文本处理包括去停用词处理、加载新词、中文分词、去掉出现次数少的分词
 - 生成字典和Bow向量，并基于Gensim转化模型（LSI、LDA、TF-IDF）转化Bow向量
 - 计算文本相似度
 - 打印词云

## 文本挖掘 -> [text_mining.py](https://github.com/DemonDamon/Listed-company-news-crawl-and-text-analysis/blob/master/Text_Analysis/text_mining.py)

 - 从新闻文本中抽取特定信息，并贴上新的文本标签方便往后训练模型
 - 从数据库中抽取与某支股票相关的所有新闻文本
 - 将贴好标签的历史新闻进行分类训练，利用训练好的模型对实时抓取的新闻文本进行分类预测

## 新闻爬取 -> [crawler_cnstock.py](https://github.com/DemonDamon/Listed-company-news-crawl-and-text-analysis/blob/master/Crawler/crawler_cnstock.py), [crawler_jrj.py](https://github.com/DemonDamon/Listed-company-news-crawl-and-text-analysis/blob/master/Crawler/crawler_jrj.py), [crawler_nbd.py](https://github.com/DemonDamon/Listed-company-news-crawl-and-text-analysis/blob/master/Crawler/crawler_nbd.py), [crawler_sina.py](https://github.com/DemonDamon/Listed-company-news-crawl-and-text-analysis/blob/master/Crawler/crawler_sina.py), [crawler_stcn.py](https://github.com/DemonDamon/Listed-company-news-crawl-and-text-analysis/blob/master/Crawler/crawler_stcn.py)

 - 分析网站结构，多线程（或协程）爬取上市公司历史新闻数据

## Tushare数据提取 -> [crawler_tushare.py](https://github.com/DemonDamon/Listed-company-news-crawl-and-text-analysis/blob/master/run_crawler_tushare.py)

 - 获取沪深所有股票的基本信息，包括股票代码、股票名称、所属行业、所属地区等

## 用法

 - 配好运行环境以及安装MongoDB，最好再安装一个MongoDB的可视化管理工具Studio 3T
 - 先运行[crawler_cnstock.py](https://github.com/DemonDamon/Listed-company-news-crawl-and-text-analysis/blob/master/Crawler/crawler_cnstock.py), [crawler_jrj.py](https://github.com/DemonDamon/Listed-company-news-crawl-and-text-analysis/blob/master/Crawler/crawler_jrj.py), [crawler_nbd.py](https://github.com/DemonDamon/Listed-company-news-crawl-and-text-analysis/blob/master/Crawler/crawler_nbd.py), [crawler_sina.py](https://github.com/DemonDamon/Listed-company-news-crawl-and-text-analysis/blob/master/Crawler/crawler_sina.py), [crawler_stcn.py](https://github.com/DemonDamon/Listed-company-news-crawl-and-text-analysis/blob/master/Crawler/crawler_stcn.py)这5个py文件，而且可能因为对方服务器没有响应而重复多次运行这几个文件才能抓取大量的历史数据
 - 接着运行[crawler_tushare.py](https://github.com/DemonDamon/Listed-company-news-crawl-and-text-analysis/blob/master/run_crawler_tushare.py)从Tushare获取基本信息和股票价格
 - 最后运行[run_main.py](https://github.com/DemonDamon/Listed-company-news-crawl-and-text-analysis/blob/master/run_main.py)文件，其中有4个步骤，除了第1步初始化外，其他几步最好单独运行
 - 注意：所有程序都必须在文件所在目录下运行

## 更新目标

 - 可以将新的新闻来源改为tushare中的新闻来源,获取更加方便.



## 个人小理解



## step 0 完成爬虫

数据结构

还有一个tushare爬虫数据库 数据库名为Stock 有Basic_Info的集合与代码为的集合

新闻爬虫数据库 : 以新闻来源为数据库,以sina_news_company为集合,以_id为主键,其中有个字段为'RelevantStock',表示相关的股票,内容可以解析出股票代码

新闻数据库: 最终用于预测的数据库 数据库名为Stock_News 集合名为股票code,以_id为主键,每个id下面内容有时间,地址,标题,文章内容,标签

```mermaid
graph TB
	WebCrawlFromcnstock实例化
	-->输入参数localhost,27017,最少页数4,Cnstock_Stock,cnstock_news_company
	-->运用其中方法coroutine_run
	-->传入参数总页数,每份的页数,起始页,网址
	-->页码分页GenPagesLst
	-->遍历每一个range
	-->协程开始,目标为CrawlHistoryCompanyNews,传入每个range的起始页,结束页,网址
	subgraph 在CrawlHistoryCompanyNews中
	协程开始,目标为CrawlHistoryCompanyNews,传入每个range的起始页,结束页,网址-->联结数据库
	-->运用extractData获得集合中地址列表
	-->1[/地址列表是否为空/]--否-->通过同样的方法-->向集合中插入文档,并且打印文档和标题
	1[/地址列表是否为空/]--是-->通过传入的网址按照规律生产地址列表进行遍历
	-->BeautifulSoup进行解析
	-->找到a标签
	-->找到标签中有href,target,title,href中有http://company.cnstock.com/company/,parent里面有span的标签-->用getUrlInfo进行解析
	subgraph 在getUrlInfo中
	用getUrlInfo进行解析-->传入标签中属性href-->找到span标签-->如果有clas属性且属性值等于timer-->获取其中该页的日期文本,加入日期字符串,结束循环-->输出article列表,date字符串
	传入标签中属性href-->找到p标签-->运用类中的countchn方法计算p中中文字符出现的频率-->对于中文数量大于prop的标签加入article字符串-->当字符串中存在&#60,&#62,将用空格替代两个尖括号之间的内容-->同样剔除\u3000-->将article字符串字符串split成列表-->输出article列表,date字符串
	end
	输出article列表,date字符串-->2[/article是否为空/]--空-->说明prop太大了,降低prop-->再提取一次-->向集合中插入文档,并且打印文档和标题
	2[/article是否为空/]--非空-->向集合中插入文档,并且打印文档和标题
	end
     向集合中插入文档,并且打印文档和标题-->over
```

爬虫其实都是大同小异,不同的地方有

* 页码顺序不同,有些需要以数字作为顺序,有些需要以时间作为顺序
* 标签内容不同,需要具体问题具体分析



对tushare进行操作 提取现在的股票基本信息放入"Stock","Basic_Info" 提取价格信息放入"Stock",'stockCode'

```mermaid
graph TB
	实例化Crawler_tushare中的CrawlStockData类-->
	传入IP,端口参数-->
	使用类下的getStockBasicFromTushare方法-->
	传入参数dbName=Stock,colname=Basic_Info-->
	提取出基本信息放入指定的集合中-->
	运用extractData将code这个字段提出出来形成一个列表-->
	对于每一个code-->
	联结dbName=Stock,对应的每一个code集合-->
	传入以stockcode为顺序的txt地址,打开txt&#40这个txt应该是自己事先下好的&#41-->
	读取txt的每行,存入列表中-->
	提取信息插入code集合
```





## step 1 联结数据库

将Text_Analysis.text_mining.py中的 TextMining类实例化,,输入数据库的端口和IP 

```python
text_mining_obj = tm.TextMining(IP="localhost",PORT=27017)
```

## step 2 从所有的网页爬虫数据库的新闻中提取相关的股票代码

### 如何定义相关

被jieba处理过的长度长度大于3的并且存在于数据库的定义为相关

为何是这个定义,可能需要亲自爬虫才能明白.

------

前提是先用爬虫将数据爬到数据库中后才能进行操作

用到了TextMining实例化后,其中的方法extractStockCodeFromArticle

```python
text_mining_obj.extractStockCodeFromArticle("NBD_Stock","nbd_news_company") # 从每经网的新闻中抽出相关的股票代码
	text_mining_obj.extractStockCodeFromArticle("Cnstock_Stock","cnstock_news_company") # 从中国证券网的新闻中抽出相关的股票代码
	text_mining_obj.extractStockCodeFromArticle("Stcn_Stock","stcn_news_company") # 从证券时报网的新闻中抽出相关的股票代码
	text_mining_obj.extractStockCodeFromArticle("Jrj_Stock","jrj_news_company") # 从金融界网的新闻中抽出相关的股票代码
```

对于extractStockCodeFromArticle ,这个是为了提取被新闻或者报告提到的股票代码,需要输入两个参数,数据库的名字和集合的名字

```mermaid
graph TB
	联结数据库与对应的集合-->类中的extractData函数-->提取爬虫id字段列表
	-->1[/数据库名是否是NBD_Stock每经网/]-->提取爬虫结果中每一个id的tiltle和article字段
	-->将title和article放入列表中
	-->将title和article列表用genDictionary生成字典和词袋模型-->输入参数:需要解析的内容,保存地址
	subgraph genDcitionary
	输入参数:需要解析的内容,保存地址
	-->将需要解析的内容传入jieba_tokenize方法中-->getchnSTW方法获得停词-->getchnSTW方法获得停词,为事先准备好的txt
	subgraph jieba_tokenize
	getchnSTW方法获得停词,为事先准备好的txt-->读取公司金融词汇-->一些列结巴操作-->生成分割后的列表
	end
	生成分割后的列表-->运用gensim中的corpora.Dictionary形成字典文档--是否保存-->返回分割列表,字典文档,词袋模型-->遍历分割后的列表-->对于词长度大于3且存在于tushare的name字段中的-->取出其name和code,标记为相关-->去重后放入对应爬虫结果的relevantStock字段中
	end 

	
```

------

## step 3 从爬虫数据库提取所有的和股票相关的新闻放入新闻数据库中

```mermaid
graph TB
	使用Text_Analysis.text_mining.TextMining类中的extractData,取出所有的股票代码形成列表-->从tushare数据库中找出相关股票的字段进行存储-->
	运用滚动窗口的方法进行循环,窗口长度为10-->
	窗口起始值是否超过code列表的长度-->对于每一个code-->
	运用threading.Thread进行多线程处理,复习一下多线程和多进行以及协程,看看是否可以优化-->
	多线程目标为getNewsOfSpecificStock在数据库中和特定股票相关的新闻-->
	需要传入的参数为:数据库和集合的元组列表,循环的股票代码以及和存储,路径有关的参数-->
	1[/是否传入参数csv/]--是-->打开指定的csv文件-->数据写入csv,列为date,address,title,article-->对元组列表进行循环,元组对应的dbName,colName-->取出集合中所有文档的id组成列表-->2[/daName是否等于Sina_Stock/]-->用id列表遍历每一个文档有RelevantStock字段的文档-->RelevantStock字段里是否有想要的StockCode--有-->将该id想要的字段写入csv-->同理
	取出集合中所有文档的id组成列表-->3[/dbName是否等于是NBD/]-->同理-->对元组列表进行循环,元组对应的dbName,colName
	1[/是否传入参数csv/]--否-->如果是database-->遍历每一个爬虫_id-->4[/不同的新闻来源不同操作/]--NBD_Stock-->对于每一个在滚动窗口中的id,为tushare中的id-->如果存在于爬虫结果的relevantStock字段中-->用judgeGoodOrBadNews方法设定标签-->插入新闻数据库,新闻集合对应StockCode的文档中
4[/不同的新闻来源不同操作/]--Sina_Stock-->插入新闻数据库,新闻集合对应StockCode的文档中
4[/不同的新闻来源不同操作/]--其他-->插入新闻数据库,新闻集合对应StockCode的文档中-->遍历每一个爬虫_id
	插入新闻数据库,新闻集合对应StockCode的文档中-->多线程存讲相应的字段于新闻数据库的stockcode集合中
	同理-->多线程存讲相应的字段于新闻数据库的stockcode集合中
```

## step 4 爬取网页列表中的现在的新闻并分类

```python
web_list = ['sina','jrj','cnstock','stcn']
	with futures.ThreadPoolExecutor(max_workers=4) as executor:
		future_to_url = {executor.submit(crawlers,param) : ind for ind, param in enumerate(web_list)} #字典格式上传到线程池中
        
```

## step 5 文本挖掘

```mermaid
graph TB
	运用Text_mining类中的classifyHistoryStockNews方法-->
	输入参数dbname,stockcode,是否更新文档,变换的模式,提取的主题数,分类器,分类器参数-->
	1[/是否更新文档/]--是,本地一片空白-->创建储存路径-->联结新闻数据库-->遍历以股票代码命名的集合中文档的Character字段-->利好标为1,利空标为-1,无影响标为0,放入Character并且取出所有文档的Article放入列表中-->运用genDictionary方法对article进行分词与生成词袋向量并储存
	1[/是否更新文档/]--否,本地有stockcode文件夹-->并且没有字典和向量的储存记录-->创建储存路径
	利好标为1,利空标为-1,无影响标为0,放入Character并且取出所有文档的Article放入列表中-->不储存
	1[/是否更新文档/]--其他情况,直接读取本地-->利好标为1,利空标为-1,无影响标为0,放入Character并且取出所有文档的Article放入列表中
	
	运用genDictionary方法对article进行分词与生成词袋向量并储存-->读取路径中的字典和向量
	不储存-->读取路径中的字典和向量-->运用文本处理类中的CallTransformationModel方法调用Gensim模块的特定转换模型-->2[/是否对词袋重新训练/]--是-->重新训练词袋转化为td-idf-->更新模型,依照modeltype进行更新-->返回模型向量
	2[/是否对词袋重新训练/]--否-->读取本地td-idf-->更新模型,依照modeltype进行更新
	返回模型向量-->通过ConvertToCSRMatrix方法转化为矩阵-->数据集分割,特征为article转化的向量,标签为character的利好利空-->训练
```

## step 6 对realtime爬虫结果进行预测

```mermaid
graph TB
	获得realtime新闻爬虫结果-->设定默认主题数为200-->运用每支股票自己的训练集对算法进行训练-->输入参数列表,通过打分获得最好的参数
	获得realtime新闻爬虫结果-->对于结果中的每一个articel取出所有相关股票-->遍历每一支股票-->将爬虫结果jieba成词袋模型-->加入原本的词袋中-->生成新的模型向量-->矩阵化-->输入参数列表,通过打分获得最好的参数-->预测
```







## 总结

```mermaid
graph TB
	爬虫-->tushare-->获得股票代码与name-->dbname=Stock,collection=股票代码--名字和代码来自-->将新闻中提到的相关股票代码和股票名称增加到一个新的字段relevantstock中
	爬虫-->新闻网站-->获得股票新闻-->dbname=新闻网站,collection=新闻网站_news_company-->将新闻中提到的相关股票代码和股票名称增加到一个新的字段relevantstock中-->将每个股票代码有关的新闻内容标记好坏后放入新闻数据库中,dbname=Stock_new,collection=股票代码-->执行文本挖掘-->对新闻数据库中的数据进行处理,将其向量化-->即每只股票有自己的新闻训练集与训练模型-->爬取新的信息将其向量化-->预测
	
```









