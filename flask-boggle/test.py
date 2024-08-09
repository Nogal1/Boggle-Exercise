from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):
    """Tests for the Boggle game."""

    def setUp(self):
        """Before every test."""
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Test if the homepage is displayed correctly."""
        with self.client as client:
            response = client.get("/")
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<table class="board">', html)
            self.assertIn('High Score:', html)
            self.assertIn('Score:', html)
            self.assertIn('Seconds Left:', html)
            self.assertIn('input name="word"', html)

    def test_board_in_session(self):
        """Test if the board is stored in the session."""
        with self.client as client:
            client.get("/")
            self.assertIn("board", session)
            self.assertIsInstance(session["board"], list)
            self.assertEqual(len(session["board"]), 5)

    def test_check_valid_word(self):
        """Test the /check-word route."""
        with self.client as client:
            client.get("/")
            response = client.get("/check-word?word=test")
            self.assertEqual(response.status_code, 200)
            self.assertIn(response.json['result'], ['ok', 'not-on-board', 'not-word'])

    def test_check_word_on_board(self):
        """Test if a valid word on the board is recognized."""
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["T", "E", "S", "T", "T"],
                                 ["T", "E", "S", "T", "T"],
                                 ["T", "E", "S", "T", "T"],
                                 ["T", "E", "S", "T", "T"],
                                 ["T", "E", "S", "T", "T"]]
            response = client.get("/check-word?word=test")
            self.assertEqual(response.json['result'], 'ok')

    def test_check_invalid_word(self):
        """Test if an invalid word not on the board is recognized."""
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["T", "E", "S", "T", "T"],
                                 ["T", "E", "S", "T", "T"],
                                 ["T", "E", "S", "T", "T"],
                                 ["T", "E", "S", "T", "T"],
                                 ["T", "E", "S", "T", "T"]]
            response = client.get("/check-word?word=hello")
            self.assertEqual(response.json['result'], 'not-on-board')

    def test_post_score(self):
        """Test the /post-score route."""
        with self.client as client:
            with client.session_transaction() as sess:
                sess['highscore'] = 10
                sess['nplays'] = 1
            response = client.post("/post-score", json={"score": 15})
            self.assertEqual(response.status_code, 200)
            self.assertIn("brokeRecord", response.json)
            self.assertTrue(response.json["brokeRecord"])

    def test_highscore_update(self):
        """Test if the high score is updated correctly."""
        with self.client as client:
            with client.session_transaction() as sess:
                sess['highscore'] = 10
                sess['nplays'] = 1
            client.post("/post-score", json={"score": 5})
            self.assertEqual(session['highscore'], 10)
            client.post("/post-score", json={"score": 15})
            self.assertEqual(session['highscore'], 15)

    def test_nplays_update(self):
        """Test if the number of plays is updated correctly."""
        with self.client as client:
            with client.session_transaction() as sess:
                sess['highscore'] = 10
                sess['nplays'] = 1
            client.post("/post-score", json={"score": 5})
            self.assertEqual(session['nplays'], 2)

