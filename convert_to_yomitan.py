#!/usr/bin/env python3
"""
Convert toki pona CSV dictionaries to Yomitan format and zip them.
"""

import csv
import json
import os
import zipfile
from pathlib import Path


def get_language_from_filename(filename):
    """Extract target language from CSV filename."""
    # Remove .csv extension and split by hyphens
    parts = filename.replace('.csv', '').split('-')
    if len(parts) >= 4 and parts[0] == 'toki' and parts[1] == 'pona' and parts[2] == 'to':
        return parts[3]
    return None


def create_yomitan_index(title, language):
    """Create the index.json file for Yomitan dictionary."""
    return {
        "title": title,
        "revision": "1.0.0",
        "sequenced": True,
        "format": 3,
        "version": 3,
        "author": "Toki Pona Dictionary Converter",
        "url": "",
        "description": f"Toki Pona to {language.title()} dictionary",
        "attribution": "",
        "sourceLanguage": "toki-pona",
        "targetLanguage": language,
        "prefixWildcardsSupported": False,
        "tags": {}
    }


def convert_csv_to_yomitan(csv_file_path, output_dir):
    """Convert a single CSV file to Yomitan format."""
    filename = os.path.basename(csv_file_path)
    language = get_language_from_filename(filename)
    
    if not language:
        print(f"Skipping {filename} - couldn't determine target language")
        return None
    
    # Create output directory for this dictionary
    dict_dir = output_dir / f"toki-pona-to-{language}"
    dict_dir.mkdir(exist_ok=True)
    
    # Read CSV and convert to Yomitan term bank format
    terms = []
    
    with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            word = row['word'].strip()
            definition = row['definition'].strip()
            
            # Yomitan term format: [expression, reading, definition_tags, rules, score, definitions, sequence, term_tags]
            term_entry = [
                word,           # expression (the toki pona word)
                "",             # reading (empty for toki pona)
                "",             # definition_tags
                "",             # rules
                0,              # score
                [definition],   # definitions array
                0,              # sequence
                ""              # term_tags
            ]
            terms.append(term_entry)
    
    # Write term bank file
    term_bank_file = dict_dir / "term_bank_1.json"
    with open(term_bank_file, 'w', encoding='utf-8') as f:
        json.dump(terms, f, ensure_ascii=False, separators=(',', ':'))
    
    # Write index file
    index_data = create_yomitan_index(f"Toki Pona to {language.title()}", language)
    index_file = dict_dir / "index.json"
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(index_data, f, ensure_ascii=False, indent=2)
    
    return dict_dir


def zip_dictionary(dict_dir):
    """Create a zip file for the dictionary."""
    zip_path = dict_dir.with_suffix('.zip')
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in dict_dir.iterdir():
            if file_path.is_file():
                zipf.write(file_path, file_path.name)
    
    return zip_path


def main():
    """Main function to process all CSV files."""
    dictionaries_dir = Path("dictionaries")
    output_dir = Path("yomitan_dictionaries")
    output_dir.mkdir(exist_ok=True)
    
    # Find all toki-pona-to-*.csv files
    csv_files = list(dictionaries_dir.glob("toki-pona-to-*.csv"))
    
    if not csv_files:
        print("No toki-pona-to-*.csv files found in dictionaries/ directory")
        return
    
    print(f"Found {len(csv_files)} dictionary files to convert:")
    
    zip_files = []
    
    for csv_file in csv_files:
        print(f"Converting {csv_file.name}...")
        
        dict_dir = convert_csv_to_yomitan(csv_file, output_dir)
        if dict_dir:
            zip_path = zip_dictionary(dict_dir)
            zip_files.append(zip_path)
            print(f"  Created: {zip_path}")
            
            # Clean up the directory after zipping
            for file_path in dict_dir.iterdir():
                file_path.unlink()
            dict_dir.rmdir()
    
    print(f"\nConversion complete! Created {len(zip_files)} Yomitan dictionary files:")
    for zip_file in zip_files:
        print(f"  {zip_file}")


if __name__ == "__main__":
    main()
