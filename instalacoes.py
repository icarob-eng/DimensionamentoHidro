from abc import abstractmethod
from math import ceil

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

testes = False  # variável que faz com que se valide a conexão entre os componentes

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
    20,
    25,
    32,
    40,
    50,
    60,
    75,
    85,
    110
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


bolsas = (
    16,
    19,
    22,
    26,
    31,
    36,
    43,
    48,
    61
)


def comp_min(d: int) -> float:
    """ Retorna o comprimento mínimo em metros de um tubo para permite a conexão de dois acessórios fêmea de mesmo
    diâmetro. """
    return ceil(bolsas[mms.index(d)] / 10)/10 * 2


""" vazões máximas para cada diâmetro na lista de diâmetros """
NOMOGRAMA = (
    0.62,
    1.08,
    2.01,
    3.51,
    5.89,
    8.48,
    13.25,
    17.02,
    28.51
)


def dim_min_vazao(q: int | float) -> int:
    """ Aplica o nomograma """
    for q_max in NOMOGRAMA:
        if q_max > q:
            i = NOMOGRAMA.index(q_max)
            return mms[i]


def dim_min_peso(p: int | float) -> int:
    """ Transforma a soma dos pesos em vazão e chama `dim_min_vazao()`"""
    return dim_min_vazao(0.3 * p ** 0.5)


class _Componente:
    _INDEF = '!definir!'

    @abstractmethod
    def __init__(self, **kwargs: int | float | str | tuple[bool, bool]):
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
        """ Função que deve retornar se o componente tem conexão macho ou fêmea"""
        pass

    @abstractmethod
    def __str__(self):
        return 'Componente'

    def __lshift__(self, other: '_Componente') -> '_Componente':
        """ Adiciona um objeto a montante e a jusante um do outro na forma `jusante` << `montante`"""

        # teste de conexão:
        if self._validate_con(other):
            raise self._validate_con(other)  # ValueError lançado aqui para ficar clara a origem do erro

        self.jusante = other
        other.montante = self
        if other.diametro == _Componente._INDEF:
            other.diametro = self.diametro
        return other

    def _validate_con(self, other: '_Componente', **kwargs) -> ValueError | None:
        """ Retorna uma string de erro ou None se não houver nenhum erro. """
        # self: montante, other: jusante
        if not isinstance(other, _Componente) and testes:
            return ValueError(f'Erro ao adicionar {other} a {self}. {other} não parece ser um componente válido.')
        SaidaReservatorio.check_invalid_connection(other)

        # se for um tê a conexão a montante e jusante serão outras
        if isinstance(self, T):
            if 'e-m' in kwargs:
                e_m = kwargs['e-m']
            elif 'entrada-m' in kwargs:
                e_m = kwargs['entrada-m']
            else:
                return ValueError('Você precisa especificar a conexão de entrada do Tê a montante.'
                                 'Use `e-m` ou `entrada-m` com valores `CENTRO`, `HORIZONTAL`, `CIMA` ou `BAIXO`')
            m = 0 if e_m == CENTRO else 1
        else:
            m = 1
        if isinstance(other, T):
            if 'e-j' in kwargs:
                e_j = kwargs['e-j']
            elif 'entrada_j' in kwargs:
                e_j = kwargs['entrada-j']
            else:
                return ValueError('Você precisa especificar a conexão de entrada do Tê a montante.'
                                 'Use `e-j` ou `entrada-j` com valores `CENTRO`, `HORIZONTAL`, `CIMA` ou `BAIXO`')
            j = 1 if e_j == CENTRO else 0
        else:
            j = 0

        error_string = start = f'{self} não pode se conectar com {other}, pois:'
        base = '\nA conexão jusante de {} é {} e a conexão jusante de {} é {};'
        if not self.rosca[m] == other.rosca[j]:
            error_string += base.format(
                self,
                'roscável' if self.rosca[m] else 'liso',
                other,
                'roscável' if other.rosca[j] else 'liso'
            )
        if not self.con[m] == other.con[j]:
            error_string += base.format(
                self,
                'fêmea' if self.con[m] == 'F' else 'macho',
                other,
                'fêmea' if other.con[j] == 'F' else 'macho'
            )
        if self.diametro < other.diametro:
            error_string += f'O diâmetro de {other} é maior que o de {self};'

        if error_string != start:  # se houve alteração na string base
            if isinstance(other, Adaptador) and not other.invertido:
                # se for um adaptador e não for invertido, inverte e testa de novo
                # não gera recursão infinita devido ao _invertido
                other.inverter_con()
                if self._validate_con(other):
                    return ValueError(error_string)
            else:
                return ValueError(error_string)
        return None

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

    def extremidades(self) -> list['PontoDeUtilizacao']:
        """ Retorna todos os pontos de utilização a jusante do componente selecionado"""
        r = []
        if isinstance(self.proxima_bifurcacao, PontoDeUtilizacao):
            # se tiver um ponto de utilização a jusante, retorne o ponto
            return [self.proxima_bifurcacao]
        elif isinstance(self.proxima_bifurcacao, T):
            try:
                # senão, se for um T, usa o mesmo método até que se retorne só pontos de utilização
                t: 'T' = self.proxima_bifurcacao
                for p in t.jusante_a.extremidades():
                    r += p  # concatena jusantes das duas bifurcações
                for p in t.jusante_b.extremidades():
                    r += p
            except AttributeError:
                raise ValueError('O Tê precisa ter dois jusantes definidos para fazer cálculos no sistema.'
                                 ' Utilize pontos de utilização de peso ou vazão 0 se quiser não por nada.')
            except RecursionError:
                raise ValueError('De duas uma: ou você fez uma encanação circular; ou '
                                 'sua encanação tem mais de 1000 bifurcações; em ambos os casos mude seu projeto.')
        else:
            raise ValueError('Toda rede precisa ter pontos de utilização em suas extremidades jusante'
                             ' Utilize pontos de utilização de peso ou vazão 0 se quiser não por nada.')
        return r

    def soma_vazoes(self) -> float:
        """ Soma as vazões. Se vazão não estiver atribuída, transforma peso relativo em vazão,
        pela fórmula q = 0.3 * sqrt(p)"""
        q = 0
        for p in self.extremidades():
            try:
                q += p.vazao
            except AttributeError:
                q += 0.3 * p.peso ** 0.5
        return q

    def soma_pesos_relativos(self) -> float:
        """ Soma os pesos relativos. Se não estiverem atribuídos, estima o peso relativo pela vazão,
        com a fórmula pr = (q / 0.3) ^ 2"""
        pr = 0
        for p in self.extremidades():
            try:
                pr += p.peso
            except AttributeError:
                pr += (p.vazao / 0.3) ** 2
        return pr

    @staticmethod
    def _criar_adaptador(tipo: str, diametro: int) -> '_Componente':
        if tipo == 'tubo':
            return Tubo(diametro=diametro, comprimento=comp_min(diametro))
        else:
            return Adaptador(tipo=tipo)

    @staticmethod
    def resolver_con(montante: '_Componente', jusante: '_Componente', **kwargs):
        """ Método que cria adaptadores para resolver uma conexão. """
        if isinstance(montante.diametro, int) and isinstance(jusante.diametro, int):
            if isinstance(montante, T):
                # substitui o Tê por um tubo ou nípel na direção especificada, para simplificar a resolução
                if 'e' in kwargs:
                    entrada = kwargs['e']
                elif 'entrada' in kwargs:
                    entrada = kwargs['entrada']
                else:
                    raise ValueError('Usando um Tê como montante na função resolver_con,'
                                     'é necessário especificar a conexão de entrada.'
                                     'Use `e` ou `entrada` com valores `CENTRO`, `HORIZONTAL`, `CIMA` ou `BAIXO`')

                if (entrada == CENTRO and montante.rosca[0]) or (entrada != CENTRO and montante.rosca[1]):
                    # se a entrada selecionada for roscada
                    substituto = Adaptador(diametro=montante.diametro, tipo='Nípel')
                else:
                    substituto = Tubo(diametro=montante.diametro, comprimento=comp_min(montante.diametro))

                montante.bifurcar(substituto, entrada=entrada)
                montante = substituto

            # busca a solução na tabela de soluções
            solucao = Adaptador.solucoes[(
                montante.diametro > jusante.diametro,
                (montante.rosca[1], jusante.rosca[0]),
                (montante.con[1] + jusante.con[0])
            )]

            if isinstance(solucao, str):  # se não for uma tupla, resolve o sistema na hor
                montante << _Componente._criar_adaptador(solucao, montante.diametro) << jusante
            else:
                dims = [montante.diametro]  # lista que conterá o diâmetro de cada componente
                for i in range(len(solucao) - 1):
                    if solucao[i] == 'tubo' or not Adaptador.tipos[solucao[i]][2]:
                        # checa se o item anterior é um tubo ou se não é redução na lista de tipos
                        # veja que o item anterior já terá diâmetro definido,
                        # estamos adicionando a lista o valor de i+1
                        dims.append(dims[i])  # se não tem redução, repete o diâmetro
                    else:
                        dims.append(jusante.diametro)
                comps: list['_Componente'] = list(map(_Componente._criar_adaptador, solucao, dims))
                montante << comps[0]
                for i in range(len(comps) - 1):
                    comps[i] << comps[i + 1]
                comps[-1] << jusante
        else:
            raise ValueError('Erro ao definir adaptadores:'
                       'peças a montante e a jusante da conexão precisam ter diâmetro definido')
#


class Tubo(_Componente):
    def __init__(self, **kwargs: int | float | str | tuple[bool, bool]):
        super().__init__(**kwargs)
        kwargs = _Componente._adapt_kwargs(kwargs)

        self.comprimento: float  # comprimento em metros
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
    def __init__(self, **kwargs: int | str | tuple[bool, bool]):
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
    def __init__(self, **kwargs: int | str | tuple[bool, bool]):
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
        """ Método de bifurcar se faz necessário para o argumento de direção de saída."""
        if self._validate_con(other):
            raise self._validate_con(other)

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

    @property
    def proxima_bifurcacao(self) -> tuple['_Componente', '_Componente']:
        return self.jusante_a, self.jusante_b


class SaidaReservatorio(_Componente):
    def __init__(self, **kwargs: int | str | tuple[bool, bool]):
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
    def __init__(self, **kwargs: int | str | tuple[bool, bool]):
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

        if self.tipo == 'gaveta':
            self.rosca = RR
        elif self.tipo == 'pressão':
            self.rosca = RR
        elif self.tipo == 'globo':
            self.rosca = LL

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
    def __init__(self, **kwargs: int | float | str | tuple[bool, bool]):
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
    """ Estrutura: tipo: (rosca, macho ou fêmea, tem redução) """
    TIPOS = {
        'Bucha Curta': (LL, 'MF', True),
        'Bucha Longa': (LL, 'FF', True),  # redução múltipla
        'Bucha Roscável': (RR, 'MF', True),
        'Nípel': (RR, 'MM', False),
        'Adaptador': (LR, 'FM', False),  # atentar para direção da rosca
        'Luva RL': (LR, 'FF', True),  # atentar para direção da rosca, com e sem redução
        'Luva LL': (LL, 'FF', False),
        'Luva RR': (RR, 'FF', False),
        'Luva de Redução LL': (LL, 'FF', True),
        'Luva de Redução RR': (RR, 'FF', True),
    }  # luvas de correr removidas, pois se tratam apenas de um facilitador de execução

    tipos = {k.lower(): v for k, v in TIPOS.items()}

    """ Estrutura de SOLUCOES: (tem redução, tem rosca, tipo de conexão): (componentes)"""
    SOLUCOES = {
        (False, LL, 'FF'): 'Tubo',
        (False, LL, 'MF'): ('Luva LL', 'Tubo'),
        (False, LL, 'FM'): ('Tubo', 'Luva LL'),
        (False, LL, 'MM'): 'Luva LL',
        (False, RL, 'FF'): ('Adaptador', 'Tubo'),
        (False, RL, 'MF'): ('Luva RL', 'Tubo'),
        (False, RL, 'FM'): 'Adaptador',
        (False, RL, 'MM'): 'Luva RL',
        (False, LR, 'FF'): ('Tubo', 'Adaptador'),
        (False, LR, 'MF'): 'Adaptador',
        (False, LR, 'FM'): ('Tubo', 'Luva RL'),
        (False, LR, 'MM'): 'Luva RL',
        (False, RR, 'FF'): 'Nípel',
        (False, RR, 'MF'): ('Luva RR', 'Nípel'),
        (False, RR, 'FM'): ('Nípel', 'Luva RR'),
        (False, RR, 'MM'): 'Luva RR',
        (True, LL, 'FF'): ('Bucha Curta', 'Tubo'),
        (True, LL, 'MF'): ('Luva de Redução LL', 'Tubo'),
        (True, LL, 'FM'): 'Bucha Curta',
        (True, LL, 'MM'): 'Luva de Redução LL',
        (True, RL, 'FF'): ('Adaptador', 'Bucha Curta'),
        (True, RL, 'MF'): ('Luva RL', 'Tubo'),
        (True, RL, 'FM'): ('Adaptador', 'Bucha Curta'),
        (True, RL, 'MM'): 'Luva RL',
        (True, LR, 'FF'): ('Tubo', 'Luva RL', 'Nípel'),
        (True, LR, 'MF'): ('Luva de Redução LL', 'Tubo', 'Adaptador'),
        (True, LR, 'FM'): ('Tubo', 'Luva RL'),
        (True, LR, 'MM'): 'Luva RL',
        (True, RR, 'FF'): ('Nípel', 'Luva de Redução RR', 'Nípel'),
        (True, RR, 'MF'): 'Bucha Roscável',
        (True, RR, 'FM'): ('Nípel', 'Luva de Redução RR'),
        (True, RR, 'MM'): ('Bucha Roscável', 'Luva RR'),
    }

    solucoes = {k: tuple(i.lower() for i in v) for k, v in SOLUCOES.items()}

    def __init__(self, **kwargs: int | str):
        super().__init__(**kwargs)
        kwargs = _Componente._adapt_kwargs(kwargs)

        self.tipo = None
        if 'tipo' in kwargs:
            if kwargs['tipo'] in Adaptador.tipos:
                self.tipo = kwargs['tipo']
            else:
                raise ValueError('Tipo de adaptador inválido')

        self.invertido = False  # variável que altera a leitura do tipo na função `con()`

    def __str__(self):
        if self.tipo:
            return self.tipo
        else:
            return 'Adaptador não especificado'

    def inverter_con(self):
        """ Inverte as conexões de uma peça, se não for de redução. """
        if Adaptador.tipos[self.tipo][2]:  # se tiver redução de diâmetro
            self.invertido = True
            self.rosca = (not self.rosca[0], not self.rosca[1])
        else:
            raise ValueError(f'Impossível inverter direção de {self.tipo}, pois este adaptador possui redução.')

    @property
    def con(self) -> str:
        r = Adaptador.tipos[self.tipo][1]
        if not self.invertido:
            return r
        else:  # se for invertido
            return r[1] + r[0]  # inverte e concatena a string


if __name__ == '__main__':
    pass
