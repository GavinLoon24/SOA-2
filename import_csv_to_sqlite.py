import pandas as pd
import sqlite3

# Load CSV data into a DataFrame
df = pd.read_csv('comments.csv')

# Normalize the text data
df['text'] = df['text'].str.strip().str.lower()

# Create a SQLite database connection
conn = sqlite3.connect('comments.db')

# Export DataFrame to SQLite
df.to_sql('comments', conn, if_exists='replace', index=False)

# Close the connection
conn.close()

print("CSV data has been imported into SQLite database successfully.")
