# MAPOWANIE KEYWORDSÓW Z HARVESTA NA NASZE
# MAPOWANIE NIEMIECKICH TAGÓW
# PRZYGOTOWANIE METADATY DO ZMIANY NAZW PLIKÓW

import pandas as pd
import glob
import re
from mappings import mapping_dicts, valid_keywords, mapping_dict_BR, valid_keywords_BR, keywords_no_colon

pd.set_option('display.max_columns', 200)
pd.set_option('display.width', 1000)

directory_path = 'C:/Users/jakub/PycharmProjects/br_metadata_and_rename/new_metadata'
csv_files = glob.glob(directory_path + '/*.csv')

columns_to_use = [
    'LIBRARY: Name',
    'ALBUM: Code',
    'TRACK: Display Title',
    'TRACK: Description',
    'TRACK: Version',
    'TRACK: Genre',
    'TRACK: Instrumentation',
    'TRACK: Keywords',
    'TRACK: Mood',
    'TRACK: Music For',
    'TRACK: Audio Filename',
    'WRITER:1: First Name',
    'WRITER:1: Last Name',
    'WRITER:2: First Name',
    'WRITER:2: Last Name',
    'WRITER:3: First Name',
    'WRITER:3: Last Name',
    'WRITER:4: First Name',
    'WRITER:4: Last Name',
    'WRITER:5: First Name',
    'WRITER:5: Last Name',
    'WRITER:6: First Name',
    'WRITER:6: Last Name',
    'WRITER:7: First Name',
    'WRITER:7: Last Name',
    'WRITER:8: First Name',
    'WRITER:8: Last Name'
]

dfs = []

for file in csv_files:
    try:
        df = pd.read_csv(file, usecols=columns_to_use)
        dfs.append(df)

    except Exception as e:
        print(f'Error reading file {file}: {e}')

df = pd.concat(dfs, ignore_index=True)

# Remove double spaces from the entire DataFrame
df = df.replace(to_replace=r'\s+', value=' ', regex=True)

###################################
### KEYWORDS FOR MP3TAG PROGRAM ###
###################################

# Columns with keywords
columns = [
    "TRACK: Genre",
    "TRACK: Instrumentation",
    "TRACK: Keywords",
    "TRACK: Mood",
    "TRACK: Music For"
]

for library_name, group_df in df.groupby('LIBRARY: Name'):
    selected_mapping_dict = mapping_dicts.get(library_name)

    if selected_mapping_dict is None:
        raise KeyError(f'No mapping found for: {library_name}')

    # Initial keywords mapping
    for column in columns:
        # We target df.loc[group_df.index, column] to update the original dataframe
        temp_col = df.loc[group_df.index, column].replace(r', ', ',', regex=True)
        temp_col = temp_col.apply(lambda keywords: ' '.join(keywords.split()).split(',') if pd.notna(keywords) else [])

        # Mapping
        temp_col = temp_col.apply(lambda keywords: [value for keyword in keywords for value in
                                                    selected_mapping_dict.get(keyword, [keyword])])
        # Filtering
        temp_col = temp_col.apply(lambda keywords: [keyword for keyword in keywords if keyword in valid_keywords])
        # Deduplication
        temp_col = temp_col.apply(lambda keywords: list(set(keywords)))
        # Join
        df.loc[group_df.index, column] = temp_col.apply(lambda keywords: ', '.join(keywords))

# Deconstructing keywords with colons
for col in columns:
    df[col] = df[col].apply(
        lambda x: ", ".join(
            keywords_no_colon.get(tag.strip(), tag.strip())
            for tag in x.split(",")
        ) if pd.notna(x) else x
    )

# Copying columns
df[[col + "_Ger" for col in columns]] = df[columns]

# Columns for German keywords mapping
columns_ger = [
    "TRACK: Genre_Ger",
    "TRACK: Instrumentation_Ger",
    "TRACK: Keywords_Ger",
    "TRACK: Mood_Ger",
    "TRACK: Music For_Ger"
]

# German keywords mapping
for column in columns_ger:
    df[column] = df[column].replace(to_replace=r', ', value=',', regex=True)
    # change strings into lists for list comprehension
    df[column] = df[column].apply(lambda keywords: ' '.join(keywords.split()).split(',') if pd.notna(keywords) else [])
    # list comprehension and mapping
    df[column] = df[column].apply(lambda keywords: [value for keyword in keywords for value in
                                                    mapping_dict_BR.get(keyword, [keyword])])
    # leave only keywords, that are on the valid_keywords list
    df[column] = df[column].apply(lambda keywords: [keyword for keyword in keywords if keyword in valid_keywords_BR])
    # remove duplicates
    df[column] = df[column].apply(lambda keywords: list(set(keywords)))
    # change keywords back to single strings
    df[column] = df[column].apply(lambda keywords: '; '.join(map(str, keywords)))

# Change commas to semicolons in columns with English tags
df[columns] = df[columns].replace(r"\s*,\s*", "; ", regex=True)

# Dictionary of GVL Label Codes
gvl_codes = {
    'APL': 'LC 91583',
    'APL Decades': 'LC 91553',
    'APL Frontrunners': 'LC 91554',
    'APL Lifestyle': 'LC 91555',
    'APL Organic': 'LC 91552',
    'APL Vocals': 'LC 91556',
    'Benztown Branding': 'LC 89388',
    'Black Label Music': 'LC 91766',
    'Catapult Music': 'LC 30315',
    'CDM MUSIC': 'LC 91765',
    'Dragon Gate Music': 'LC 95635',
    'Dronebox Audio Library': 'LC 101560',
    'Edition Klangidee': 'LC 91332',
    'Hungry Human': 'LC 104034',
    'Influence': 'LC 100335',
    'John Fulford Music': 'LC 95634',
    'Lemoncake Music': 'LC 37208',
    'Nordic Production Library': 'LC 91767',
    'Simple Things': 'LC 103591',
    'Swimming Pool': 'LC 70919',
    'The Diner': 'LC 29728',
    'The Hit House': 'LC 27260',
    'The Hit House Records': 'LC 26510',
    'The Nerve': 'LC 98597',
    'Tonosfera': 'LC 103550',
    'World Pop': 'LC 100539'
}

df['CODE: GVL Label Code'] = df['LIBRARY: Name'].map(gvl_codes)

columns_to_join = [
    'TRACK: Description',
    'TRACK: Genre',
    'TRACK: Instrumentation',
    'TRACK: Keywords',
    'TRACK: Mood',
    'TRACK: Music For',
    'TRACK: Genre_Ger',
    'TRACK: Instrumentation_Ger',
    'TRACK: Keywords_Ger',
    'TRACK: Mood_Ger',
    'TRACK: Music For_Ger',
    'TRACK: Version',
    'CODE: GVL Label Code'
]

df['COMMENT'] = (
    df[columns_to_join]
        .apply(lambda row: "; ".join(
            dict.fromkeys(
                str(x).strip()
                for x in row
                if pd.notna(x) and str(x).strip() != ""
            )
        ), axis=1)
)

def remove_duplicates_preserving_order(text):
    if not isinstance(text, str):
        return text

    # Split by semicolon
    parts = [p.strip() for p in text.split(';')]

    # We want to keep everything, but remove duplicates from the middle keywords
    # Assuming parts[0] is the description and parts[-1] is the LC code
    description = parts[0]
    lc_code = parts[-1]
    keywords = parts[1:-1]

    # Use dict.fromkeys to remove duplicates while keeping order
    seen = set()
    unique_keywords = []
    for kw in keywords:
        # Standardize for comparison (case-insensitive)
        standardized = kw.lower()
        if standardized not in seen:
            unique_keywords.append(kw)
            seen.add(standardized)

    # Reassemble: Description + unique keywords + LC code
    return '; '.join([description] + unique_keywords + [lc_code])

df['COMMENT'] = df['COMMENT'].apply(remove_duplicates_preserving_order)

########################
### FILENAMES REWORK ###
########################

# Create 'old_filename' by taking the first 25 chars and adding .mp3
df['old_filename'] = df['TRACK: Audio Filename'].str[:25] + '.mp3'

# Album codes standardization

# Regex pattern:
# ([a-zA-Z]+) captures the letters (e.g., BLM)
# \D* matches any non-digits (spaces, underscores, etc.)
# (\d+) captures the sequence of numbers (e.g., 184)
pattern = r'(?P<label>[a-zA-Z]+)\D*(?P<number>\d+)'

# Extract and format
extracted = df['ALBUM: Code'].str.extract(pattern)
df['ALBUM: Code'] = extracted['label'].str.upper() + '_' + extracted['number']

# Check for any failures to standardize
missing = df[df['ALBUM: Code'].isna()]
if not missing.empty:
    print(f"Warning: Found {len(missing)} rows that couldn't be standardized.")

# Create the enumeration (starting at 1) and pad to 3 digits
df['TRACK: Number'] = (
    df.groupby('ALBUM: Code').cumcount() + 1
).apply(lambda x: f'{x:03d}')

# Track titles to upper case
df['TRACK: Display Title'] = df['TRACK: Display Title'].str.upper()

def format_composers(row):
    composers = []
    # Iterate through the pairs (1 to 8)
    for i in range(1, 9):
        first = row.get(f'WRITER:{i}: First Name')
        last = row.get(f'WRITER:{i}: Last Name')

        # Check if they exist and are not NaN
        if pd.notna(first) and pd.notna(last):
            composers.append(f"{first} {last}")
        elif pd.notna(first):  # Case where only first name exists
            composers.append(first)
        elif pd.notna(last):  # Case where only last name exists
            composers.append(last)

    return "; ".join(composers)

df['Composer_String'] = df.apply(format_composers, axis=1)

# Build the final filename
df['new_filename'] = (
        df['ALBUM: Code'] + '_' +
        df['TRACK: Number'] + '_' +
        df['TRACK: Display Title'] + '_' +
        df['Composer_String'] + '.mp3'
)

df_filenames = df[['old_filename', 'new_filename']]

df_filenames.to_csv('br_file_rename2 update.csv', index=False)

df_Mp3tag = df[['new_filename', 'COMMENT']].sort_values('new_filename')

# A file for MP3tag program
df_Mp3tag.to_csv('br_keywords_Mp3tag.csv', index=False, header=None)

print(df_Mp3tag.shape, df_filenames.shape)