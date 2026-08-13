(.rag_project) PS F:\Agentic_Project\agentic-rag> Start-Transcript -Path "F:\Agentic_Project\agentic-rag\logs\log_config.txt"
Transcript started, output file is F:\Agentic_Project\agentic-rag\logs\log_config.txt
(.rag_project) PS F:\Agentic_Project\agentic-rag> uvicorn src.agentic_rag.api.main:app --reload                              
INFO:     Will watch for changes in these directories: ['F:\\Agentic_Project\\agentic-rag']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [26016] using WatchFiles
2026-08-13 14:23:18,301 | INFO | LLM provider chain initialized (primary tier): ['openrouter', 'cerebras', 'groq', 'nvidia']
2026-08-13 14:23:18,360 | INFO | LLM provider chain initialized (fast tier): ['openrouter', 'cerebras', 'groq', 'nvidia']
2026-08-13 14:23:21,732 | INFO | No device provided, using cpu
2026-08-13 14:23:22,083 | INFO | HTTP Request: HEAD https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/main/modules.json "HTTP/1.1 307 Temporary Redirect"
Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.
2026-08-13 14:23:22,084 | WARNING | Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.
2026-08-13 14:23:22,128 | INFO | HTTP Request: HEAD https://huggingface.co/api/resolve-cache/models/sentence-transformers/all-MiniLM-L6-v2/1110a243fdf4706b3f48f1d95db1a4f5529b4d41/modules.json "HTTP/1.1 200 OK"
2026-08-13 14:23:22,380 | INFO | HTTP Request: HEAD https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/main/config_sentence_transformers.json "HTTP/1.1 307 Temporary Redirect"
2026-08-13 14:23:22,424 | INFO | HTTP Request: HEAD https://huggingface.co/api/resolve-cache/models/sentence-transformers/all-MiniLM-L6-v2/1110a243fdf4706b3f48f1d95db1a4f5529b4d41/config_sentence_transformers.json "HTTP/1.1 200 OK"
2026-08-13 14:23:22,426 | INFO | Loading SentenceTransformer model from sentence-transformers/all-MiniLM-L6-v2.
2026-08-13 14:23:22,675 | INFO | HTTP Request: HEAD https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/main/config_sentence_transformers.json "HTTP/1.1 307 Temporary Redirect"
2026-08-13 14:23:22,720 | INFO | HTTP Request: HEAD https://huggingface.co/api/resolve-cache/models/sentence-transformers/all-MiniLM-L6-v2/1110a243fdf4706b3f48f1d95db1a4f5529b4d41/config_sentence_transformers.json "HTTP/1.1 200 OK"
2026-08-13 14:23:22,970 | INFO | HTTP Request: HEAD https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/main/README.md "HTTP/1.1 307 Temporary Redirect"
2026-08-13 14:23:23,015 | INFO | HTTP Request: HEAD https://huggingface.co/api/resolve-cache/models/sentence-transformers/all-MiniLM-L6-v2/1110a243fdf4706b3f48f1d95db1a4f5529b4d41/README.md "HTTP/1.1 200 OK"
2026-08-13 14:23:23,269 | INFO | HTTP Request: HEAD https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/main/modules.json "HTTP/1.1 307 Temporary Redirect"
2026-08-13 14:23:23,314 | INFO | HTTP Request: HEAD https://huggingface.co/api/resolve-cache/models/sentence-transformers/all-MiniLM-L6-v2/1110a243fdf4706b3f48f1d95db1a4f5529b4d41/modules.json "HTTP/1.1 200 OK"
2026-08-13 14:23:23,567 | INFO | HTTP Request: HEAD https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/main/sentence_bert_config.json "HTTP/1.1 307 Temporary Redirect"
2026-08-13 14:23:23,611 | INFO | HTTP Request: HEAD https://huggingface.co/api/resolve-cache/models/sentence-transformers/all-MiniLM-L6-v2/1110a243fdf4706b3f48f1d95db1a4f5529b4d41/sentence_bert_config.json "HTTP/1.1 200 OK"
2026-08-13 14:23:23,864 | INFO | HTTP Request: HEAD https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/main/adapter_config.json "HTTP/1.1 404 Not Found"
2026-08-13 14:23:24,117 | INFO | HTTP Request: HEAD https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/main/config.json "HTTP/1.1 307 Temporary Redirect"
2026-08-13 14:23:24,161 | INFO | HTTP Request: HEAD https://huggingface.co/api/resolve-cache/models/sentence-transformers/all-MiniLM-L6-v2/1110a243fdf4706b3f48f1d95db1a4f5529b4d41/config.json "HTTP/1.1 200 OK"
Loading weights: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 103/103 [00:00<00:00, 7763.74it/s]
2026-08-13 14:23:24,543 | INFO | HTTP Request: HEAD https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/main/processor_config.json "HTTP/1.1 404 Not Found"
2026-08-13 14:23:24,802 | INFO | HTTP Request: HEAD https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/main/preprocessor_config.json "HTTP/1.1 404 Not Found"
2026-08-13 14:23:25,057 | INFO | HTTP Request: HEAD https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/main/video_preprocessor_config.json "HTTP/1.1 404 Not Found"
2026-08-13 14:23:25,312 | INFO | HTTP Request: HEAD https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/main/preprocessor_config.json "HTTP/1.1 404 Not Found"
2026-08-13 14:23:25,562 | INFO | HTTP Request: HEAD https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/main/tokenizer_config.json "HTTP/1.1 307 Temporary Redirect"
2026-08-13 14:23:25,608 | INFO | HTTP Request: HEAD https://huggingface.co/api/resolve-cache/models/sentence-transformers/all-MiniLM-L6-v2/1110a243fdf4706b3f48f1d95db1a4f5529b4d41/tokenizer_config.json "HTTP/1.1 200 OK"
2026-08-13 14:23:25,862 | INFO | HTTP Request: HEAD https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/main/config.json "HTTP/1.1 307 Temporary Redirect"
2026-08-13 14:23:25,905 | INFO | HTTP Request: HEAD https://huggingface.co/api/resolve-cache/models/sentence-transformers/all-MiniLM-L6-v2/1110a243fdf4706b3f48f1d95db1a4f5529b4d41/config.json "HTTP/1.1 200 OK"
2026-08-13 14:23:26,156 | INFO | HTTP Request: HEAD https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/main/config.json "HTTP/1.1 307 Temporary Redirect"
2026-08-13 14:23:26,200 | INFO | HTTP Request: HEAD https://huggingface.co/api/resolve-cache/models/sentence-transformers/all-MiniLM-L6-v2/1110a243fdf4706b3f48f1d95db1a4f5529b4d41/config.json "HTTP/1.1 200 OK"
2026-08-13 14:23:26,558 | INFO | HTTP Request: HEAD https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/main/tokenizer_config.json "HTTP/1.1 307 Temporary Redirect"
2026-08-13 14:23:26,602 | INFO | HTTP Request: HEAD https://huggingface.co/api/resolve-cache/models/sentence-transformers/all-MiniLM-L6-v2/1110a243fdf4706b3f48f1d95db1a4f5529b4d41/tokenizer_config.json "HTTP/1.1 200 OK"
2026-08-13 14:23:26,862 | INFO | HTTP Request: GET https://huggingface.co/api/models/sentence-transformers/all-MiniLM-L6-v2/tree/main/additional_chat_templates?recursive=false&expand=false "HTTP/1.1 404 Not Found"
2026-08-13 14:23:27,119 | INFO | HTTP Request: GET https://huggingface.co/api/models/sentence-transformers/all-MiniLM-L6-v2/tree/main?recursive=true&expand=false "HTTP/1.1 200 OK"
2026-08-13 14:23:27,408 | INFO | HTTP Request: HEAD https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/main/1_Pooling/config.json "HTTP/1.1 307 Temporary Redirect"
2026-08-13 14:23:27,453 | INFO | HTTP Request: HEAD https://huggingface.co/api/resolve-cache/models/sentence-transformers/all-MiniLM-L6-v2/1110a243fdf4706b3f48f1d95db1a4f5529b4d41/1_Pooling%2Fconfig.json "HTTP/1.1 200 OK"
2026-08-13 14:23:27,707 | INFO | HTTP Request: GET https://huggingface.co/api/models/sentence-transformers/all-MiniLM-L6-v2 "HTTP/1.1 200 OK"
INFO:     Started server process [18220]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:62862 - "GET /documents HTTP/1.1" 200 OK
INFO:     127.0.0.1:62963 - "GET /documents HTTP/1.1" 200 OK

======================================================================
QUERY INTENT
======================================================================
Question: What is the main topic of the document?
Intent: new_question
Control query: False
[TIMING] contextualize_question             0.00 sec

======================================================================
GRAPH ROUTER: AFTER CONTEXTUALIZATION
======================================================================
Query intent: new_question
ROUTE -> retrieve
2026-08-13 14:23:42,806 | INFO | [route_after_contextualization] query_intent='new_question' | decision='retrieve'

======================================================================
2. RETRIEVAL
======================================================================
Query sent to retriever:
What is the main topic of the document?
Document scope: 8354069b86193aa9d4c6f88b576443523f00ad68b9637711ad9f801869ffa1b2

Overview chunks retrieved: 1
Content chunks retrieved: 5

------------------------------------------------------------
DOCUMENT 1
Similarity score: 0.351621687
Metadata: {'creationdate': '', 'creator': 'PyPDF', 'document_id': '8354069b86193aa9d4c6f88b576443523f00ad68b9637711ad9f801869ffa1b2', 'filename': 'AI_Engineering_2025Book.pdf', 'page': 122.0, 'page_label': '123', 'producer': 'PyPDF', 'source': 'AI_Engineering_2025Book.pdf', 'total_pages': 300.0, 'type': 'content'}

Content preview:
DailyDoseofDS.com    As shown above:  First, we deﬁne two chunks (the two paragraphs in purple).  Next, paragraph 1 is further split into smaller chunks.  Unlike ﬁxed-size chunks, this approach also maintains the natural ﬂow of  language and preserves complete ideas.  However, there is some extra overhead in terms of implementation and  computational complexity.  4) Document structure-based chunking    It utilizes the inherent structure of documents, like headings, sections, or  paragraphs, to d

------------------------------------------------------------
DOCUMENT 2
Similarity score: 0.343752891
Metadata: {'creationdate': '', 'creator': 'PyPDF', 'document_id': '8354069b86193aa9d4c6f88b576443523f00ad68b9637711ad9f801869ffa1b2', 'filename': 'AI_Engineering_2025Book.pdf', 'page': 178.0, 'page_label': '179', 'producer': 'PyPDF', 'source': 'AI_Engineering_2025Book.pdf', 'total_pages': 300.0, 'type': 'content'}

Content preview:
DailyDoseofDS.com      ● A Filtering Agent scans the retrieved papers, identifying the most relevant  ones based on citation count, publication date, and keywords.        ● A Summarization Agent extracts key insights and condenses them into an  easy-to-read report.      ● A Formatting Agent structures the ﬁnal report, ensuring it follows a clear,  professional layout.  178

------------------------------------------------------------
DOCUMENT 3
Similarity score: 0.319090873
Metadata: {'creationdate': '', 'creator': 'PyPDF', 'document_id': '8354069b86193aa9d4c6f88b576443523f00ad68b9637711ad9f801869ffa1b2', 'filename': 'AI_Engineering_2025Book.pdf', 'page': 1.0, 'page_label': '2', 'producer': 'PyPDF', 'source': 'AI_Engineering_2025Book.pdf', 'total_pages': 300.0, 'type': 'content'}

Content preview:
DailyDoseofDS.com  How to make the most out of  this book and your time?  The reading time of this book is about 20 hours. But not all chapters will be of  relevance to you. This 2-minute assessment will test your current expertise and  recommend chapters that will be most useful to you.    Scan the QR code below or open this link to start the assessment. It will only take  2 minutes to complete.      https://bit.ly/ai-engg-assessment  1

------------------------------------------------------------
DOCUMENT 4
Similarity score: 0.317609787
Metadata: {'creationdate': '', 'creator': 'PyPDF', 'document_id': '8354069b86193aa9d4c6f88b576443523f00ad68b9637711ad9f801869ffa1b2', 'filename': 'AI_Engineering_2025Book.pdf', 'page': 119.0, 'page_label': '120', 'producer': 'PyPDF', 'source': 'AI_Engineering_2025Book.pdf', 'total_pages': 300.0, 'type': 'content'}

Content preview:
DailyDoseofDS.com  Since the additional document(s) can be large, step 1 also involves chunking,  wherein a large document is divided into smaller/manageable pieces.  This step is crucial since it ensures the text ﬁts the input size of the embedding  model.  Here are ﬁve chunking strategies for RAG:    Let’s understand them!  1) Fixed-size chunking  119

------------------------------------------------------------
DOCUMENT 5
Similarity score: 0.270604163
Metadata: {'creationdate': '', 'creator': 'PyPDF', 'document_id': '8354069b86193aa9d4c6f88b576443523f00ad68b9637711ad9f801869ffa1b2', 'filename': 'AI_Engineering_2025Book.pdf', 'page': 8.0, 'page_label': '9', 'producer': 'PyPDF', 'source': 'AI_Engineering_2025Book.pdf', 'total_pages': 300.0, 'type': 'content'}

Content preview:
DailyDoseofDS.com    With enough exposure, the model becomes remarkably good at continuing any  piece of text in a coherent, meaningful way.  At the technical level, an LLM processes text in small units called tokens. A  token may be a word, part of a word or even punctuation.    The model looks at the tokens so far and predicts the next one. Repeating this  process generates full answers, explanations, or code.  Everything an LLM does from summarizing a document, generating a function or  expla

------------------------------------------------------------
DOCUMENT 6
Similarity score: 0.170393
Metadata: {'document_id': '8354069b86193aa9d4c6f88b576443523f00ad68b9637711ad9f801869ffa1b2', 'filename': 'AI_Engineering_2025Book.pdf', 'source': 'AI_Engineering_2025Book.pdf', 'type': 'overview'}

Content preview:
This document covers the main subject of AI Engineering, specifically focusing on System Design Patterns for Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), and AI Agents. The document is structured into various sections and chapters, including introductions to LLMs, RAG, and AI Agents, as well as more advanced topics such as fine-tuning, prompt engineering, and context engineering. The scope of the document appears to be comprehensive, covering both theoretical and practical
2026-08-13 14:23:46,195 | INFO | RETRIEVAL | query='What is the main topic of the document?' | scores=[0.3516, 0.3438, 0.3191, 0.3176, 0.2706, 0.1704] | top=0.3516 | second=0.3438 | gap=0.0079 | mean=0.2955 | top/mean=1.1899 | gap_ratio=0.0224
[TIMING] retrieve                           3.39 sec

======================================================================
3. RETRIEVAL ASSESSMENT
======================================================================
Top score: 0.3516
Second score: 0.3438
Top/mean ratio: 1.1899
Gap ratio: 0.0224
Top document type: content
Overview dominant: False
Evidence strength: strong
Retrieval decision: generate
Decision reason: strong_score_distribution
[TIMING] assess_retrieval                   0.00 sec

======================================================================
GRAPH ROUTER: AFTER RETRIEVAL ASSESSMENT
======================================================================
Retrieval decision: generate
ROUTE -> generate
2026-08-13 14:23:46,198 | INFO | [route_after_retrieval_assessment] retrieval_decision='generate' | decision='generate'

======================================================================
6. GENERATION
======================================================================
Context characters : 3392
History characters : 4
Prompt characters  : 3891
Documents supplied : 6
History turns      : 0
2026-08-13 14:23:46,199 | INFO | [LLM:primary] Attempt 1/4 → openrouter
2026-08-13 14:23:49,562 | INFO | [LLM:primary] openrouter → SUCCESS
Output characters  : 184
[TIMING] generate                           3.36 sec

======================================================================
7. HALLUCINATION CHECK
======================================================================
2026-08-13 14:23:49,563 | INFO | [LLM:fast] Attempt 1/4 → openrouter
2026-08-13 14:23:49,998 | INFO | [LLM:fast] openrouter → SUCCESS
[TIMING] check_hallucination                0.44 sec

======================================================================
GRAPH ROUTER: AFTER HALLUCINATION CHECK
======================================================================
Hallucination grade: grounded
Retry count: 0
Maximum retries: 2
ROUTE -> record_turn
2026-08-13 14:23:49,999 | INFO | [route_after_hallucination_check] hallucination_grade='grounded' | retry_count='0' | decision='end'

======================================================================
8. RECORD TURN
======================================================================

======================================================================
STRUCTURED TRACE SUMMARY (full request, end to end)
======================================================================
[
  {
    "stage": "check_hallucination",
    "raw_grade": "grounded",
    "normalized_grade": "grounded",
    "hallucination_retry_count": 0
  },
  {
    "stage": "record_turn",
    "final_route": "end",
    "retry_count": 0,
    "retrieval_decision": "generate",
    "retrieval_evidence_strength": "strong",
    "retrieval_decision_reason": "strong_score_distribution"
  }
]

======================================================================
PERFORMANCE SUMMARY
======================================================================
contextualize_question            0.00 sec (  0.0%) [1 call(s)]
retrieve                          3.39 sec ( 47.1%) [1 call(s)]
assess_retrieval                  0.00 sec (  0.0%) [1 call(s)]
generate                          3.36 sec ( 46.8%) [1 call(s)]
check_hallucination               0.44 sec (  6.1%) [1 call(s)]
----------------------------------------------------------------------
TOTAL                             7.19 sec

BOTTLENECK: retrieve
BOTTLENECK TIME: 3.39 sec
======================================================================
INFO:     127.0.0.1:62963 - "POST /query HTTP/1.1" 200 OK
INFO:     127.0.0.1:63216 - "GET /documents HTTP/1.1" 200 OK

======================================================================
QUERY INTENT
======================================================================
Question: Can you elaborate further on that?
Intent: follow_up
Control query: False
2026-08-13 14:24:04,115 | INFO | [LLM:fast] Attempt 1/4 → openrouter
2026-08-13 14:24:05,350 | INFO | [LLM:fast] openrouter → SUCCESS
[TIMING] contextualize_question             1.24 sec

======================================================================
GRAPH ROUTER: AFTER CONTEXTUALIZATION
======================================================================
Query intent: follow_up
ROUTE -> retrieve
2026-08-13 14:24:05,351 | INFO | [route_after_contextualization] query_intent='follow_up' | decision='retrieve'

======================================================================
2. RETRIEVAL
======================================================================
Query sent to retriever:
What is a detailed explanation of System Design Patterns for Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), and AI Agents in the context of AI Engineering?
Document scope: 8354069b86193aa9d4c6f88b576443523f00ad68b9637711ad9f801869ffa1b2

Overview chunks retrieved: 1
Content chunks retrieved: 5

------------------------------------------------------------
DOCUMENT 1
Similarity score: 0.797829628
Metadata: {'document_id': '8354069b86193aa9d4c6f88b576443523f00ad68b9637711ad9f801869ffa1b2', 'filename': 'AI_Engineering_2025Book.pdf', 'source': 'AI_Engineering_2025Book.pdf', 'type': 'overview'}

Content preview:
This document covers the main subject of AI Engineering, specifically focusing on System Design Patterns for Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), and AI Agents. The document is structured into various sections and chapters, including introductions to LLMs, RAG, and AI Agents, as well as more advanced topics such as fine-tuning, prompt engineering, and context engineering. The scope of the document appears to be comprehensive, covering both theoretical and practical

------------------------------------------------------------
DOCUMENT 2
Similarity score: 0.676486075
Metadata: {'creationdate': '', 'creator': 'PyPDF', 'document_id': '8354069b86193aa9d4c6f88b576443523f00ad68b9637711ad9f801869ffa1b2', 'filename': 'AI_Engineering_2025Book.pdf', 'page': 181.0, 'page_label': '182', 'producer': 'PyPDF', 'source': 'AI_Engineering_2025Book.pdf', 'total_pages': 300.0, 'type': 'content'}

Content preview:
DailyDoseofDS.com  RAG (Retrieval-Augmented Generation)  RAG enhances an LLM by retrieving external documents (from a vector DB,  search engine, etc.) and feeding them into the LLM as context before generating  a response.    RAG makes the LLM aware of updated, relevant info without retraining.  Agent  An Agent adds autonomy to the mix.    It doesn’t just answer a question—it decides what steps to take:  Should it call a tool? Search the web? Summarize? Store info?  An Agent uses an LLM, calls t

------------------------------------------------------------
DOCUMENT 3
Similarity score: 0.626716614
Metadata: {'creationdate': '', 'creator': 'PyPDF', 'document_id': '8354069b86193aa9d4c6f88b576443523f00ad68b9637711ad9f801869ffa1b2', 'filename': 'AI_Engineering_2025Book.pdf', 'page': 199.0, 'page_label': '200', 'producer': 'PyPDF', 'source': 'AI_Engineering_2025Book.pdf', 'total_pages': 300.0, 'type': 'content'}

Content preview:
DailyDoseofDS.com  ● User Memory  Each serves a unique purpose in helping agents “remember” and utilize past  information.  To simulate memory, the system has to manage context explicitly: choosing what  to keep, what to discard, and what to retrieve before each new model call.    This is why memory is not a property of the model itself. It is a system design  problem.  5 Agentic AI Design Patterns  Agentic behaviors allow LLMs to reﬁne their output by incorporating  self-evaluation, planning, a

------------------------------------------------------------
DOCUMENT 4
Similarity score: 0.611985266
Metadata: {'creationdate': '', 'creator': 'PyPDF', 'document_id': '8354069b86193aa9d4c6f88b576443523f00ad68b9637711ad9f801869ffa1b2', 'filename': 'AI_Engineering_2025Book.pdf', 'page': 0.0, 'page_label': '1', 'producer': 'PyPDF', 'source': 'AI_Engineering_2025Book.pdf', 'total_pages': 300.0, 'type': 'content'}

Content preview:
FREE AI Engineering 2025 EDITION Akshay Pachaar & Avi Chawla DailyDoseofDS.com Daily Dose of Data Science System Design Patterns for LLMs, RAG and Agents

------------------------------------------------------------
DOCUMENT 5
Similarity score: 0.602832317
Metadata: {'creationdate': '', 'creator': 'PyPDF', 'document_id': '8354069b86193aa9d4c6f88b576443523f00ad68b9637711ad9f801869ffa1b2', 'filename': 'AI_Engineering_2025Book.pdf', 'page': 156.0, 'page_label': '157', 'producer': 'PyPDF', 'source': 'AI_Engineering_2025Book.pdf', 'total_pages': 300.0, 'type': 'content'}

Content preview:
DailyDoseofDS.com  6 Types of Contexts for AI  Agents  A poor LLM can possibly work with an appropriate context, but a SOTA LLM  can never make up for an incomplete context.  That is why production-grade LLM apps don’t just need instructions but rather  structure, which is the full ecosystem of context that deﬁnes their reasoning,  memory, and decision loops.  And all advanced agent architectures now treat context as a multi-dimensional  design layer, not a line in a prompt.  Here’s the mental m

------------------------------------------------------------
DOCUMENT 6
Similarity score: 0.599497318
Metadata: {'creationdate': '', 'creator': 'PyPDF', 'document_id': '8354069b86193aa9d4c6f88b576443523f00ad68b9637711ad9f801869ffa1b2', 'filename': 'AI_Engineering_2025Book.pdf', 'page': 241.0, 'page_label': '242', 'producer': 'PyPDF', 'source': 'AI_Engineering_2025Book.pdf', 'total_pages': 300.0, 'type': 'content'}

Content preview:
DailyDoseofDS.com  At the core, you have LLMs like GPT, DeepSeek, etc.  Core concepts here:  ● Tokenization & inference parameters: how text is broken into tokens and  processed by the model.  ● Prompt engineering: designing inputs to get better outputs.  ● LLM APIs: programmatic interfaces to interact with the model.  This is the engine that powers everything else.  2) AI Agents (built on LLMs)  Agents wrap around LLMs to give them the ability to act autonomously.  Key responsibilities:  ● Tool
2026-08-13 14:24:07,609 | INFO | RETRIEVAL | query='What is a detailed explanation of System Design Patterns for Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), and AI Agents in the context of AI Engineering?' | scores=[0.7978, 0.6765, 0.6267, 0.612, 0.6028, 0.5995] | top=0.7978 | second=0.6765 | gap=0.1213 | mean=0.6526 | top/mean=1.2226 | gap_ratio=0.1521
[TIMING] retrieve                           2.26 sec

======================================================================
3. RETRIEVAL ASSESSMENT
======================================================================
Top score: 0.7978
Second score: 0.6765
Top/mean ratio: 1.2226
Gap ratio: 0.1521
Top document type: overview
Overview dominant: True
Evidence strength: strong
Retrieval decision: generate
Decision reason: overview_dominant_with_clear_margin
[TIMING] assess_retrieval                   0.00 sec

======================================================================
GRAPH ROUTER: AFTER RETRIEVAL ASSESSMENT
======================================================================
Retrieval decision: generate
ROUTE -> generate
2026-08-13 14:24:07,612 | INFO | [route_after_retrieval_assessment] retrieval_decision='generate' | decision='generate'

======================================================================
6. GENERATION
======================================================================
Context characters : 4324
History characters : 235
Prompt characters  : 5049
Documents supplied : 6
History turns      : 2
2026-08-13 14:24:07,614 | INFO | [LLM:primary] Attempt 1/4 → openrouter
2026-08-13 14:24:10,025 | INFO | [LLM:primary] openrouter → SUCCESS
Output characters  : 2254
[TIMING] generate                           2.41 sec

======================================================================
7. HALLUCINATION CHECK
======================================================================
2026-08-13 14:24:10,026 | INFO | [LLM:fast] Attempt 1/4 → openrouter
2026-08-13 14:24:10,537 | INFO | [LLM:fast] openrouter → SUCCESS
[TIMING] check_hallucination                0.51 sec

======================================================================
GRAPH ROUTER: AFTER HALLUCINATION CHECK
======================================================================
Hallucination grade: grounded
Retry count: 0
Maximum retries: 2
ROUTE -> record_turn
2026-08-13 14:24:10,539 | INFO | [route_after_hallucination_check] hallucination_grade='grounded' | retry_count='0' | decision='end'

======================================================================
8. RECORD TURN
======================================================================

======================================================================
STRUCTURED TRACE SUMMARY (full request, end to end)
======================================================================
[
  {
    "stage": "check_hallucination",
    "raw_grade": "grounded",
    "normalized_grade": "grounded",
    "hallucination_retry_count": 0
  },
  {
    "final_route": "end",
    "retry_count": 0,
    "retrieval_decision": "generate",
    "retrieval_evidence_strength": "strong",
    "retrieval_decision_reason": "overview_dominant_with_clear_margin"
  }
]

======================================================================
PERFORMANCE SUMMARY
======================================================================
contextualize_question            1.24 sec (  9.1%) [2 call(s)]
    └─ Run #1                         0.00 sec
    └─ Run #2                         1.24 sec
retrieve                          5.64 sec ( 41.5%) [2 call(s)]
    └─ Run #1                         3.39 sec
    └─ Run #2                         2.26 sec
assess_retrieval                  0.00 sec (  0.0%) [2 call(s)]
    └─ Run #1                         0.00 sec
    └─ Run #2                         0.00 sec
generate                          5.78 sec ( 42.4%) [2 call(s)]
    └─ Run #1                         3.36 sec
    └─ Run #2                         2.41 sec
check_hallucination               0.95 sec (  7.0%) [2 call(s)]
    └─ Run #1                         0.44 sec
    └─ Run #2                         0.51 sec
----------------------------------------------------------------------
TOTAL                            13.61 sec

BOTTLENECK: generate
BOTTLENECK TIME: 5.78 sec
======================================================================
INFO:     127.0.0.1:63216 - "POST /query HTTP/1.1" 200 OK
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [18220]
INFO:     Stopping reloader process [26016]
(.rag_project) PS F:\Agentic_Project\agentic-rag> Stop-Transcript                                                            
Transcript stopped, output file is F:\Agentic_Project\agentic-rag\logs\log_config.txt
(.rag_project) PS F:\Agentic_Project\agentic-rag> 












































