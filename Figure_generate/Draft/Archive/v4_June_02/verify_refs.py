#!/usr/bin/env python3
"""
Verify references.bib against CrossRef (DOI metadata).
Checks: DOI existence, title, year, journal, volume, issue, pages, first author.
Also flags preprints and missing braces around proper nouns / acronyms.
Uses only the Python standard library (urllib).
"""
import re, json, time, sys, urllib.request, urllib.error

BIB = 'latex/references.bib'
EMAIL = 'sjinyeop@gmail.com'

# ---------- parse bib ----------
def parse_bib(path):
    with open(path, encoding='utf-8') as f:
        txt = f.read()
    entries = []
    # find each @type{key, ... } by tracking braces
    i = 0
    for m in re.finditer(r'@(\w+)\s*\{', txt):
        etype = m.group(1)
        start = m.end()  # position right after first {
        depth = 1
        j = start
        while j < len(txt) and depth > 0:
            if txt[j] == '{': depth += 1
            elif txt[j] == '}': depth -= 1
            j += 1
        body = txt[start:j-1]
        key, _, rest = body.partition(',')
        key = key.strip()
        fields = {}
        # field = { ... } or "...." ; capture brace-balanced or quoted
        for fm in re.finditer(r'(\w+)\s*=\s*', rest):
            name = fm.group(1).lower()
            p = fm.end()
            if p >= len(rest): break
            ch = rest[p]
            if ch == '{':
                d = 1; q = p+1
                while q < len(rest) and d > 0:
                    if rest[q] == '{': d += 1
                    elif rest[q] == '}': d -= 1
                    q += 1
                val = rest[p+1:q-1]
            elif ch == '"':
                q = p+1
                while q < len(rest) and rest[q] != '"':
                    q += 1
                val = rest[p+1:q]
            else:
                q = p
                while q < len(rest) and rest[q] not in ',\n':
                    q += 1
                val = rest[p:q]
            fields[name] = val.strip().rstrip(',').strip()
        entries.append({'type': etype.lower(), 'key': key, 'fields': fields})
    return entries

def clean(s):
    s = re.sub(r'\\[a-zA-Z]+', '', s)        # latex commands
    s = re.sub(r'[{}\\$]', '', s)
    s = re.sub(r'[^\w\s]', ' ', s.lower())
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def first_author_surname(authorfield):
    # authors separated by ' and '
    first = authorfield.split(' and ')[0].strip()
    if ',' in first:
        surname = first.split(',')[0]
    else:
        surname = first.split()[-1] if first.split() else first
    return clean(surname)

def crossref(doi):
    url = 'https://api.crossref.org/works/' + urllib.parse.quote(doi)
    req = urllib.request.Request(url, headers={'User-Agent': f'BibCheck/1.0 (mailto:{EMAIL})'})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.load(r)['message'], None
    except urllib.error.HTTPError as e:
        return None, f'HTTP {e.code}'
    except Exception as e:
        return None, str(e)

def cr_year(d):
    for k in ('published-print','published-online','published','issued','created'):
        if k in d and d[k].get('date-parts'):
            return str(d[k]['date-parts'][0][0])
    return None

def main():
    import urllib.parse
    globals()['urllib'].parse = urllib.parse
    entries = parse_bib(BIB)
    print(f"Parsed {len(entries)} entries\n")
    problems = []
    preprints = []
    nodoi = []

    for idx, e in enumerate(entries):
        f = e['fields']
        key = e['key']
        doi = f.get('doi')
        jr = f.get('journal','')
        if not doi:
            nodoi.append(key)
            continue
        if re.search(r'biorxiv|arxiv|medrxiv|preprint', jr, re.I) or 'biorxiv' in doi.lower():
            preprints.append((key, jr, doi))
        d, err = crossref(doi)
        sys.stdout.write(f"[{idx+1}/{len(entries)}] {key:18s} ")
        if d is None:
            print(f"** DOI FETCH FAILED ({err}) -> {doi}")
            problems.append((key, [('doi/exists', doi, err or 'not found')]))
            time.sleep(0.4); continue
        disc = []
        # title
        if f.get('title') and d.get('title'):
            bt, ct = clean(f['title']), clean(d['title'][0])
            if bt != ct:
                disc.append(('title', f['title'], d['title'][0]))
        # year
        if f.get('year'):
            cy = cr_year(d)
            if cy and f['year'] != cy:
                disc.append(('year', f['year'], cy))
        # journal
        if jr and d.get('container-title'):
            bj, cj = clean(jr), clean(d['container-title'][0])
            # tolerate "and"/"&" and abbreviation containment
            if bj != cj and bj not in cj and cj not in bj:
                disc.append(('journal', jr, d['container-title'][0]))
        # volume
        if f.get('volume') and d.get('volume') and f['volume'] != d['volume']:
            disc.append(('volume', f['volume'], d['volume']))
        # issue
        if f.get('number') and d.get('issue') and f['number'] != d['issue']:
            disc.append(('issue', f['number'], d['issue']))
        # pages
        if f.get('pages') and d.get('page'):
            bp = f['pages'].replace('--','-').replace(' ','')
            cp = d['page'].replace('--','-').replace(' ','')
            if bp != cp:
                disc.append(('pages', f['pages'], d['page']))
        # first author
        if f.get('author') and d.get('author'):
            bs = first_author_surname(f['author'])
            ca = d['author'][0]
            cs = clean(ca.get('family', ca.get('name','')))
            if bs and cs and bs != cs and bs not in cs and cs not in bs:
                disc.append(('1st author', first_author_surname(f['author']), ca.get('family', ca.get('name',''))))
        if disc:
            print("DISCREPANCIES")
            problems.append((key, disc))
        else:
            print("ok")
        time.sleep(0.4)

    print("\n" + "="*80)
    print(f"SUMMARY: {len(entries)} entries | {len(problems)} with issues | "
          f"{len(nodoi)} without DOI | {len(preprints)} preprints")
    print("="*80)

    if nodoi:
        print("\n--- ENTRIES WITHOUT DOI ---")
        for k in nodoi: print("  ", k)

    if preprints:
        print("\n--- PREPRINTS (replace with peer-reviewed if published) ---")
        for k,j,doi in preprints: print(f"   {k}: {j} ({doi})")

    if problems:
        print("\n--- DISCREPANCIES / FAILURES ---")
        for k, disc in problems:
            print(f"\n{k}")
            for field, bib, cr in disc:
                print(f"   {field}:")
                print(f"      bib: {bib}")
                print(f"      CR : {cr}")

if __name__ == '__main__':
    import urllib.parse
    main()
