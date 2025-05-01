def sanitize_sheet_name(name: str) -> str:
    invalid_chars = ['/', '\\', '*', '?', ':', '[', ']']
    for char in invalid_chars:
        name = name.replace(char, '')
    return name[:31]  # Excelのシート名は31文字以内
