import findspark
findspark.init()

spark_url = 'local'

from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder\
        .master(spark_url)\
        .appName('Spark SQL')\
        .getOrCreate()

df = spark.read.