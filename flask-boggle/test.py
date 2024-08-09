from unittest import TestCase
from app import app, boggle_game
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

   

    # TODO -- write tests for every view function / feature!

    def setUp(self):
        """Set up test client and configure Flask app for testing."""
        self.client = app.test_client()
        app.config['TESTING'] = True
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = boggle_game.make_board()
                sess['high_score'] = 0
                sess['games_played'] = 0

    def tearDown(self):
        """Clean up any leftover data after each test."""
        pass

    def test_home_page(self):
        """Test that the home page loads and a board is generated."""
        with self.client as client:
            response = client.get("/")
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"<table>", response.data)  # Check if the board is displayed
            self.assertIn("board", session)  # Check if the board is stored in session

    def test_valid_word_submission(self):
        """Test submitting a valid word."""
        with self.client as client:
            response = client.post("/check-word", json={"word": "test"})
            self.assertEqual(response.status_code, 200)
            json_data = response.get_json()
            self.assertIn("result", json_data)

    def test_invalid_word_submission(self):
        """Test submitting an invalid word."""
        with self.client as client:
            response = client.post("/check-word", json={"word": "notaword"})
            self.assertEqual(response.status_code, 200)
            json_data = response.get_json()
            self.assertEqual(json_data["result"], "not-word")

    def test_not_on_board_submission(self):
        """Test submitting a word that is not on the board."""
        with self.client as client:
            response = client.post("/check-word", json={"word": "python"})
            self.assertEqual(response.status_code, 200)
            json_data = response.get_json()
            self.assertEqual(json_data["result"], "not-on-board")

    def test_post_score(self):
        """Test posting a score and updating the session statistics."""
        with self.client as client:
            response = client.post("/post-score", json={"score": 10})
            self.assertEqual(response.status_code, 200)
            json_data = response.get_json()
            self.assertIn("high_score", json_data)
            self.assertIn("games_played", json_data)
            self.assertEqual(session["high_score"], 10)
            self.assertEqual(session["games_played"], 1)