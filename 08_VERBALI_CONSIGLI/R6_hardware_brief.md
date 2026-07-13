# R6 — Brief: hardware per la produzione (Mac e alternative)

**Data verifica: 13 luglio 2026.** Contesto critico: da fine 2025 è in corso una **crisi mondiale delle memorie DRAM** (domanda dei datacenter AI). Apple ha **tagliato le configurazioni RAM alte** (maggio 2026) e **aumentato i listini** anche in Italia (27 giugno 2026, Mac +15-20%). I prezzi sotto sono quelli correnti ma **volatili**; i tempi di consegna del Mac Studio erano a 9-10 settimane a maggio 2026 — rilevante se l'acquisto deve avvenire prima di S6.

## Lineup Apple corrente e prezzi (verificati)

**Mac Mini (ottobre 2024, ancora attuale):** solo chip **M4 e M4 Pro**. Confermato: **non esiste Mac Mini con M4 Max**. Per la crisi DRAM Apple ha **rimosso** le opzioni 32 GB (M4) e **64 GB (M4 Pro)** e il taglio SSD 256 GB:

| Config | RAM disponibile | Prezzo Italia (lug 2026) |
|---|---|---|
| M4 16 GB / 512 GB | 16 o 24 GB | **979 €** |
| M4 24 GB / 512 GB | — | ~1.209 € (base + upgrade RAM ~230 €, da confermare a configuratore) |
| M4 Pro 24 GB / 512 GB | 24 o 48 GB (max) | **1.929 €** (era 1.679 €) |
| M4 Pro 48 GB / 512 GB | — | ~2.389 € (upgrade storico +460 €, da riverificare) |

**Mac Studio (marzo 2025, ancora attuale):** **M4 Max** e **M3 Ultra**. **Non esiste M4 Ultra.** Il taglio M3 Ultra 256/512 GB è stato **ritirato dal listino**: resta solo 96 GB.

| Config | Prezzo Italia (lug 2026) |
|---|---|
| M4 Max (14-core) 36 GB / 512 GB | **3.049 €** (era ~2.549 €) |
| M3 Ultra 96 GB / 1 TB | **6.399 €** |

**Novità 2025-2026:** M5 base esiste (MacBook Pro, ott. 2025); **M5 Pro e M5 Max** sono usciti a **marzo 2026 ma solo sui MacBook Pro** (M5 Max: ~614 GB/s). **Mac Mini M5 e Mac Studio M5 Max/Ultra sono attesi entro fine 2026 ma non ancora usciti** — aspettarli è un rischio calendario incompatibile con "acquisto prima di S6".

## Banda di memoria e prestazioni LLM reali

La generazione token è limitata dalla **banda di memoria**; il prompt processing dalla GPU (punto debole di Apple vs NVIDIA su contesti lunghi, es. RAG/OCR).

| Chip | Banda | 27B Q4 (tok/s) | 70B Q4 (tok/s) |
|---|---|---|---|
| M4 | 120 GB/s | **~4-5 (stima)** — sotto soglia | non entra |
| M4 Pro | 273 GB/s | **8-9 GGUF / 14-15 MLX** (misurati, Gemma 3 27B) | non entra |
| M4 Max | 546 GB/s (410 binned 36 GB) | ~25-30 | **12,5** llama.cpp / **17,2** Ollama (misurati) |
| M3 Ultra | 819 GB/s | ~40+ | ~15-20 (stime community); **gpt-oss-120B ~60 tok/s** (misurato, MLX 8-bit) |

**Regola pratica (>10 tok/s):** M4 base → solo ≤14B; **M4 Pro → fino a 27-32B Q4 (con MLX)**; M4 Max → fino a 70B Q4 al limite; M3 Ultra → 70B comodo + MoE giganti. **Il documento attuale ("Mac Mini M4 24 GB") ha quindi due problemi: il 27B Q4 girerebbe a ~4-5 tok/s (frustrante) e il taglio 32 GB non è più ordinabile.**

## RAM necessaria per classe di modello (tabella)

Pesi Q4 + KV cache (2-6 GB secondo contesto) + stack gestionale/OCR/embedding (~4-6 GB) + macOS (~4-6 GB). Nota: macOS limita la memoria GPU "wired" a ~75% della RAM (alzabile via `sysctl`, con cautela).

| Modello | Pesi Q4 | RAM minima sensata | Su lineup attuale |
|---|---|---|---|
| 27B Q4 (Gemma 3) | ~16-17 GB | 32 GB (24 GB = al pelo, contesto corto) | **M4 Pro 48 GB** (il 32 GB non esiste più) |
| 32B Q4 (Qwen) | ~19-20 GB | 48 GB | M4 Pro 48 GB |
| 70B Q4 | ~40-43 GB | 64 GB | **Mac Studio** (Mini max 48 GB): M4 Max 64 GB+ o M3 Ultra 96 GB |
| gpt-oss-120B MoE (MXFP4) | ~61-66 GB | 96 GB | M3 Ultra 96 GB |

## Alternative non-Apple e costi nascosti

| Opzione | Prezzo | LLM | Note |
|---|---|---|---|
| **Ryzen AI Max+ 395 "Strix Halo" 128 GB** (Framework Desktop ~2.000 $, ~2.300-2.600 € EU; GMKtec EVO-X2 ~1.500-2.000 $) | ~2.000-2.600 € | Banda ~256 GB/s (reali ~215): 70B dense Q4 **solo ~5 tok/s**; eccellente sui **MoE** (Qwen3-30B MoE 66-72 tok/s, gpt-oss-120B ~30-40) | 65-120 W sotto carico, silenzioso; richiede Linux (Vulkan/ROCm) |
| **NVIDIA DGX Spark** 128 GB | **4.699 $** (rincarato da 3.999 $, feb. 2026) | gpt-oss-120B ~38 tok/s; 70B dense limitato dalla banda (273 GB/s) | Strumento da sviluppatore (DGX OS/Ubuntu), non da ufficio |
| **PC + RTX 4090/5090** (24-32 GB VRAM) | 2.500-4.000 €+ (GPU gonfiate dalla crisi memorie) | 27-32B Q4 **velocissimi** (30-60+ tok/s); **70B Q4 non entra in VRAM** | Rumore, ingombro, idle 60-100 W |

**Costo nascosto di lasciare macOS** (gli ADR ci sono costruiti sopra): riscrivere launchd→systemd, Keychain→secret-service, FileVault→LUKS, strategia backup; e soprattutto **amministrare Linux/Windows in un'agenzia senza IT interno**. Stima onesta: giorni di rilavorazione ADR/setup + rischio operativo permanente. LibreOffice e Ollama girano ovunque; PaddleOCR-VL anzi va meglio su CUDA. Ma il TCO "umano" pende nettamente verso il Mac per questo utente.

## Consumo elettrico 24/7

Uso reale: idle quasi sempre, burst LLM di una persona. A 0,25-0,30 €/kWh:

| Macchina | Idle / Max (dati Apple + misure) | kWh/anno stimati | Costo/anno |
|---|---|---|---|
| Mac Mini M4 / M4 Pro | ~4-5 W / 65-140 W | 60-100 | **~17-30 €** |
| Mac Studio (M4 Max / M3 Ultra) | ~8-11 W / 270-480 W | 110-180 | ~30-55 € |
| Strix Halo mini-PC | ~10-15 W / 120-170 W | 120-200 | ~35-60 € |
| PC con GPU dedicata | 60-100 W a riposo / 450-600 W | 550-900 | **~150-270 €** |

Il PC con GPU costa da solo ~120-220 €/anno più del Mini: in 5 anni ~600-1.100 € di differenza.

## Configurazioni candidate (2-3, con pro/contro)

**A. Minima — Mac Mini M4 Pro 24 GB / 512 GB — 1.929 €.** Il 27B Q4 gira a ~14 tok/s con MLX, ma con gestionale+OCR attivi la RAM è al pelo: contesto corto, o ripiego su 12-14B. Pro: prezzo, consumi irrisori, zero rilavorazione ADR. Contro: nessun margine di crescita; il "vorrei modelli più grandi" del proprietario resta insoddisfatto.

**B. Consigliata dai dati — Mac Mini M4 Pro 48 GB / 512 GB (o 1 TB) — ~2.400-2.600 €.** 27B/32B Q4 comodi (>10-15 tok/s via MLX) con tutto lo stack residente e contesti decenti; MoE classe 30B veloci. Contro: 70B dense escluso per sempre (RAM saldata); prezzo da riconfermare al configuratore dopo i rincari.

**C. Esagerata — Mac Studio M3 Ultra 96 GB / 1 TB — 6.399 €.** Unica via Apple oggi per 70B Q4 fluido (~15-20 tok/s) e gpt-oss-120B (~60 tok/s). Contro: 2,7× il prezzo della B, consegna 9-10 settimane (ordinare subito se scelta), potenza sprecata per 200 contratti.

*Wild card fuori ADR:* Strix Halo 128 GB a ~2.000-2.600 € offre più RAM del Mac Studio a un terzo del prezzo, ma solo per MoE, e comporta l'abbandono di macOS — contraddice gli ADR, va eventualmente rimessa al consiglio come revisione formale.

**Incertezze dichiarate:** listini e disponibilità RAM cambiano di mese in mese (due tagli config e un rincaro negli ultimi 90 giorni); i tok/s variano ±30% tra backend (MLX vs GGUF), quantizzazioni e lunghezza contesto; i prezzi upgrade RAM Apple post-rincaro non sono pubblicati nelle fonti e vanno letti sul configuratore. La decisione resta al consiglio/proprietario.

## Fonti (URL verificati)

- Lineup/roundup Mac Mini: https://www.macrumors.com/roundup/mac-mini/
- Rincaro Mac Mini M4 Pro (giu 2026): https://www.macrumors.com/2026/06/25/apple-hikes-m4-pro-mac-mini-starting-price/
- Tagli RAM Mac Mini/Studio (mag 2026): https://www.macrumors.com/2026/05/05/apple-mac-studio-mac-mini-ram-cuts/ ; https://appleinsider.com/articles/26/05/05/apple-culls-more-high-end-mac-mini-mac-studio-configs
- Nuovi listini Italia (27 giu 2026): https://www.ispazio.net/2241246/apple-aumento-prezzi-mac-ipad-italia-nuovi-listini ; https://www.tomshw.it/hardware/macbook-air-costa-200eur-in-piu-la-crisi-ha-colpito-anche-apple-2026-06-25
- M5 Pro/Max (solo MacBook Pro, mar 2026): https://www.apple.com/newsroom/2026/03/apple-debuts-m5-pro-and-m5-max-to-supercharge-the-most-demanding-pro-workflows/
- Attese Mac Studio/Mini M5: https://www.macworld.com/article/2973459/2026-mac-studio-m5-release-date-specs-price-rumors.html ; https://www.macworld.com/article/2964754/2026-mac-mini-m5-pro-design-specs-release-date.html
- Banda memoria chip: https://en.wikipedia.org/wiki/Apple_M4 ; https://www.apple.com/mac-studio/specs/ ; https://support.apple.com/en-us/122211
- Benchmark llama.cpp Apple Silicon: https://github.com/ggml-org/llama.cpp/discussions/4167 ; https://markaicode.com/benchmarks/llamacpp-m4-max-benchmark/ ; https://forums.macrumors.com/threads/mac-studio-m3-ultra-96gb-28-60-llm-performance.2456559/ ; https://siliconscore.com/models/gpt-oss-120b/
- Strix Halo: https://llm-tracker.info/AMD-Strix-Halo-(Ryzen-AI-Max+-395)-GPU-Performance ; https://forum.level1techs.com/t/strix-halo-ryzen-ai-max-395-llm-benchmark-results/233796
- DGX Spark: https://github.com/ggml-org/llama.cpp/discussions/16578 ; https://intuitionlabs.ai/articles/nvidia-dgx-spark-review
- Consumi: https://support.apple.com/en-us/103253 (Mac Mini) ; https://support.apple.com/en-us/102027 (Mac Studio) ; https://www.jeffgeerling.com/blog/2024/m4-mac-minis-efficiency-incredible/
