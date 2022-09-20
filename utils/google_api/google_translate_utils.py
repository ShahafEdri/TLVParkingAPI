from googletrans import Translator

# print(googletrans.LANGUAGES)

translator = Translator()

# res = translator.translate('check',dest='en', src='iw')
if __name__=="__main__":
    translation = translator.translate('ארלוזרוב', src='iw', dest='en')
    print(translation.origin, ' -> ', translation.text)
