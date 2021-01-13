from pyspark.streaming import StreamingContext
from pyspark.sql import Row,SQLContext
import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import lower,split
import numpy as np

#get twitter credentials, actually this is not important
import pandas as pd
import math
from pyspark.sql.functions import *

#run instructions: spark-submit main.py


#log=pd.read_csv('Login.csv')
#print(log)

#consumer_key=log['key'][0]
#consumer_secret=log['key'][1]
#access_token=log['key'][2]
#access_secret=log['key'][3]

spark = (SparkSession
           .builder
           .appName("FinalProject")
           .getOrCreate())

sc = spark.sparkContext
sc.setLogLevel('WARN')

#upload twitter data
twitter_data=sc.textFile('result_Tweets_full.csv').flatMap(lambda line: line.split(" "))
#print(twitter_data.take(5))


#wordcount sample function

#twitter_data_Wordcount=twitter_RDD.map(lambda line: (line,1)).reduceByKey(lambda a,b:a+b)
#print(twitter_data_Wordcount.take(5))
#wordCounts.saveAsTextFile("output/")



#remove stop words
StopWordsFile=sc.textFile('stopWords_List.txt').flatMap(lambda line: line.split(" "))

#Converting above RDDs to lowercase
def Func(lines):
      lines = lines.lower()
      lines=lines.split()
      return lines

lowercaseInput = twitter_data.map(Func)
#print(lowercaseInput.collect())
lowercaseStopWordsInput = StopWordsFile.map(Func)


##Creating a tuple(word, 1) using map for above RDDs
tupleInput = twitter_data.map(lambda x : (x,1))
tupleStopWordsInput = StopWordsFile.map(lambda x : (x,1))
#tupleInput = lowercaseInput.map(lambda x : (x,1))
#tupleStopWordsInput = lowercaseStopWordsInput.map(lambda x : (x,1))

#using subtractByKey
tupleWords = tupleInput.subtractByKey(tupleStopWordsInput)

#to have only words in RDD
words = tupleWords.keys
#print(words.collect())

data=tupleWords.reduceByKey(lambda a,b:a+b).collect() # calculated the wordcount here 
print(data)
#print(data)# prints (word,1)


#find the frequency of values 
#data_freq=tupleWords.map(lambda x:(x[1],(x[0],x[1],1))).reduceByKey(lambda a,b:a+b).collect()
#print(data_freq)

#trial of Naive bayes classsifier. or Td-IDF algorithm, whichever produces results. 

#calculate IDF
#data_IDF_Map1=tupleWords.map(lambda x:(x[1],(x[0],x[1],1)))#.reduceByKey(lambda a,b:a+b)
#print(data_IDF_Map1.collect()) 
#data_IDF_Map2=data_IDF_Map1.map(lambda x:(x[0],x[1])).reduceByKey(lambda a,b:a+b)
#print(data_IDF_Map2.collect())

#idf=data_IDF_Map2.map(lambda x: (x[0],math.log10(len(twitter_data/(x[1]))))).collect()
#print(idf)


