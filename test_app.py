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
            self.assertIn('<div id="alert-container"></div>', html)

    def test_check_word(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['board'] = [
                ['Z', 'Q', 'Y', 'U', 'R'],
                ['N', 'B', 'V', 'M', 'V'],
                ['S', 'S', 'Z', 'J', 'G'],
                ['K', 'A', 'V', 'I', 'D'],
                ['B', 'A', 'I', 'F', 'X']
                ]
                
                resp = client.post('/check', json={'params': {'word': 'a'}})
                pdb.set_trace()
                json = resp.get_data(as_text=True)

                # pdb.set_trace()


                self.assertEqual(resp.status_code, 200)
                # self.assertEqual(resp.result, 'ok')
