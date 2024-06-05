import streamlit as st
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os

# Function to convert speech to text
def speech_to_text(language):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        st.info(f"Speak in {language}...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language=language)
        st.write("You said:", text)
        return text
    except sr.UnknownValueError:
        st.error("Sorry, I couldn't understand what you said.")
        return ""
    except sr.RequestError:
        st.error("Sorry, unable to access Google Speech Recognition service.")
        return ""

# Function to translate text
def translate_text(text, dest_lang):
    translator = Translator()
    translation = translator.translate(text, dest=dest_lang)
    return translation.text

# Function to convert text to speech
def text_to_speech(text, lang):
    tts = gTTS(text=text, lang=lang)
    tts.save("output.mp3")
    st.audio("output.mp3")
    os.remove("output.mp3")

# Function to get language code from language name
def get_language_code(language):
    lang_codes = {
        'af': 'afrikaans', 'sq': 'albanian', 'am': 'amharic', 'ar': 'arabic', 'hy': 'armenian',
        'az': 'azerbaijani', 'eu': 'basque', 'be': 'belarusian', 'bn': 'bengali', 'bs': 'bosnian',
        'bg': 'bulgarian', 'ca': 'catalan', 'ceb': 'cebuano', 'ny': 'chichewa', 'zh-cn': 'chinese (simplified)',
        'zh-tw': 'chinese (traditional)', 'co': 'corsican', 'hr': 'croatian', 'cs': 'czech', 'da': 'danish',
        'nl': 'dutch', 'en': 'english', 'eo': 'esperanto', 'et': 'estonian', 'tl': 'filipino', 'fi': 'finnish',
        'fr': 'french', 'fy': 'frisian', 'gl': 'galician', 'ka': 'georgian', 'de': 'german', 'el': 'greek',
        'gu': 'gujarati', 'ht': 'haitian creole', 'ha': 'hausa', 'haw': 'hawaiian', 'he': 'hebrew', 'hi': 'hindi',
        'hmn': 'hmong', 'hu': 'hungarian', 'is': 'icelandic', 'ig': 'igbo', 'id': 'indonesian', 'ga': 'irish',
        'it': 'italian', 'ja': 'japanese', 'jw': 'javanese', 'kn': 'kannada', 'kk': 'kazakh', 'km': 'khmer',
        'ko': 'korean', 'ku': 'kurdish (kurmanji)', 'ky': 'kyrgyz', 'lo': 'lao', 'la': 'latin', 'lv': 'latvian',
        'lt': 'lithuanian', 'lb': 'luxembourgish', 'mk': 'macedonian', 'mg': 'malagasy', 'ms': 'malay',
        'ml': 'malayalam', 'mt': 'maltese', 'mi': 'maori', 'mr': 'marathi', 'mn': 'mongolian', 'my': 'myanmar (burmese)',
        'ne': 'nepali', 'no': 'norwegian', 'or': 'odia', 'ps': 'pashto', 'fa': 'persian', 'pl': 'polish',
        'pt': 'portuguese', 'pa': 'punjabi', 'ro': 'romanian', 'ru': 'russian', 'sm': 'samoan', 'gd': 'scots gaelic',
        'sr': 'serbian', 'st': 'sesotho', 'sn': 'shona', 'sd': 'sindhi', 'si': 'sinhala', 'sk': 'slovak',
        'sl': 'slovenian', 'so': 'somali', 'es': 'spanish', 'su': 'sundanese', 'sw': 'swahili', 'sv': 'swedish',
        'tg': 'tajik', 'ta': 'tamil', 'te': 'telugu', 'th': 'thai', 'tr': 'turkish', 'uk': 'ukrainian', 'ur': 'urdu',
        'ug': 'uyghur', 'uz': 'uzbek', 'vi': 'vietnamese', 'cy': 'welsh', 'xh': 'xhosa', 'yi': 'yiddish', 'yo': 'yoruba',
        'zu': 'zulu'
    }
    return lang_codes.get(language.lower(), None)

# Streamlit app
st.title("Real-Time Speech-to-Speech Translation")

input_language = st.text_input("Enter input language code (e.g., 'en' for English):").lower()
output_language = st.text_input("Enter output language code (e.g., 'es' for Spanish):").lower()

if st.button("Translate"):
    input_lang_name = get_language_code(input_language)
    output_lang_name = get_language_code(output_language)

    if not input_lang_name:
        st.error("Invalid input language code.")
    elif not output_lang_name:
        st.error("Invalid output language code.")
    else:
        input_text = speech_to_text(input_language)
        if input_text:
            translated_text = translate_text(input_text, output_language)
            st.write(f"Translated text ({output_lang_name}):", translated_text)
            text_to_speech(translated_text, output_language)
