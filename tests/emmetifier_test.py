import unittest
from emmetify import Emmetifier
from emmetify.config.base_config import EmmetifierConfig

class TestEmmetifier(unittest.TestCase):
    def setUp(self):
        self.emmetifier = Emmetifier(config=EmmetifierConfig(debug=False, indent=False))

    def test_single(self):
        case = '<div id="main" class="container" data-test="ignore">Tytus Bomba</div>' 
        expected = 'div#main.container{Tytus Bomba}'
        self.assertEqual(self.emmetifier.emmetify(case)['result'], expected)
