import re

EXPECTED_FIELDS = {
    "title": [
        "title", "book title", "name", "book name", "book_title",
        "title name", "booktitle", "bookname"
    ],
    "author": [
        "author", "writer", "author name", "written by", "creator",
        "author_name", "book author", "book_writer"
    ],
    "isbn": [
        "isbn", "isbn code", "isbn-13", "isbn13", "isbn_13",
        "book id", "book code", "identifier", "book_identifier"
    ]
}

def normalize(header):
    return re.sub(r'[^a-z0-9]', '', header.lower())

def map_headers(header_row):
    normalized_headers = {normalize(h): h for h in header_row}
    field_map = {}

    for key, aliases in EXPECTED_FIELDS.items():
        for alias in aliases:
            norm_alias = normalize(alias)
            if norm_alias in normalized_headers:
                field_map[key] = normalized_headers[norm_alias]
                break

    return field_map
