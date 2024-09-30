import pandas as pd

# Specify the path to your JSON file
json_file_path = "new_college_stories.json"

# Read the JSON file and load the data into a dataframe
df = pd.read_json(json_file_path)


#print columns
print(df.columns)
print(df.head(1))

print("Types of Categories: ", df['category'].unique())

unique_categories = df['category'].unique()

# Create a new dataframe for each unique category
for category in unique_categories:
    category_df = df[df['category'] == category]
    print(f"Category: {category}")
    #save category_df to a CSV file
    category_df.to_csv(f"categorized_stories/{category}.csv", index=False)