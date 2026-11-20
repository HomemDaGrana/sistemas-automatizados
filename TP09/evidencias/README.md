# Evidências de análise do modelo de rede

Autor: Denner Ferreira · RA: 823127322

Execução reproduzível com Python 3, sem bibliotecas externas: `python TP09/verificar_rede.py`.

Entradas: `rede.drawio` e `nos.csv`. Os enlaces são analisados como conexões físicas bidirecionais. Alcançabilidade no grafo não comprova ping, ACL, suporte de protocolo, comunicação PN, latência ou recuperação. A análise não altera a planilha nem os dispositivos.

| ID | Cenário | Resultado | Evidência calculada |
|---|---|---|---|
| T01 | Todos os enlaces presentes | PASSOU no modelo | 14/14 nós do desenho pertencem ao componente do SCADA |
| T02 | Gateway B removido | PASSOU no modelo | Nós isolados: ctrl, gw |
| T03 | IP duplicado injetado e removido | PASSOU no modelo | Detector encontrou 10.20.30.10; mapa original permanece sem duplicidade |
| T04 | Fibra FW-OT / SW-A removida | PASSOU no modelo | CLP, HMI, remotas e inversores permanecem conectados localmente; SCADA perde o caminho para A |
| T05 | Novo nó na reserva A1 | PASSOU no modelo | Novo nó usa 10.20.30.60; endereços existentes preservados |

Os ensaios da planilha devem ser executados na bancada para registrar comunicação e tempos reais. A perda de um caminho no grafo indica isolamento topológico; a permanência do caminho não garante funcionamento do processo.

[Captura da topologia aberta no editor](editor-verificado.jpg).
