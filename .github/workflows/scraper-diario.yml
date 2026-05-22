name: 🤖 Scraper Diário - Aresta Online

on:
  schedule:
    - cron: '0 7 * * *'
  workflow_dispatch:
    inputs:
      data_inicio:
        description: 'Data início (YYYY-MM-DD) - opcional'
        required: false
        default: ''
      data_fim:
        description: 'Data fim (YYYY-MM-DD) - opcional'
        required: false
        default: ''
      hotel_id:
        description: 'Hotel específico - opcional (padrão: todos)'
        required: false
        default: ''

permissions:
  contents: write

jobs:
  alto_da_boa_vista:
    runs-on: ubuntu-latest
    timeout-minutes: 90
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: 📦 Instalar
        run: cd scraper && pip install -r requirements.txt && playwright install --with-deps chromium
      - name: 🦈 Scraper
        run: cd scraper && python scraper.py "${{ github.event.inputs.data_inicio }}" "${{ github.event.inputs.data_fim }}" alto_da_boa_vista
      - name: 💾 Commit
        run: |
          git config user.name "Aresta Bot"
          git config user.email "aresta-bot@noreply.github.com"
          git add -f dados/alto_da_boa_vista.json
          git diff --staged --quiet && echo "Sem mudanças" || (
            for i in 1 2 3 4 5; do
              git commit -m "🤖 alto_da_boa_vista $(date -u +'%Y-%m-%d %H:%M UTC')" &&
              git push && break ||
              (echo "Tentativa $i falhou, tentando novamente..." && git pull --rebase && sleep $((i * 5)))
            done
          )

  hamburgo:
    runs-on: ubuntu-latest
    timeout-minutes: 90
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: 📦 Instalar
        run: cd scraper && pip install -r requirements.txt && playwright install --with-deps chromium
      - name: 🦈 Scraper
        run: cd scraper && python scraper.py "${{ github.event.inputs.data_inicio }}" "${{ github.event.inputs.data_fim }}" hamburgo
      - name: 💾 Commit
        run: |
          git config user.name "Aresta Bot"
          git config user.email "aresta-bot@noreply.github.com"
          git add -f dados/hamburgo.json
          git diff --staged --quiet && echo "Sem mudanças" || (
            for i in 1 2 3 4 5; do
              git commit -m "🤖 hamburgo $(date -u +'%Y-%m-%d %H:%M UTC')" &&
              git push && break ||
              (echo "Tentativa $i falhou, tentando novamente..." && git pull --rebase && sleep $((i * 5)))
            done
          )

  terrazzo:
    runs-on: ubuntu-latest
    timeout-minutes: 90
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: 📦 Instalar
        run: cd scraper && pip install -r requirements.txt && playwright install --with-deps chromium
      - name: 🦈 Scraper
        run: cd scraper && python scraper.py "${{ github.event.inputs.data_inicio }}" "${{ github.event.inputs.data_fim }}" terrazzo
      - name: 💾 Commit
        run: |
          git config user.name "Aresta Bot"
          git config user.email "aresta-bot@noreply.github.com"
          git add -f dados/terrazzo.json
          git diff --staged --quiet && echo "Sem mudanças" || (
            for i in 1 2 3 4 5; do
              git commit -m "🤖 terrazzo $(date -u +'%Y-%m-%d %H:%M UTC')" &&
              git push && break ||
              (echo "Tentativa $i falhou, tentando novamente..." && git pull --rebase && sleep $((i * 5)))
            done
          )

  serra_negra:
    runs-on: ubuntu-latest
    timeout-minutes: 90
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: 📦 Instalar
        run: cd scraper && pip install -r requirements.txt && playwright install --with-deps chromium
      - name: 🦈 Scraper
        run: cd scraper && python scraper.py "${{ github.event.inputs.data_inicio }}" "${{ github.event.inputs.data_fim }}" serra_negra
      - name: 💾 Commit
        run: |
          git config user.name "Aresta Bot"
          git config user.email "aresta-bot@noreply.github.com"
          git add -f dados/serra_negra.json
          git diff --staged --quiet && echo "Sem mudanças" || (
            for i in 1 2 3 4 5; do
              git commit -m "🤖 serra_negra $(date -u +'%Y-%m-%d %H:%M UTC')" &&
              git push && break ||
              (echo "Tentativa $i falhou, tentando novamente..." && git pull --rebase && sleep $((i * 5)))
            done
          )

  honorato:
    runs-on: ubuntu-latest
    timeout-minutes: 90
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: 📦 Instalar
        run: cd scraper && pip install -r requirements.txt && playwright install --with-deps chromium
      - name: 🦈 Scraper
        run: cd scraper && python scraper.py "${{ github.event.inputs.data_inicio }}" "${{ github.event.inputs.data_fim }}" honorato
      - name: 💾 Commit
        run: |
          git config user.name "Aresta Bot"
          git config user.email "aresta-bot@noreply.github.com"
          git add -f dados/honorato.json
          git diff --staged --quiet && echo "Sem mudanças" || (
            for i in 1 2 3 4 5; do
              git commit -m "🤖 honorato $(date -u +'%Y-%m-%d %H:%M UTC')" &&
              git push && break ||
              (echo "Tentativa $i falhou, tentando novamente..." && git pull --rebase && sleep $((i * 5)))
            done
          )

  golden_plaza:
    runs-on: ubuntu-latest
    timeout-minutes: 90
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: 📦 Instalar
        run: cd scraper && pip install -r requirements.txt && playwright install --with-deps chromium
      - name: 🦈 Scraper
        run: cd scraper && python scraper.py "${{ github.event.inputs.data_inicio }}" "${{ github.event.inputs.data_fim }}" golden_plaza
      - name: 💾 Commit
        run: |
          git config user.name "Aresta Bot"
          git config user.email "aresta-bot@noreply.github.com"
          git add -f dados/golden_plaza.json
          git diff --staged --quiet && echo "Sem mudanças" || (
            for i in 1 2 3 4 5; do
              git commit -m "🤖 golden_plaza $(date -u +'%Y-%m-%d %H:%M UTC')" &&
              git push && break ||
              (echo "Tentativa $i falhou, tentando novamente..." && git pull --rebase && sleep $((i * 5)))
            done
          )

  maper_ouro:
    runs-on: ubuntu-latest
    timeout-minutes: 90
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: 📦 Instalar
        run: cd scraper && pip install -r requirements.txt && playwright install --with-deps chromium
      - name: 🦈 Scraper
        run: cd scraper && python scraper.py "${{ github.event.inputs.data_inicio }}" "${{ github.event.inputs.data_fim }}" maper_ouro
      - name: 💾 Commit
        run: |
          git config user.name "Aresta Bot"
          git config user.email "aresta-bot@noreply.github.com"
          git add -f dados/maper_ouro.json
          git diff --staged --quiet && echo "Sem mudanças" || (
            for i in 1 2 3 4 5; do
              git commit -m "🤖 maper_ouro $(date -u +'%Y-%m-%d %H:%M UTC')" &&
              git push && break ||
              (echo "Tentativa $i falhou, tentando novamente..." && git pull --rebase && sleep $((i * 5)))
            done
          )
