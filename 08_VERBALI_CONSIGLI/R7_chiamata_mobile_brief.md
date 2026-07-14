# BRIEF RICERCA R7 — Modalità Chiamata JARVIS, versione mobile, Tailscale (fatti verificati con fonti)

> A supporto del Consiglio C9. Ricerca web condotta il 2026-07-13. Distingue **fatti verificati** da ipotesi. Il vincolo di riferimento è: tutto-locale sul **Mac Mini M4 24GB Apple Silicon (nessuna GPU NVIDIA)**, stack "noioso", nessuna dipendenza senza permesso.

## 1. Orchestrazione voce realtime — i due tool proposti
- **NVIDIA/personaplex**: NON è un orchestratore, è un **modello speech-to-speech full-duplex** (base Moshi/Kyutai), monolitico, PyTorch+CUDA, **richiede GPU NVIDIA**. Ufficialmente **non gira su Apple Silicon** (solo port community MLX/Swift non mantenuti da NVIDIA). Non collega Ollama/whisper/Piper (sistema end-to-end). Codice MIT, **pesi sotto NVIDIA Open Model License**. ~10,2k★, nessuna release (solo commit), modello 7B (gen 2026). → **incompatibile** con hardware, architettura, RAM e igiene di licenza del progetto.
- **livekit/agents**: **vero framework di orchestrazione** (Python, **Apache-2.0**), compone STT+LLM+TTS come plugin sostituibili; supporta **Ollama, whisper self-hosted, Piper locali**; **gira su Apple Silicon, nessuna dipendenza NVIDIA**. ~11,4k★, v1.6.5 (lug 2026), molto attivo. Prezzo: richiede un **media server LiveKit (WebRTC) sempre attivo** = secondo servizio pesante. → dei due è **nettamente il migliore**, ma sovradimensionato per 1 utente vocale su rete privata.
- **Alternativa**: **Pipecat** (BSD-2, ~13,4k★, v1.5.0 lug 2026) più leggero per un agente locale single-user; e l'opzione **"nessun framework"** (glue custom whisper.cpp+Ollama+Piper, latenza community ~1–1,5s con LLM 8B). I pattern HITL/turn-detection di LiveKit **si copiano, non si installano**.
- Fonti: github.com/NVIDIA/personaplex; huggingface.co/nvidia/personaplex-7b-v1; github.com/livekit/agents; docs.livekit.io/agents/models/llm/plugins/ollama; github.com/pipecat-ai/pipecat.

## 2. STT / TTS locali su Apple Silicon con ITALIANO
- **STT**: `whisper.cpp` (MIT, v1.8.6 giu 2026, Core ML/ANE, ottimo italiano su Apple Silicon) — maturo, cross-platform. `WhisperKit` (Argmax, MIT, Swift/CoreML, **streaming reale ~0,45s**) ideale per una call mode nativa. `faster-whisper` **sconsigliato su Mac** (CTranslate2 senza buon backend Metal → gira su CPU). Nativo Apple **SpeechTranscriber/SpeechAnalyzer** (iOS 26 / macOS Tahoe): on-device, it_IT, **~2,2× più veloce di Whisper Large V3 Turbo** in test indipendenti — ma richiede macOS 26 + helper Swift.
- **TTS italiano**: `say`/**AVSpeechSynthesizer** nativo (voci Premium it_IT, gratis anche commerciale, zero dipendenze); **Piper** voce `it_IT-paola` (realtime CPU; **repo MIT archiviato, binari GPL-3.0** → usare solo come processo esterno, mai linkato; verificare la licenza della singola voce); **Kokoro-82M** (pesi **Apache-2.0**, MLX oltre realtime). **XTTS v2 / Coqui: ESCLUSO** — licenza **CPML non commerciale**, azienda chiusa, nessuno da cui comprare licenza.
- Combo raccomandate dalla ricerca: (A) nativa Apple SpeechTranscriber+AVSpeech (più semplice, ma macOS 26); (B) WhisperKit+AVSpeech/Piper (streaming a bassa latenza, Swift); (C) whisper.cpp+Kokoro (interamente MIT/Apache, cross-platform).
- Fonti: github.com/ggml-org/whisper.cpp; promptquorum.com/.../local-whisper-stt-comparison-2026; arxiv.org/abs/2507.10860; github.com/Blaizzy/mlx-audio.

## 3. Sicurezza / backup DB locale — databasement
- **David-Crty/databasement**: **NON** è un backup tool leggero — è una **web app self-hosted Laravel/PHP via Docker**, backup manager centralizzato per **flotte** di DB eterogenei (MySQL/PG/Mongo/…), con UI web, agent remoti, S3/SFTP, MCP. MIT, attivo (v1.6.2 lug 2026, ~1,1k★). Gira su Mac solo **dentro Docker**. → per un **singolo SQLite locale** duplica ADR-06 aggiungendo stack e superficie d'attacco. **Scartare.**
- **Litestream** (Apache-2.0, binario Go arm64): **colma un buco reale** — replica **continua** del WAL vs gli snapshot schedulati di ADR-06 (riduce la finestra di perdita dati). Candidato per un **ADR separato** solo se servisse RPO di secondi.
- **SQLCipher** (BSD-3 + Community): **in gran parte ridondante** — ADR-06 ha già FileVault (at-rest) + offsite cifrato.
- **Default raccomandato: nessun tool aggiuntivo, basta ADR-06.**
- Fonti: github.com/David-Crty/databasement; github.com/benbjohnson/litestream; simonwillison.net/2025/Oct/3/litestream.

## 4. UI e animazioni — bklit-ui, anime.js, orb/waveform
- **bklit/bklit-ui**: registry di componenti **chart per React/Next via shadcn**. Doppio mismatch: il frontend è **server-rendered FastAPI senza React**, e sono **grafici, non orb/waveform**. **Scartare.**
- **anime.js** (v4.5.0 giu 2026, **MIT**, ~10KB gzip, vanilla, 70,9k★): libreria sana e usabile senza framework, **ma non necessaria**.
- **Waveform voce in ingresso**: **Web Audio `AnalyserNode` + Canvas 2D**, **zero dipendenze** (getUserMedia + getByteTimeDomainData). `wavesurfer.js` è per file audio, sovradimensionato.
- **Orb "Jarvis che parla"**: CSS custom property `--level` pilotata dall'**RMS dello stesso AnalyserNode**, zero dipendenze; `siriwave` (MIT, Canvas, no-dep, fermo al 2023) solo se serve l'estetica Siri esatta.
- **Conclusione: nativo (AnalyserNode + Canvas + CSS).** Ordine di eventuale rientro con permesso: nativo → siriwave → anime.js. L'animazione è **rifinitura finale**, non requisito.
- Fonti: github.com/bklit/bklit-ui; github.com/juliangarnier/anime; github.com/kopiro/siriwave; github.com/katspaugh/wavesurfer.js.

## 5. Accesso remoto sicuro + conferma vocale (HITL)
- **Accesso remoto**: la soluzione corretta per "usarlo alla guida" senza esporre il Mac né spostare dati in cloud è una **VPN mesh**. **Tailscale** (WireGuard, mesh P2P, chiavi private mai fuori dal device, traffico **E2E**): **niente port-forwarding, Mac mai esposto a Internet**, IP stabile `100.x`, client Apple Silicon nativo. Trade-off: **control-plane cloud proprietario** (vede metadati/topologia, relay DERP per il traffico cifrato, **mai i dati**). Massima sovranità: **Headscale/NetBird/WireGuard puro** (control-plane self-hosted) — più manutenzione, un endpoint da esporre.
- **Conferma vocale sicura (HITL)**: unico pattern che soddisfa ADR-07/34 = **gate di scrittura NEL CODICE** (token di approvazione generabile solo dalla UI dopo il render del diff, non forgiabile dall'LLM — "security boundaries belong in code, not in prompts"), **read-back verbale** dei campi chiave per le azioni consultive, e **scritture solo in coda con approvazione a video**. La trascrizione vocale è **input non fidato** (come le email IMAP di S10).
- Fonti: tailscale.com/use-cases/remote-access; tailscale.com/compare/wireguard; appleinsider.com/.../tailscale-remotely-connect-mac; comparitech.com/.../tailscale-vs-wireguard.

## Sintesi operativa per il Consiglio
Nessuno dei 5 tool proposti va adottato così com'è: 4 scartati, `livekit/agents` tenuto solo come **riferimento di pattern**. Lo stack vocale locale "noioso" è **whisper.cpp + Ollama (27B già residente) + TTS italiano scelto con demo audio**, orchestrato da **glue custom on-demand dentro FastAPI**, senza secondo servizio sempre acceso. Mobile = **PWA responsive** sullo stesso FastAPI. Accesso = **Tailscale** (deroga dichiarata + hardening). Voce = **input non fidato**, scritture **mai** a voce.
