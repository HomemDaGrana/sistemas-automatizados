# Requisitos do controle do tanque T-101

## Processo e fronteira

A bomba P-101 transfere água de uma fonte disponível para o tanque T-101. O consumo retira água do tanque e constitui perturbação externa. O controlador observa sensores discretos, comanda a bomba e apresenta estado e alarmes. Consumo e vazão não são medidos neste primeiro modelo.

Os três sensores de nível indicam presença de água na sua altura. As posições de projeto são mínimo de 20%, máximo de 80% e alto-alto de 95%. Esses números são hipóteses para modelar o cenário, não especificações de equipamento ou exigências expressas do professor. O tanque não deve ser apresentado como sistema de segurança certificado.

## Critérios verificáveis

| ID | Regra | Critério de aceitação |
|---|---|---|
| R01 | Partida voluntária | Ao energizar, AUTO e bomba desligados; é necessária borda de START após condições válidas por 3 s |
| R02 | Parada | STOP remove habilitação e desliga comando na próxima varredura do modelo; retorno depende do equipamento real |
| R03 | Enchimento automático | Com AUTO habilitado, iniciar quando o sensor mínimo estiver seco |
| R04 | Histerese | Após iniciar, manter enchimento ao cobrir o mínimo e parar ao cobrir o máximo |
| R05 | Alto-alto | HH molhado desliga bomba e memoriza falha; baixar nível sozinho não reinicia |
| R06 | Emergência | EMG_OK falso desliga bomba, remove AUTO e memoriza falha |
| R07 | Sobrecarga | OL_OK falso memoriza falha e bloqueia comando |
| R08 | Fonte sem água | FONTE_OK falso bloqueia enchimento e memoriza falha |
| R09 | Coerência dos sensores | Máximo molhado com mínimo seco, ou HH molhado com máximo seco, bloqueia operação |
| R10 | Tempo máximo | Enchimento que não atinge máximo em 30 s memoriza falha e para |
| R11 | Retorno do motor | Comando e retorno divergentes por 2 s memorizam falha; retorno é entrada independente |
| R12 | Reset seguro | RESET só limpa falhas com START solto, permissivos válidos, HH seco e retorno da bomba desligado |
| R13 | Sem repartida automática | RESET e retorno dos permissivos não habilitam AUTO; exigir nova borda de START após 3 s válidos |
| R14 | Contagem | Incrementar um ciclo apenas quando enchimento ativo alcançar máximo; não contar leituras repetidas de máximo |
| R15 | Reinicialização | Modelo reinicializado retorna parado; contador não retentivo neste protótipo |
| R16 | Prioridade | Falhas e parada prevalecem sobre partida; máximo prevalece sobre continuação do enchimento |

## Estados e observação

Estados lógicos: PARADO, PRONTO, AGUARDANDO_NIVEL, ENCHENDO e FALHA. PRONTO representa condições válidas por 3 s, sem habilitação automática. AGUARDANDO_NIVEL mantém AUTO ligado e bomba desligada até o mínimo secar.

A indicação de bomba comandada deve ser distinta do retorno de funcionamento. O contador registra enchimentos concluídos, sem estimar volume. Não existem modo manual, acesso remoto ou comandos MQTT neste escopo inicial da A3.

## Limites

Sensores travados de modo coerente podem escapar ao diagnóstico lógico; o tempo máximo limita somente uma consequência. O alarme de retorno detecta uma divergência, sem identificar sozinho sua causa. Um HH real deve ser avaliado como proteção independente do programa conforme o projeto físico e os equipamentos adotados. Não são feitos ensaios físicos, dimensionamento hidráulico ou análise normativa de segurança nesta etapa.
