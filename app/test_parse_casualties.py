import unittest
import responses
import requests
from bs4 import BeautifulSoup
import pandas as pd
from update_dataset import parse_casualties

# URL of the website containing the data
url = 'https://index.minfin.com.ua/ua/russian-invading/casualties/'

# Unit tests to validate the data parsing
class TestParseCasualties(unittest.TestCase):
    
    @responses.activate
    def test_parse_casualties(self):
        # Mock the HTTP response
        responses.add(
            responses.GET,
            url,
            body="""
            <html>
                <h4>02.06.2024</h4>
                <table>
                    <tr><td>Танки</td><td>7765 (+25)</td></tr>
                    <tr><td>ББМ</td><td>14980 (+33)</td></tr>
                </table>
                <h4>01.06.2024</h4>
                <table>
                    <tr><td>Танки</td><td>7740 (+12)</td></tr>
                    <tr><td>ББМ</td><td>14947 (+12)</td></tr>
                </table>
            </html>
            """,
            status=200,
            content_type='text/html'
        )
        
        # Fetch the mocked webpage
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Parse the data
        parsed_df = parse_casualties(soup)
        
        # Print the parsed DataFrame for debugging
        print(parsed_df)
        
        # Check the parsed data
        self.assertIn('tanks', parsed_df.columns)
        self.assertIn('bbm', parsed_df.columns)
        self.assertEqual(parsed_df.iloc[0]['date'], '02.06.2024')
        self.assertEqual(parsed_df.iloc[0]['tanks'], 7765)
        self.assertEqual(parsed_df.iloc[0]['bbm'], 14980)
        self.assertEqual(parsed_df.iloc[1]['date'], '01.06.2024')
        self.assertEqual(parsed_df.iloc[1]['tanks'], 7740)
        self.assertEqual(parsed_df.iloc[1]['bbm'], 14947)

if __name__ == '__main__':
    unittest.main()
