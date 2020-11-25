#### Instructions

Analysis.py为主要的分析代码，先做Pearson相关系数分析，再做频繁模式挖掘。

crawlData.py为数据爬虫，配置好MongoDB后可以直接将数据存在MongoDB，并实现定时更新。

具体的运行环境见技术报告。


运行方式非常简单：

```python
python crawlData.py
python Analysis.py
```



