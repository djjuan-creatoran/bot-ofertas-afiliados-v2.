# Bot de Ofertas Afiliadas

Projeto simples em Python para validar ofertas, exibir mensagens no log do GitHub Actions e guardar histórico para evitar links repetidos.

## Como cadastrar ofertas

Edite `ofertas.json` e use uma lista de objetos com estes campos:

- `loja`: Shopee ou Mercado Livre
- `produto`: nome do produto
- `preco`: preço informado (texto)
- `link`: link HTTPS do afiliado

Substitua o exemplo pelo seu link real. Não deixe o link de exemplo no arquivo.

## Como executar

No GitHub, abra **Actions** → **Executar Bot de Ofertas** → **Run workflow** → escolha `main` → **Run workflow**.

O workflow também está programado para executar a cada 6 horas. O GitHub pode atrasar execuções agendadas.

## O que faz e o que ainda não faz

- Valida campos e links HTTPS.
- Ignora links já presentes em `ofertas_publicadas.json`.
- Imprime mensagens de oferta nos logs.
- Tenta salvar o histórico de volta no repositório.
- **Não publica nem envia mensagens ao WhatsApp ainda.** Isso requer configurar uma integração de envio compatível e autorizada.

## Observação

O arquivo `ofertas_publicadas.json` guarda ofertas processadas pelo bot; isso não significa que elas foram enviadas para um grupo.
