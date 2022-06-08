# define direções que serão usadas como constantes para o joelho
BAIXO = -1
HORIZONTAL = 0
CIMA = 1
CENTRO = 2


class _Componente:
    _INDEF = '!definir!'

    def __init__(self, **kwargs):
        self.montante = None
        if 'd' in kwargs:
            self.diametro = kwargs['d']
        elif 'diametro' in kwargs:
            self.diametro = kwargs['diametro']
        else:
            self.diametro = _Componente._INDEF

        if 'm' in kwargs:
            self.material = kwargs['m']
        elif 'material' in kwargs:
            self.material = kwargs['material']
        else:
            self.material = _Componente._INDEF

    def __lshift__(self, other):
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

    def __str__(self):
        return 'Componente'

    def detalhar(self):
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

    def acessar_montante(self):
        x = self.montante
        while True:
            try:
                x = x.montante
            except AttributeError:
                return x

    def acessar_bifurcacao(self):
        x = self.jusante
        while True:
            try:
                x = x.jusante
            except AttributeError:
                return x


class Tubo(_Componente):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
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

    def detalhar(self):
        return super().detalhar() + f'\nComprimento: {self.comprimento}'


class _Joelho(_Componente):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'direc' in kwargs:
            self.direc = kwargs['direc']
        elif 'direcao' in kwargs:
            self.direc = kwargs['direcao']
        else:
            raise ValueError('Você precisa especificar uma direção.'
                             'Use `direc` ou `direcao` com valores `BAIXO`, `HORIZONTAL` ou `CIMA`')


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
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
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

    def __lshift__(self, other, **kwargs):
        raise Exception('Para bifurcações de Tês (quaisquer conexão a montante de um Tê), use o método'
                        '`t.bifurcar(componente, args).`\nSó podem ser feitas duas bifurcações por Tê.\n'
                        'Lembre-se de especificar a direção de saída usando `direc` ou `direcao` com valores'
                        '`CENTRO`, `HORIZONTAL`, `CIMA` ou `BAIXO`, nos args')

    def bifurcar(self, other, **kwargs):
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
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
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

    def detalhar(self):
        return f'Altura máxima do reservatório: {self.coluna}\n' + super().detalhar()

    @staticmethod
    def check_invalid_connection(other):
        if isinstance(other, SaidaReservatorio):
            raise ValueError('Não é possível fazer conexões a montante da saída do reservatório.')


if __name__ == '__main__':
    base = SaidaReservatorio(d=32, coluna=2, direc=HORIZONTAL)
    base << Tubo(c=4) << T(e=HORIZONTAL).bifurcar(Tubo(c=5), direc=BAIXO)
    t = base.acessar_bifurcacao().jusante_a
    t << Joelho90(direc=HORIZONTAL)
    base.ver_jusantes()
    t.ver_jusantes()

