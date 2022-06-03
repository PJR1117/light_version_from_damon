import time, datetime, threading
from concurrent import futures
from Crawler.Crawler_news import WebCrawlFromjrj
import Text_Analysis.text_mining as tm

def crawlers(web):
    web_crawl_obj = WebCrawlFromjrj("2009-01-05", "2018-02-03", 100, ThreadsNum=4, IP="localhost", PORT=27017, \
                                    dbName="Jrj_Stock", collectionName="jrj_news_company")
    web_crawl_obj.classifyRealtimeStockNews()

if __name__ == '__main__':
    # Step 1. Initiate
    text_mining_obj = tm.TextMining(IP="localhost",PORT=27017) #联结数据库

    # Step 2. Extract relevant stock codes of news(articles/documents) from all database
    text_mining_obj.extractStockCodeFromArticle("Jrj_Stock", "jrj_news_company")  # 从金融界网的新闻中抽出相关的股票代码

    # Step 3. Extract all news related to specific stock to new database(this step will take long time)
    codeLst = text_mining_obj.extractData("Stock","Basic_Info",['code']).code
    Range = 10
    Idx = 0
    while Idx < len(codeLst):
        thread_lst = []
        for stockcode in codeLst[Idx:Idx+Range]:
            thread = threading.Thread(target=text_mining_obj.getNewsOfSpecificStock,\
            args=([("Jrj_Stock","jrj_news_company")],stockcode),kwargs={"export":['database','Stock_News',stockcode],"judgeTerm":3})
        thread_lst.append(thread)
        for thread in thread_lst:
            thread.start()
        for thread in thread_lst:
            thread.join()
        print(' [*] have extracted ' + codeLst[Idx:Idx+Range])
        Idx += Range

    # Step 4. Crawl real-time news from 'web_list' and make classification
    web_list = ['sina', 'jrj', 'cnstock', 'stcn']
    with futures.ThreadPoolExecutor(max_workers=4) as executor:
        future_to_url = {executor.submit(crawlers, param): \
                             ind for ind, param in enumerate(web_list)}