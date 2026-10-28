ATUALIZAÇÃO DA AUTOMAÇÃO DE PRONTUÁRIOS

Arquivos incluídos:
- processar_documentos.py: lê os PDFs em entrada e cria/atualiza lote_atual.json.
- gerar_capas.py: gera documentos somente para registros do lote_atual.json.
- menu_documentos.py: menu para gerar o lote atual ou localizar funcionários no histórico.
- IMPORTANTE: mantenha cópias de segurança dos arquivos atuais antes de substituir.

COMO INSTALAR
1. Feche o Excel e o Word.
2. Faça uma cópia de segurança dos arquivos atuais:
   processar_documentos.py, gerar_capas.py e revisao_funcionarios.xlsx.
3. Copie os dois scripts atualizados para a pasta principal do projeto, substituindo
   processar_documentos.py e gerar_capas.py.
4. Copie menu_documentos.py para a mesma pasta.
5. Não substitua planilha_revisao.py nem preencher_declaracao.py; a atualização
   não exige mudanças nesses arquivos.
6. Para cada novo lote, coloque os PDFs desejados em entrada e execute
   processar_documentos.py. Isso atualiza lote_atual.json.
7. Revise os dados no Excel.
8. Execute menu_documentos.py e escolha 1 para gerar o lote atual.
9. Para procurar um funcionário antigo, escolha 2.

LIMITAÇÃO ATUAL DA REIMPRESSÃO
Os geradores existentes não sobrescrevem arquivos Word já existentes. O menu permite
localizar o registro antigo, mas se o documento já existir, a função não o substitui.
Para reimprimir, mova/renomeie o arquivo existente na pasta saida antes de tentar
novamente. Não apague o registro do Excel: ele é o histórico.

OBSERVAÇÕES
- O lote é identificado por nome do PDF + número da página.
- O lote_atual.json permanece salvo mesmo depois que os PDFs forem removidos da pasta entrada.
- Ao executar processar_documentos.py com PDFs novos, o lote_atual.json é substituído
  pelo novo lote; isso não apaga registros antigos da planilha.
- Teste primeiro com um lote pequeno e confira os documentos gerados.
