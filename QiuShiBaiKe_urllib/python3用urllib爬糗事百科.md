## 简介

本文要讲的是使用python3去爬取糗事百科文字模块的内容。通过使用urllib爬取相应的网站源码，使用re正则表达式去匹配我们需要的文章信息。从而，收集我们想要的文章列表。

![这里写图片描述](https://img-blog.csdn.net/20180426114024117?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1FReGlhb3FpYW5nMTU3Mw==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

下图是爬取糗事百科的文章信息，包括作者、文章、好笑数、评论数等：

![这里写图片描述](https://img-blog.csdn.net/20180426114004311?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1FReGlhb3FpYW5nMTU3Mw==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)


## 实战

既然我们要爬取别人家的网站内容，那我们就先要爬取其网站源码。再从其源码中过滤出我们想要的内容。基本思路有了，那我们就开始实战吧。

### 第一步：爬取网站源码

我们要爬取网站源码，我们就要导入urllib.request模块，具体的调用代码如下：

``` java
import urllib.request

# 网站地址
url = 'https://www.qiushibaike.com/text/page/1'
# 请求头
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
request = urllib.request.Request(url, headers=headers)
response = urllib.request.urlopen(request)
# read()读取到的结果是byte
page = response.read()
# decode将byte转换为string
page.decode()
```

通过上面这段代码我们就可以获取到指定网址网页的源码了。这里需要注意的是：一定要加请求头即headers(`{'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}`)。如果不加的话，网站是不会接受我们的请求的，这样我们就得不到想要的网页源码。

### 第二步：过滤信息

整个网站的源码我们已经得到了，那就开始过滤不需要的信息吧。用于过滤信息的方法就是使用正则表达式，这里我们需要导入re模块。同时，我们要知道过滤信息的规则。这里我用的Chrome浏览器，点击鼠标右键，选中检查就会显示对应网站内容中模块的源码。如图：

![这里写图片描述](https://img-blog.csdn.net/20180426141321845?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1FReGlhb3FpYW5nMTU3Mw==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

通过上图，我们知道我要去过滤文章信息，就要找到`<div class="article *>`这元素块。在这一页中所有的文章元素块都是以这个开头的。然后在分析里面具体对应的作者、文章内容、好笑数、评论数等信息，把他们提取出来。我们的正则表达式如下：

``` java
pattern = '<div class="article.*?' \
          '<h2>(.*?)</h2>.*?' \
          '<a href="(.*?)".*?' \
          '<div class="content">.*?<span>(.*?)</span>(.*?class="contentForAll")*.*?' \
          '<span class="stats-vote"><i class="number">(.*?)</i>.*?' \
          '<span class="stats-comments">.*?<i class="number">(.*?)</i>'
```

上面这个字符串里面的规则都是根据网站源码总结出来的，感觉兴趣的朋友可以实际去查看下源码，对比下结果。其中.*?表示非贪婪模式只获取最少的匹配结果，()代表一个分组。有了正则表达式后，我们就要开始匹配字符串了。把我们在第一步获取到的源码全部传入和我们的正则表达式开始匹配，代码如下：

``` java
# pattern正则表达式规则
# page要查找的源码内容
# re.S匹配模式DOTALL模式，.能匹配任意字符包括换行符\n
articles = re.findall(pattern, page, re.S)
for article in articles:
    # 0:作者 1:文章链接 2：内容 3:是否有查看全部的标志 4：好笑数 5：评论数
    print('qsbk:', article[0].strip(), article[1].strip(), article[2].strip(), article[3].strip(), article[4].strip(), article[5].strip())
```

articles就是我们匹配后的所有文章的列表。article就单独一篇文章信息。里面包括了作者、文章链接、内容、查看全部、好笑数和评论数。article[0...5]对应的正则表达式里面的一个分组即()，上面的正则表达式中，我们用了6个(.*?)所有就有6个article元素，分组从0开始计数，依次累加。每个分组就是我们想要去获取的文章信息。

这里注意文章链接和查看全部，我们好像还没使用到。这是因为有的文章一次性显示不完，需要进入它的文章页面才能完整显示，这个时候我们就可以通过查看全部，来判断是否需要去获取文章页面里的完整文章内容了。

获取单个文章的内容的方法跟获取文章列表的方法是一样的，只是正则表达式的规则要根据实际的源码来分析。就不在多说了。


## 总结

通过上面两步我们已经获取到了我们想要的文章信息列表了。之后的具体怎么去利用这些列表信息就可以根据自身需求去定义实现了。掌握了爬数据的核心技术，其他就是发挥给位的聪明才智了。

下面来分享下我实现的爬取糗事百科的需求：
[爬取糗事百科文字模块的所有页面文章信息](https://github.com/GeorgePengZhang/Python3_Crawler_Practice/blob/master/QiuShiBaiKe_urllib/QiuShiBaiKe.py)

![这里写图片描述](https://img-blog.csdn.net/2018042615552746?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1FReGlhb3FpYW5nMTU3Mw==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)












