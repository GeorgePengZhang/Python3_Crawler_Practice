# encoding=utf-8
import re
import time
import urllib.error
import urllib.request

class QiuShiBaikey:
    def __init__(self, host):
        # 请求地址
        self.host = host
        # 请求头
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
        # 所有文章存储列表
        self.stores = []
        # 总页数
        self.total_page = 1

    # 获取指定页数或者文章的源码内容
    def get_page(self, page_number=None, article=None):
        try:
            url = self.host
            if page_number:
                url = self.host + '/text/page/'+str(page_number)
            elif article:
                url = self.host + article

            request = urllib.request.Request(url, headers=self.header)
            response = urllib.request.urlopen(request)
            page = response.read()
            return page.decode()
        except urllib.error.HTTPError as e:
            print(e.code)
            print(e.reason)
        except urllib.error.URLError as e:
            print(e.reason)
        else:
            return None

    # 获取指定文章链接的全部内容
    def get_item_article(self, article):
        page = self.get_page(article=article)
        if page is None:
            return None
        pattern = '<div class="article.*?' \
                  '<div class="content">(.*?)</div>'

        content = re.search(pattern, page, re.S)
        if content:
            return content.group(1).replace('<br/>', '\n')

    # 获取指定页数的文章
    def get_page_item(self, page_number):
        page = self.get_page(page_number)
        if page is None:
            return
        if self.total_page <= 1:
            self.set_page_total(page)

        pattern = '<div class="article.*?' \
                  '<h2>(.*?)</h2>.*?' \
                  '<a href="(.*?)".*?' \
                  '<div class="content">.*?<span>(.*?)</span>(.*?class="contentForAll")*.*?' \
                  '<span class="stats-vote"><i class="number">(.*?)</i>.*?' \
                  '<span class="stats-comments">.*?<i class="number">(.*?)</i>'

        articles = re.findall(pattern, page, re.S)
        for article in articles:
            # 0:作者 1:文章链接 2：内容 3:是否有查看全部的标志 4：好笑数 5：评论数
            content = article[2].strip().replace('<br/>', '\n')
            # 如果存在查看全部的标志，就去加载对应文章的全部内容
            if article[3].strip():
                item = self.get_item_article(article=article[1].strip())
                if item:
                    content = item

            self.stores.append('作者：%s\n\n文章：\n%s\n\n好笑数：%s\t评论数：%s' % (article[0].strip(), content, article[4].strip(), article[5].strip()))

    # 获取全部文章
    def get_all_articles(self):
        return self.stores

    # 获取指定索引的文章
    def get_article(self, index):
        return self.stores[index]

    # 设置总页数
    def set_page_total(self, page):
        pattern = "<span class=\"page-numbers\">(.*?)</span>"
        results = re.findall(pattern, page, re.S)
        max_number = 1
        for result in results:
            max_number = max(max_number, int(result.strip()))
        self.total_page = max_number

    # 获取总页数
    def get_page_total(self):
        return self.total_page

    # 打印全部页数的文章
    def print_all_page(self):
        index = 1
        for article in self.stores:
            print('----------------------------------------------------')
            print(index, '.', article)
            index += 1

    # 加载全部页数的文章
    def load_all_page(self):
        print('开始加载糗事百科')
        # 通过加载第一页获取到总的页数
        self.get_page_item(1)
        print('已经加载%d/%d' % (1, self.total_page))
        page = 2
        while page <= self.total_page:
            self.get_page_item(page)
            print('已经加载%d/%d' % (page, self.total_page))
            time.sleep(2)
            page += 1
        print('加载完成!!!')


if __name__ == '__main__':
    host_url = 'https://www.qiushibaike.com'
    qsbk = QiuShiBaikey(host_url)
    qsbk.load_all_page()
    qsbk.print_all_page()

    print('\n\n\n')

    while True:
        s = input('请输入q退出')
        if s == 'q':
            break

