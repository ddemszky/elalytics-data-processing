from deep_translator import GoogleTranslator

# translate text to spanish
def translate_to_spanish(text):
    translated_text = GoogleTranslator(source='english', target='spanish').translate(text)
    return translated_text