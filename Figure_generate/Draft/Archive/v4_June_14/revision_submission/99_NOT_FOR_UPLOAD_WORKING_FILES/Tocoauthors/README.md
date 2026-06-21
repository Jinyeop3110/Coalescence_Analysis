# To Coauthors: Revision Submission PDF Package

This folder documents the local recipe used to make the coauthor-facing revision PDF ZIP.

## Output ZIP

The current ZIP is:

`../upload_extras/Tocoauthors_revision_submission_pdfs.zip`

It contains:

1. `01_cover_letter_revision.pdf`
2. `02_main_revised.pdf`
3. `03_supplementary_revised.pdf`
4. `04_response_to_reviewers.pdf`

## Source Files

The ZIP was made from the active compiled files:

- `../../latex/cover_letter_revision.pdf`
- `../../latex/main.pdf`
- `../../latex/supplementary.pdf`
- `../../latex/revision/response_letter.pdf`

## Rebuild Recipe

From the repository root:

```bash
out="Figure_generate/Draft/v4/revision_submission/upload_extras/Tocoauthors_revision_submission_pdfs.zip"
tmpdir=$(mktemp -d)
cp "Figure_generate/Draft/v4/latex/cover_letter_revision.pdf" "$tmpdir/01_cover_letter_revision.pdf"
cp "Figure_generate/Draft/v4/latex/main.pdf" "$tmpdir/02_main_revised.pdf"
cp "Figure_generate/Draft/v4/latex/supplementary.pdf" "$tmpdir/03_supplementary_revised.pdf"
cp "Figure_generate/Draft/v4/latex/revision/response_letter.pdf" "$tmpdir/04_response_to_reviewers.pdf"
rm -f "$out"
(cd "$tmpdir" && zip -q -9 "$OLDPWD/$out" 01_cover_letter_revision.pdf 02_main_revised.pdf 03_supplementary_revised.pdf 04_response_to_reviewers.pdf)
rm -rf "$tmpdir"
unzip -l "$out"
```

## Notes

- This ZIP is for coauthor review or easy sharing of the core revision PDFs.
- The Reporting Summary is not included because the local copy is still marked `NEEDS_COMPLETION`.
- Source data, data availability links, and code availability materials are separate submission-preparation items.
