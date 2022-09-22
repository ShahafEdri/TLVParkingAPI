from googletrans import Translator

# print(googletrans.LANGUAGES)

from google_utils import get_google_api_key
# translator = Translator(key)


def translate_text(text, target='iw'):
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    import six
    from google.cloud import translate_v2 as translate

    translate_client = translate.Client()

    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, target_language=target)

    print(u"Text: {}".format(result["input"]))
    print(u"Translation: {}".format(result["translatedText"]))
    print(u"Detected source language: {}".format(result["detectedSourceLanguage"]))


# res = translator.translate('check',dest='en', src='iw')
if __name__ == "__main__":
    # translation = translator.translate('ארלוזרוב', src='iw', dest='en')
    translation = translate_text('ארלוזרוב')
    # print(translation.origin, ' -> ', translation.text)
