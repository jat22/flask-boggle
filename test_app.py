from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle
import pdb

class FlaskTests(TestCase):

# app is imported but I don't understand where its coming from
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
        self.client = app.test_client()
    
    def test_show_index(self):

        # checking my understanding - test_client() is a method on app, "client" could be named anything? and is basically a variable representing the testing server?
        with app.test_client() as client:

            # .get() is a method on client that simulates a get request?
            resp = client.get('/')

            # .get_data() is a method on the response object from the get request; it gets the data from that response.
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<title>BOGGLE</title>', html)
            self.assertIn('board', session)

            # why are these none? At line 19 and 20 values for highscore and num_plays are being added to session.
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('num_plays'))


    def test_check_word_ok(self):
        with app.test_client() as client:
            
            # session_transaction() is a method on the client object? I don't really understand the syntax of sess:sess['board']. I understand that sess is representing the session object. Is this just unittest syntax?
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

            #when working with APIs previously, to access the data within the reponse, it was on a 'data' object. Here there's just an opject returned from resp.json. How can I access the entire response? When I try to do so in pdb it just gives the <WraperTestResponse>
            self.assertEqual(resp.json["high_score"], 4)
            self.assertEqual(resp.json["num_plays"], 2)

