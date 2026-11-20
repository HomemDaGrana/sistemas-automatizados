# Lógica proposta para implementação em CLP

Os endereços de E/S são proposta de documentação. No simulador poderão ser usadas tags simbólicas, preservando a mesma semântica.

## Ordem de varredura proposta

1. Ler entradas e calcular coerência: `LS_MAX → LS_MIN` e `LS_HH → LS_MAX`.
2. Avaliar permissivos e diagnóstico. Qualquer falha crítica memoriza FALHA e desliga AUTO e ENCHENDO.
3. Avaliar RESET por borda, com START solto, permissivos válidos, HH seco e P101_RUN desligado. Limpar falhas e zerar temporizadores, mantendo AUTO desligado.
4. Executar TON de prontidão de 3 s com condições normais e ausência de falhas. START recebido antes da prontidão não fica pendente.
5. Avaliar STOP; sua atuação remove AUTO e ENCHENDO.
6. Avaliar borda START com PRONTO e habilitar AUTO.
7. Em AUTO, se LS_MAX estiver molhado, desligar ENCHENDO; se havia enchimento, gerar pulso de ciclo concluído. Senão, se LS_MIN estiver seco, ligar ENCHENDO. Entre mínimo e máximo, preservar memória.
8. Executar TON de limite de enchimento de 30 s. Timeout memoriza falha e remove comando.
9. Calcular P101_CMD = AUTO AND ENCHENDO AND permissivos AND NOT FALHA.
10. Comparar P101_CMD com P101_RUN. Divergência por 2 s memoriza falha e remove comando. Não substituir retorno pelo comando.
11. Aplicar pulso de conclusão ao contador. Atualizar memórias de borda START e RESET mesmo quando bloqueado, para evitar partida ao liberar permissivo com botão mantido.

## Simulação de referência

`modelo_tanque.py` segue essa ordem para testar decisões antes da tradução para Ladder. O passo de tempo é parâmetro explícito e representa tempo virtual. A ordem da lógica e o comportamento dos temporizadores deverão ser conferidos no CLP escolhido.

Os testes do modelo não são capturas do simulador de CLP. A etapa seguinte deve registrar, para cada cenário, entradas aplicadas, estado observado, temporização e saídas no ambiente online.
