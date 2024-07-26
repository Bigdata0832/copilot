import re
from concurrent.futures import ThreadPoolExecutor

def preprocess_text(text):
    # Remove icon and undesired characters except desired punctuation
    text = re.sub(r'[^\w\s.,/*，。！？\-:]', '', text)
    
    # Remove newline characters
    text = text.replace('\n', ' ')
    
    # Handle spaces and punctuation
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'，+', '，', text)
    text = re.sub(r'。+', '。', text)
    text = re.sub(r'！+', '！', text)
    text = re.sub(r'？+', '？', text)
    text = re.sub(r'/+', '/', text)
    text = re.sub(r'\*+', '*', text)
    text = re.sub(r'\.+', '.', text)
    text = re.sub(r'\-+', '-', text)
    text = re.sub(r'\:+', ':', text)
    
    # Remove network link
    text = re.sub(r'http\S+', '', text)
    
    return text

def preprocess_texts(text_list):
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(preprocess_text, text_list))
    return results