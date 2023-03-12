from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

class FlaskTests(TestCase):
    def test_show_index(self):
        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<div id="alert-container"></div>', html)

    def test_check_word(self):
        with app.test_client() as client:
            resp = client.post('/check', { params: {'word' : 'if'}})
            session['board'] = [
                ['Z', 'Q', 'Y', 'U', 'R'],
                ['N', 'B', 'V', 'M', 'V'],
                ['S', 'S', 'Z', 'J', 'G'],
                ['K', 'A', 'V', 'I', 'D'],
                ['B', 'A', 'I', 'F', 'X']
                ]
            # json = resp.get_data(as_text=True)
            # print(f'********json: {json}*********')

            self.assertEqual(resp.status_code, 200)
