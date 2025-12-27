def generate_markdown(header, items, totals):
    md = []

    md.append("# Invoice\n")

    if header:
        md.append("## Details\n")
        for h in header:
            md.append(f"- {h}")
        md.append("")

    if items:
        md.append("## Items\n")
        for item in items:
            md.append(f"- {item}")
        md.append("")

    if totals:
        md.append("## Summary\n")
        for t in totals:
            md.append(f"- {t}")
        md.append("")

    return "\n".join(md)
