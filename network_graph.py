from pyspark.sql.functions import collect_list,  explode_outer,col
import networkx as nx
import matplotlib.pyplot as plt
from spark import get_network_graph_data

# Example DataFrame


df = get_network_graph_data() #title, affilname
# df.show()# df.show()
# df.write.csv("network_graph")

joined_df = df.alias("df1").join(df.alias("df2"), "Title")
# Filter out the rows where the affiliation names are the same
filtered_df = joined_df.filter(col("df1.affilname") != col("df2.affilname"))

# Select the necessary columnss
edge_df = filtered_df.select("df1.affilname", "df2.affilname")

df = df.withColumnRenamed("affilname", "Source").withColumnRenamed("affilname", "Target")

edge_df.show()


# Write the resulting DataFrame to a CSV file
# edge_df.write.csv("affiliation_edges.csv", header=True)




# grouped = df.groupBy('title').agg(collect_list('affilname').alias('affiliations'))
# grouped = grouped.select('affiliations')
# grouped.head(1)
# # Add nodes and edges
# pairs = grouped.select('affiliations').withColumn('pair', explode_outer('affiliations')) \
#     .select('pair', 'affiliations').withColumn('affiliation', explode_outer('affiliations')) \
#     .where('pair != affiliation').groupBy('pair', 'affiliation').count()
# print('done')

# # Create graph
# edges = [(row['pair'], row['affiliation']) for row in pairs.collect()]
# G = nx.Graph(edges)

# # Draw the graph
# pos = nx.spring_layout(G)  # Positions for all nodes
# nx.draw(G, pos, with_labels=True, node_size=700, node_color="skyblue", font_size=10, font_weight="bold")
# plt.title("Affiliation Graph")
# plt.show()

# print('done')