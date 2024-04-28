import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

class Preprocess_text:
    def __init__(self, text_list) -> None:
        self.preprocessed = self.get_lemmatized(
            self.to_lowercase(
                self.remove_stopwords(
                    self.remove_punc(text_list))))

    # REMOVE PUNCTUATION
    def remove_punc(self, body_texts):
        X_no_punc = []
        for sentence in body_texts:
            # Remove all punctuations except for '.'
            remove = string.punctuation.replace('.', '')
            remove = remove.replace('/', '')
            remove = remove.replace('-', '')
            remove = remove.replace(':', '')
            X_no_punc.append(sentence.translate(
                sentence.maketrans('', '', remove)))
        return X_no_punc

    # REMOVE STOPWORDS
    def remove_stopwords(self, text_list):
        # Removing stopwords from dataset.
        # Tokenizing data set.
        X_tokenized = []
        for sentence in text_list:
            X_tokenized.append(word_tokenize(sentence))

        X_no_stopwords = []
        stop_words = set(stopwords.words('english'))
        for word_list in X_tokenized:
            filtered_words = [
                word for word in word_list if word.lower() not in stop_words]
            X_no_stopwords.append(" ".join(filtered_words))
        return X_no_stopwords

    # CONVERT TO LOWERCASE
    def to_lowercase(self, text_list):
        X_lower = []
        for sentence in text_list:
            X_lower.append(sentence.lower())
        return X_lower

    # LEMMATISATION
    def get_lemmatized(self, text_list):
        lemmatizer = WordNetLemmatizer()
        X_preprocessed = []
        for sentence in text_list:
            tokens = word_tokenize(sentence)
            lemmatized_sentence = " ".join(
                [lemmatizer.lemmatize(word) for word in tokens])
            X_preprocessed.append(lemmatized_sentence)
        return X_preprocessed