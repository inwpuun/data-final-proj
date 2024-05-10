from pyspark.sql.functions import col
from spark import get_network_graph_data
import pandas as pd
import math

# Example DataFrame

df1 = get_network_graph_data() 
df2 = get_network_graph_data()

df2 = df2.withColumnRenamed("affilname", "targetAffilname")
# df2.show()
joined_df = df1.join(df2, "Title")

# Filter out the rows where the affiliation names are the same
filtered_df = joined_df.filter(col("affilname") != col("targetAffilname"))

# Select the necessary columnss
edge_df = filtered_df.select("affilname", "targetAffilname")
edge_df = edge_df.withColumnRenamed("affilname",'Source')
edge_df = edge_df.withColumnRenamed("targetAffilname",'Target')

edge_df = edge_df.distinct()

edge_df.sort('Source').show()

# edge_df.explain()
# edge_df.toDF('Source','Target').show()
# Write the resulting DataFrame to a CSV file
# edge_df.toJSON().first()
# result_df = edge_df.toPandas()
# result_df.head(10)
# result_df.to_csv('file_name.csv')



edge_df.write.option("header", True).option("encoding", "ISO-8859-1").mode("overwrite").csv("result")



# edge_df.to_excel("graph.xlsx", sheet_name='sheet')
# edge_df.write.csv("edges2", header=True,sep=',')

