#!/usr/bin/env python3
"""
Split multilanguage Toki Pona dictionary into separate CSV files.
Creates one CSV per language with columns: word, definition
"""

import csv
import os

def split_dictionary():
    input_file = 'dictionaries/multilanguage-toki-pona-dictionary.csv'
    output_dir = 'dictionaries'
    
    # Read the input CSV
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)  # Get header row
        rows = list(reader)
    
    # Find column indices
    tok_col = headers.index('tok')  # Toki Pona column
    
    # Language codes and their full names for output files
    languages = {
        'de': 'german',
        'eo': 'esperanto', 
        'fr': 'french',
        'ru': 'russian',
        'sk': 'slovak',
        'en': 'english',
        'cs': 'czech',
        'it': 'italian',
        'id': 'indonesian',
        'nl': 'dutch',
        'es': 'spanish',
        'pl': 'polish',
        'tr': 'turkish',
        'zh': 'chinese',
        'pt': 'portuguese'
    }
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Process each language
    for lang_code, lang_name in languages.items():
        if lang_code not in headers:
            print(f"Warning: Language code '{lang_code}' not found in headers")
            continue
            
        lang_col = headers.index(lang_code)
        output_file = os.path.join(output_dir, f'toki-pona-to-{lang_name}.csv')
        
        with open(output_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['word', 'definition'])  # Header
            
            for row in rows:
                if len(row) > max(tok_col, lang_col):
                    toki_word = row[tok_col].strip()
                    definition = row[lang_col].strip()
                    
                    # Skip empty entries
                    if toki_word and definition:
                        writer.writerow([toki_word, definition])
        
        print(f"Created: {output_file}")

if __name__ == '__main__':
    split_dictionary()
