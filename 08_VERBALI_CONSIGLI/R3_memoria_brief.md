# R3 — Brief: memoria personale locale per JARVIS

*Verificato via web il 13/07/2026. Nessuna prova hands-on: tutte le affermazioni derivano da repo/doc ufficiali fetchati direttamente.*

## Verifica del nome «Graphify»

**Esistono due progetti distinti, ed è probabile una confusione.**

1. **Graphify** (Graphify-Labs/graphify) esiste davvero — ma **non è una memoria personale**. Descrizione verbatim del repo: *"AI coding assistant skill (Claude Code, Codex, …). Turn any folder of code, SQL schemas, R scripts, shell scripts, docs, papers, images, or videos into a queryable knowledge graph."* È uno strumento che trasforma **codebase e documenti** in un knowledge graph per assistenti di coding (parsing locale via tree-sitter, output `graph.json`/`graph.html`). MIT, Python, ~84k stelle, release v0.9.14 del 13/07/2026: progetto vivo e popolare, ma risolve un problema diverso (comprensione di repository di codice, non "ricordare ciò che mi dice il proprietario").
2. **Graphiti** (getzep/graphiti) è quasi certamente ciò che il proprietario intendeva: *"a framework for building and querying temporal context graphs for AI agents"*. Apache-2.0, ~28,7k stelle, manutenzione attiva (v0.29.2, giugno 2026). **Requisiti pesanti**: serve un graph database esterno — Neo4j 5.26+ (default) o FalkorDB 1.1.2+ (Kuzu, l'opzione embedded, è *deprecated* perché il progetto upstream non è più mantenuto). Sul fronte LLM il README avverte esplicitamente: *"Graphiti works best with LLM services that support Structured Output… Using other services may result in incorrect output schemas and ingestion failures. This is particularly problematic when using smaller models"* e, per i modelli locali: *"Very small models frequently emit JSON that doesn't match the requested schema."* Con un 27B Q4 via Ollama funzionerebbe forse, ma è dichiaratamente zona a rischio.

**Conclusione della verifica**: nessuno dei due è "un local RAG per memoria personale" chiavi in mano. Graphify è fuori tema; Graphiti è in tema ma richiede Neo4j/FalkorDB sempre acceso — un servizio in più da mantenere per anni sul Mac Mini.

## Panorama opzioni (tabella comparativa)

| Progetto | Licenza | Dipendenze/servizi | Italiano | Maturità | Complessità operativa (anni, no-ops) |
|---|---|---|---|---|---|
| **Graphiti** (getzep) | Apache-2.0 | Neo4j 5.26+ o FalkorDB (servizio separato); LLM con structured output | dipende dall'LLM | Alta, attivissimo | **Alta**: DB grafo da amministrare; fragile con LLM piccoli |
| **GraphRAG** (Microsoft) | MIT | Pipeline batch LLM-intensiva; README: *"indexing can be an expensive operation"* | dipende dall'LLM | Alta (v3.1.0, mag 2026) | **Alta**: re-indicizzazione batch, pensato per corpora, non per memoria incrementale |
| **LightRAG** (HKUDS) | MIT | Default file-based *"only for development"*; produzione = Postgres/Neo4j/ecc. Doc: *"higher capability requirements for LLMs… complex entity-relation extraction"* | dipende dall'LLM | Alta (37,6k ★, v1.5.4 giu 2026) | **Media-alta**: molte parti mobili |
| **mem0** (OSS) | Apache-2.0 | Da fine 2025/2026 **niente più graph DB esterno**: *"replaced by built-in graph memory (entity linking), which runs natively with no external dependencies"*; vector store configurabile; Ollama supportato | dipende da LLM/embedding | Alta (60,7k ★, release lug 2026) | **Media**: framework in evoluzione rapida (breaking change 2026); divergenza OSS/piattaforma cloud |
| **Letta** (ex MemGPT) | Apache-2.0 | Server + Docker; nota nel repo: sviluppo attivo **spostato su altro repo** (server "legacy") | dipende dall'LLM | Media-alta ma in transizione | **Alta**: un server-agente intero per una sola persona |
| **sqlite-vec** | MIT/Apache-2.0 | *"pure C, no dependencies, runs anywhere SQLite runs"*; estensione in-process | n/a (vettori) | v0.1.9 (mar 2026), *"pre-v1, expect breaking changes"* | **Bassissima**: un file, dentro il DB già esistente |
| **Chroma** | Apache-2.0 | Embedded in-process con persistenza (`pip install chromadb`); core Rust | n/a | Alta (28,8k ★, v1.5.9 mag 2026) | **Bassa**, ma è comunque una dipendenza grossa per ciò che serve |
| **"Noiosa": SQLite FTS5 + embedding Ollama** | dominio pubblico (SQLite) | Zero nuove dipendenze oltre a un modello embedding (es. `bge-m3`, 1,2 GB, *"more than 100 working languages"*) | **Sì**, con accortezze (v. sotto) | SQLite: la cosa più matura che esista | **Minima** |

**Nota italiano/FTS5** (verificata su sqlite.org): lo stemmer `porter` di FTS5 è *"designed for use with English language terms only"*. Per l'italiano: tokenizer `unicode61` (default, senza stemming) o `trigram` per substring matching; lo stemming italiano richiederebbe un'estensione snowball esterna. In pratica: FTS5 per keyword + embedding multilingue (bge-m3) per la semantica coprono bene l'italiano.

## Quando il knowledge graph paga (e quando no)

- **Paga** per domande *globali* e *multi-hop* su corpora grandi. Microsoft stessa delimita il campo: baseline RAG fallisce quando serve *"traversing disparate pieces of information through their shared attributes"* o *"holistically understand summarized semantic concepts over large data collections"*.
- **Non paga** per il recupero puntuale di fatti personali. Il paper di mem0 (arXiv 2504.19413) sul benchmark LoCoMo è il dato più onesto: la variante a grafo Mem0g batte la variante vettoriale di **poco** (J-score 68,44 vs 66,88), vincendo sul ragionamento temporale ma con latenza superiore (p50 ~1,09s vs ~0,71s) e più token. E il segnale operativo più forte è che **mem0 stessa nel 2026 ha rimosso il supporto ai graph store esterni** dall'SDK open-source, sostituendolo con semplice entity linking su vector store.
- **Dimensionamento onesto**: per UN utente con qualche migliaio di ricordi, una scansione KNN esaustiva in sqlite-vec è questione di millisecondi; non c'è alcun problema di scala che giustifichi Neo4j. Il ragionamento temporale ("cosa mi aveva detto prima che cambiasse idea?") — l'unico punto forte reale del grafo — si ottiene in modo noioso con colonne `valid_from`/`superseded_by` in SQLite.

## Pattern per il filtro dei ricordi

Pattern reali, verificati nei progetti citati:

1. **Estrazione fatti a due fasi** (paper mem0): un LLM estrae fatti candidati dalla conversazione; una seconda fase li confronta con i ricordi simili esistenti e decide ADD/UPDATE/DELETE/NOOP. Nota: nel 2026 mem0 ha **semplificato** a estrazione single-pass ADD-only (*"one LLM call, no UPDATE/DELETE. Memories accumulate; nothing is overwritten"*) — un'ammissione che la pipeline complessa non pagava.
2. **Invalidazione invece di cancellazione** (Graphiti/Zep, arXiv 2501.13956): ogni fatto ha `valid_at`/`invalid_at`; un fatto nuovo contraddittorio *invalida* il vecchio senza cancellarlo, preservando la storia. Replicabile con due colonne data in SQLite.
3. **TTL / scadenza** (mem0 Platform, doc "Expiration Date"): parametro `expiration_date` per ricordi a tempo ("l'appuntamento di martedì"); scaduti, escono dal retrieval ma restano archiviati.
4. **Categorie + auto-gestione** (Letta): memoria organizzata in *memory blocks* etichettati (*"structured sections of the agent's context window… always visible"*) che l'agente auto-modifica, più memoria archiviale recuperabile.
5. **Conferma umana**: nessun framework la impone, ma per un utente non tecnico è il filtro più robusto: l'LLM propone "Vuoi che ricordi: *X*?" e salva solo su conferma (un tap). Elimina alla radice il problema dei falsi ricordi da estrazione LLM — il rischio principale con un 27B Q4.

## Candidati raccomandabili (2-3, con pro/contro — decide il consiglio)

1. **Soluzione noiosa: tabella `ricordi` in SQLite + FTS5 + sqlite-vec + embedding bge-m3 via Ollama, con estrazione LLM e conferma umana.** Pro: zero servizi nuovi, backup = già il backup del DB, ricerca ibrida keyword+semantica, italiano coperto, sopravvive anni senza manutenzione. Contro: sqlite-vec è pre-v1 (breaking changes possibili — mitigabile fissando la versione); il filtro va scritto in casa (~poche centinaia di righe).
2. **mem0 OSS in modalità locale (Ollama + vector store locale).** Pro: pipeline di estrazione/retrieval già pronta, Apache-2.0, ora senza graph DB esterno, progetto vivissimo. Contro: framework che cambia in fretta (breaking change nel 2026), superficie di dipendenze molto maggiore del necessario per un utente singolo, benchmark dichiarati sulla piattaforma cloud non identici all'OSS.
3. **Graphiti — solo se il consiglio valuta indispensabile il grafo temporale.** Pro: il modello bi-temporale più maturo sul mercato, Apache-2.0, MCP server disponibile. Contro: Neo4j/FalkorDB da tenere accesi per anni; avvertenza ufficiale contro LLM piccoli/structured output fragile → rischio concreto con 27B Q4; sovradimensionato per migliaia di ricordi di una persona.

**Incertezze dichiarate**: numeri di stelle/release letti oggi da GitHub (volatili); non ho testato la qualità di estrazione del 27B Q4 in italiano (da validare con un pilota); il confronto Mem0/Mem0g è del vendor stesso, seppur pubblicato su arXiv.

## Fonti (URL verificati)

- https://github.com/Graphify-Labs/graphify — Graphify (code KG, MIT)
- https://github.com/getzep/graphiti — Graphiti (Apache-2.0, requisiti Neo4j/FalkorDB, warning LLM piccoli)
- https://github.com/mem0ai/mem0 e https://docs.mem0.ai/open-source/graph_memory/overview — mem0, rimozione graph store esterni
- https://docs.mem0.ai/platform/features/expiration-date — TTL ricordi
- https://arxiv.org/abs/2504.19413 — paper mem0, LoCoMo (Mem0 vs Mem0g)
- https://arxiv.org/html/2501.13956v1 — Zep, grafo temporale / invalidazione fatti
- https://github.com/HKUDS/LightRAG — LightRAG (MIT, requisiti LLM)
- https://github.com/microsoft/graphrag e https://www.microsoft.com/en-us/research/blog/graphrag-unlocking-llm-discovery-on-narrative-private-data/ — GraphRAG, costi e casi d'uso
- https://github.com/asg017/sqlite-vec — sqlite-vec (pre-v1, zero dipendenze)
- https://github.com/chroma-core/chroma — Chroma (Apache-2.0, embedded)
- https://github.com/letta-ai/letta e https://docs.letta.com/guides/agents/memory-blocks — Letta/MemGPT, memory blocks
- https://sqlite.org/fts5.html — FTS5, porter English-only, trigram
- https://ollama.com/library/bge-m3 — embedding multilingue via Ollama
