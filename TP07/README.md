# TP07 - Temporização e contagem

## Atraso obrigatório
START mantido com STOP_OK e EMG_OK habilita TON T1 por 3 s. Antes de PT, Q=0; ao atingir PT, Q=1 e MOTOR_DELAY=1. Interrupção zera ET e Q. Não há selo de START neste exercício. MOTOR_DELAY também recebe permissivos diretamente.

## Extensões
1. PISCA alterna OFF/ON a cada 1 s. Avaliar conclusões dos timers usando o estado anterior e aplicar no máximo uma mudança por varredura. Em seis segundos: OFF [0,1), ON [1,2), OFF [2,3), ON [3,4), OFF [4,5), ON [5,6).
2. CTU acumula uma borda de subida por peça, PV=5. Manter sensor ativo não aumenta CV. LOTE_OK usa CV≥5.
3. RESET_LOTE vence uma borda simultânea. CV=0 e LOTE_OK=0, qualquer que seja CV anterior. O sinal anterior do sensor continua sendo atualizado durante reset.
4. E0 transporta, E1 enche por 2 s e E2 libera. A passagem E1→E2 incrementa quantidade. Uma etapa por vez. Emergência bloqueia ações e exige RESET seguro, sem peça, para reinicializar. A temporização pressupõe vazão constante; não mede volume real.

## Arquivos e reprodução
ladder.txt detalha rungs e ordem de avaliação. testes_modelo.csv e traco_temporal.csv serão resultados de um modelo computacional auxiliar, quando presentes; não são observações do PLC Simulator Online. casos_teste.csv é a verificação a executar no simulador principal. Fonte: Calvetti TP07, slides 60–69. A contingência documental não substitui o programa Ladder executável, conforme slide 67.

## Execução no simulador

TON com PT de 3000 ms e CTU com PV de 5 peças foram executados no PLC Simulator Online. Os testes incluem interrupção, sinal mantido e reset. No T08, as duas entradas foram configuradas antes de iniciar a simulação e foi lido o resultado estabilizado. A intermitência foi executada em 20/11/2026, com PT de 1000 ms em cada fase e amostragem da saída durante 6,3 segundos. A sequência livre segue pendente. Veja a [tabela de testes](casos_teste.csv) e a [captura](ton-atingido.png). [Abrir programa Ladder compartilhado](https://app.plcsimulator.online/LElaHuINNP5UewWBBrE9).

### Intermitência

Foram usados TON T_OFF e T_ON com PT=1000 ms. ENABLE e contato negado de PISCA habilitam T_OFF, cuja saída aciona SET PISCA. ENABLE e PISCA habilitam T_ON, cuja saída aciona RESET PISCA. ENABLE falso aciona RESET PISCA. A observação começou com PISCA falso e registrou três intervalos ligados, separados por intervalos desligados. Ao desabilitar, a saída ficou falsa.

O [registro observado](intermitencia-observada.json) usa o relógio da coleta no navegador, sujeito à latência de amostragem. A [captura](intermitencia.png) mostra o programa montado e desabilitado após o teste.

O projeto compartilhado também contém os rungs da TP04 e TP06. Para o TON, habilite EMG_OK, STOP_OK e START. Para a intermitência, altere ENABLE e observe PISCA. Para o contador, aplique bordas em S_PECA e observe LOTE_OK. RESET_LOTE limpa o contador.
