# FDCA
> Financial data crawler and analyst

Analysis.py is the main analysis code, first do Pearson correlation coefficient analysis, and then do frequent pattern mining.

crawlData.py contains the code of data crawler, after configuring mongodb and running it, the data can be directly stored in mongodb and updated regularly.

# Prerequisites:
------
Ubuntu 18.04
python 3.7.4
numpy 1.19.4
scipy 1.5.4
schedule 0.6.0
pymongo 3.11.1
MongoDB 3.6.3

# Usage
------
This code is particularly easy to use:

```python
python crawlData.py
python Analysis.py
```


