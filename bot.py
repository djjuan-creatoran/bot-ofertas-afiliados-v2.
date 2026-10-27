import json
from pathlib import Path

ARQUIVO_OFERTAS = Path("ofertas.json")
ARQUIVO_HISTORICO = Path("ofertas_publicadas.json")


def carregar_lista(caminho: Path) -> list:
    """Lê um arquivo JSON que deve conter uma lista."""
    if not caminho.exists():
        return []

    try:
        dados = json.loads(caminho.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as erro:
        raise RuntimeError(f"Não foi possível ler {caminho}: {erro}") from erro

    if not isinstance(dados, list):
        raise RuntimeError(f"O arquivo {caminho} precisa conter uma lista JSON.")
    return dados


def salvar_lista(caminho: Path, dados: list) -> None:
    caminho.write_text(
        json.dumps(dados, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def formatar_oferta(oferta: dict) -> str:
    loja = str(oferta.get("loja", "Loja")).strip()
    produto = str(oferta.get("produto", "Produto")).strip()
    preco = str(oferta.get("preco", "")).strip()
    link = str(oferta.get("link", "")).strip()

    linhas = [f"🔥 OFERTA: {produto}", f"🏪 Loja: {loja}"]
    if preco:
        linhas.append(f"💰 Preço informado: R$ {preco}")
    linhas.extend([
        "",
        f"🛒 Confira a oferta: {link}",
        "",
        "⚠️ Consulte o preço e a disponibilidade na loja.",
    ])
    return "\n".join(linhas)


def executar() -> None:
    print("BOT DE OFERTAS — VERSÃO LIMPA")
    print("=" * 40)

    ofertas = carregar_lista(ARQUIVO_OFERTAS)
    historico = carregar_lista(ARQUIVO_HISTORICO)

    links_registrados = {
        item.get("link", "").strip()
        for item in historico
        if isinstance(item, dict) and isinstance(item.get("link"), str)
    }

    novas = []
    ignoradas = 0

    print(f"Ofertas no arquivo: {len(ofertas)}")

    for numero, oferta in enumerate(ofertas, start=1):
        if not isinstance(oferta, dict):
            print(f"[AVISO] Oferta {numero}: formato inválido; ignorada.")
            ignoradas += 1
            continue

        loja = str(oferta.get("loja", "")).strip()
        produto = str(oferta.get("produto", "")).strip()
        preco = str(oferta.get("preco", "")).strip()
        link = oferta.get("link", "")

        if not isinstance(link, str):
            print(f"[AVISO] {produto or f'Oferta {numero}'}: link inválido.")
            ignoradas += 1
            continue

        link = link.strip()
        if not loja or not produto or not link or not link.startswith("https://"):
            print(f"[AVISO] Oferta {numero}: preencha loja, produto e link HTTPS.")
            ignoradas += 1
            continue

        if link in links_registrados:
            print(f"[JÁ REGISTRADA] {produto}")
            ignoradas += 1
            continue

        oferta_limpa = {
            "loja": loja,
            "produto": produto,
            "preco": preco,
            "link": link,
        }

        print("\n" + "-" * 40)
        print(formatar_oferta(oferta_limpa))
        print("-" * 40)

        novas.append({
            "loja": loja,
            "produto": produto,
            "preco": preco,
            "link": link,
        })
        links_registrados.add(link)

    if novas:
        salvar_lista(ARQUIVO_HISTORICO, historico + novas)
        print(f"\nNovas ofertas registradas no histórico: {len(novas)}")
    else:
        print("\nNenhuma oferta nova válida encontrada.")

    print(f"Ofertas ignoradas: {ignoradas}")
    print("OBSERVAÇÃO: o envio ao WhatsApp ainda não está conectado.")
    print("Execução finalizada.")


if __name__ == "__main__":
    executar()
