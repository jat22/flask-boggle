from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle
import pdb

class FlaskTests(TestCase):
    
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
        self.client = app.test_client()
    
    def test_show_index(self):
        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<title>BOGGLE</title>', html)
            self.assertIn('board', session)
            # why are these actually none? is the function not adding highscore:0 to the session object?
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('num_plays'))
            

    def test_check_word_ok(self):
        with app.test_client() as client:
            with self.client.session_transaction() as sess:
                sess['board'] = [
                ['Z', 'Q', 'Y', 'U', 'R'],
                ['N', 'B', 'V', 'M', 'V'],
                ['S', 'S', 'Z', 'J', 'G'],
                ['K', 'A', 'V', 'I', 'D'],
                ['B', 'A', 'I', 'F', 'X']
                ]

            resp = self.client.get('/check?word=if')
                
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json['result'], 'ok')
    
    def test_check_word_not_on_board(self):
        with app.test_client() as client:
            with self.client.session_transaction() as sess:
                sess['board'] = [
                ['Z', 'Q', 'Y', 'U', 'R'],
                ['N', 'B', 'V', 'M', 'V'],
                ['S', 'S', 'Z', 'J', 'G'],
                ['K', 'A', 'V', 'I', 'D'],
                ['B', 'A', 'I', 'F', 'X']
                ]

            resp = self.client.get('/check?word=apple')
                
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json['result'], 'not-on-board')

    def test_check_word_not_word(self):
        with app.test_client() as client:
            with self.client.session_transaction() as sess:
                sess['board'] = [
                ['Z', 'Q', 'Y', 'U', 'R'],
                ['N', 'B', 'V', 'M', 'V'],
                ['S', 'S', 'Z', 'J', 'G'],
                ['K', 'A', 'V', 'I', 'D'],
                ['B', 'A', 'I', 'F', 'X']
                ]

            resp = self.client.get('/check?word=asdfaweg')
                
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json['result'], 'not-word')

    def test_score(self):
        with app.test_client() as client:

            resp = self.client.post('/score', json={"new_score" : 4})



            self.assertEqual(resp.json["high_score"], 4)
            self.assertEqual(resp.json["num_plays"], 2)

