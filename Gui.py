import tkinter as tk
from tkinter import messagebox
from Model import MovieRecommender
from Data import load_movie_data

class MovieRecommendationGUI:
    def __init__(self, root, recommender):
        self.root = root
        self.recommender = recommender
        self.root.title("Movie Recommendation System")

        self.label = tk.Label(root, text="Enter a movie title:")
        self.label.pack(pady=10)

        self.entry = tk.Entry(root, width=50)
        self.entry.pack(pady=5)

        self.button = tk.Button(root, text="Get Recommendations", command=self.get_recommendations)
        self.button.pack(pady=10)

        self.result_label = tk.Label(root, text="Recommended Movies:")
        self.result_label.pack(pady=10)

        self.result_text = tk.Text(root, height=10, width=60)
        self.result_text.pack(pady=5)

    def get_recommendations(self):
        movie_title = self.entry.get()
        if not movie_title:
            messagebox.showwarning("Input Error", "Please enter a movie title.")
            return
        recommendations = self.recommender.recommend(movie_title)
        self.result_text.delete(1.0, tk.END)
        if recommendations:
            for movie in recommendations:
                self.result_text.insert(tk.END, movie + "\n")
        else:
            self.result_text.insert(tk.END, "No recommendations found for this movie.")

def run_gui():
    movies_df = load_movie_data()
    recommender = MovieRecommender(movies_df)
    root = tk.Tk()
    app = MovieRecommendationGUI(root, recommender)
    root.mainloop()

if __name__ == "__main__":
    run_gui()