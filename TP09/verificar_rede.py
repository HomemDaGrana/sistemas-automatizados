"""Audita arquivos do projeto; não envia pacotes e não representa equipamentos reais.

Executar: python TP09/verificar_rede.py
"""
from pathlib import Path
from collections import Counter
import csv
import ipaddress
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
edges = [(c.attrib['source'], c.attrib['target'])
         for c in ET.parse(ROOT / 'rede.drawio').iter('mxCell')
         if c.get('edge') == '1']
nodes = {n for e in edges for n in e}

def reachable(start, excluded=(), links=None):
    """Conectividade física bidirecional; não modela ACL, protocolo ou latência."""
    seen, queue = {start}, [start]
    for current in queue:
        for a, b in edges if links is None else links:
            if a in excluded or b in excluded:
                continue
            other = b if a == current else a if b == current else None
            if other is not None and other not in seen:
                seen.add(other)
                queue.append(other)
    return seen

with (ROOT / 'nos.csv').open(encoding='utf-8-sig', newline='') as f:
    rows = list(csv.DictReader(f))
ips = [r['Endereço'] for r in rows if r['Endereço'].startswith('10.')]
assert len(ips) == len(set(ips)), 'Duplicidade no projeto original'
for r in rows:
    if r['Endereço'] in ips:
        interface = ipaddress.IPv4Interface(r['Endereço'] + '/' + r['Máscara'])
        assert interface.ip not in (interface.network.network_address,
                                    interface.network.broadcast_address)
        if r['Gateway'] != '-':
            assert ipaddress.IPv4Address(r['Gateway']) in interface.network

normal = reachable('scada')
without_gateway = reachable('scada', excluded={'gw'})
without_fiber = [(a,b) for a,b in edges if {a,b} != {'fw','swa'}]
local = reachable('plc', links=without_fiber)
supervision = reachable('scada', links=without_fiber)
duplicate = ips + ['10.20.30.10']
conflicts = sorted(ip for ip, count in Counter(duplicate).items() if count > 1)
reserved = '10.20.30.60'
installed = [r['Endereço'] for r in rows if r['Função'] != 'Reserva expansão']
expanded = edges + [('swa', 'exp-a1')]
checks = [
 ('T01', 'Todos os enlaces presentes', normal == nodes,
  f'{len(normal)}/{len(nodes)} nós do desenho pertencem ao componente do SCADA'),
 ('T02', 'Gateway B removido', nodes - without_gateway == {'gw','ctrl'},
  'Nós isolados: ' + ', '.join(sorted(nodes - without_gateway))),
 ('T03', 'IP duplicado injetado e removido', conflicts == ['10.20.30.10'] and len(ips) == len(set(ips)),
  'Detector encontrou 10.20.30.10; mapa original permanece sem duplicidade'),
 ('T04', 'Fibra FW-OT / SW-A removida',
  {'plc','hmi','r1','r2','i1','i2','i3'} <= local and 'plc' not in supervision,
  'CLP, HMI, remotas e inversores permanecem conectados localmente; SCADA perde o caminho para A'),
 ('T05', 'Novo nó na reserva A1', reserved not in installed and 'exp-a1' in reachable('scada', links=expanded),
  f'Novo nó usa {reserved}; endereços existentes preservados'),
]
out = ROOT / 'evidencias'
out.mkdir(exist_ok=True)
with (out / 'resultados-modelo.csv').open('w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f, lineterminator="\n")
    writer.writerow(['ID','Cenário','Resultado no modelo','Obtido','Método'])
    for id_, scenario, ok, obtained in checks:
        writer.writerow([id_,scenario,'PASSOU' if ok else 'FALHOU',obtained,'Análise de grafo e endereçamento; sem tráfego real'])
report = ['# Evidências de análise do modelo de rede', '',
          'Autor: Denner Ferreira · RA: 823127322', '',
          'Execução reproduzível com Python 3, sem bibliotecas externas: `python TP09/verificar_rede.py`.', '',
          'Entradas: `rede.drawio` e `nos.csv`. Os enlaces são analisados como conexões físicas bidirecionais. '
          'Alcançabilidade no grafo não comprova ping, ACL, suporte de protocolo, comunicação PN, latência ou recuperação. '
          'A análise não altera a planilha nem os dispositivos.', '',
          '| ID | Cenário | Resultado | Evidência calculada |', '|---|---|---|---|']
for id_, scenario, ok, obtained in checks:
    report.append(f'| {id_} | {scenario} | {"PASSOU" if ok else "FALHOU"} no modelo | {obtained} |')
report += ['', 'Os ensaios da planilha devem ser executados na bancada para registrar comunicação e tempos reais. '
           'A perda de um caminho no grafo indica isolamento topológico; a permanência do caminho não garante funcionamento do processo.', '']
(out / 'README.md').write_bytes('\n'.join(report).encode('utf-8'))
for id_, scenario, ok, obtained in checks:
    print(f'{id_}: {"PASSOU" if ok else "FALHOU"} no modelo — {obtained}')
assert all(ok for _,_,ok,_ in checks)
