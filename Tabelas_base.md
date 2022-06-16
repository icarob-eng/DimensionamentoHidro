# Tabelas base usadas para o programa
Este arquivo contém tabelas e referências das tabelas que servem de base para o programa principal, bem como uma explicação intuitiva dos valores.

## Equivalência de diâmetros comerciais
Tubos podem ter diversos diâmetros, mas no mercado só se produzem alguns diâmetros comerciais. Exemplos:

| mm  | pol   | Bolsa Usada (mm) |
|-----|-------|------------------|
| 20  | 1/2   | 16               |
| 25  | 3/4   | 19               |
| 32  | 1     | 22               |
| 40  | 1 1/4 | 26               |
| 50  | 1 1/2 | 31               |
| 60  | 2     | 36               |
| 75  | 2 1/2 | 43               |
| 85  | 3     | 48               |
| 110 | 4     | 61               |

Sobre a bolsa, trata-se do comprimento que um tubo macho entra num tubo fêmea.

## Adaptadores e conexões
Existem adaptadores de vários tipos, formas e funções, esta tabela baseada no catálogo da krona deve ajudar a entender.

**Conexões lisas** (ou soldáveis) são conexões que precisam de solda (como uma cola), para serem efetuadas. **Conexões roscáveis** podem ser feitas
e desfeitas, mas às vezes podem ser piores para se executar em campo. Você não pode conectar uma peça soldável diretamente numa roscável.

**Conexões macho** entram em **conexões fêmea**. Você não óde conectar uma peça macho com outra macho, nem uma fêmea com outra fêmea, pois elas não terão
contato interno para se conectarem. ~~Não me critique, eu não criei esse padrão~~

Adaptadores podem servir apenas para adaptar o tipo ou formato da conexão, mas também podem servir para reduzir o diâmetro. No caso apenas da bucha de
redução longa, é possível saltar mais de um diâmetro, entretanto, normalmente é apenas um, ou seja, 25 mm para 20 mm, e não para 15 mm, por exemplo.
Ver tabela de diâmetros.

| Nome               | Liso / Roscável | Macho / Fêmea         | Redução  |
|--------------------|-----------------|-----------------------|----------|
| Trecho de tubo     | LL              | Macho - Macho         | Não      |
| Bucha Curta        | LL              | Macho - Fêmea (menor) | Sim      |
| Bucha Longa        | LL              | Fêmea - Fêmea         | Bastante |
| Bucha Roscável     | RR              | Macho - Fêmea (maior) | Sim      |
| Nípel              | RR              | Macho - Macho         | Não      |
| Adaptador          | RL              | Macho (R) - Fêmea (L) | Não      |
| Luva RL            | RL              | Fêmea - Fêmea         | Ambos    |
| Luva LL            | LL              | Fêmea - Fêmea         | Não      |
| Luva RR            | RR              | Fêmea - Fêmea         | Não      |
| Luva de Correr LL  | LL              | Fêmea - Fêmea         | Não      |
| Luva de Correr RR  | RR              | Fêmea - Fêmea         | Não      |
| Luva de Redução LL | LL              | Fêmea - Fêmea         | Sim      |
| Luva de Redução RR | RR              | Fêmea - Fêmea         | Sim      |

Existe um número limitado de possíveis conexões diferentes, assim é possível pensar na solução mais simples
(não necessariamente a ideal) para cada conexão possível.

| Conexão | Solução p/ mesmo diâmetro    | Solução c/ redução                                             |
|---------|------------------------------|----------------------------------------------------------------|
| LL + FF | Trecho de Tubo               | Bucha Curta + Tubo                                             |
| LL + MF | Luva LL + Tubo               | Luva de Redução LL + Tubo                                      |
| LL + FM | Tubo + Luva LL               | Bucha Curta                                                    |
| LL + MM | Luva LL                      | Luva de Redução LL<br/>(ou Bucha Longa)                        |
| RL + FF | Adaptador + Tubo             | Adaptador + Bucha Curta + Tubo<br/>(ou Nípel + Luva RL + Tubo) |
| RL + MF | Luva RL + Tubo               | Luva RL + Tubo                                                 |
| RL + FM | Adaptador                    | Adaptador + Bucha Curta                                        |
| RL + MM | Luva RL                      | Luva RL                                                        |
| LR + FF | Tubo + Adaptador (invertido) | Tubo + Luva RL + Nípel                                         |
| LR + MF | Adaptador (invertido)        | Luva de Redução LL + Tubo + Adaptador                          |
| LR + FM | Tubo + Luva RL               | Tubo + Luva RL                                                 |
| LR + MM | Luva LR                      | Luva LR                                                        |
| RR + FF | Nípel                        | Nípel + Luva de Redução RR + Nípel                             |
| RR + MF | Luva RR + Nípel              | Bucha Roscável                                                 |
| RR + FM | Nípel + Luva RR              | Nípel + Luva de Redução RR                                     |
| RR + MM | Luva RR                      | Bucha Roscável + Luva RR                                       |
 
A solução para conexões fêmea a jusante são tubos, sem bolsa, portanto, machos,
uma vêz que não há adaptadores com macho a jusante. Para saber o comprimento do tubo,
consulte tabela de Diâmetros em mm, polegadas e Comprimentos de bolsas de um acessório.

## Pontos de utilização

Os pontos de utilização são o motivo de todo o projeto.
Precisamos considerar as demandas de cada ponto, em acordo com sua instalação no ambiente
— sabemos que não haverá vasos sanitários fora do banheiro. Sejam estas demandas o diâmetro mínimo do ponto,
seja a demanda de água: um chuveiro gasta mais água que uma torneira de lavatório.
Por fim, no dimensionamento de um projeto hidráulico ainda é necessário considerar se a pressão da água no ponto
é adequada para o uso, ninguém quer ficar reclamando do chuveiro com pouca pressão depois.

| Descrição                 | Vazão de<br/>Projeto (L/s) | Peso<br/>Relativo | Diâmetro Nominal<br/>Mínimo (mm) | Pressão Dinâmica<br/>Mínima (mca)*** |
|---------------------------|----------------------------|-------------------|----------------------------------|--------------------------------------|
| Bacia Sanitária c Caixa   | 0.15                       | 0.3               | 20                               | 1,5 (20mm) ou 0,5 (25mm)*            |
| Bacia Sanitária c Válvula | 1.7                        | 32                | 40**                             | 1,2                                  |
| Banheira                  | 0.3                        | 1                 | 20                               | 0,5                                  |
| Bidê                      | 0.1                        | 0.1               | 20                               | Sem informações                      |
| Ducha Higiênica           | 0.2                        | 0.4               | 20                               | 3                                    |
| Chuveiro                  | 0.2                        | 0.4               | 20                               | 2 (20mm) ou 1 (25mm)*                |
| Chuveiro Elétrico         | 0.1                        | 0.1               | 20                               | 1 (0,7 com pressurização)            |
| Lava Louças               | 0.3                        | 1                 | 25                               | 2,5                                  |
| Lava Roupas               | 0.3                        | 1                 | 25                               | 2,5                                  |
| Lavatório                 | 0.15                       | 0.3               | 20                               | 0,5                                  |
| Mictório Cerâmico c Sifão | 0.5                        | 2.8               | 32                               | Sem informações                      |
| Mictório Cerâmico s Sifão | 0.15                       | 0.3               | 20                               | Sem informações                      |
| Pia                       | 0.25                       | 0.7               | 20                               | 0,5                                  |
| Pia c Torneira Elétrica   | 0.1                        | 0.1               | 20                               | 2                                    |
| Tanque                    | 0.25                       | 0.7               | 25                               | 0,5                                  |
| Torneira de Jardim        | 0.2                        | 0.4               | 25                               | Sem informações                      |

-* Pressão para diâmetros nominais do ponto de utilização de 20 ou 25 mm;

** Para pressões inferiores a 3 mca, o diâmetro de 50 mm é recomendado;

*** Recomenda-se conferir o manual de eletrodomésticos e acessórios do ponto de utilização para uma pressão mínima ideal;

Sobre o dimensionamento do diâmetro de tubos e acessórios, deve-se considerar as demandas dos pontos de utilização.
Para o cálculo das demandas existem dois métodos: o da Demanda Máxima Possível e o da Demanda Máxima Provável.

O método da **Demanda Máxima Possível** consiste em considerar que todos os pontos de utilização estão ligados
em simultâneo, e assim achar a vazão resultante (basicamente somando as vazões da tabela). É utilizado mais para casos
extremos em que se têm grande e constante utilização dos aparelhos.

O método da **Demanda Máxima Provável** por sua vez, faz considerações estatísticas para que dimensionemos apenas para
casos prováveis, permitindo fazer sistemas mais realistas e assim mais econômicas. Sendo assim, em usos residenciais,
este é o método **recomendado**.

## Bibliografia
1. http://docente.ifrn.edu.br/carlindoneto/disciplinas/instalacoes-hidrossanitarias-i/tabelas
2. https://www.krona.com.br/wp-content/uploads/2021/03/AF-613047765-CATALOGO-KRONA-ATUALIZACAO-2021-WEB.pdf
