from geopy.geocoders import Nominatim

# Initialize Nominatim API
geolocator = Nominatim(user_agent="MyApp")

location = geolocator.geocode("Hyderabad")

print("The latitude of the location is: ", location.latitude)
print("The longitude of the location is: ", location.longitude)

import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Create some sample text
text = 'Fun, fun, awesome, awesome, tubular, astounding, superb, great, amazing, amazing, amazing, amazing,Fun, fun, awesome, awesome, tubular, astounding, superb, great, amazing, amazing, amazing, amazing'

# Create and generate a word cloud image:
wordcloud = WordCloud(background_color="rgba(255, 255, 255, 0)",width=1000,height=1000, mode="RGBA").generate(text)

# Display the generated image:
# st.image(wordcloud.to_array(), caption='Word Cloud')
fig, ax = plt.subplots()
fig.patch.set_alpha(0)  # Set figure background to transparent
ax.patch.set_alpha(0)   # Set axis background to transparent
# Display the word cloud on the axis
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis("off")

# Display the Matplotlib figure using Streamlit
st.pyplot(fig)