#!/usr/bin/env python3
"""
BibTeX Verification Script
Checks references.bib entries against CrossRef API for accuracy.
"""

import re
import requests
import time
import json

def parse_bibtex(filepath):
    """Parse BibTeX file and extract entries with DOIs."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern to match BibTeX entries
    entry_pattern = r'@(\w+)\{([^,]+),([^@]*?)(?=\n@|\n%|\Z)'
    entries = []

    for match in re.finditer(entry_pattern, content, re.DOTALL):
        entry_type = match.group(1)
        cite_key = match.group(2).strip()
        fields_str = match.group(3)

        # Extract fields
        fields = {}
        field_pattern = r'(\w+)\s*=\s*[{"](.+?)[}"](?=,\s*\w+\s*=|\s*\}|\s*$)'
        for field_match in re.finditer(field_pattern, fields_str, re.DOTALL):
            field_name = field_match.group(1).lower()
            field_value = field_match.group(2).strip()
            # Clean up LaTeX formatting
            field_value = re.sub(r'[{}\\\'`"]', '', field_value)
            fields[field_name] = field_value

        entries.append({
            'type': entry_type,
            'key': cite_key,
            'fields': fields
        })

    return entries

def query_crossref(doi):
    """Query CrossRef API for DOI metadata."""
    url = f"https://api.crossref.org/works/{doi}"
    headers = {
        'User-Agent': 'BibTeX-Checker/1.0 (mailto:check@example.com)'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()['message']
        else:
            return None
    except Exception as e:
        return None

def compare_entry(bib_entry, crossref_data):
    """Compare BibTeX entry with CrossRef data."""
    discrepancies = []
    fields = bib_entry['fields']

    # Compare title
    if 'title' in fields and crossref_data.get('title'):
        bib_title = fields['title'].lower().strip()
        cr_title = crossref_data['title'][0].lower().strip() if crossref_data['title'] else ''
        # Remove common punctuation for comparison
        bib_title_clean = re.sub(r'[^\w\s]', '', bib_title)
        cr_title_clean = re.sub(r'[^\w\s]', '', cr_title)
        if bib_title_clean != cr_title_clean:
            discrepancies.append({
                'field': 'title',
                'bibtex': fields['title'],
                'crossref': crossref_data['title'][0] if crossref_data['title'] else 'N/A'
            })

    # Compare year
    if 'year' in fields:
        bib_year = fields['year']
        cr_year = None
        if 'published-print' in crossref_data:
            cr_year = str(crossref_data['published-print']['date-parts'][0][0])
        elif 'published-online' in crossref_data:
            cr_year = str(crossref_data['published-online']['date-parts'][0][0])
        elif 'created' in crossref_data:
            cr_year = str(crossref_data['created']['date-parts'][0][0])

        if cr_year and bib_year != cr_year:
            discrepancies.append({
                'field': 'year',
                'bibtex': bib_year,
                'crossref': cr_year
            })

    # Compare journal
    if 'journal' in fields and crossref_data.get('container-title'):
        bib_journal = fields['journal'].lower().strip()
        cr_journal = crossref_data['container-title'][0].lower().strip() if crossref_data['container-title'] else ''
        # Normalize common variations
        bib_journal_clean = re.sub(r'[^\w\s]', '', bib_journal)
        cr_journal_clean = re.sub(r'[^\w\s]', '', cr_journal)
        if bib_journal_clean != cr_journal_clean:
            discrepancies.append({
                'field': 'journal',
                'bibtex': fields['journal'],
                'crossref': crossref_data['container-title'][0] if crossref_data['container-title'] else 'N/A'
            })

    # Compare volume
    if 'volume' in fields and crossref_data.get('volume'):
        if fields['volume'] != crossref_data['volume']:
            discrepancies.append({
                'field': 'volume',
                'bibtex': fields['volume'],
                'crossref': crossref_data['volume']
            })

    # Compare pages
    if 'pages' in fields and crossref_data.get('page'):
        bib_pages = fields['pages'].replace('--', '-')
        cr_pages = crossref_data['page'].replace('--', '-')
        if bib_pages != cr_pages:
            discrepancies.append({
                'field': 'pages',
                'bibtex': fields['pages'],
                'crossref': crossref_data['page']
            })

    return discrepancies

def main():
    bib_path = 'latex/references.bib'
    entries = parse_bibtex(bib_path)

    print(f"Found {len(entries)} BibTeX entries\n")
    print("=" * 80)
    print("CHECKING ENTRIES AGAINST CROSSREF")
    print("=" * 80)

    entries_with_doi = [e for e in entries if 'doi' in e['fields']]
    entries_without_doi = [e for e in entries if 'doi' not in e['fields']]

    print(f"\nEntries with DOI: {len(entries_with_doi)}")
    print(f"Entries without DOI: {len(entries_without_doi)}")

    if entries_without_doi:
        print("\n--- Entries WITHOUT DOI (cannot verify) ---")
        for e in entries_without_doi:
            print(f"  - {e['key']}: {e['fields'].get('title', 'No title')[:60]}...")

    print("\n" + "=" * 80)
    print("VERIFYING ENTRIES WITH DOI...")
    print("=" * 80 + "\n")

    all_discrepancies = []
    verified_count = 0
    error_count = 0

    for i, entry in enumerate(entries_with_doi):
        doi = entry['fields']['doi']
        print(f"[{i+1}/{len(entries_with_doi)}] Checking {entry['key']}...", end=' ')

        crossref_data = query_crossref(doi)

        if crossref_data:
            discrepancies = compare_entry(entry, crossref_data)
            if discrepancies:
                print(f"DISCREPANCIES FOUND")
                all_discrepancies.append({
                    'key': entry['key'],
                    'doi': doi,
                    'discrepancies': discrepancies
                })
            else:
                print("OK")
                verified_count += 1
        else:
            print(f"ERROR: Could not fetch DOI")
            error_count += 1

        # Rate limiting - be polite to CrossRef API
        time.sleep(0.5)

    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total entries: {len(entries)}")
    print(f"Entries with DOI: {len(entries_with_doi)}")
    print(f"Entries without DOI: {len(entries_without_doi)}")
    print(f"Verified (no issues): {verified_count}")
    print(f"With discrepancies: {len(all_discrepancies)}")
    print(f"API errors: {error_count}")

    if all_discrepancies:
        print("\n" + "=" * 80)
        print("DETAILED DISCREPANCIES")
        print("=" * 80)
        for item in all_discrepancies:
            print(f"\n{item['key']} (DOI: {item['doi']})")
            for d in item['discrepancies']:
                print(f"  {d['field'].upper()}:")
                print(f"    BibTeX:   {d['bibtex']}")
                print(f"    CrossRef: {d['crossref']}")

if __name__ == '__main__':
    main()
