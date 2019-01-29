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
            "Egidio de Araujo Pereira Júnior"

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
                                       'Pereira Júnior|Egidio}}')

        assert self.parser.linha(False) == ('{{TitularVisitante|'
                                            'Egidio de Araujo '
                                            'Pereira Júnior|Egidio}}')

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
            class="list-desc">Jose Welison da Silva</span></li>
            """
        )
        self.parser.html = BeautifulSoup(html_code,
                                         'html.parser').find_all('li')[0]

        assert self.parser.linha() == ('{{ReservaMandante|'
                                       'José Welison da Silva'
                                       '|Welison|num=45|tempo=}}')

        assert self.parser.linha(False) == ('{{ReservaVisitante|'
                                            'José Welison da Silva'
                                            '|Welison|num=45|tempo=}}')

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

    def test_gol(self):
        html_code = """
                <li><span class="list-number pull-left p-t-15 m-r-10 w-20">9</span> <strong class="block list-title p-b-5">
            Brenner
                                      <i title="25' (1ºT)" class="icon small"><svg width="16px" height="16px" viewBox="0 -1 22 22" xmlns="https://www.w3.org/2000/svg"><ellipse id="Oval" stroke="#000000" fill="#FFFFFF" cx="10.5" cy="10" rx="9.84375" ry="10"></ellipse><path d="M2.953125,6.33333333 L6.890625,3" stroke="#000000"></path><path d="M2.953125,10.3333333 L6.234375,12.3333333" stroke="#000000"></path><path d="M12.140625,13 L17.390625,9.66666667" stroke="#000000"></path><path d="M12.140625,16.3333333 L14.109375,17.6666667" stroke="#000000"></path><path d="M7.546875,16.3333333 L6.234375,17.6666667" stroke="#000000"></path><path d="M9.515625,10.3333333 L9.515625,4.33333333" stroke="#000000"></path><path d="M17.390625,6.33333333 L12.140625,2.33333333" stroke="#000000"></path><polygon fill="#000000" transform="translate(9.698930, 13.266044) scale(1, -1) translate(-9.698930, -13.266044) " points="7.21775522 9.8459266 6.13805412 14.1952927 9.5590965 16.6861614 13.2598062 14.1952927 12.4160295 9.8459266"></polygon><polygon fill="#000000" points="18.9163145 4.62690754 16.4527158 5.93259637 16.4527158 10.3302002 19.9355978 13.3555258 20.4653712 10.6885192 20.4653712 8.73574569 19.9355978 6.63692267"></polygon><polygon fill="#000000" points="8.220868 0.0283335625 6.01323944 3.70556576 9.52298362 6.15054747 13.6228614 3.70556576 12.148373 0.0283335625"></polygon><polygon fill="#000000" points="2.07713399 4.82075107 3.40897271 6.4073239 3.40897271 10.6751813 1.24094156 13.6663449 0.503524135 11.0696096 0.817581754 8.01138888 1.6734033 6.00782039"></polygon><polygon fill="#000000" points="13.4092267 19.3750731 14.2307564 17.6514721 19.2988956 14.3599089 16.7021338 17.7707938"></polygon><polygon fill="#000000" points="3.33190831 16.5885193 6.33026023 17.5754567 8.25771734 19.4181781 7.23903454 19.4181781 5.13530703 18.4585411 3.89428439 17.3948283"></polygon></svg></i> <i class="icon pull-right"><svg width="26" height="21" viewBox="0 0 26 21" xmlns="https://www.w3.org/2000/svg"><path d="M16 9h-5l8-9 7 9h-5v11h-5V9z" fill="#FA1200" transform="rotate(180, 18, 10)"></path></svg></i></strong> <span class="list-desc">Brenner Marlos Varanda de Oliveira</span></li>
                """

        self.parser.html = BeautifulSoup(html_code, 'html.parser')
        assert self.parser.linha() == (
            '{{TitularMandante|'
            'Brenner Marlos Varanda de Oliveira|Brenner'
            '|gol1=1'
            '}}'
        )

    def test_gol_amarelo(self):
        html_code = """
        <li><span class="list-number pull-left p-t-15 m-r-10 w-20">10</span> <strong class="block list-title p-b-5">
            De Arrascaeta
                          <i class="icon small icon-yellow-card"></i> <i title="5' (2ºT)" class="icon small"><svg width="16px" height="16px" viewBox="0 -1 22 22" xmlns="https://www.w3.org/2000/svg"><ellipse id="Oval" stroke="#000000" fill="#FFFFFF" cx="10.5" cy="10" rx="9.84375" ry="10"></ellipse><path d="M2.953125,6.33333333 L6.890625,3" stroke="#000000"></path><path d="M2.953125,10.3333333 L6.234375,12.3333333" stroke="#000000"></path><path d="M12.140625,13 L17.390625,9.66666667" stroke="#000000"></path><path d="M12.140625,16.3333333 L14.109375,17.6666667" stroke="#000000"></path><path d="M7.546875,16.3333333 L6.234375,17.6666667" stroke="#000000"></path><path d="M9.515625,10.3333333 L9.515625,4.33333333" stroke="#000000"></path><path d="M17.390625,6.33333333 L12.140625,2.33333333" stroke="#000000"></path><polygon fill="#000000" transform="translate(9.698930, 13.266044) scale(1, -1) translate(-9.698930, -13.266044) " points="7.21775522 9.8459266 6.13805412 14.1952927 9.5590965 16.6861614 13.2598062 14.1952927 12.4160295 9.8459266"></polygon><polygon fill="#000000" points="18.9163145 4.62690754 16.4527158 5.93259637 16.4527158 10.3302002 19.9355978 13.3555258 20.4653712 10.6885192 20.4653712 8.73574569 19.9355978 6.63692267"></polygon><polygon fill="#000000" points="8.220868 0.0283335625 6.01323944 3.70556576 9.52298362 6.15054747 13.6228614 3.70556576 12.148373 0.0283335625"></polygon><polygon fill="#000000" points="2.07713399 4.82075107 3.40897271 6.4073239 3.40897271 10.6751813 1.24094156 13.6663449 0.503524135 11.0696096 0.817581754 8.01138888 1.6734033 6.00782039"></polygon><polygon fill="#000000" points="13.4092267 19.3750731 14.2307564 17.6514721 19.2988956 14.3599089 16.7021338 17.7707938"></polygon><polygon fill="#000000" points="3.33190831 16.5885193 6.33026023 17.5754567 8.25771734 19.4181781 7.23903454 19.4181781 5.13530703 18.4585411 3.89428439 17.3948283"></polygon></svg></i></strong> <span class="list-desc">Giorgian Daniel de Arrascaeta Benedetti</span></li>
        """
        self.parser.html = BeautifulSoup(html_code, 'html.parser')
        assert self.parser.linha(False) == (
            '{{TitularVisitante|'
            'Giorgian Daniel de Arrascaeta Benedetti|De Arrascaeta'
            "|amar1=1"
            '|gol1=1'
            '}}'
        )

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
