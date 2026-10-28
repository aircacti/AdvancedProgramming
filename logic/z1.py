def is_palindrome(text: str) -> bool:
    return text.lower().replace(" ", "") == text[::-1].lower().replace(" ", "")
