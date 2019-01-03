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

    def test_linha_jogador(self):
        assert self.parser.linha() == ('{{TitularMandante|Egidio de Araujo '
                                       'Pereira Junior|Egidio}}')

        assert self.parser.linha(False) == ('{{TitularVisitante|'
                                            'Egidio de Araujo '
                                            'Pereira Junior|Egidio}}')

    def test_linha_jogador_reserva(self):
        html_code = (
            """
            <li class="p-l-30">
            <span class="list-number pull-left p-t-15 m-r-10
            w-20">45</span> <strong class="block list-title p-b-5">
                          Welison
                                                      <i class="icon
                                                      pull-right"><svg
            width="26" height="21" viewBox="0 0 26 21"
            xmlns="https://www.w3.org/2000/svg"><path d="M16 9h-5l8-9 7
            9h-5v11h-5V9z" fill="#399C00"></path></svg></i></strong> <span
            class="list-desc">José Welison da Silva</span></li>
            """
        )
        self.parser.html = BeautifulSoup(html_code,
                                         'html.parser').find_all('li')[0]

        assert self.parser.linha() == ('{{ReservaMandante|'
                                       'José Welison da Silva'
                                       '|Welison|num=45}}')

        assert self.parser.linha(False) == ('{{ReservaVisitante|'
                                            'José Welison da Silva'
                                            '|Welison|num=45}}')

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
        assert self.parser.linha() == ('{{TitularMandante|'
                                       'Alejandro Ariel Cabral'
                                       '|Ariel Cabral'
                                       '|amar1=1'
                                       '}}')

    def test_vermelho(self):
        html_code = (
            '<li>'
            '<span class="list-number pull-left p-t-15 m-r-10 w-20">5</span>'
            '<strong class="block list-title p-b-5">'
            '              Rhodolfo'
            '                              <i class="icon small'
            '                              icon-red-card"></i> <i class="icon'
            'pull-right"><svg width="26" height="21" viewBox="0 0 26 21"'
            'xmlns="https://www.w3.org/2000/svg"><path d="M16 9h-5l8-9 7'
            '9h-5v11h-5V9z" fill="#399C00"></path></svg></i></strong>'
            '<span class="list-desc">Rhodolfo Silva</span>'
            '</li>'
        )

        self.parser.html = BeautifulSoup(html_code, 'html.parser')
        assert self.parser.linha(False) == ('{{TitularVisitante|'
                                            'Rhodolfo Silva|Rhodolfo'
                                            '|verm=1'
                                            '}}')

        assert self.parser.vermelho()

    def test_arbitragem(self):
        html_code = """
                <table class="table"><thead><tr><th class="p-b-15 p-t-15">Função</th> <th class="p-b-15 p-t-15">Nome</th> <th class="p-b-15 p-t-15">Categoria</th> <th class="p-b-15 p-t-15">Federação</th></tr></thead> <tbody><tr><th scope="row">Árbitro</th> <td><a href="http://historicoarbitro.cbf.com.br/?id=1042" target="_blank" rel="noopener">
                  Dewson Fernando Freitas da Silva
                </a></td> <td>FIFA</td> <td>PA</td></tr> <tr><th scope="row">Árbitro Assistente 1</th> <td><a href="http://historicoarbitro.cbf.com.br/?id=596" target="_blank" rel="noopener">
                  Cleriston Clay Barreto Rios
                </a></td> <td>MTR</td> <td>SE</td></tr> <tr><th scope="row">Árbitro Assistente 2</th> <td><a href="http://historicoarbitro.cbf.com.br/?id=862" target="_blank" rel="noopener">
                  Heronildo S Freitas da Silva
                </a></td> <td>AB</td> <td>PA</td></tr> <tr><th scope="row">Quarto Árbitro</th> <td><a href="http://historicoarbitro.cbf.com.br/?id=976" target="_blank" rel="noopener">
                  Pedro Martinelli Christino
                </a></td> <td>AB</td> <td>PR</td></tr> <tr><th scope="row">Árbitro Assistente Adicional 1</th> <td><a href="http://historicoarbitro.cbf.com.br/?id=1030" target="_blank" rel="noopener">
                  Eduardo Cordeiro Guimaraes
                </a></td> <td>CD</td> <td>SC</td></tr> <tr><th scope="row">Árbitro Assistente Adicional 2</th> <td><a href="http://historicoarbitro.cbf.com.br/?id=14660" target="_blank" rel="noopener">
                  Edson da Silva
                </a></td> <td>CD</td> <td>SC</td></tr> <tr><th scope="row">Analista de Campo</th> <td><a href="http://historicoarbitro.cbf.com.br/?id=1296" target="_blank" rel="noopener">
                  Anderson Carlos Gonçalves
                </a></td> <td>CBF</td> <td>PR</td></tr></tbody></table>
                """

        self.parser.html = BeautifulSoup(html_code, 'html.parser')

        assert self.parser.arbitragem() == {
            'bandeira': '{{Bandeira|PA}}',
            'arbitro': {
                'nome': 'Dewson Fernando Freitas da Silva',
                'bandeira': None
            },
            'aux1': {
                'nome': 'Cleriston Clay Barreto Rios',
                'bandeira': '{{Bandeira|SE}}'
            },
            'aux2': {
                'nome': 'Heronildo S Freitas da Silva',
                'bandeira': None
            }
        }
