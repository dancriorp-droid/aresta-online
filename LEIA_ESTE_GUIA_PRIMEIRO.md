# 🦈 ARESTA ONLINE — Guia Mestre Final

**Daniel, esse é o documento que tu vai seguir hoje.** Tudo aqui, do começo ao fim, pra teu site ficar **no ar funcionando sozinho**.

⏱️ **Tempo total:** ~45 minutos
💰 **Custo:** R$ 0,00
🎯 **Resultado:** Site profissional online + robô rodando todo dia às 4h da manhã automaticamente

---

## 📦 O QUE TU TEM NA PASTA `aresta-final/`

Essa pasta que eu te entreguei já está **PRONTA PRO GITHUB**. Estrutura:

```
aresta-final/
├── index.html              ← tela de login
├── dashboard.html          ← painel principal
├── hoteis_config.json      ← lista dos hotéis (pra o site)
├── servidor.py             ← (opcional, pra testar local)
├── .gitignore              ← arquivo de configuração
├── .github/
│   └── workflows/
│       └── scraper-diario.yml  ← 🤖 O ROBÔ AUTOMÁTICO!
├── scraper/
│   ├── scraper.py          ← motor de scraping
│   ├── hoteis_config.json  ← cópia da config (pra o robô)
│   └── requirements.txt    ← dependências
└── dados/
    └── hamburgo.json       ← dados que tu já tem
```

**TUDO QUE TU PRECISA FAZER:** copiar essa pasta pro GitHub. Pronto.

---

## 🚀 PARTE 1 — Criar o repositório no GitHub (3 min)

### 1.1
Acessa: **https://github.com/new**

### 1.2 — Preencher

- **Repository name:** `aresta-online`
- **Description:** `Rate shopper online - Aresta Soluções`
- **Public** ✅ (precisa ser público pro GitHub Pages grátis)
- **NÃO marca** "Add a README" (a gente vai subir os próprios arquivos)
- Clica **Create repository**

### 1.3 — Anota o link

Depois de criar, tu vai cair numa página com instruções. **Ignora elas.** O importante é o link do teu repo no topo, tipo:
```
https://github.com/SEU-USUARIO/aresta-online
```

---

## 📤 PARTE 2 — Subir os arquivos (10 min)

Vou te mostrar o jeito **mais fácil possível** — sem terminal, sem Git, só arrastar.

### 2.1 — Clicar pra fazer upload

Na tela do repo recém-criado, vai aparecer um link **"uploading an existing file"**. Clica nele.

Ou acessa direto: `https://github.com/SEU-USUARIO/aresta-online/upload/main`

### 2.2 — Arrastar os arquivos

1. Abre o **Windows Explorer** com a pasta `aresta-final/`
2. Coloca o navegador (GitHub) e o Windows Explorer **lado a lado**
3. **Seleciona TODO o conteúdo** de `aresta-final/` (Ctrl+A dentro da pasta)
4. **Arrasta** pra área "Drag files here" do GitHub

⚠️ **ATENÇÃO IMPORTANTE:** o GitHub vai mostrar os arquivos sendo enviados. **Aguarda subir TUDO** antes do próximo passo. Inclusive os arquivos dentro de pastas (a estrutura precisa ficar igual).

Se algum arquivo importante não aparecer (tipo `.github/workflows/scraper-diario.yml`), me avisa que a gente resolve.

### 2.3 — Confirmar (commit)

No rodapé da página:
- **Commit message:** `Primeira versão do Aresta Online`
- Clica **Commit changes**

✅ Pronto, código no GitHub!

---

## 🌐 PARTE 3 — Ativar o site (GitHub Pages) (2 min)

### 3.1
No teu repo, clica em **Settings** (lá no topo, à direita)

### 3.2
Na barra lateral esquerda, clica em **Pages**

### 3.3 — Configurar
- **Source:** Deploy from a branch
- **Branch:** `main`
- **Folder:** `/ (root)`
- Clica **Save**

### 3.4 — Esperar

Vai aparecer uma mensagem amarela tipo:
> Your site is live at https://seu-usuario.github.io/aresta-online/

**Aguarda 2-5 minutos** (GitHub demora um pouco no primeiro deploy).

### 3.5 — Testar! 🎉

Acessa o link. Vai abrir a tela de login. Usa:

| Usuário | Senha |
|---------|-------|
| `admin` | `aresta2026` |
| `daniel` | `aresta2026` |

**Tabela do Hamburgo já vai aparecer com os dados!** Os outros hotéis vão dizer "Sem dados" até o robô rodar (próxima parte).

---

## 🤖 PARTE 4 — Ativar o robô automático (5 min)

Aqui é a parte mágica: o GitHub vai **rodar o scraper sozinho todo dia às 4h da manhã**.

### 4.1 — Verificar se o workflow tá lá

No teu repo, clica na aba **Actions** (no topo).

Vai aparecer "🤖 Scraper Diário - Aresta Online" na lista.

Se não aparecer: o arquivo `.github/workflows/scraper-diario.yml` não subiu corretamente. Me avisa.

### 4.2 — Rodar uma vez manualmente (pra testar!)

Antes de esperar até as 4h da manhã, **vamos testar agora**:

1. Clica em **🤖 Scraper Diário - Aresta Online**
2. Clica no botão **"Run workflow"** (à direita)
3. Deixa os campos vazios (vai usar o padrão: mês atual, todos hotéis)
4. Clica no botão verde **"Run workflow"**

### 4.3 — Acompanhar a execução

Após uns 10 segundos, vai aparecer um item amarelo na lista (rodando). Clica nele pra ver o progresso.

Tu vai ver os logs em tempo real, tipo:
```
🎯 Pousada Alto Da Boa Vista (Campos do Jordão) — 30 datas
  [1/240] 21/05 | Pousada Villa Capivary         = R$ 380 (Quarto Standard)
  [2/240] 21/05 | Pousada Da Pedra               = R$ 290 (Quarto Duplo)
  ...
```

**Duração esperada:** 30-90 minutos pros 7 hotéis. Pode fechar o navegador, ele continua rodando.

### 4.4 — Quando terminar

Quando o robô terminar (vai ficar verde ✅), ele **automaticamente faz commit dos JSONs gerados** no repo. Os dados aparecem em `dados/` no GitHub.

**Aguarda 1-2 minutos** e acessa teu site. Agora **todos os hotéis vão ter dados**! 🎉

---

## ⏰ PARTE 5 — Ele vai rodar sozinho daqui pra frente

Pronto, tu não precisa fazer **NADA**:

- **Todo dia às 4h da manhã** (horário de Brasília), o robô:
  1. 🤖 Acorda automaticamente
  2. 📡 Roda as buscas no Booking
  3. 💾 Atualiza os JSONs no repo
  4. 🌐 Site automaticamente reflete os novos dados
  5. 😴 Dorme até o próximo dia

- **Tua equipe**:
  - Acessa o link de manhã
  - Vê os preços atualizados
  - Fim!

---

## 🛠️ Como editar coisas depois

### Adicionar/remover um hotel

1. Acessa `https://github.com/seu-usuario/aresta-online/blob/main/hoteis_config.json`
2. Clica no lápis ✏️ (Edit)
3. Edita o JSON
4. Commit changes
5. **IMPORTANTE:** edita também `scraper/hoteis_config.json` (mesma coisa, em outro lugar)

### Trocar senhas

1. Acessa `https://github.com/seu-usuario/aresta-online/blob/main/index.html`
2. Clica no lápis ✏️
3. Procura por `const USUARIOS = {`
4. Edita as senhas
5. Commit changes

### Forçar o robô a rodar agora

- Vai em **Actions → Scraper Diário → Run workflow**

---

## ❓ Problemas que podem rolar

### "Site mostra 404"
- Aguarda mais uns minutos (primeiro deploy demora)
- Verifica em **Settings → Pages** se ativou direito

### "Aparece 'Configuração não encontrada'"
- Verifica se `hoteis_config.json` está na **raiz** do repo (não dentro de subpasta)

### "Robô rodou mas só pegou Esgotado"
- Pode ser que o IP do GitHub esteja sendo bloqueado pelo Booking
- Acontece raramente com 1x/dia e delays
- Se acontecer muito, a gente vê o "plano B" (proxies baratos)

### "Robô falhou"
- Vai em Actions, clica na execução vermelha, lê o log
- Me manda print que eu te ajudo

### "Mudei o config mas o site não atualiza"
- GitHub Pages cacheia. Aperta Ctrl+Shift+R
- Aguarda 2-3 minutos

---

## 🎓 Resumindo a vida do Aresta Online

**De agora em diante:**

🌅 **Manhã (4h):** robô roda sozinho
☀️ **Dia:** equipe acessa o site, vê os dados
🌙 **Noite:** sistema dorme

🤖 **Tu:** não faz nada. Só usa.

---

## 📞 Quando subir, me manda:

1. 🔗 **Link do site** (`https://seu-usuario.github.io/aresta-online/`)
2. 📸 **Print do site funcionando**
3. ✅ **Print do GitHub Actions** rodando (Parte 4)
4. 🐛 **Qualquer erro** que apareceu

VAMOOOO BABY SHARK! 🦈🚀🎉

---

## 🎁 Bônus: o que vem depois

Quando tudo estiver rodando, podemos:
- ➕ Adicionar mais hotéis
- 📊 Adicionar gráfico de evolução de preços
- 📧 Notificação por email/Telegram quando algo mudar muito
- 📱 Versão mobile específica
- 🎨 Customizar mais o visual
- 🔐 Login mais seguro (Clerk, Auth0)

Mas isso fica pra outra hora. **Primeiro: deixa funcionando!** 🦈
