import pandas as pd

def load_movie_data():
    # Load Bollywood movie dataset from GitHub raw CSV URL
    url = 'https://raw.githubusercontent.com/devensinghbhagtani/Bollywood-Movie-Dataset/main/IMDB-Movie-Dataset(2023-1951).csv'
    try:
        df = pd.read_csv(url)
        # Select relevant columns and rename for consistency
        df = df[['movie_name', 'genre', 'overview']].dropna()
        df.columns = ['title', 'genres', 'overview']
        return df
    except Exception as e:
        print(f"Failed to load dataset from URL: {e}")
        # Fallback to small hardcoded dataset
        data = {
            'title': ['Dilwale Dulhania Le Jayenge', '3 Idiots', 'PK'],
            'genres': ['Comedy|Drama|Romance', 'Comedy|Drama', 'Comedy|Drama|Sci-Fi'],
            'overview': ['Raj and Simran meet during a trip to Europe and fall in love.',
                         'Two friends search for their long-lost companion.',
                         'An alien comes to Earth to study human religion.']
        }
        return pd.DataFrame(data)