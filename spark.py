import findspark
import streamlit as st
from geopy.geocoders import Nominatim
findspark.init()

spark_url = 'local'

from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, count

spark = SparkSession.builder\
        .master(spark_url)\
        .appName('Spark SQL')\
        .getOrCreate()

from pyspark.sql.functions import explode, count
path = "/out/scopus_data.csv"
df = spark.read.option("delimiter", ";").option("header", True).csv(path)
df = df.dropDuplicates()

from pyspark.sql.types import ArrayType, StringType, StructType, StructField
from pyspark.sql.functions import col, from_json

affilSchema = ArrayType(StructType([
    StructField("affilname", StringType()),
    StructField("affiliation-city", StringType()),
    StructField("affiliation-country", StringType())
]))

subjectSchema = ArrayType(StringType())
df = df.withColumn("subject_array", from_json(col("subject"), subjectSchema))
explodedDF = df.select("title", "affiliation", explode(col("subject_array")).alias("subject"), "year", "source_id", "citedby_count")
explodedDF = explodedDF.withColumn("affiliation_array", from_json(col("affiliation"), affilSchema))
explodedDF = explodedDF.select("title", explode(col("affiliation_array")).alias("affiliation"),"subject", "year", "source_id", "citedby_count")

resultDF = explodedDF.select(
    "title",
    explodedDF["affiliation.affilname"].alias("affilname"),
    explodedDF["affiliation.affiliation-city"].alias("affiliation_city"),
    explodedDF["affiliation.affiliation-country"].alias("affiliation_country"),
    "subject",
    "year",
    "source_id",
    "citedby_count"
)


def get_all_affil():
    return [row.affilname for row in resultDF.select("affilname").distinct().collect()]

def get_all_country():
    return [row.affiliation_country for row in resultDF.select("affiliation_country").distinct().collect()] 

def get_all_year():
    return [row.year for row in resultDF.select("year").distinct().collect()]

def get_affil_count_filter_by_year(year):
    output = resultDF.filter(resultDF.year == year)
    return output.groupBy('affilname').agg(count("*").alias("count"))

# def get_affil_count_filter_by_subject(subject):
#     output = resultDF.filter(resultDF.subject in subject)
#     return output.groupBy('year').agg(count("*"))

def get_filter_by_affilname(affilname):
    output = resultDF.filter(resultDF.affilname == affilname)
    return output.groupBy('year').agg(count("*").alias("count")).toPandas()

def get_affil_count_filter_by_subject_year(subjects, year, test):
    combined_output = None
    for subject in subjects:
        filtered_output = resultDF.filter((resultDF.subject == subject) & (resultDF.year == year))
        output = filtered_output.groupBy(test).agg(count("*").alias("count"))
        if combined_output is None:
            combined_output = output
        else:
            combined_output = combined_output.unionAll(output)
    return combined_output

from pyspark.sql.functions import lit

# first graph
def get_year_count_filter_by_subject(subjects):
    combined_output = None
    for subject in subjects:
        filtered_output = resultDF.filter(resultDF.subject == subject)
        output = filtered_output.groupBy('year').agg(count("*").alias("count"))
        output = output.withColumn("subject", lit(subject))
        if combined_output is None:
            combined_output = output
        else:
            combined_output = combined_output.unionAll(output)
    return combined_output.toPandas()


def get_affil_count_filter_by_year(year):
    output = resultDF.filter((resultDF.year == year) & (~resultDF.affilname.contains("Chulalongkorn University")))
    return output.groupBy('subject','affilname').agg(count("*").alias("count")).toPandas()

def get_all_subject_count():
    return resultDF.groupBy('subject').agg(count("*").alias("count")).toPandas()

def get_chula_thai_collaboration_by_subject_year_count():
    output = resultDF.filter((resultDF.affiliation_country == "Thailand") & (~resultDF.affilname.contains("Chulalongkorn University")))
    return output.groupBy('affilname').agg(count("*").alias("count")).toPandas()

def get_chula_thai_collaboration_country_by_subject_year_count():
    output = resultDF.filter(~resultDF.affilname.contains("Chulalongkorn University"))
    mapDf = output.groupBy('affiliation_country').agg(count("*").alias("count")).toPandas()
    return mapDf
def get_country_count_radius_lat_lon():
    output = resultDF.filter(~resultDF.affilname.contains("Chulalongkorn University"))
    mapDf = output.groupBy('affiliation_country').agg(count("*").alias("count")).toPandas()
    geolocator = Nominatim(user_agent="MyApp")
    def get_lat_long(country):
        location = geolocator.geocode(country)
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    mapDf['lat'], mapDf['lon'] = zip(*mapDf['affiliation_country'].apply(get_lat_long))
    max_count = mapDf['count'].max()
    mapDf['radius'] = mapDf['count'] / max_count 
    return mapDf

def get_network_graph_data():
    output = resultDF.select('title','affilname')
    return output

# print(df.count())
# print(get_all_affil())
# print(get_all_country())
# print(get_all_year())
# resultDF.show()
# resultDF.groupby('title')['affiliation'].apply(list).show()
# get_year_count_filter_by_subject(["MATH", "COMP"]).show(40)
# get_affil_count_filter_by_year(2022).show()
# get_affil_count_filter_by_subject_year(["MATH", "COMP"], "2022", "affiliation_country").show()
# get_affil_count_filter_by_subject("MATH").show()
# get_all_subject_count().show()
# get_chula_thai_collaboration_by_subject_year_count().show(40)
# get_chula_thai_collaboration_country_by_subject_year_count().show()
# get_filter_by_affilname("Chulalongkorn University").show()
# print(get_filter_by_affilname("Chulalongkorn University"))
