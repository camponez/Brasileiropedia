"""
Parser CBF
"""

URL = "https://www.cbf.com.br"
URL += "/futebol-brasileiro/competicoes/"


class ParserCBF():
    """Parser para site CBF."""

    ano = None
    serie_name = None

    def __init__(self, ano=None, serie_name=None):
        """Initialize """
        self.__html = None
        self.ano = ano
        self.serie_name = serie_name

    @property
    def html(self):
        return self.__html

    @html.setter
    def html(self, value):
        self.__html = value


    def player_name(self):
        """
        Format playername
        """
        name = self.__html.find(class_='block').text.strip().title()
        return self.replace_name(name)

    def replace_name(self, name):
        """Replace names."""

        name = name.replace(' De ', ' de ')
        name = name.replace(' Da ', ' da ')
        name = name.replace(' E ', ' e ')
        name = name.replace(' Dos ', ' dos ')
        name = name.replace(' Do ', ' do ')
        name = name.replace('Junior', 'Júnior')
        name = name.replace('Antonio', 'Antônio')
        name = name.replace('Cesar', 'César')
        name = name.replace('Julio', 'Júlio')
        name = name.replace('Fabio', 'Fábio')
        name = name.replace('Jose', 'José')
        return name

    def player_number(self):
        try:
            return self.__html.find(class_='list-number').text
        except BaseException:
            __import__('pdb').set_trace()

    def player_full_name(self):
        """Show player full name."""
        full_name = self.__html.find(class_='list-desc').text.strip().title()
        return self.replace_name(full_name)

    def titular(self):
        return not self.reserva()

    def reserva(self):
        return self.html.has_attr('class')

    def gols(self):
        return len(self.__html.find_all('ellipse'))

    def amarelo(self):
        if not self.__html.i:
            return False
        return 'icon-yellow-card' in self.__html.i.get('class')

    def vermelho(self):
        if not self.__html.i:
            return False
        return 'icon-red-card' in self.__html.i.get('class')

    def linha(self, mand=True):
        r_out = '{{'
        r_out += 'Titular' if self.titular() else 'Reserva'
        r_out += 'Mandante' if mand else 'Visitante'
        r_out += '|{}|{}'.format(self.player_full_name(), self.player_name())
        r_out += '|num={}'.format(
            self.player_number()) if not self.titular() else ''
        r_out += '|tempo=' if not self.titular() else ''
        r_out += '|amar1=1' if self.amarelo() else ''
        r_out += '|verm=1' if self.vermelho() else ''
        for gol in range(0, self.gols()):
            r_out += '|gol{}=1'.format(gol + 1)

        return r_out + '}}'

    def arbitragem(self):

        html = self.__html.find('table').find_all('td')

        band = html[2].text.strip()
        band2 = html[5].text.strip()
        band3 = html[8].text.strip()

        arbitros = {
            'bandeira': "{{Bandeira|" + band + "}}",
            'arbitro': {
                'nome': html[0].text.strip(),
                'bandeira': None},
            'aux1': {
                'nome': html[3].text.strip(),
                'bandeira': None if band2 == band else "{{Bandeira|" +
                band2 + "}}"
            },
            'aux2': {
                'nome': html[6].text.strip(),
                'bandeira': None if band3 == band else "{{Bandeira|" +
                band3 + "}}"}
        }

        return arbitros

    def parse_page(self):
        """
        TODO: move all the parsing
        """
        pass

class Masculino(ParserCBF):
    """
    Class Masculino
    """

    competicao = "campeonato-brasileiro-{}/{}/{}"
    genero = 'Masculino '

    def __init__(self, serie_path, ano, n_jogo, serie_name):
        ParserCBF.__init__(self, ano, serie_name)
        self.url = URL + self.competicao.format(serie_path, ano, n_jogo)
        self.serie_path = serie_path


class Feminino(ParserCBF):
    """
    Class Feminino
    """

    competicao = "campeonato-brasileiro-feminino-{}/{}/{}"
    genero = 'Feminino '

    def __init__(self, serie_path, ano, n_jogo, serie_name):
        ParserCBF.__init__(self, ano, serie_name)
        self.url = URL + self.competicao.format(serie_path, ano, n_jogo)
        self.serie_path = 'serie-' + serie_path
