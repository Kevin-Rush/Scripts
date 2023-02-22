from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
from math import log
from wordcloud import WordCloud


df = pd.read_csv ('jobs_in_California.csv')
#print(df)

df_title = df["Job Title"]
#print(df_title)

"""
frequent_titles = " ".join(cat.split()[1] for cat in df.category)

print(frequent_titles)

word_cloud = WordCloud(collocations = False, background_color = 'white').generate(frequent_titles)


plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()

#plt.scatter(*zip(*frequent_titles))
#plt.show()


# Start with one review:
text = df["Job Title"].description[0]
print(text)

# Create and generate a word cloud image:
wordcloud = WordCloud().generate(text)

# Display the generated image:
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()

"""
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Load the CSV file into a Pandas dataframe
df = pd.read_csv('jobs_in_California.csv')

# Concatenate all the text into a single string
text = ' '.join(df['Job Title'])

# Generate the wordcloud
wordcloud = WordCloud().generate(text)

# Display the wordcloud using matplotlib
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()
