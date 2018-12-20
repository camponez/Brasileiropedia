from parser.parser_cbf import ParserCBF
from bs4 import BeautifulSoup


class TestCBFParse(object):

    def setup(self):
        self.parser = ParserCBF()
        html_code = (
            '<li>'
            '<span class="list-number pull-left p-t-15 m-r-10 w-20">6</span>'
            '<strong class="block list-title p-b-5">Egidio</strong>'
            '<span class="list-desc">Egidio de Araujo Pereira Junior</span>'
            '</li>')

        self.parser.html = BeautifulSoup(html_code, 'html.parser')

    def test_player_name(self):
        assert self.parser.player_name() == "Egidio"

    def test_player_number(self):
        assert self.parser.player_number() == '6'

    def test_player_full_name(self):
        assert self.parser.player_full_name() == \
            "Egidio de Araujo Pereira Junior"

    def test_titular(self):
        assert self.parser.titular()

    def test_reserva(self):
        assert not self.parser.reserva()

    def test_no_amarelo(self):
        assert not self.parser.amarelo()

    def test_no_vermelho(self):
        assert not self.parser.vermelho()

    def test_amarelo(self):
        html_code = (
            '<li>'
            '<span class="list-number pull-left p-t-15 m-r-10 w-20">5</span>'
            '<strong class="block list-title p-b-5">'
            '            Ariel Cabral'
            '                          <i class="icon small'
            '                          icon-yellow-card"></i>'
            '<i class="icon pull-right">'
            '<svg height="21" viewbox="0 0 26 21" width="26"'
            'xmlns="https://www.w3.org/2000/svg">'
            '<path d="M16 9h-5l8-9 7 9h-5v11h-5V9z" fill="#FA1200"'
            'transform="rotate(180, 18, 10)"></path>'
            '</svg>'
            '</i>'
            '</strong>'
            '<span class="list-desc">Alejandro Ariel Cabral</span>'
            '</li>'
        )

        self.parser.html = BeautifulSoup(html_code, 'html.parser')

        assert self.parser.amarelo()
