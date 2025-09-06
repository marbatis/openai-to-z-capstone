# Rede de Águas & Tesos (RAT) — Projeto (PT)

**Resumo:** Mapear **redes de “tesos” e “caceias/currais de peixe”** nas várzeas amazônicas do Brasil usando **SAR L‑banda sazonal** + **plausibilidade hidrodinâmica** e validar com **GEDI WSCI** (complexidade estrutural do dossel).

**Objetivo (estilo do desafio):** Gerar **novas redes de sítios** no Brasil, comprovadas por **≥2 métodos independentes**, com IDs públicos e relatório reproduzível.

## 1) Área e escopo
- Foco: várzeas do Pará e Amazonas (expansível para Acre/Rondônia).
- Incluir margens de terra firme até 50–100 km dos principais rios.
- Apenas dados públicos; coordenadas **ofuscadas** em artefatos públicos (ver `docs/ETHICS.md`).

## 2) Conjuntos de dados (públicos, com IDs)
- **ALOS‑2 PALSAR‑2 ScanSAR L2.2 (25 m)** — Série temporal L‑banda 2014–atual (`JAXA/ALOS/PALSAR-2/Level2_2/ScanSAR`). Converter DN→γ0 dB: `10*log10(DN^2) - 83`. *Sinal sazonal primário.*
- **Sentinel‑1 C‑banda** — Contra‑checagem sazonal.
- **GEDI L4C — WSCI** — Índice de complexidade estrutural por pegada (download via ORNL DAAC, produto `GEDI04_C` v2). *Sinal estrutural independente.*
- **Hidrologia/topografia** — MERIT Hydro (HAND, área de drenagem), SRTM/AW3D30 conforme necessário.

## 3) Métodos (para cumprir “dois métodos independentes”)
**Sinal A — Histerese sazonal L‑banda (primário):**
1. Compositos **chuvoso** (dez–mai) e **seco** (jun–nov) em γ0 dB.
2. Calcular **Δ = chuvoso − seco (dB)** e z‑scores locais; extrair segmentos lineares/denteados alinhados ao fluxo.
3. Candidatos = componentes conectados com sinal/força consistentes e espaçamento plausível.

**Sinal B — Plausibilidade hidrodinâmica (física):**
1. Usar **HAND** e área de drenagem para estimar **alagamento/desvio**.
2. Pontuar sobreposição com HAND≤N m e pixels de **convergência de fluxo**.

**Sinal C (opcional) — GEDI L4C WSCI:**
- Estatísticas WSCI sobre bermas/tesos vs controles; espera‑se diferença de complexidade do dossel.

## 4) Evidências & logging
- Para cada rede candidata: AOI, métricas, **IDs de cenas/tiles**, parâmetros e sementes em `logs/evidence_log.jsonl` (via `zexplorer.data_id_logger`).

## 5) Entregáveis
- **Mapas + sobreposições** (ΔdB, HAND, GEDI), **relatório de 2–3 páginas** (PT/EN) e repositório reproduzível.
- CSV dos candidatos (coordenadas ofuscadas ≥1–2 km nos artefatos públicos).

## 6) Cronograma (4 semanas)
- **S1:** Compositos sazonais ALOS‑2 + candidatos por ΔdB (v0).
- **S2:** Plausibilidade hidrodinâmica + poda; registrar evidências.
- **S3:** Extração GEDI WSCI e estatísticas; lista final.
- **S4:** Relatório, revisão ética e README bilíngue.

## 7) Ética
- **Não** publicar coordenadas exatas publicamente; seguir `docs/ETHICS.md` e normas brasileiras (IPHAN, terras indígenas).

## Referências (documentação de dados)
- ALOS‑2 ScanSAR L2.2 (GEE): https://developers.google.com/earth-engine/datasets/catalog/JAXA_ALOS_PALSAR-2_Level2_2_ScanSAR
- GEDI L4C WSCI (UMD/ORNL DAAC): https://gedi.umd.edu/gedi-l4c-footprint-level-waveform-structural-complexity-index-released/
