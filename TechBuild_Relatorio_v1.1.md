# TechBuild — Relatório de versão

## v1.1 Beta (atual)
- **Dados desacoplados (JSON externo):** catálogo de peças (`HARDWARE_DB`) migrado do HTML para `data/hardware.json` e criação de `data/benchmarks.json` para armazenar benchmarks reais. O carregamento no `index.html` passou a ser assíncrono via `fetch()`.
- **Simulador de FPS com dados reais:** função `updateFpsMeter()` atualizada para priorizar médias de FPS reais obtidas do `benchmarks.json`, mantendo a fórmula matemática como plano B quando não houver dado registrado.
- **Vídeos de análise na aba FPS:** adicionado botão dinâmico no card de FPS (`#fps-video-box`) com link direto para o vídeo de teste da combinação CPU + GPU no YouTube.
- **Automação com YouTube + IA:** criado o script `scripts/atualizar_benchmarks.py` (YouTube Data API v3, `youtube-transcript-api` e Gemini `gemini-3.8-flash`) com salvamento incremental, pausa entre requisições e retentativa automática para erros `503`. Primeiras combinações (`cpu1_gpu1` e `cpu1_gpu2`) já coletadas e salvas.
- **Integração contínua (GitHub Actions):** estruturado o workflow `.github/workflows/update.yml` para atualizar `data/benchmarks.json` automaticamente sempre que novos modelos forem adicionados em `data/hardware.json`.

## v1.0 Beta
- **Meus Setups Salvos:** novo botão (ícone de lápis) em cada setup para renomeá-lo, com janela própria de edição (1 a 30 caracteres). O novo nome é salvo na conta (IndexedDB).
- **Personalizar perfil:** removidos os campos "Jogo favorito" e "Orçamento" do formulário e das etiquetas do cartão do perfil.
- Versão exibida na tela de login atualizada para v1.0.

## v0.9 Beta
- Aba Perfil: botão "Personalizar perfil" com modal de edição.
- Campos salvos na conta: nome de exibição, bio (até 120 caracteres), perfil de uso, jogo favorito e orçamento.
- Validação do nome de exibição (3 a 20 caracteres); o nome de usuário único de login não é alterado.

## v0.8 Beta
- Setups salvos, alertas de preço e inventário por usuário.

## v0.7 Beta
- Foto de perfil (upload ou avatares prontos).

## v0.5 Beta
- Login e cadastro com PBKDF2 (IndexedDB).