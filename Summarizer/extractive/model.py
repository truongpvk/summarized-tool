from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
import numpy as np


from langdetect import detect
import nltk
import re
import langcodes
nltk.download('punkt_tab', quiet=True, download_dir="../../venv/nltk_data")
nltk.data.path.append("../../venv/nltk_data")

def code_to_language_name(code: str) -> str:
    try:
        return langcodes.get(code).display_name().lower()
    except:
        return None

def split_sentence(text):
    try:
        lang = detect(text)[:2]
    except:
        return [text]

    if lang in [
        'cs',
        'nl',
        'en',
        'fr', 
        'de',
        'it',
        'pt',
        'ru',
        'es',
        'tr',
    ]:
        return nltk.sent_tokenize(text, language=code_to_language_name(lang))

    elif lang == 'vi':
        return [s.strip() for s in text.replace("!", ".").replace("?", ".").split(".") if s.strip()]

    elif lang == 'zh': # Chinese
        import re
        return re.split(r'(。|！|\!|\.|？|\?)', text)

    elif lang == 'ar': # Arabic
        return [s.strip() for s in text.replace("؟", ".").replace("!", ".").split(".") if s.strip()]

    else: # Defautl
        return [s.strip() for s in text.replace("!", ".").replace("?", ".").split(".") if s.strip()]

def extract_top_n_sentences(text: str, n: int=3) -> str:
    sentences = split_sentence(text)
    
    if len(sentences) <= n:
        return f"This document is not long enough to summary (Document: {len(sentences)} sentences but need to extract {n} sentences)"
    
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(sentences)
    
    svd = TruncatedSVD(n_components=1)
    svd.fit(X)
    
    scores = np.linalg.norm(svd.transform(X), axis=1)

    top_n_indices = np.argsort(scores)[::-1][:n]
    summary = [sentences[i] for i in sorted(top_n_indices)]

    return ". ".join(summary)