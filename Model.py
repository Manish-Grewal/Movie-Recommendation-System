import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

class MovieRecommender:
    def __init__(self, movies_df: pd.DataFrame):
        self.movies_df = movies_df.copy()
        self.tfidf_matrix = None
        self.indices = None
        self.stop_words = set(stopwords.words('english'))
        self.stemmer = PorterStemmer()
        self._prepare()

    def _preprocess_text(self, text):
        # Lowercase
        text = text.lower()
        # Remove punctuation and non-alphabetic characters
        text = re.sub(r'[^a-z\s]', '', text)
        # Tokenize and remove stopwords, then stem
        tokens = [self.stemmer.stem(word) for word in text.split() if word not in self.stop_words]
        return ' '.join(tokens)

    def _prepare(self):
        # Combine genres and overview for content-based filtering
        self.movies_df['content'] = self.movies_df['genres'].fillna('') + ' ' + self.movies_df['overview'].fillna('')
        # Preprocess the combined content
        self.movies_df['content'] = self.movies_df['content'].apply(self._preprocess_text)
        # Initialize TF-IDF Vectorizer with n-grams and max features
        tfidf = TfidfVectorizer(stop_words='english', ngram_range=(1,2), max_features=5000)
        # Fit and transform the content
        self.tfidf_matrix = tfidf.fit_transform(self.movies_df['content'])
        # Create a reverse map of indices and movie titles
        self.indices = pd.Series(self.movies_df.index, index=self.movies_df['title']).drop_duplicates()

    def recommend(self, title, top_n=5):
        if title not in self.indices:
            return []
        idx = self.indices[title]
        # Compute cosine similarity between the movie and all others
        cosine_similarities = linear_kernel(self.tfidf_matrix[idx], self.tfidf_matrix).flatten()
        # Get the indices of the top_n most similar movies (excluding itself)
        similar_indices = cosine_similarities.argsort()[-top_n-1:-1][::-1]
        # Return the titles of the recommended movies
        return self.movies_df['title'].iloc[similar_indices].tolist()