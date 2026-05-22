"""
ARESTA ONLINE — Motor de Scraping
==================================
Roda 1x por dia (ou manualmente).
Busca preços no Booking dos hotéis configurados em hoteis_config.json.
Salva resultados em /dados/{hotel_id}.json
"""

import json
import os
import sys
import time
import random
import re
from datetime import date, datetime, timedelta
from pathlib import Path
from playwright.sync_api import sync_playwright

# ============================================================
# CONFIGURAÇÃO DE CAMINHOS
# ============================================================
PASTA_BASE = Path(__file__).parent.parent
ARQUIVO_CONFIG = Path(__file__).parent / "hoteis_config.json"
PASTA_DADOS = PASTA_BASE / "dados"
PASTA_DADOS.mkdir(exist_ok=True)


# ============================================================
# UTILITÁRIOS
# ============================================================
def log(msg):
    """Imprime mensagem com timestamp."""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)


def carregar_config():
    """Lê o arquivo de configuração dos hotéis."""
    with open(ARQUIVO_CONFIG, "r", encoding="utf-8") as f:
        return json.load(f)


def gerar_datas_mes(data_inicio=None, data_fim=None):
    """
    Gera lista de (check-in, check-out), dia por dia.
    Se nenhuma data for fornecida: do dia atual até o último dia do MÊS SEGUINTE.
    (Ex: se hoje é 22/maio, busca de 22/maio até 30/junho.)
    """
    hoje = date.today()

    if data_inicio is None:
        data_inicio = hoje

    if data_fim is None:
        # Último dia do MÊS SEGUINTE (mês atual + próximo)
        # Avança 2 meses e pega o dia 1, depois volta 1 dia = último dia do mês seguinte
        mes = hoje.month + 2
        ano = hoje.year
        if mes > 12:
            mes -= 12
            ano += 1
        primeiro_dia_dois_meses_a_frente = date(ano, mes, 1)
        data_fim = primeiro_dia_dois_meses_a_frente - timedelta(days=1)

    datas = []
    atual = data_inicio
    while atual < data_fim:
        check_in = atual
        check_out = atual + timedelta(days=1)
        datas.append((check_in, check_out))
        atual += timedelta(days=1)
    return datas


def montar_url_booking(slug, check_in, check_out, config_busca):
    """Monta a URL do Booking pra um hotel específico em uma data."""
    return (
        f"https://www.booking.com/hotel/br/{slug}.pt-br.html"
        f"?checkin={check_in.isoformat()}"
        f"&checkout={check_out.isoformat()}"
        f"&group_adults={config_busca['adultos']}"
        f"&no_rooms={config_busca['quartos']}"
        f"&selected_currency={config_busca['moeda']}"
        f"&lang={config_busca['idioma']}"
    )


def _texto_para_numero(texto):
    """Converte texto tipo 'R$ 1.234,56' ou 'BRL 350' em int (354). Retorna None se inválido."""
    if not texto:
        return None
    # Pega só dígitos e vírgula/ponto
    so_numeros = re.findall(r'[\d.,]+', texto)
    if not so_numeros:
        return None
    # Pega o primeiro grupo numérico (geralmente o preço)
    bruto = so_numeros[0]
    # Remove separadores de milhar (.) e troca vírgula decimal por nada (pegamos só reais)
    limpo = bruto.replace('.', '').replace(',', '.')
    try:
        return int(float(limpo))
    except (ValueError, TypeError):
        return None


def extrair_preco_pagina(page, adultos_esperados=2):
    """
    Extrai o MENOR preço da página do hotel no Booking PARA O NÚMERO DE ADULTOS PEDIDO.

    Estratégia:
    1. Procura linhas de quartos (cada <tr> da tabela é um tipo de quarto)
    2. Pra cada quarto, verifica se ele comporta o número de adultos pedido
       (Booking mostra ícones de pessoa: ⚊ = 1 adulto, ⚊⚊ = 2 adultos)
    3. Pega o preço daquela linha
    4. Retorna o MENOR preço entre os quartos válidos

    Retorna: dict {'preco': int, 'nome_quarto': str} ou None
    """

    # ESTRATÉGIA 1: Tabela tradicional de quartos (hprt-table)
    # Cada <tr> é um quarto, com info de ocupação e preço
    try:
        linhas_quartos = page.query_selector_all('tr.js-rt-block-row, tr[data-block-id]')

        candidatos = []
        for linha in linhas_quartos:
            try:
                texto_linha = linha.inner_text()

                # Verifica capacidade: procura ícones de pessoa ou texto indicando adultos
                # Booking usa: "Máximo de X pessoas" ou ícones SVG de hóspedes
                capacidade = _detectar_capacidade(linha, texto_linha)

                # Pula quartos que claramente são pra menos pessoas que pedimos
                if capacidade is not None and capacidade < adultos_esperados:
                    continue

                # Tenta pegar preço da linha
                preco = _extrair_preco_da_linha(linha)
                if preco and 80 <= preco <= 50000:
                    # Tenta pegar o nome do quarto
                    nome_quarto = ""
                    try:
                        el_nome = linha.query_selector(
                            'span.hprt-roomtype-icon-link, .hprt-roomtype-link, '
                            '[data-testid="property-card-room-name"]'
                        )
                        if el_nome:
                            nome_quarto = el_nome.inner_text().strip()
                    except Exception:
                        pass

                    candidatos.append({"preco": preco, "nome_quarto": nome_quarto})
            except Exception:
                continue

        if candidatos:
            # Retorna o quarto mais barato dos que comportam 2 adultos
            melhor = min(candidatos, key=lambda x: x["preco"])
            return melhor
    except Exception:
        pass

    # NOTA: removido o fallback "preço do card" porque ele pegava
    # preços de OUTROS hotéis quando o Booking redirecionava (hotel esgotado).
    # Agora a detecção de redirect em buscar_hotel() já retorna None nesses casos.

    return None


def _detectar_capacidade(linha_elem, texto_linha):
    """
    Detecta quantos adultos o quarto comporta.
    Retorna int ou None se não conseguir detectar.
    """
    texto_lower = texto_linha.lower()

    # Padrão 1: "X adultos" ou "X hóspedes"
    match = re.search(r'(\d+)\s*(?:adulto|hóspede|guest|pessoa)', texto_lower)
    if match:
        return int(match.group(1))

    # Padrão 2: Contar ícones de pessoa (SVG ou imagens)
    try:
        icones_pessoa = linha_elem.query_selector_all(
            'svg.bk-icon-occupancy, '
            'i.bicon-occupancy, '
            'span.c-occupancy-icons__item, '
            '[data-testid="occupancy-icon"]'
        )
        if icones_pessoa:
            return len(icones_pessoa)
    except Exception:
        pass

    # Não conseguiu detectar → retorna None (vamos aceitar a linha por padrão)
    return None


def _extrair_preco_da_linha(linha):
    """Extrai o preço numérico de uma linha de quarto."""
    seletores_preco = [
        'span.prco-valign-middle-helper',
        '.bui-price-display__value',
        '[data-testid="price-and-discounted-price"]',
        '[data-testid="price-text"]',
        'div.bui-price-display__value',
    ]

    for sel in seletores_preco:
        try:
            el = linha.query_selector(sel)
            if el:
                preco = _texto_para_numero(el.inner_text())
                if preco:
                    return preco
        except Exception:
            continue
    return None


def buscar_hotel(page, slug, check_in, check_out, config_busca, nome_hotel=""):
    """
    Faz UMA busca: abre página do hotel, espera carregar, pega preço.
    Retorna dict {'preco': int, 'nome_quarto': str} ou None.

    IMPORTANTE: Se o Booking redirecionar (hotel esgotado/não existe),
    retorna None pra evitar pegar preço de outro hotel.
    """
    url = montar_url_booking(slug, check_in, check_out, config_busca)
    adultos = config_busca.get("adultos", 2)

    try:
        page.goto(url, timeout=30000, wait_until="domcontentloaded")

        # ⚠️ CHECAGEM DE REDIRECT
        # Se o Booking redirecionar pra outro hotel ou pra busca,
        # a URL final NÃO vai mais conter o slug que pedimos.
        url_atual = page.url.lower()
        slug_lower = slug.lower()

        # Se o slug saiu da URL OU veio pra página de search → esgotado
        if slug_lower not in url_atual or "searchresults" in url_atual:
            log(f"  ⚠️  Hotel {nome_hotel} redirecionado (esgotado/não encontrado)")
            return None

        # Espera elementos de preço aparecerem (até 10s)
        try:
            page.wait_for_selector(
                'tr.js-rt-block-row, tr[data-block-id]',
                timeout=10000
            )
        except Exception:
            pass  # Sem seletor exato, ainda tenta extrair

        resultado = extrair_preco_pagina(page, adultos_esperados=adultos)
        return resultado
    except Exception as e:
        log(f"  ⚠️  Erro buscando {nome_hotel}: {str(e)[:80]}")
        return None


# ============================================================
# FUNÇÃO PRINCIPAL DE VARREDURA
# ============================================================
def varrer_hotel(page, hotel, config_busca, datas):
    """
    Faz a varredura completa de UM hotel-base + seus concorrentes.
    Retorna dicionário com todos os preços por data.
    """
    log(f"\n{hotel['emoji']} {hotel['nome']} ({hotel['cidade']}) — {len(datas)} datas")

    resultado = {
        "hotel_id": hotel["id"],
        "hotel_nome": hotel["nome"],
        "cidade": hotel["cidade"],
        "emoji": hotel["emoji"],
        "data_busca": datetime.now().isoformat(),
        "concorrentes": [hotel["nome"]] + [c["nome"] for c in hotel["concorrentes"]],
        "precos_por_data": []
    }

    # Todos os hotéis a buscar: o próprio + concorrentes
    todos_hoteis = [{"nome": hotel["nome"], "slug": hotel["slug"], "eh_base": True}] + \
                   [{"nome": c["nome"], "slug": c["slug"], "eh_base": False}
                    for c in hotel["concorrentes"]]

    total_buscas = len(datas) * len(todos_hoteis)
    buscas_feitas = 0

    for check_in, check_out in datas:
        linha = {
            "check_in": check_in.isoformat(),
            "check_out": check_out.isoformat(),
            "precos": {}
        }

        for h in todos_hoteis:
            buscas_feitas += 1
            resultado_busca = buscar_hotel(
                page, h["slug"], check_in, check_out,
                config_busca, nome_hotel=h["nome"]
            )

            if resultado_busca and resultado_busca.get("preco"):
                preco = resultado_busca["preco"]
                nome_quarto = resultado_busca.get("nome_quarto", "")
                linha["precos"][h["nome"]] = preco
                linha["precos"][f"{h['nome']}__quarto"] = nome_quarto
                quarto_label = f" ({nome_quarto[:30]})" if nome_quarto else ""
                log(f"  [{buscas_feitas}/{total_buscas}] {check_in.strftime('%d/%m')} | {h['nome'][:35]:35s} = R$ {preco}{quarto_label}")
            else:
                linha["precos"][h["nome"]] = None
                linha["precos"][f"{h['nome']}__quarto"] = ""
                log(f"  [{buscas_feitas}/{total_buscas}] {check_in.strftime('%d/%m')} | {h['nome'][:35]:35s} = Esgotado/Erro")

            # Delay aleatório entre 2-5s pra não parecer robô
            time.sleep(random.uniform(2.0, 5.0))

        resultado["precos_por_data"].append(linha)

    return resultado


def salvar_resultado(resultado):
    """Salva resultado em JSON na pasta /dados/."""
    arquivo = PASTA_DADOS / f"{resultado['hotel_id']}.json"

    # Se já existe, mantém histórico das últimas 30 buscas
    historico = []
    if arquivo.exists():
        try:
            with open(arquivo, "r", encoding="utf-8") as f:
                dados_antigos = json.load(f)
                historico = dados_antigos.get("historico", [])
                # Adiciona a busca atual anterior ao histórico
                if "precos_por_data" in dados_antigos:
                    historico.insert(0, {
                        "data_busca": dados_antigos.get("data_busca"),
                        "precos_por_data": dados_antigos["precos_por_data"]
                    })
                # Limita histórico a 30 dias
                historico = historico[:30]
        except Exception:
            pass

    resultado["historico"] = historico

    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)
    log(f"💾 Salvo em: {arquivo.name}")


# ============================================================
# MAIN
# ============================================================
def main(data_inicio=None, data_fim=None, hotel_id=None):
    """
    Executa o scraper.

    Parâmetros:
    - data_inicio (date): data inicial da busca. Padrão: hoje
    - data_fim (date): data final. Padrão: último dia do mês
    - hotel_id (str): se preenchido, busca apenas este hotel. Padrão: todos
    """
    log("=" * 60)
    log("🚀 ARESTA ONLINE — Iniciando scraping")
    log("=" * 60)

    config = carregar_config()
    config_busca = config["configuracoes_busca"]
    hoteis = config["hoteis"]

    # Filtra hotel específico, se solicitado
    if hotel_id:
        hoteis = [h for h in hoteis if h["id"] == hotel_id]
        if not hoteis:
            log(f"❌ Hotel '{hotel_id}' não encontrado!")
            return

    # Gera as datas a buscar
    datas = gerar_datas_mes(data_inicio, data_fim)
    log(f"📅 Período: {datas[0][0]} até {datas[-1][1]} ({len(datas)} dias)")
    log(f"🏨 Hotéis: {len(hoteis)} base(s) + concorrentes")

    # Tenta carregar cookies do Booking (Genius)
    # Vem da variável de ambiente BOOKING_COOKIES (GitHub Secret)
    # ou do arquivo cookies_booking.json (teste local)
    cookies_booking = []
    try:
        import os, base64
        cookies_b64 = os.environ.get("BOOKING_COOKIES", "")
        if cookies_b64:
            cookies_booking = json.loads(base64.b64decode(cookies_b64).decode())
            log(f"🍪 Cookies Genius carregados! ({len(cookies_booking)} cookies)")
        else:
            # Tenta arquivo local (pra testar no PC)
            arquivo_cookies = Path(__file__).parent / "cookies_booking.json"
            if arquivo_cookies.exists():
                with open(arquivo_cookies, "r") as f:
                    cookies_booking = json.load(f)
                log(f"🍪 Cookies locais carregados! ({len(cookies_booking)} cookies)")
            else:
                log("ℹ️  Sem cookies — buscando preço público (sem Genius)")
    except Exception as e:
        log(f"⚠️  Erro ao carregar cookies: {e} — continuando sem Genius")

    # Inicia o navegador
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-dev-shm-usage",
            ]
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                       "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080},
            locale="pt-BR",
        )

        # Injeta cookies do Booking se disponíveis (ativa Genius!)
        if cookies_booking:
            try:
                context.add_cookies(cookies_booking)
                log("✅ Cookies injetados — buscando com Genius!")
            except Exception as e:
                log(f"⚠️  Erro ao injetar cookies: {e}")

        # Bloqueia imagens pra acelerar (igual o Aresta faz)
        context.route("**/*.{png,jpg,jpeg,gif,webp,svg}", lambda route: route.abort())

        page = context.new_page()

        for hotel in hoteis:
            try:
                resultado = varrer_hotel(page, hotel, config_busca, datas)
                salvar_resultado(resultado)
            except Exception as e:
                log(f"❌ Erro fatal no hotel {hotel['nome']}: {e}")

        browser.close()

    log("=" * 60)
    log("✅ Scraping concluído!")
    log("=" * 60)


if __name__ == "__main__":
    # Permite passar argumentos via linha de comando:
    # python scraper.py                                 → todos hotéis, mês atual
    # python scraper.py 2026-06-01 2026-06-30           → datas customizadas
    # python scraper.py 2026-06-01 2026-06-30 hamburgo  → 1 hotel específico

    args = sys.argv[1:]
    # Trata argumentos vazios (vêm do GitHub Actions quando não preenchido)
    data_ini_str   = args[0].strip() if len(args) >= 1 else ''
    data_fim_str   = args[1].strip() if len(args) >= 2 else ''
    hotel_filtro   = args[2].strip() if len(args) >= 3 else ''

    data_ini     = date.fromisoformat(data_ini_str)   if data_ini_str   else None
    data_fim     = date.fromisoformat(data_fim_str)   if data_fim_str   else None
    hotel_filtro = hotel_filtro                        if hotel_filtro   else None

    main(data_inicio=data_ini, data_fim=data_fim, hotel_id=hotel_filtro)
