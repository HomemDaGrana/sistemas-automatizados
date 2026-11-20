# TP08 - Supervisório do reservatório R-101

## Modelo
Nível 0–100%, bomba P-101, modos MANUAL/AUTOMATICO/LOCAL. H=75% e HH=90% são limites adotados neste protótipo para reproduzir 58% normal, 78% atenção e 92% alarme. Qualidade ruim domina classificação: mostrar --- e bloquear comandos, mantendo indicação da última leitura válida somente se identificada como histórica.

## Arquivos
[tags.csv](prototipo/tags.csv) contém tipos, unidades, acesso e função. [prototipo.drawio](prototipo/prototipo.drawio) contém onze páginas com navegação entre processo, alarmes, manutenção, estados e confirmação. [prototipo.pdf](evidencias/prototipo.pdf) é a versão estática de consulta. A fonte diagrams.net é alternativa prevista no slide 54 **quando a autenticação no Figma estiver bloqueada**; seu uso não deve ser apresentado como arquivo Figma. Não há link Figma criado neste pacote.

## Autoridade e ações
MANUAL: operador solicita partir/parar quando permissivos e qualidade permitem. AUTOMATICO: sequência local decide; comandos diretos ficam desabilitados. LOCAL: autoridade está no equipamento e comandos remotos ficam desabilitados. Configurações e testes de manutenção exigem perfil de manutenção. Alterar perfil no protótipo não equivale a autenticação real.

Parar abre confirmação com alvo P-101, estado e consequência. Confirmar registra solicitação; retorno STATUS é separado. Não afirmar movimento ou parada apenas porque CMD foi alterado. Reconhecer alarme altera ACK, não condição de processo.

## Validação
Abrir .drawio em diagrams.net, usar os links das caixas de navegação e conferir ida/volta. As páginas de estado são casos simulados de interface. Não há comunicação com CLP nem histórico industrial. Revisão por pares requer outra pessoa e não foi inventada.

Fonte: Calvetti TP08, slides 53–69.

Acesso verificado em 05/11/2026: abrir Figma Files redirecionou para Login. Por isso foi preparada a alternativa diagrams.net prevista no enunciado.

[Roteiro de testes](testes/casos_teste.csv) e [capturas](evidencias/).

## Navegação conferida

Em 20/11/2026, os links do protótipo conduziram da tela de processo a alarmes e de volta ao processo, depois à manutenção e de volta ao processo. Os destinos page0, page1 e page2 estão no [registro da navegação](testes/navegacao-verificada.json). A [captura](evidencias/editor-verificado.jpg) mostra o arquivo aberto no editor. Os cinco casos obrigatórios e quatro cenários adicionais foram conferidos no editor após a revisão do protótipo.

## Cenários revisados

O protótipo inclui seletores para 58% normal, 78% atenção, 92% HH e comunicação BAD. PARTIR e PARAR navegam para páginas de solicitação e confirmação. Os modos AUTOMÁTICO e LOCAL exibem comandos indisponíveis. A confirmação de parada mostra alvo P-101, estado LIGADA, consequência e orientação para aguardar o retorno. As cores verde, amarela, vermelha e cinza acompanham textos de estado.

## Resultados finais da interface

Os cinco casos obrigatórios estão preenchidos em [casos_teste.csv](testes/casos_teste.csv). O [registro detalhado](testes/estados-verificados.json) inclui feedback de parada, bloqueio LOCAL, bloqueio AUTOMÁTICO e solicitação de partida. Os testes usaram os links das caixas no editor diagrams.net.

O [protótipo navegável](https://app.diagrams.net/#Uhttps%3A%2F%2Fraw.githubusercontent.com%2FHomemDaGrana%2Fsistemas-automatizados%2Fmain%2FTP08%2Fprototipo%2Fprototipo.drawio) abre a fonte publicada. Foi usada a alternativa diagrams.net prevista no enunciado após a tela de login do Figma. Os valores exibidos são dados de demonstração.
