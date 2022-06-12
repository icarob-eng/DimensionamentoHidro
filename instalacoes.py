from abc import abstractmethod

# define direções que serão usadas como constantes de direção
BAIXO = -1
HORIZONTAL = 0
CIMA = 1
CENTRO = 2

# tipos de conexão (liso ou roscável, a jusante ou a montante)
# L = False, R = True
LL = (False, False)
LR = (False, True)
RL = (True, False)
RR = (True, True)

""" USOS:
    Formato: 'nome': (vazão, peso relativo)
"""
USOS = {
    'Bacia Sanitária c Caixa': (0.15, 0.3),
    'Bacia Sanitária c Válvula': (1.7, 32),
    'Banheira': (0.3, 1),
    'Bidê': (0.1, 0.1),
    'Ducha Higiênica': (0.2, 0.4),
    'Chuveiro': (0.2, 0.4),
    'Chuveiro Elétrico': (0.1, 0.1),
    'Lava Louças': (0.3, 1),
    'Lava Roupas': (0.3, 1),
    'Lavatório': (0.15, 0.3),
    'Mictório Cerâmico c Sifão': (0.5, 2.8),
    'Mictório Cerâmico s Sifão': (0.15, 0.3),
    'Pia': (0.25, 0.7),
    'Pia c Torneira Elétrica': (0.1, 0.1),
    'Tanque': (0.25, 0.7),
    'Torneira de Jardim': (0.2, 0.4)
}
usos = {k.lower(): v for k, v in USOS.items()}

pols = (
    '1/2',
    '3/4',
    '1',
    '1 1/4',
    '1 1/2',
    '2',
    '2 1/2',
    '3',
    '4'
)
mms = (
    15,
    20,
    25,
    32,
    40,
    50,
    60,
    75,
    100
)


def pol_em_mm(pol: str) -> int:
    if pol in pols:
        return mms[pols.index(pol)]
    else:
        raise ValueError('Valor em polegadas não é um valor válido. Exs de valores válidos: "3/4" e "3"')


def mm_em_pol(mm: str | int) -> str:
    if mm in mms:
        return pols[mms.index(mm)]
    else:
        raise ValueError('Valor em milímetros não é um valor padrão')


class _Componente:
    _INDEF = '!definir!'

    @abstractmethod
    def __init__(self, **kwargs: int | float | str):
        kwargs = _Componente._adapt_kwargs(kwargs)

        self.montante = None
        if 'd' in kwargs:
            self.diametro = _Componente._get_mm(kwargs['d'])
        elif 'diametro' in kwargs:
            self.diametro = _Componente._get_mm(kwargs['diametro'])
        else:
            self.diametro = _Componente._INDEF

        if 'm' in kwargs:
            self.material = kwargs['m']
        elif 'material' in kwargs:
            self.material = kwargs['material']
        else:
            self.material = _Componente._INDEF

        if 'rosca' in kwargs:
            self.rosca = kwargs['rosca']
        elif 'r' in kwargs:
            self.rosca = kwargs['r']
        else:
            self.rosca = LL

    @property
    @abstractmethod
    def con(self) -> str:
        """ Função que deve retronar se o componente tem conexão macho ou fêmea"""
        pass

    @abstractmethod
    def __str__(self):
        return 'Componente'

    def __lshift__(self, other: '_Componente') -> '_Componente':
        """ Adiciona um objeto a montante e a jusante um do outro na forma `jusante` << `montante`"""
        if not isinstance(other, _Componente):
            raise ValueError(f'Erro ao adicionar {other} a {self}. {other} não parece ser um componente válido.')
        SaidaReservatorio.check_invalid_connection(other)

        self.jusante = other
        other.montante = self
        if other.diametro == _Componente._INDEF:
            other.diametro = self.diametro
        elif other.diametro > self.diametro:
            raise Warning(f'Ao adicionar {other} a {self}.'
                          f'Verificou-se que o diâmetro de {other} é maior que o de {self}')
        return other

    @staticmethod
    def _get_mm(val: int | str) -> int:
        """ Função responsável por tratar input de diâmetro e retornar. """
        if isinstance(val, int) or isinstance(val, float):  # se for um número
            val = int(val)  # remove problemas de anotação de tipo
            mm_em_pol(val)  # levanta erro se o valor não for um valor válido
            return val  # retorna o número
        elif isinstance(val, str):  # se for uma string
            try:
                i = int(val)  # tenta converter para int
                if i in mms:  # testa se o int é milímetro
                    return i
                else:
                    return pol_em_mm(val)
            except ValueError:
                pass

        # trecho só executado se nada for retornado
        raise ValueError('Valor de diâmetro inválido.')

    @staticmethod
    def _adapt_kwargs(kwargs: dict) -> dict:
        """ Adapta os argumentos para lower case, permitindo não ser case sensitive """
        nkwargs = {}
        for k, v in kwargs.items():
            nkwargs[k.lower()] = v
        return nkwargs

    @property
    def detalhes(self) -> str:
        return f'Diâmetro: {self.diametro} mm\nMaterial: {self.material}'

    def ver_jusantes(self):
        print(f'Checando conexões a jusante de {self}.')
        x = self.jusante
        while True:
            try:
                print(x)
                x = x.jusante
            except AttributeError:
                break

    def ver_montantes(self):
        print(f'Checando conexões a montante de {self}.')
        x = self.montante
        while True:
            try:
                print(x)
                x = x.montante
            except AttributeError:
                break

    @property
    def primeiro_montante(self) -> '_Componente':
        x = self.montante
        while True:
            try:
                x = x.montante
            except AttributeError:
                return x

    @property
    def proxima_bifurcacao(self) -> '_Componente':
        x = self.jusante
        while True:
            try:
                x = x.jusante
            except AttributeError:
                return x


class Tubo(_Componente):
    def __init__(self, **kwargs: int | float | str):
        super().__init__(**kwargs)
        kwargs = _Componente._adapt_kwargs(kwargs)

        if 'c' in kwargs:
            self.comprimento = kwargs['c']
        elif 'comp' in kwargs:
            self.comprimento = kwargs['comp']
        elif 'comprimento' in kwargs:
            self.comprimento = kwargs['comprimento']
        else:
            raise ValueError('Você precisa especificar o comprimento do tubo')

    def __str__(self):
        return 'Tubo'

    @property
    def con(self) -> str:
        return 'MM'

    @property
    def detalhes(self) -> str:
        return super().detalhes + f'\nComprimento: {self.comprimento}'


class _Joelho(_Componente):
    def __init__(self, **kwargs: int | str):
        super().__init__(**kwargs)
        kwargs = _Componente._adapt_kwargs(kwargs)

        if 'direc' in kwargs:
            self.direc = kwargs['direc']
        elif 'direcao' in kwargs:
            self.direc = kwargs['direcao']
        else:
            raise ValueError('Você precisa especificar uma direção.'
                             'Use `direc` ou `direcao` com valores `BAIXO`, `HORIZONTAL` ou `CIMA`')

    def __str__(self):
        return 'Joelho de curva indefinida'

    @property
    def con(self) -> str:
        return 'FF'


class Joelho90(_Joelho):
    def __str__(self):
        return "Joelho de 90°"


class Joelho45(_Joelho):
    def __str__(self):
        return "Joelho de 45°"


class Curva90(_Joelho):
    def __str__(self):
        return "Curva de 90°"


class Curva45(_Joelho):
    def __str__(self):
        return "Curva de 45°"


class T(_Componente):
    def __init__(self, **kwargs: int | str):
        super().__init__(**kwargs)
        kwargs = _Componente._adapt_kwargs(kwargs)

        self.jusante_b = None
        self.jusante_a = None
        self.direc_b = None
        self.direc_a = None

        if 'e' in kwargs:
            self.entrada = kwargs['e']
        elif 'entrada' in kwargs:
            self.entrada = kwargs['entrada']
        else:
            raise ValueError('Você precisa especificar a conexão de entrada.'
                             'Use `e` ou `entrada` com valores `CENTRO`, `HORIZONTAL`, `CIMA` ou `BAIXO`')

    def __str__(self):
        return 'Tê'

    def __lshift__(self, other) -> None:
        raise Exception('Para bifurcações de Tês (quaisquer conexão a montante de um Tê), use o método'
                        '`t.bifurcar(componente, args).`\nSó podem ser feitas duas bifurcações por Tê.\n'
                        'Lembre-se de especificar a direção de saída usando `direc` ou `direcao` com valores'
                        '`CENTRO`, `HORIZONTAL`, `CIMA` ou `BAIXO`, nos args')

    @property
    def con(self) -> str:
        return 'FF'

    def bifurcar(self, other: _Componente, **kwargs: int) -> 'T':
        if not isinstance(other, _Componente):
            raise ValueError(f'Erro ao adicionar "{other}" a "{self}". "{other}" não parece ser um componente válido.')
        SaidaReservatorio.check_invalid_connection(other)

        if not self.jusante_a:
            if 'direc' in kwargs:
                self.direc_a = kwargs['direc']
            elif 'direcao' in kwargs:
                self.direc_a = kwargs['direcao']
            else:
                raise ValueError('Você precisa especificar uma direção.'
                                 'Use `direc` ou `direcao` com valores `BAIXO`, `HORIZONTAL` ou `CIMA`')
            self.jusante_a = other
        elif not self.jusante_b:
            if 'direc' in kwargs:
                self.direc_b = kwargs['direc']
            elif 'direcao' in kwargs:
                self.direc_b = kwargs['direcao']
            else:
                raise ValueError('Você precisa especificar uma direção.'
                                 'Use `direc` ou `direcao` com valores `BAIXO`, `HORIZONTAL` ou `CIMA`')
            self.jusante_b = other
        else:
            raise ValueError(f'Esse Tê já possui duas conexões, a saber: um {self.jusante_a} e um {self.jusante_b}')
        other.montante = self
        return self


class SaidaReservatorio(_Componente):
    def __init__(self, **kwargs: int | str):
        super().__init__(**kwargs)
        kwargs = _Componente._adapt_kwargs(kwargs)

        if 'direc' in kwargs:
            self.direc = kwargs['direc']
        elif 'direcao' in kwargs:
            self.direc = kwargs['direcao']

        if 'coluna' in kwargs:
            self.coluna = kwargs['coluna']
        elif 'coluna_de_água' in kwargs:
            self.coluna = kwargs['coluna_de_água']
        else:
            raise ValueError('Você precisa especificar a altura máxima da coluna d\'água.')

        if self.diametro == _Componente._INDEF:
            raise ValueError('O diâmetro da saída do reservatório deve ser especificado.')

    def __str__(self):
        return 'Saída do reservatório'

    @property
    def detalhes(self) -> str:
        return f'Altura máxima do reservatório: {self.coluna}\n' + super().detalhes

    @property
    def con(self) -> str:
        return 'FF'

    @staticmethod
    def check_invalid_connection(other) -> None:
        if isinstance(other, SaidaReservatorio):
            raise ValueError('Não é possível fazer conexões a montante da saída do reservatório.')


class Registro(_Componente):
    def __init__(self, **kwargs: int | str):
        super().__init__(**kwargs)
        kwargs = _Componente._adapt_kwargs(kwargs)

        if 't' in kwargs:
            self.tipo = kwargs['t'].lower()
        elif 'tipo' in kwargs:
            self.tipo = kwargs['tipo'].lower()
        else:
            self.tipo = 'globo'  # define registro de globo como padrão

        if self.con:  # serve para testar se o tipo é válido
            pass

    def __str__(self):
        return f'Registro de {self.tipo}'

    @property
    def con(self) -> str:
        if self.tipo == 'gaveta':
            return 'FF'
        elif self.tipo == 'pressão':
            return 'FM'
        elif self.tipo == 'globo':
            return 'FF'
        else:
            ValueError('Tipo de registro não reconhecido, deve ser de: gaveta, pressão ou globo')


class PontoDeUtilizacao(_Componente):
    def __init__(self, **kwargs: int | float | str):
        super().__init__(**kwargs)
        kwargs = _Componente._adapt_kwargs(kwargs)

        self.uso = None
        if 'u' in kwargs:
            self.uso = kwargs['u']
        elif 'uso' in kwargs:
            self.uso = kwargs['uso']

        elif 'peso_relativo' in kwargs:
            self.peso = kwargs['peso_relativo']
        elif 'peso' in kwargs:
            self.peso = kwargs['peso']
        elif 'pr' in kwargs:
            self.peso = kwargs['pr']
        elif 'p' in kwargs:
            self.peso = kwargs['p']

        elif 'vazao' in kwargs:
            self.vazao = kwargs['vazao']
        elif 'v' in kwargs:
            self.vazao = kwargs['v']

        else:
            raise ValueError('É necessário identificar algum tipo de uso do ponto de utilização, seja pelo uso'
                             '(ver tabela de usos), seja pelo peso relativo, seja pela vazão de projeto (L/s).')

        if self.uso and self.uso not in usos:
            raise ValueError('Uso {}')
        else:
            self.vazao = usos[self.uso][0]
            self.peso = usos[self.uso][1]

    def __str__(self):
        r = 'Ponto de utilização{}'
        if self.uso:
            return r.format(f' de {self.uso}.')
        else:
            return r.format('.')

    @property
    def con(self) -> None:
        return None


class Adaptador(_Componente):
    # todo: joelho e tê de redução
    """ Estrutura: tipo: (rosca, macho ou fêmea, tem redução) """
    TIPOS = {
        'Bucha Curta': (LL, 'FF', True),
        'Bucha Longa': (LL, 'FF', True),  # redução múltipla
        'Bucha Roscável': (RR, 'MF', True),
        'Nípel': (RR, 'MM', False),
        'Adaptador': (LR, 'FM', False),  # atentar para direção da rosca
        'Luva LR': (LR, 'MF', True),  # atentar para direção da rosca, com e sem redução
        'Luva LL': (LL, 'FF', False),
        'Luva RR': (RR, 'FF', False),
        'Luva de Correr LL': (LL, 'FF', False),
        'Luva de Correr RR': (RR, 'FF', False),
        'Luva de Redução': (LL, 'FF', False),
    }

    tipos = {k.lower(): v for k, v in TIPOS.items()}

    def __init__(self, **kwargs: int | str):
        super().__init__(**kwargs)
        kwargs = _Componente._adapt_kwargs(kwargs)

        self.tipo = None
        if 'tipo' in kwargs:
            if kwargs['tipo'] in Adaptador.tipos:
                self.tipo = kwargs['tipo']
            else:
                raise ValueError('Tipo de adaptador inválido')

    def validar_tipo(self):
        dados = Adaptador.tipos[self.tipo]
        if self.jusante:  # se jusante é definido
            pass
            # deve-se acessar as propriedades de jusante. Apenas Tês e Joelhos têm saídas não definidas quanto a rosca,
            # ambos têm diâmetro definido. Todos os componentes exceto adaptadores têm saída Macho ou Fêmea definidos
            # deve-se suportar tipo não especificado
        if self.montante:  # se montante é definido
            pass

    def __str__(self):
        if self.tipo:
            return self.tipo
        else:
            return 'Adaptador não especificado'


if __name__ == '__main__':
    pass
