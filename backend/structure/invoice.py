from .lines import is_price

def is_header_line(text):
    keywords = [
        "invoice",
        "issued",
        "account",
        "date",
        "pay to",
        "invoice no",
    ]
    t = text.lower()
    return any(k in t for k in keywords)


def is_total_line(text):
    keywords = ["total", "subtotal", "tax", "amount"]
    t = text.lower()
    return any(k in t for k in keywords)


def is_item_line(text):
    """
    Invoice item lines usually:
    - contain letters (description)
    - contain a price-like token
    """
    if not any(c.isalpha() for c in text):
        return False

    return any(is_price(token) for token in text.split())


def build_invoice_sections(lines):
    header = []
    items = []
    totals = []

    for line in lines:
        if is_total_line(line):
            totals.append(line)
        elif is_item_line(line):
            items.append(line)
        elif is_header_line(line):
            header.append(line)

    return header, items, totals
