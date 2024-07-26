from src.data.load_data import keypo_textlist
from src.data.preprocess import preprocess_texts

def main():
    text_list = keypo_textlist()
    print(text_list)
    preprocessed_text = preprocess_texts(text_list)
    print(preprocessed_text)


if __name__ == "__main__":
    main()