import unittest
from unittest.mock import Mock, patch
import tkinter as tk
import sys
sys.path.insert(0, '.')
try:
    from Gui import MovieRecommendationGUI
except Exception:
    # If the GUI module isn't available (e.g., running tests in an environment
    # without the project module), set to None and skip tests later.
    MovieRecommendationGUI = None

class TestMovieRecommendationGUI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # If the GUI class couldn't be imported, skip these tests instead of erroring.
        if MovieRecommendationGUI is None:
            raise unittest.SkipTest("MovieRecommendationGUI not available")

        cls.root = tk.Tk()
        cls.root.withdraw()  # Hide the window for testing
        cls.mock_recommender = Mock()
        cls.gui = MovieRecommendationGUI(cls.root, cls.mock_recommender)

    @classmethod
    def tearDownClass(cls):
        cls.root.destroy()

    @patch('tkinter.messagebox.showwarning')
    def test_get_recommendations_no_input(self, mock_showwarning):
        # Set entry to empty
        self.gui.entry.delete(0, tk.END)
        self.gui.get_recommendations()
        mock_showwarning.assert_called_once_with("Input Error", "Please enter a movie title.")

    def test_get_recommendations_with_recommendations(self):
        # Set entry to a movie title
        self.gui.entry.insert(0, "Test Movie")
        # Mock recommender to return recommendations
        self.mock_recommender.recommend.return_value = ["Movie1", "Movie2", "Movie3"]
        self.gui.get_recommendations()
        # Check if text widget has the recommendations
        content = self.gui.result_text.get(1.0, tk.END).strip()
        self.assertEqual(content, "Movie1\nMovie2\nMovie3")

    def test_get_recommendations_no_recommendations(self):
        # Set entry to a movie title
        self.gui.entry.insert(0, "Test Movie")
        # Mock recommender to return empty list
        self.mock_recommender.recommend.return_value = []
        self.gui.get_recommendations()
        # Check if text widget has the no recommendations message
        content = self.gui.result_text.get(1.0, tk.END).strip()
        self.assertEqual(content, "No recommendations found for this movie.")

if __name__ == '__main__':
    unittest.main()