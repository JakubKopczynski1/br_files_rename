import pandas as pd
import re

br_names = pd.read_csv("br_names.csv")

# Define a regex pattern to identify doubled names
pattern = re.compile(r'(\b\w+\b \b\w+\b);\s*\1')

# Check each filename for the pattern and update the 'doubled names' column
br_names['doubled name'] = br_names['filename'].apply(lambda x: 'yes' if pattern.search(x) else 'no')

# Save the updated DataFrame back to a CSV file if needed
br_names.to_csv('br_names_output.csv', index=False)
