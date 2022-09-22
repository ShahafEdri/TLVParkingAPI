from googletrans import Translator


if __name__ == "__main__":
    translator = Translator()
    translation = translator.translate('checking google translate application', src='iw', dest='en')
    print(translation.origin, ' -> ', translation.text)
