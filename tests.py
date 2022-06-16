from instalacoes import *

# todo: escrever testes com: tudo funcional, conexões erradas, valores incorretos, projeto incompleto.

b = SaidaReservatorio(direc=HORIZONTAL, coluna_de_água=2)
b << Tubo(comprimento=2) << Joelho90(direc=BAIXO) << Tubo(comprimento=1) << T(entrada=CENTRO)

t = b.proxima_bifurcacao
t.bifurcar(Tubo(c=5), direc=HORIZONTAL)
t.bifurcar(Tubo(c=2), direc=HORIZONTAL)

ja = t.jusante_a
jb = t.jusante_b

ja << Joelho90(direc=HORIZONTAL, rosca=LR) << PontoDeUtilizacao(u='Pia')
jb << Joelho90(direc=HORIZONTAL, rosca=LR) << PontoDeUtilizacao(u='Ducha Higiênica')
