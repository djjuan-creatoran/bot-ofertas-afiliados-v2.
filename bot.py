import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
OFERTAS_FILE = BASE_DIR / "ofertas.json"
HISTORICO_FILE = BASE_DIR / "ofertas_publicadas.json"

def carregar_json(caminho, padrao):
    if not caminho.exists():
        caminho.write_text(json.dumps(padrao, ensure_ascii=False, indent=2), encoding="utf-8")
        return padrao
    try:
        return json.loads(caminho.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"O arquivo {caminho.name} não contém JSON válido.") from exc

def main():
    ofertas = carregar_json(OFERTAS_FILE, [])
    historico = carregar_json(HISTORICO_FILE, [])
    if not isinstance(ofertas, list):
        raise ValueError("ofertas.json precisa conter uma lista.")
    if not isinstance(historico, list):
        raise ValueError("ofertas_publicadas.json precisa conter uma lista.")

    links = {x.get("link") for x in historico if isinstance(x, dict) and x.get("link")}
    novas = []
    for i, oferta in enumerate(ofertas, 1):
        if not isinstance(oferta, dict):
            print(f"Oferta {i} ignorada: formato inválido.")
            continue
        titulo = str(oferta.get("titulo", "")).strip()
        link = str(oferta.get("link", "")).strip()
        preco = str(oferta.get("preco", "")).strip()
        loja = str(oferta.get("loja", "Oferta")).strip()
        if not titulo or not link.startswith("https://"):
            print(f"Oferta {i} ignorada: informe título e link HTTPS válido.")
            continue
        if link in links:
            print(f"Oferta já registrada, ignorando: {titulo}")
            continue
        mensagem = f"🔥 {titulo}\n"
        if preco:
            mensagem += f"💰 Preço: {preco}\n"
        mensagem += f"🛒 Loja: {loja}\n🔗 Link: {link}"
        print("\n" + "=" * 40 + "\n" + mensagem + "\n" + "=" * 40)
        novas.append({"titulo": titulo, "link": link, "preco": preco, "loja": loja})
        links.add(link)

    if novas:
        historico.extend(novas)
        HISTORICO_FILE.write_text(json.dumps(historico, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\nConcluído: {len(novas)} oferta(s) nova(s) registrada(s) no histórico.")
    else:
        print("\nConcluído: nenhuma oferta nova para registrar.")
    print("Aviso: esta versão ainda não envia mensagens ao WhatsApp.")

if __name__ == "__main__":
    main()
