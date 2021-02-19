import pandas as pd
import re
import string
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
from nltk.tokenize import WordPunctTokenizer, RegexpTokenizer

STOPWORDS = stopwords.words('english')


class DatasetCleaner():
    """This class is used to clean text taken from various sources"""
    
    def __init__(self, data_path, text_column):
        """This function initializes the class with necessary class variables."""

        super(DatasetCleaner,self).__init__()
        self.data_path = data_path
        self.text_column = text_column
        self.word_punct_tokenizer = WordPunctTokenizer()
        self.regex_tokenizer = RegexpTokenizer(r"\w+")

    def _text_processing(self, text):
        no_punctuation = [char for char in text if char not in string.punctuation]
        no_punctuation = ''.join(no_punctuation)
        return ' '.join([word for word in no_punctuation.split() if word.lower() not in STOPWORDS])

    def tweet_cleaner(self):
        """This is the driving function that is used for cleaning text by removing special characters, unicodes,
           stopwords etc."""
        
        read_data = self._read_data()

        username_pattern = r'@[A-Za-z0-9]+'
        email_pattern = r'https?://[A-Za-z0-9./%_]+'
        match_pattern = r'|'.join((username_pattern, email_pattern))
        
        read_data = read_data[[self.text_column]]

        read_data['stripped'] = read_data[self.text_column].apply(lambda x: re.sub(match_pattern, '', str(x)))
        
        try:
            read_data['clean'] = read_data['stripped'].apply(lambda x: x.decode("utf-8-sig").replace(u"\ufffd", "?"))
        except:
            read_data['clean'] = read_data['stripped']
            
        read_data['processed'] = read_data['clean'].apply(self._text_processing)
        
        return read_data

    def _read_data(self):
        read_data = pd.read_csv(self.data_path, lineterminator='\n')

        return read_data




