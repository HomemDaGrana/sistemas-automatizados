# A3 - Controle automatizado de tanque de água

**Integrante confirmado: Denner Ferreira · RA: 823127322**

**Situação: desenvolvimento iniciado.** Os demais integrantes serão informados pelo aluno. A especificação exige grupo de 4 a 6 estudantes e participação de todos. Este diretório ainda não contém a entrega final da A3.

## Fonte e entregas obrigatórias

[Especificação do professor Calvetti](https://drive.google.com/file/d/1Y7cP66B0OESlEDB1WGPfMryrCtQQSsHg/view), versão 1.0 de 07/10/2026. Tema escolhido: item 6.4, controle de tanque de água com sensores de nível, acionamento automático da bomba e controle de transbordamento.

O documento prevê entrega e apresentação presencial em **02/12/2026**, sujeitas a alteração comunicada pelo professor. Cada integrante deve publicar cópia idêntica dos materiais em seu GitHub.

| Entrega | Requisito | Situação |
|---|---|---|
| Programa CLP | Ladder executável em simulador online e demonstração | A implementar e validar |
| Relatório PDF | 10 a 20 páginas, padrão ABNT | A redigir após validação |
| Slides PPTX | Problema, sistema, arquitetura, lógica, demonstração e conclusões | A preparar após validação |
| Apresentação | 10 a 15 minutos, participação de todos | Roteiro e divisão após confirmação do grupo |
| Materiais adicionais | Fontes, diagramas, mapa de E/S e testes | Base técnica iniciada |

## Arquivos iniciais

- [Requisitos e decisões de projeto](requisitos.md).
- [Mapa de entradas e saídas](entradas_saidas.csv).
- [Sequência e lógica de controle](logica.md).
- [Modelo de referência executável](modelo_tanque.py).
- [Testes do modelo de referência](testar_modelo.py).
- [Resultado dos 24 testes locais](testes-modelo.csv): todos passaram no modelo Python.

O modelo Python auxilia a definição e verificação das regras. Não substitui a implementação Ladder ou a demonstração no simulador exigidas pelo professor. Os tempos dos testes são virtuais; não representam medições de equipamentos reais.

## Próximas etapas

1. Implementar o programa Ladder conforme os requisitos e a ordem de prioridades.
2. Executar os mesmos cenários no simulador online, capturar resultados e corrigir divergências.
3. Produzir os diagramas finais e o relatório de 10 a 20 páginas com os resultados observados.
4. Preparar slides e demonstração para 10 a 15 minutos.
5. Completar identificação do grupo, revisar os materiais e distribuir cópias idênticas.

Não há nomes, contribuições de colegas, resultados de CLP ou apresentação presencial presumidos nesta base.
