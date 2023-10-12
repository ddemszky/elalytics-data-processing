from deep_translator import GoogleTranslator

# translate text to spanish
def translate_to_spanish(text):
    """Translate text to spanish
    Args:
        text (str): The text to be translated
    Returns:
        str: The translated text
    """
    translated_text = GoogleTranslator(source='english', target='spanish').translate(text)
    return translated_text