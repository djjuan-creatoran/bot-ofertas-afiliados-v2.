# Bot de Ofertas de Afiliados

Esta versão executa pelo GitHub Actions, exibe as ofertas nos logs e registra links no histórico para evitar processar o mesmo link de novo.

## Arquivos
- `bot.py`: lógica do bot.
- `ofertas.json`: ofertas a processar.
- `ofertas_publicadas.json`: histórico de links registrados.
- `.github/workflows/bot.yml`: execução manual e agendada.

## Cadastrar ofertas
Edite `ofertas.json` seguindo este formato:

```json
[
  {
    "titulo": "Nome do produto",
    "preco": "R$ 99,90",
    "loja": "Shopee",
    "link": "https://seu-link-de-afiliado"
  }
]
```

Substitua o exemplo por um link real gerado na sua conta de afiliado.

## Executar
No GitHub, entre em **Actions** → **Executar Bot de Ofertas** → **Run workflow**. O agendamento tenta executar a cada seis horas.

## Importante
Esta versão ainda **não envia mensagens ao WhatsApp**. Ela apenas mostra as mensagens nos logs e registra os links no histórico. O envio automático exige configurar uma integração separada.
