# Tabelas base usadas para o programa
Este arquivo contém tabelas e referências das tabelas que servem de base para o programa principal, bem como uma explicação intuitiva dos valores.

## Equivalência de diâmetros comerciais
Tubos podem ter diversos diâmetros, mas no mercado só se produzem alguns diâmetros comerciais. Exemplos:

| mm  | pol   | Bolsa (mm) |
|-----|-------|------------|
| 15  | 1/2   | 16         |
| 20  | 3/4   | 19         |
| 25  | 1     | 22         |
| 32  | 1 1/4 | 26         |
| 40  | 1 1/2 | 31         |
| 50  | 2     | 36         |
| 60  | 2 1/2 | 43         |
| 75  | 3     | 48         |
| 100 | 4     | 61         |

Sobre a bolsa, trata-se do comprimento que um tubo macho entra num tubo fêmea.

## Adaptadores
Existem adaptadores de vários tipos, formas e funções, esta tabela baseada no catálogo da krona deve ajudar a entender.

**Conexões lisas** (ou soldáveis) são conexões que precisam de solda (como uma cola), para serem efetuadas. **Conexões roscáveis** podem ser feitas
e desfeitas, mas as vezes podem ser piores para se executar em campo. Você não pode conectar uma peça soldável diretamente numa roscável.

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
| LL + MF | Luva LL + Tubo               | Luva de redução + Tubo                                         |
| LL + FM | Tubo + Luva LL               | Bucha Curta                                                    |
| LL + MM | Luva LL                      | Luva de Redução<br/>(ou Bucha Longa)                           |
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
Bucha Curta + Tubo                                            
Luva de redução + Tubo                                        
Bucha Curta                                                   
Luva de Redução<br/>(ou Bucha Longa)                          
Adaptador + Bucha Curta + Tubo<br/>(ou Nípel + Luva RL + Tubo)
Luva RL + Tubo                                                
Adaptador + Bucha Curta                                       
Luva RL                                                       
Tubo + Luva RL + Nípel                                        
Luva de Redução LL + Tubo + Adaptador                         
Tubo + Luva RL                                                
Luva LR                                                       
Nípel + Luva de Redução RR + Nípel                            
Bucha Roscável                                                
Nípel + Luva de Redução RR                                    
Bucha Roscável + Luva RR                                      
A solução para conexões fêmea a jusante são tubos, sem bolsa, portanto, machos,
uma vêz que não há adaptadores com macho a jusante. Para saber o comprimento do tubo,
consulte tabela de Diâmetros em mm, polegadas e Comprimentos de bolsas de um acessório.

## Bibliografia
1. http://docente.ifrn.edu.br/carlindoneto/disciplinas/instalacoes-hidrossanitarias-i/tabelas
2. https://www.krona.com.br/wp-content/uploads/2021/03/AF-613047765-CATALOGO-KRONA-ATUALIZACAO-2021-WEB.pdf
