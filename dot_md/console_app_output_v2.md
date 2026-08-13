\]

\======================================================================  
PERFORMANCE SUMMARY  
\======================================================================  
contextualize\_question            0.00 sec (  0.0%) \[1 call(s)\]  
retrieve                          3.26 sec ( 54.5%) \[1 call(s)\]  
assess\_retrieval                  0.00 sec (  0.0%) \[1 call(s)\]  
generate                          2.28 sec ( 38.1%) \[1 call(s)\]  
check\_hallucination               0.44 sec (  7.4%) \[1 call(s)\]  
\----------------------------------------------------------------------  
TOTAL                             5.98 sec

BOTTLENECK: retrieve  
BOTTLENECK TIME: 3.26 sec  
\======================================================================  
INFO:     127.0.0.1:57251 \- "POST /query HTTP/1.1" 200 OK  
INFO:     127.0.0.1:57688 \- "GET /documents HTTP/1.1" 200 OK  
2026-08-12 16:47:47,517 | INFO | \[LLM:fast\] Attempt 1/4 → openrouter  
2026-08-12 16:47:48,635 | INFO | HTTP Request: POST https://openrouter.ai/api/v1/chat/completions "HTTP/1.1 200 OK"  
2026-08-12 16:47:48,855 | INFO | \[LLM:fast\] openrouter → SUCCESS  
\[TIMING\] contextualize\_question             1.34 sec

\======================================================================  
2\. RETRIEVAL  
\======================================================================  
Query sent to retriever:  
What are the factors affecting Explainable AI and designing and implementing explainable machine learning solutions?  
Document scope: 92f92d40c9b94deefa0d98d0c384a0402755d69cf7485641513fc8bbeb968d21

Overview chunks retrieved: 1  
Content chunks retrieved: 5

\------------------------------------------------------------  
DOCUMENT 1  
Similarity score: 0.801272452  
Metadata: {'document\_id': '92f92d40c9b94deefa0d98d0c384a0402755d69cf7485641513fc8bbeb968d21', 'filename': 'Explainable-AI-for-Practitioners.pdf', 'source': 'Explainable-AI-for-Practitioners.pdf', 'type': 'overview'}

Content preview:  
This document covers the topic of Explainable AI for practitioners, focusing on designing and implementing explainable machine learning solutions. The excerpt provided appears to be from the first chapter, "An Overview of Explainability", which introduces the concept of explainability in AI and its importance. The chapter discusses the history of explainability, the different types of explanations, and the various consumers of explainability, including practitioners, observers, and end-users. Th

\------------------------------------------------------------  
DOCUMENT 2  
Similarity score: 0.78797543  
Metadata: {'author': 'Michael Munn & David Pitman', 'creationdate': '2023-02-11T09:02:57+00:00', 'creator': 'calibre 2.55.0 \[http://calibre-ebook.com\]', 'document\_id': '92f92d40c9b94deefa0d98d0c384a0402755d69cf7485641513fc8bbeb968d21', 'filename': 'Explainable-AI-for-Practitioners.pdf', 'moddate': '2023-02-11T10:04:57+01:00', 'page': 4.0, 'page\_label': '5', 'producer': '3-Heights(TM) PDF Optimization Shell 5.9.1.5 (http://www.pdf-tools.com)', 'source': 'Explainable-AI-for-Practitioners.pdf', 'title': 'Explainable AI for Practitioners', 'total\_pages': 74.0, 'type': 'content'}

Content preview:  
Chapter 1\.      An      Overview        of      Explainability A        NOTE    FOR     EARLY   RELEASE READERS With    Early   Release ebooks, you     get     books   in      their   earliest form—the        author’s        raw     and     unedited content        as      they    write—so        you     can     take    advantage       of      these   technologies    long     before  the     official release        of      these   titles. This    will    be      the     2nd     chapter of      the     final   book.   Please  note    that    the     GitHub   repo    will    be      made    active later    on. If  you     have    comments        about   how     we      might   improve the     content and/or  examples        in      this     book,   or      if you  n

\------------------------------------------------------------  
DOCUMENT 3  
Similarity score: 0.76118958  
Metadata: {'author': 'Michael Munn & David Pitman', 'creationdate': '2023-02-11T09:02:57+00:00', 'creator': 'calibre 2.55.0 \[http://calibre-ebook.com\]', 'document\_id': '92f92d40c9b94deefa0d98d0c384a0402755d69cf7485641513fc8bbeb968d21', 'filename': 'Explainable-AI-for-Practitioners.pdf', 'moddate': '2023-02-11T10:04:57+01:00', 'page': 5.0, 'page\_label': '6', 'producer': '3-Heights(TM) PDF Optimization Shell 5.9.1.5 (http://www.pdf-tools.com)', 'source': 'Explainable-AI-for-Practitioners.pdf', 'title': 'Explainable AI for Practitioners', 'total\_pages': 74.0, 'type': 'content'}

Content preview:  
techniques      so      you     can     assess  which   will    best    suit    your    audience’s      needs.  In      Chapter 7,      we      will    go      into more       detail  about    how     to      build   good    experiences     for     these   different       audiences       with    explainability. More    broadly,        we      can     think   of      anyone   as      a       consumer        of      an      explanation.    The     ML      system  is      presenting additional   information     to      help    a       human   perceivewhat     is      unique  about   the     circumstances   of      a       prediction, comprehend  how     the     ML      system  behaves,        and,    ultimately,     be      able    to       extrapolate     to      what    could   infl

\------------------------------------------------------------  
DOCUMENT 4  
Similarity score: 0.729804099  
Metadata: {'author': 'Michael Munn & David Pitman', 'creationdate': '2023-02-11T09:02:57+00:00', 'creator': 'calibre 2.55.0 \[http://calibre-ebook.com\]', 'document\_id': '92f92d40c9b94deefa0d98d0c384a0402755d69cf7485641513fc8bbeb968d21', 'filename': 'Explainable-AI-for-Practitioners.pdf', 'moddate': '2023-02-11T10:04:57+01:00', 'page': 6.0, 'page\_label': '7', 'producer': '3-Heights(TM) PDF Optimization Shell 5.9.1.5 (http://www.pdf-tools.com)', 'source': 'Explainable-AI-for-Practitioners.pdf', 'title': 'Explainable AI for Practitioners', 'total\_pages': 74.0, 'type': 'content'}

Content preview:  
be      machine learning        algorithms.     Although        very    sophisticated,  these   techniques      are     all     “dumb”  in      the sense       that    we      cannot  interact with    them    in      a       two-way dialogue.       A       smart   explainability  technique       could adapt     to      our     queries,        learning        how     to       guide   us      towards the     best    explanation,    or      answer  the     question        we didn’t       know    we      were    asking. For     now,    if      we      want     to      try     and     obtain  more    information     about   a       prediction, the best    we      can     do      is      to      change  the     parameters      of      our      explanation     request,        or      try     a       differen

\------------------------------------------------------------  
DOCUMENT 5  
Similarity score: 0.725931227  
Metadata: {'author': 'Michael Munn & David Pitman', 'creationdate': '2023-02-11T09:02:57+00:00', 'creator': 'calibre 2.55.0 \[http://calibre-ebook.com\]', 'document\_id': '92f92d40c9b94deefa0d98d0c384a0402755d69cf7485641513fc8bbeb968d21', 'filename': 'Explainable-AI-for-Practitioners.pdf', 'moddate': '2023-02-11T10:04:57+01:00', 'page': 4.0, 'page\_label': '5', 'producer': '3-Heights(TM) PDF Optimization Shell 5.9.1.5 (http://www.pdf-tools.com)', 'source': 'Explainable-AI-for-Practitioners.pdf', 'title': 'Explainable AI for Practitioners', 'total\_pages': 74.0, 'type': 'content'}

Content preview:  
researchers     focused on      surviving       the     first   AI      winter  by      turning to      techniques      that    were    “explainable” because   they    relied  solely  on       statistical     techniques      that    were    well-proven     in      other   fields. Explainability in       its     modern  form    (and    what    we      largely focus   on       in      this    book)   was     revived,        now     as      a       distinct        field   of research,    in      the     mid     2010s   in      response        to      the      persistent      question        of      “this   model   works   really  well…   but how?” In    just    a       few     years,  the     field   has     gone    from    obscurityto      one     of      intense inter

\------------------------------------------------------------  
DOCUMENT 6  
Similarity score: 0.718055785  
Metadata: {'author': 'Michael Munn & David Pitman', 'creationdate': '2023-02-11T09:02:57+00:00', 'creator': 'calibre 2.55.0 \[http://calibre-ebook.com\]', 'document\_id': '92f92d40c9b94deefa0d98d0c384a0402755d69cf7485641513fc8bbeb968d21', 'filename': 'Explainable-AI-for-Practitioners.pdf', 'moddate': '2023-02-11T10:04:57+01:00', 'page': 22.0, 'page\_label': '23', 'producer': '3-Heights(TM) PDF Optimization Shell 5.9.1.5 (http://www.pdf-tools.com)', 'source': 'Explainable-AI-for-Practitioners.pdf', 'title': 'Explainable AI for Practitioners', 'total\_pages': 74.0, 'type': 'content'}

Content preview:  
Summary In      this    chapter we      gave    a       high    level   overview        of      the     main    ideas   you     are     likely  to      consider        as      a practitioner   developing      explainable     ML      solutions.      We      started by      discussing      what    explanations    and     how an  explanation     may     change  dependingon      the     audience        (e.g.   ML      Engineer        vs      Business        Stakeholders    vs Users).      Each    of      these   groups  have    distinct        needs   and      thus    will    interact        with    explanations    in      their   own way. We     then    discussed       the     different       types   of      common  explainability  techniques,      providing       a       si  
2026-08-12 16:47:51,105 | INFO | RETRIEVAL | query='What are the factors affecting Explainable AI and designing and implementing explainable machine learning solutions?' | scores=\[0.8013, 0.788, 0.7612, 0.7298, 0.7259, 0.7181\] | top=0.8013 | second=0.7880 | gap=0.0133 | mean=0.7540 | top/mean=1.0626 | gap\_ratio=0.0166  
\[TIMING\] retrieve                           2.25 sec

\======================================================================  
3\. RETRIEVAL ASSESSMENT  
\======================================================================  
Top score: 0.8013  
Second score: 0.7880  
Top/mean ratio: 1.0626  
Gap ratio: 0.0166  
Top document type: overview  
Overview dominant: False  
Evidence strength: ambiguous  
Retrieval decision: grade  
Decision reason: top\_candidates\_too\_close  
\[TIMING\] assess\_retrieval                   0.00 sec

\======================================================================  
GRAPH ROUTER: AFTER RETRIEVAL ASSESSMENT  
\======================================================================  
Retrieval decision: grade  
ROUTE \-\> grade\_documents  
2026-08-12 16:47:51,107 | INFO | \[route\_after\_retrieval\_assessment\] retrieval\_decision='grade' | decision='grade\_documents'

\======================================================================  
4\. DOCUMENT RELEVANCE GRADING  
\======================================================================  
Question/query being graded:  
What are the factors affecting Explainable AI and designing and implementing explainable machine learning solutions?  
Candidates sent to grader: 4  
2026-08-12 16:47:51,109 | INFO | \[LLM:fast\] Attempt 1/4 → openrouter  
2026-08-12 16:47:51,491 | INFO | HTTP Request: POST https://openrouter.ai/api/v1/chat/completions "HTTP/1.1 200 OK"  
2026-08-12 16:47:51,555 | INFO | \[LLM:fast\] openrouter → SUCCESS

Raw LLM grading response: relevant

Normalized relevance grade: relevant  
\[TIMING\] grade\_documents                    0.45 sec

\======================================================================  
GRAPH ROUTER: AFTER DOCUMENT GRADING  
\======================================================================  
Relevance grade: relevant  
Retry count: 0  
Maximum retries: 2  
ROUTE \-\> generate  
2026-08-12 16:47:51,556 | INFO | \[route\_after\_grading\] relevance\_grade='relevant' | retry\_count='0' | decision='generate'

\======================================================================  
6\. GENERATION  
\======================================================================  
2026-08-12 16:47:51,557 | INFO | \[LLM:primary\] Attempt 1/4 → openrouter  
2026-08-12 16:47:59,802 | INFO | HTTP Request: POST https://openrouter.ai/api/v1/chat/completions "HTTP/1.1 200 OK"  
2026-08-12 16:48:06,132 | INFO | \[LLM:primary\] openrouter → SUCCESS  
\[TIMING\] generate                          14.58 sec

\======================================================================  
7\. HALLUCINATION CHECK  
\======================================================================  
2026-08-12 16:48:06,134 | INFO | \[LLM:fast\] Attempt 1/4 → openrouter  
2026-08-12 16:48:06,600 | INFO | HTTP Request: POST https://openrouter.ai/api/v1/chat/completions "HTTP/1.1 200 OK"  
2026-08-12 16:48:06,713 | INFO | \[LLM:fast\] openrouter → SUCCESS  
\[TIMING\] check\_hallucination                0.58 sec

\======================================================================  
GRAPH ROUTER: AFTER HALLUCINATION CHECK  
\======================================================================  
Hallucination grade: grounded  
Retry count: 0  
Maximum retries: 2  
ROUTE \-\> record\_turn  
2026-08-12 16:48:06,714 | INFO | \[route\_after\_hallucination\_check\] hallucination\_grade='grounded' | retry\_count='0' | decision='end'

\======================================================================  
8\. RECORD TURN  
\======================================================================

\======================================================================  
STRUCTURED TRACE SUMMARY (full request, end to end)  
\======================================================================  
\[  
  {  
    "stage": "check\_hallucination",  
    "raw\_grade": "grounded",  
    "normalized\_grade": "grounded",  
    "hallucination\_retry\_count": 0  
  },  
  {  
    "stage": "record\_turn",  
    "final\_route": "end",  
    "retry\_count": 0,  
    "retrieval\_decision": "grade",  
    "retrieval\_evidence\_strength": "ambiguous",  
    "retrieval\_decision\_reason": "top\_candidates\_too\_close"  
  }  
\]

\======================================================================  
PERFORMANCE SUMMARY  
\======================================================================  
contextualize\_question            1.34 sec (  5.3%) \[2 call(s)\]  
    └─ Run \#1                         0.00 sec  
    └─ Run \#2                         1.34 sec  
retrieve                          5.51 sec ( 21.9%) \[2 call(s)\]  
    └─ Run \#1                         3.26 sec  
    └─ Run \#2                         2.25 sec  
assess\_retrieval                  0.00 sec (  0.0%) \[2 call(s)\]  
    └─ Run \#1                         0.00 sec  
    └─ Run \#2                         0.00 sec  
generate                         16.85 sec ( 66.9%) \[2 call(s)\]  
    └─ Run \#1                         2.28 sec  
    └─ Run \#2                        14.58 sec  
check\_hallucination               1.02 sec (  4.1%) \[2 call(s)\]  
    └─ Run \#1                         0.44 sec  
    └─ Run \#2                         0.58 sec  
grade\_documents                   0.45 sec (  1.8%) \[1 call(s)\]  
\----------------------------------------------------------------------  
TOTAL                            25.17 sec

BOTTLENECK: generate  
BOTTLENECK TIME: 16.85 sec  
\======================================================================  
INFO:     127.0.0.1:57688 \- "POST /query HTTP/1.1" 200 OK  
INFO:     127.0.0.1:58040 \- "GET /documents HTTP/1.1" 200 OK  
2026-08-12 16:48:16,324 | INFO | \[LLM:fast\] Attempt 1/4 → openrouter  
2026-08-12 16:48:16,981 | INFO | HTTP Request: POST https://openrouter.ai/api/v1/chat/completions "HTTP/1.1 200 OK"  
2026-08-12 16:48:17,291 | INFO | \[LLM:fast\] openrouter → SUCCESS  
\[TIMING\] contextualize\_question             0.97 sec

\======================================================================  
2\. RETRIEVAL  
\======================================================================  
Query sent to retriever:  
What are the key factors affecting Explainable AI discussed in the document?  
Document scope: 92f92d40c9b94deefa0d98d0c384a0402755d69cf7485641513fc8bbeb968d21

Overview chunks retrieved: 1  
Content chunks retrieved: 5

\------------------------------------------------------------  
DOCUMENT 1  
Similarity score: 0.738546431  
Metadata: {'author': 'Michael Munn & David Pitman', 'creationdate': '2023-02-11T09:02:57+00:00', 'creator': 'calibre 2.55.0 \[http://calibre-ebook.com\]', 'document\_id': '92f92d40c9b94deefa0d98d0c384a0402755d69cf7485641513fc8bbeb968d21', 'filename': 'Explainable-AI-for-Practitioners.pdf', 'moddate': '2023-02-11T10:04:57+01:00', 'page': 4.0, 'page\_label': '5', 'producer': '3-Heights(TM) PDF Optimization Shell 5.9.1.5 (http://www.pdf-tools.com)', 'source': 'Explainable-AI-for-Practitioners.pdf', 'title': 'Explainable AI for Practitioners', 'total\_pages': 74.0, 'type': 'content'}

Content preview:  
Chapter 1\.      An      Overview        of      Explainability A        NOTE    FOR     EARLY   RELEASE READERS With    Early   Release ebooks, you     get     books   in      their   earliest form—the        author’s        raw     and     unedited content        as      they    write—so        you     can     take    advantage       of      these   technologies    long     before  the     official release        of      these   titles. This    will    be      the     2nd     chapter of      the     final   book.   Please  note    that    the     GitHub   repo    will    be      made    active later    on. If  you     have    comments        about   how     we      might   improve the     content and/or  examples        in      this     book,   or      if you  n

\------------------------------------------------------------  
DOCUMENT 2  
Similarity score: 0.714777  
Metadata: {'document\_id': '92f92d40c9b94deefa0d98d0c384a0402755d69cf7485641513fc8bbeb968d21', 'filename': 'Explainable-AI-for-Practitioners.pdf', 'source': 'Explainable-AI-for-Practitioners.pdf', 'type': 'overview'}

Content preview:  
This document covers the topic of Explainable AI for practitioners, focusing on designing and implementing explainable machine learning solutions. The excerpt provided appears to be from the first chapter, "An Overview of Explainability", which introduces the concept of explainability in AI and its importance. The chapter discusses the history of explainability, the different types of explanations, and the various consumers of explainability, including practitioners, observers, and end-users. Th

\------------------------------------------------------------  
DOCUMENT 3  
Similarity score: 0.685202658  
Metadata: {'author': 'Michael Munn & David Pitman', 'creationdate': '2023-02-11T09:02:57+00:00', 'creator': 'calibre 2.55.0 \[http://calibre-ebook.com\]', 'document\_id': '92f92d40c9b94deefa0d98d0c384a0402755d69cf7485641513fc8bbeb968d21', 'filename': 'Explainable-AI-for-Practitioners.pdf', 'moddate': '2023-02-11T10:04:57+01:00', 'page': 1.0, 'page\_label': '2', 'producer': '3-Heights(TM) PDF Optimization Shell 5.9.1.5 (http://www.pdf-tools.com)', 'source': 'Explainable-AI-for-Practitioners.pdf', 'title': 'Explainable AI for Practitioners', 'total\_pages': 74.0, 'type': 'content'}

Content preview:  
Explainable     AI      for     Practitioners Designing and     Implementing    Explainable     ML      Solutions With  Early   Release ebooks, you     get     books   in      their   earliest form—the        author’s        raw     and     unedited content        as      they    write—so        you     can     take    advantage       of      these   technologies    long     before  the     official release        of      these   titles. Michael Munn    and     David   Pitman

\------------------------------------------------------------  
DOCUMENT 4  
Similarity score: 0.65599066  
Metadata: {'author': 'Michael Munn & David Pitman', 'creationdate': '2023-02-11T09:02:57+00:00', 'creator': 'calibre 2.55.0 \[http://calibre-ebook.com\]', 'document\_id': '92f92d40c9b94deefa0d98d0c384a0402755d69cf7485641513fc8bbeb968d21', 'filename': 'Explainable-AI-for-Practitioners.pdf', 'moddate': '2023-02-11T10:04:57+01:00', 'page': 4.0, 'page\_label': '5', 'producer': '3-Heights(TM) PDF Optimization Shell 5.9.1.5 (http://www.pdf-tools.com)', 'source': 'Explainable-AI-for-Practitioners.pdf', 'title': 'Explainable AI for Practitioners', 'total\_pages': 74.0, 'type': 'content'}

Content preview:  
researchers     focused on      surviving       the     first   AI      winter  by      turning to      techniques      that    were    “explainable” because   they    relied  solely  on       statistical     techniques      that    were    well-proven     in      other   fields. Explainability in       its     modern  form    (and    what    we      largely focus   on       in      this    book)   was     revived,        now     as      a       distinct        field   of research,    in      the     mid     2010s   in      response        to      the      persistent      question        of      “this   model   works   really  well…   but how?” In    just    a       few     years,  the     field   has     gone    from    obscurityto      one     of      intense inter

\------------------------------------------------------------  
DOCUMENT 5  
Similarity score: 0.641298354  
Metadata: {'author': 'Michael Munn & David Pitman', 'creationdate': '2023-02-11T09:02:57+00:00', 'creator': 'calibre 2.55.0 \[http://calibre-ebook.com\]', 'document\_id': '92f92d40c9b94deefa0d98d0c384a0402755d69cf7485641513fc8bbeb968d21', 'filename': 'Explainable-AI-for-Practitioners.pdf', 'moddate': '2023-02-11T10:04:57+01:00', 'page': 5.0, 'page\_label': '6', 'producer': '3-Heights(TM) PDF Optimization Shell 5.9.1.5 (http://www.pdf-tools.com)', 'source': 'Explainable-AI-for-Practitioners.pdf', 'title': 'Explainable AI for Practitioners', 'total\_pages': 74.0, 'type': 'content'}

Content preview:  
techniques      so      you     can     assess  which   will    best    suit    your    audience’s      needs.  In      Chapter 7,      we      will    go      into more       detail  about    how     to      build   good    experiences     for     these   different       audiences       with    explainability. More    broadly,        we      can     think   of      anyone   as      a       consumer        of      an      explanation.    The     ML      system  is      presenting additional   information     to      help    a       human   perceivewhat     is      unique  about   the     circumstances   of      a       prediction, comprehend  how     the     ML      system  behaves,        and,    ultimately,     be      able    to       extrapolate     to      what    could   infl

\------------------------------------------------------------  
DOCUMENT 6  
Similarity score: 0.585794449  
Metadata: {'author': 'Michael Munn & David Pitman', 'creationdate': '2023-02-11T09:02:57+00:00', 'creator': 'calibre 2.55.0 \[http://calibre-ebook.com\]', 'document\_id': '92f92d40c9b94deefa0d98d0c384a0402755d69cf7485641513fc8bbeb968d21', 'filename': 'Explainable-AI-for-Practitioners.pdf', 'moddate': '2023-02-11T10:04:57+01:00', 'page': 2.0, 'page\_label': '3', 'producer': '3-Heights(TM) PDF Optimization Shell 5.9.1.5 (http://www.pdf-tools.com)', 'source': 'Explainable-AI-for-Practitioners.pdf', 'title': 'Explainable AI for Practitioners', 'total\_pages': 74.0, 'type': 'content'}

Content preview:  
Explainable     AI      for     Practitioners by        Michael Munn    and     David   Pitman Copyright        ©       2022    Michael Munn,   David   Pitman  and     O’Reilly        Media,   Inc.    All     rights  reserved. Printed       in      the     United  States  of      America. Published      by      O’Reilly        Media,  Inc.,   1005    Gravenstein     Highway  North,  Sebastopol,     CA      95472\. O’Reilly books   may     be      purchased       for     educational,    business,       or      sales   promotional     use.    Online  editions are     also    available       for     most    titles  (http://oreilly.com).   For     more    information,    contact our corporate/institutiona  
2026-08-12 16:48:19,539 | INFO | RETRIEVAL | query='What are the key factors affecting Explainable AI discussed in the document?' | scores=\[0.7385, 0.7148, 0.6852, 0.656, 0.6413, 0.5858\] | top=0.7385 | second=0.7148 | gap=0.0238 | mean=0.6703 | top/mean=1.1019 | gap\_ratio=0.0322  
\[TIMING\] retrieve                           2.25 sec

\======================================================================  
3\. RETRIEVAL ASSESSMENT  
\======================================================================  
Top score: 0.7385  
Second score: 0.7148  
Top/mean ratio: 1.1019  
Gap ratio: 0.0322  
Top document type: content  
Overview dominant: False  
Evidence strength: strong  
Retrieval decision: generate  
Decision reason: strong\_score\_distribution  
\[TIMING\] assess\_retrieval                   0.00 sec

\======================================================================  
GRAPH ROUTER: AFTER RETRIEVAL ASSESSMENT  
\======================================================================  
Retrieval decision: generate  
ROUTE \-\> generate  
2026-08-12 16:48:19,541 | INFO | \[route\_after\_retrieval\_assessment\] retrieval\_decision='generate' | decision='generate'

\======================================================================  
6\. GENERATION  
\======================================================================  
2026-08-12 16:48:19,543 | INFO | \[LLM:primary\] Attempt 1/4 → openrouter  
2026-08-12 16:48:20,753 | INFO | HTTP Request: POST https://openrouter.ai/api/v1/chat/completions "HTTP/1.1 200 OK"  
2026-08-12 16:48:21,226 | INFO | \[LLM:primary\] openrouter → SUCCESS  
\[TIMING\] generate                           1.68 sec

\======================================================================  
7\. HALLUCINATION CHECK  
\======================================================================  
2026-08-12 16:48:21,227 | INFO | \[LLM:fast\] Attempt 1/4 → openrouter  
2026-08-12 16:48:21,645 | INFO | HTTP Request: POST https://openrouter.ai/api/v1/chat/completions "HTTP/1.1 200 OK"  
2026-08-12 16:48:21,762 | INFO | \[LLM:fast\] openrouter → SUCCESS  
\[TIMING\] check\_hallucination                0.54 sec

\======================================================================  
GRAPH ROUTER: AFTER HALLUCINATION CHECK  
\======================================================================  
Hallucination grade: grounded  
Retry count: 0  
Maximum retries: 2  
ROUTE \-\> record\_turn  
2026-08-12 16:48:21,763 | INFO | \[route\_after\_hallucination\_check\] hallucination\_grade='grounded' | retry\_count='0' | decision='end'

\======================================================================  
8\. RECORD TURN  
\======================================================================

\======================================================================  
STRUCTURED TRACE SUMMARY (full request, end to end)  
\======================================================================  
\[  
  {  
    "stage": "check\_hallucination",  
    "raw\_grade": "grounded",  
    "normalized\_grade": "grounded",  
    "hallucination\_retry\_count": 0  
  },  
  {  
    "stage": "record\_turn",  
    "final\_route": "end",  
    "retry\_count": 0,  
    "retrieval\_decision": "generate",  
    "retrieval\_evidence\_strength": "strong",  
    "retrieval\_decision\_reason": "strong\_score\_distribution"  
  }  
\]

\======================================================================  
PERFORMANCE SUMMARY  
\======================================================================  
contextualize\_question            2.31 sec (  7.5%) \[3 call(s)\]  
    └─ Run \#1                         0.00 sec  
    └─ Run \#2                         1.34 sec  
    └─ Run \#3                         0.97 sec  
retrieve                          7.76 sec ( 25.3%) \[3 call(s)\]  
    └─ Run \#1                         3.26 sec  
    └─ Run \#2                         2.25 sec  
    └─ Run \#3                         2.25 sec  
assess\_retrieval                  0.00 sec (  0.0%) \[3 call(s)\]  
    └─ Run \#1                         0.00 sec  
    └─ Run \#2                         0.00 sec  
    └─ Run \#3                         0.00 sec  
generate                         18.54 sec ( 60.6%) \[3 call(s)\]  
    └─ Run \#1                         2.28 sec  
    └─ Run \#2                        14.58 sec  
    └─ Run \#3                         1.68 sec  
check\_hallucination               1.56 sec (  5.1%) \[3 call(s)\]  
    └─ Run \#1                         0.44 sec  
    └─ Run \#2                         0.58 sec  
    └─ Run \#3                         0.54 sec  
grade\_documents                   0.45 sec (  1.5%) \[1 call(s)\]  
\----------------------------------------------------------------------  
TOTAL                            30.61 sec

BOTTLENECK: generate  
BOTTLENECK TIME: 18.54 sec  
\======================================================================  
INFO:     127.0.0.1:58040 \- "POST /query HTTP/1.1" 200 OK  
INFO:     127.0.0.1:58040 \- "GET /documents HTTP/1.1" 200 OK  
\[TIMING\] contextualize\_question             0.00 sec

\======================================================================  
2\. RETRIEVAL  
\======================================================================  
Query sent to retriever:  
ENd  
Document scope: 92f92d40c9b94deefa0d98d0c384a0402755d69cf7485641513fc8bbeb968d21

Overview chunks retrieved: 1  
Content chunks retrieved: 5

\------------------------------------------------------------  
DOCUMENT 1  
Similarity score: 0.148048401  
Metadata: {'document\_id': '92f92d40c9b94deefa0d98d0c384a0402755d69cf7485641513fc8bbeb968d21', 'filename': 'Explainable-AI-for-Practitioners.pdf', 'source': 'Explainable-AI-for-Practitioners.pdf', 'type': 'overview'}

Content preview:  
This document covers the topic of Explainable AI for practitioners, focusing on designing and implementing explainable machine learning solutions. The excerpt provided appears to be from the first chapter, "An Overview of Explainability", which introduces the concept of explainability in AI and its importance. The chapter discusses the history of explainability, the different types of explanations, and the various consumers of explainability, including practitioners, observers, and end-users. Th

\------------------------------------------------------------  
DOCUMENT 2  
Similarity score: 0.145760536  
Metadata: {'author': 'Michael Munn & David Pitman', 'creationdate': '2023-02-11T09:02:57+00:00', 'creator': 'calibre 2.55.0 \[http://calibre-ebook.com\]', 'document\_id': '92f92d40c9b94deefa0d98d0c384a0402755d69cf7485641513fc8bbeb968d21', 'filename': 'Explainable-AI-for-Practitioners.pdf', 'moddate': '2023-02-11T10:04:57+01:00', 'page': 73.0, 'page\_label': '74', 'producer': '3-Heights(TM) PDF Optimization Shell 5.9.1.5 (http://www.pdf-tools.com)', 'source': 'Explainable-AI-for-Practitioners.pdf', 'title': 'Explainable AI for Practitioners', 'total\_pages': 74.0, 'type': 'content'}

Content preview:  
About   the     Authors Michael Munn    is      an      ML      Solutions       Engineer        at      Google  where   he      works   with    customers       of      Google Cloud    on       helping them    design, implement,      and     deploy  machine learning        models. He      also    teaches an      ML Immersion    Program at      the     Advanced        Solutions        Lab.    Michael has     a       PhD     in      mathematics     from    the     City University of      New     York.   Before  joining Google, he      worked  as      aresearch        professor. David        Pitman  is      a       Senior  Engineering     Manager working in      Google  Cloud   on      the     AI      Platform,       where   he leadsthe      Explai

\------------------------------------------------------------  
DOCUMENT 3  
Similarity score: 0.135744095  
Metadata: {'author': 'Michael Munn & David Pitman', 'creationdate': '2023-02-11T09:02:57+00:00', 'creator': 'calibre 2.55.0 \[http://calibre-ebook.com\]', 'document\_id': '92f92d40c9b94deefa0d98d0c384a0402755d69cf7485641513fc8bbeb968d21', 'filename': 'Explainable-AI-for-Practitioners.pdf', 'moddate': '2023-02-11T10:04:57+01:00', 'page': 7.0, 'page\_label': '8', 'producer': '3-Heights(TM) PDF Optimization Shell 5.9.1.5 (http://www.pdf-tools.com)', 'source': 'Explainable-AI-for-Practitioners.pdf', 'title': 'Explainable AI for Practitioners', 'total\_pages': 74.0, 'type': 'content'}

Content preview:  
learned to      focus   on      the     right   things  so      we’re   not     surprised       later?” Regulators      are     often   from    a       public  organization    or      industry body,   but     they    may     also    come    from    another part    of      a       company,        (i.e.,  Model   Risk    Management)     or      an      auditor from    another  company,        such    as      an insurance    company.        Regulators      seek    to      validate        and     verify  that    a       model   adheres to      a       specific set     of criteria,    and     will    continue        to      do      so      in      the     future. Unlike  stakeholders,   a       regulator’s     explainability  needs canrange   from    quite   techn

\------------------------------------------------------------  
DOCUMENT 4  
Similarity score: 0.128405571  
Metadata: {'author': 'Michael Munn & David Pitman', 'creationdate': '2023-02-11T09:02:57+00:00', 'creator': 'calibre 2.55.0 \[http://calibre-ebook.com\]', 'document\_id': '92f92d40c9b94deefa0d98d0c384a0402755d69cf7485641513fc8bbeb968d21', 'filename': 'Explainable-AI-for-Practitioners.pdf', 'moddate': '2023-02-11T10:04:57+01:00', 'page': 28.0, 'page\_label': '29', 'producer': '3-Heights(TM) PDF Optimization Shell 5.9.1.5 (http://www.pdf-tools.com)', 'source': 'Explainable-AI-for-Practitioners.pdf', 'title': 'Explainable AI for Practitioners', 'total\_pages': 74.0, 'type': 'content'}

Content preview:  
Figure  2-3.    At      some    point   in      the     straight        line    path    from    the     baseline        to      the     full    input   image,  around  when     ,      the      model becomes   very    confident       in      the     prediction      “sulfur-crested cockatoo”. We   can     achieve this    straight        line    path    in      python  with     the     interpolate\_images      function        described       here (see       the     GitHub  repository      for     the     full    code    example). def interpolate\_images(baseline,                        image,                        alphas):     alphas\_x \= alphas\[:, tf.newaxis, tf.newaxis, tf.newaxis\]

\------------------------------------------------------------  
DOCUMENT 5  
Similarity score: 0.114188202  
Metadata: {'author': 'Michael Munn & David Pitman', 'creationdate': '2023-02-11T09:02:57+00:00', 'creator': 'calibre 2.55.0 \[http://calibre-ebook.com\]', 'document\_id': '92f92d40c9b94deefa0d98d0c384a0402755d69cf7485641513fc8bbeb968d21', 'filename': 'Explainable-AI-for-Practitioners.pdf', 'moddate': '2023-02-11T10:04:57+01:00', 'page': 29.0, 'page\_label': '30', 'producer': '3-Heights(TM) PDF Optimization Shell 5.9.1.5 (http://www.pdf-tools.com)', 'source': 'Explainable-AI-for-Practitioners.pdf', 'title': 'Explainable AI for Practitioners', 'total\_pages': 74.0, 'type': 'content'}

Content preview:  
baseline\_x \= tf.expand\_dims(baseline, axis=0)     input\_x \= tf.expand\_dims(image, axis=0)     images \= alphas\_x \* input\_x \+ (1 \- alphas\_x) \* baseline\_x     return images The   interpolate\_images       function        produces        a       series  of      images  as      the     values  of      the      ’s     vary,   starting        from the        baseline        image    when            and     ending  at      the     full    input   image   when            as      shown   in      Figure  2- 4\. Figure    2-4.    As      the     value   of      alpha    varies  from    0       to      1,      we      obtain  a       series  of      images  creating        a       straight        line    path    in      image   space   from

\------------------------------------------------------------  
DOCUMENT 6  
Similarity score: 0.109952927  
Metadata: {'author': 'Michael Munn & David Pitman', 'creationdate': '2023-02-11T09:02:57+00:00', 'creator': 'calibre 2.55.0 \[http://calibre-ebook.com\]', 'document\_id': '92f92d40c9b94deefa0d98d0c384a0402755d69cf7485641513fc8bbeb968d21', 'filename': 'Explainable-AI-for-Practitioners.pdf', 'moddate': '2023-02-11T10:04:57+01:00', 'page': 59.0, 'page\_label': '60', 'producer': '3-Heights(TM) PDF Optimization Shell 5.9.1.5 (http://www.pdf-tools.com)', 'source': 'Explainable-AI-for-Practitioners.pdf', 'title': 'Explainable AI for Practitioners', 'total\_pages': 74.0, 'type': 'content'}

Content preview:  
Figure  2-26.   LIME    uses    a       linear  model   trained on      perturbations   of      the     original        input   image   to      determine       which   superpixel      regions  were most       influential     for     the     complex model’s prediction. In  Figure  2-26,   we      can     see     the     superpixel      regions that    most    positively       contributed     to      the     prediction ’sulfur-crested      cockatoo’.      It      is      also    possible        to      see     which   superpixel      regions provide anegative contribution   as      well.   To      do      this,   set     positive\_only   to      False.  This    produces        the     output  image   as      shown   in Figure       2-  
2026-08-12 16:48:27,471 | INFO | RETRIEVAL | query='ENd' | scores=\[0.148, 0.1458, 0.1357, 0.1284, 0.1142, 0.11\] | top=0.1480 | second=0.1458 | gap=0.0023 | mean=0.1303 | top/mean=1.1358 | gap\_ratio=0.0155  
\[TIMING\] retrieve                           2.21 sec

\======================================================================  
3\. RETRIEVAL ASSESSMENT  
\======================================================================  
Top score: 0.1480  
Second score: 0.1458  
Top/mean ratio: 1.1358  
Gap ratio: 0.0155  
Top document type: overview  
Overview dominant: False  
Evidence strength: ambiguous  
Retrieval decision: grade  
Decision reason: top\_candidates\_too\_close  
\[TIMING\] assess\_retrieval                   0.00 sec

\======================================================================  
GRAPH ROUTER: AFTER RETRIEVAL ASSESSMENT  
\======================================================================  
Retrieval decision: grade  
ROUTE \-\> grade\_documents  
2026-08-12 16:48:27,473 | INFO | \[route\_after\_retrieval\_assessment\] retrieval\_decision='grade' | decision='grade\_documents'

\======================================================================  
4\. DOCUMENT RELEVANCE GRADING  
\======================================================================  
Question/query being graded:  
ENd  
Candidates sent to grader: 4  
2026-08-12 16:48:27,474 | INFO | \[LLM:fast\] Attempt 1/4 → openrouter  
2026-08-12 16:48:28,376 | INFO | HTTP Request: POST https://openrouter.ai/api/v1/chat/completions "HTTP/1.1 200 OK"  
2026-08-12 16:48:28,478 | INFO | \[LLM:fast\] openrouter → SUCCESS

Raw LLM grading response: irrelevant

Normalized relevance grade: irrelevant  
\[TIMING\] grade\_documents                    1.00 sec

\======================================================================  
GRAPH ROUTER: AFTER DOCUMENT GRADING  
\======================================================================  
Relevance grade: irrelevant  
Retry count: 0  
Maximum retries: 2  
ROUTE \-\> rewrite\_query  
2026-08-12 16:48:28,479 | INFO | \[route\_after\_grading\] relevance\_grade='irrelevant' | retry\_count='0' | decision='rewrite\_query'

\======================================================================  
5\. QUERY REWRITE  
\======================================================================  
2026-08-12 16:48:28,480 | INFO | \[LLM:fast\] Attempt 1/4 → openrouter  
2026-08-12 16:48:28,773 | INFO | HTTP Request: POST https://openrouter.ai/api/v1/chat/completions "HTTP/1.1 200 OK"  
2026-08-12 16:48:28,967 | INFO | \[LLM:fast\] openrouter → SUCCESS  
\[TIMING\] rewrite\_query                      0.49 sec

\======================================================================  
2\. RETRIEVAL  
\======================================================================  
Query sent to retriever:  
End what or end how? Please provide more context or details about what you want to end.  
Document scope: 92f92d40c9b94deefa0d98d0c384a0402755d69cf7485641513fc8bbeb968d21

Overview chunks retrieved: 1  
Content chunks retrieved: 5

\------------------------------------------------------------  
DOCUMENT 1  
Similarity score: 0.159653679  
Metadata: {'document\_id': '92f92d40c9b94deefa0d98d0c384a0402755d69cf7485641513fc8bbeb968d21', 'filename': 'Explainable-AI-for-Practitioners.pdf', 'source': 'Explainable-AI-for-Practitioners.pdf', 'type': 'overview'}

Content preview:  
This document covers the topic of Explainable AI for practitioners, focusing on designing and implementing explainable machine learning solutions. The excerpt provided appears to be from the first chapter, "An Overview of Explainability", which introduces the concept of explainability in AI and its importance. The chapter discusses the history of explainability, the different types of explanations, and the various consumers of explainability, including practitioners, observers, and end-users. Th

\------------------------------------------------------------  
DOCUMENT 2  
Similarity score: 0.137449279  
Metadata: {'author': 'Michael Munn & David Pitman', 'creationdate': '2023-02-11T09:02:57+00:00', 'creator': 'calibre 2.55.0 \[http://calibre-ebook.com\]', 'document\_id': '92f92d40c9b94deefa0d98d0c384a0402755d69cf7485641513fc8bbeb968d21', 'filename': 'Explainable-AI-for-Practitioners.pdf', 'moddate': '2023-02-11T10:04:57+01:00', 'page': 6.0, 'page\_label': '7', 'producer': '3-Heights(TM) PDF Optimization Shell 5.9.1.5 (http://www.pdf-tools.com)', 'source': 'Explainable-AI-for-Practitioners.pdf', 'title': 'Explainable AI for Practitioners', 'total\_pages': 74.0, 'type': 'content'}

Content preview:  
be      machine learning        algorithms.     Although        very    sophisticated,  these   techniques      are     all     “dumb”  in      the sense       that    we      cannot  interact with    them    in      a       two-way dialogue.       A       smart   explainability  technique       could adapt     to      our     queries,        learning        how     to       guide   us      towards the     best    explanation,    or      answer  the     question        we didn’t       know    we      were    asking. For     now,    if      we      want     to      try     and     obtain  more    information     about   a       prediction, the best    we      can     do      is      to      change  the     parameters      of      our      explanation     request,        or      try     a       differen

\------------------------------------------------------------  
DOCUMENT 3  
Similarity score: 0.125631824  
Metadata: {'author': 'Michael Munn & David Pitman', 'creationdate': '2023-02-11T09:02:57+00:00', 'creator': 'calibre 2.55.0 \[http://calibre-ebook.com\]', 'document\_id': '92f92d40c9b94deefa0d98d0c384a0402755d69cf7485641513fc8bbeb968d21', 'filename': 'Explainable-AI-for-Practitioners.pdf', 'moddate': '2023-02-11T10:04:57+01:00', 'page': 7.0, 'page\_label': '8', 'producer': '3-Heights(TM) PDF Optimization Shell 5.9.1.5 (http://www.pdf-tools.com)', 'source': 'Explainable-AI-for-Practitioners.pdf', 'title': 'Explainable AI for Practitioners', 'total\_pages': 74.0, 'type': 'content'}

Content preview:  
learned to      focus   on      the     right   things  so      we’re   not     surprised       later?” Regulators      are     often   from    a       public  organization    or      industry body,   but     they    may     also    come    from    another part    of      a       company,        (i.e.,  Model   Risk    Management)     or      an      auditor from    another  company,        such    as      an insurance    company.        Regulators      seek    to      validate        and     verify  that    a       model   adheres to      a       specific set     of criteria,    and     will    continue        to      do      so      in      the     future. Unlike  stakeholders,   a       regulator’s     explainability  needs canrange   from    quite   techn

\------------------------------------------------------------  
DOCUMENT 4  
Similarity score: 0.107522495  
Metadata: {'author': 'Michael Munn & David Pitman', 'creationdate': '2023-02-11T09:02:57+00:00', 'creator': 'calibre 2.55.0 \[http://calibre-ebook.com\]', 'document\_id': '92f92d40c9b94deefa0d98d0c384a0402755d69cf7485641513fc8bbeb968d21', 'filename': 'Explainable-AI-for-Practitioners.pdf', 'moddate': '2023-02-11T10:04:57+01:00', 'page': 4.0, 'page\_label': '5', 'producer': '3-Heights(TM) PDF Optimization Shell 5.9.1.5 (http://www.pdf-tools.com)', 'source': 'Explainable-AI-for-Practitioners.pdf', 'title': 'Explainable AI for Practitioners', 'total\_pages': 74.0, 'type': 'content'}

Content preview:  
as      expected.       Even    the     terms   explainability  and     interpretability        are     routinely       swapped,        despite having very     different       focuses.For      example,        while   writing this    book,   we      were    asked   by      a       knowledgeable industry  organization    to      describe        explainable     and     interpretable    capabilities    of      a       system, but     the definitions of      explainability  and     interpretability        were    flipped in      comparison      to      how      the     rest    of      industry defines        the     terms\!  Recognizing     the     confusion       over    explainability, the     purpose of      this    chapter is      to

\------------------------------------------------------------  
DOCUMENT 5  
Similarity score: 0.105560318  
Metadata: {'author': 'Michael Munn & David Pitman', 'creationdate': '2023-02-11T09:02:57+00:00', 'creator': 'calibre 2.55.0 \[http://calibre-ebook.com\]', 'document\_id': '92f92d40c9b94deefa0d98d0c384a0402755d69cf7485641513fc8bbeb968d21', 'filename': 'Explainable-AI-for-Practitioners.pdf', 'moddate': '2023-02-11T10:04:57+01:00', 'page': 1.0, 'page\_label': '2', 'producer': '3-Heights(TM) PDF Optimization Shell 5.9.1.5 (http://www.pdf-tools.com)', 'source': 'Explainable-AI-for-Practitioners.pdf', 'title': 'Explainable AI for Practitioners', 'total\_pages': 74.0, 'type': 'content'}

Content preview:  
Explainable     AI      for     Practitioners Designing and     Implementing    Explainable     ML      Solutions With  Early   Release ebooks, you     get     books   in      their   earliest form—the        author’s        raw     and     unedited content        as      they    write—so        you     can     take    advantage       of      these   technologies    long     before  the     official release        of      these   titles. Michael Munn    and     David   Pitman

\------------------------------------------------------------  
DOCUMENT 6  
Similarity score: 0.0947141722  
Metadata: {'author': 'Michael Munn & David Pitman', 'creationdate': '2023-02-11T09:02:57+00:00', 'creator': 'calibre 2.55.0 \[http://calibre-ebook.com\]', 'document\_id': '92f92d40c9b94deefa0d98d0c384a0402755d69cf7485641513fc8bbeb968d21', 'filename': 'Explainable-AI-for-Practitioners.pdf', 'moddate': '2023-02-11T10:04:57+01:00', 'page': 6.0, 'page\_label': '7', 'producer': '3-Heights(TM) PDF Optimization Shell 5.9.1.5 (http://www.pdf-tools.com)', 'source': 'Explainable-AI-for-Practitioners.pdf', 'title': 'Explainable AI for Practitioners', 'total\_pages': 74.0, 'type': 'content'}

Content preview:  
models  for     drift   and     skew    in      their   predictions,    indicating      when    a       model   should  be      retrained. And  of      course, you     may     simply  be       interested      in      an      explanation     because,        like    any     practitioner,   you’ve encountered      a       situation       when    the     model   made    you      squint  and     say     “what   the...?” Observers:     Business        Stakeholders    &       Regulators Another      group   of      explainability  consumers       is      observers.       These   are     individuals,    committees,     or organizations,       who     are     not     involved        in      the     research,       design, and     engineering      of      the     mode  
2026-08-12 16:48:31,221 | INFO | RETRIEVAL | query='End what or end how? Please provide more context or details about what you want to end.' | scores=\[0.1597, 0.1374, 0.1256, 0.1075, 0.1056, 0.0947\] | top=0.1597 | second=0.1374 | gap=0.0222 | mean=0.1218 | top/mean=1.3113 | gap\_ratio=0.1391  
\[TIMING\] retrieve                           2.25 sec

\======================================================================  
3\. RETRIEVAL ASSESSMENT  
\======================================================================  
Top score: 0.1597  
Second score: 0.1374  
Top/mean ratio: 1.3113  
Gap ratio: 0.1391  
Top document type: overview  
Overview dominant: True  
Evidence strength: strong  
Retrieval decision: generate  
Decision reason: overview\_dominant\_with\_clear\_margin  
\[TIMING\] assess\_retrieval                   0.00 sec

\======================================================================  
GRAPH ROUTER: AFTER RETRIEVAL ASSESSMENT  
\======================================================================  
Retrieval decision: generate  
ROUTE \-\> generate  
2026-08-12 16:48:31,226 | INFO | \[route\_after\_retrieval\_assessment\] retrieval\_decision='generate' | decision='generate'

\======================================================================  
6\. GENERATION  
\======================================================================  
2026-08-12 16:48:31,227 | INFO | \[LLM:primary\] Attempt 1/4 → openrouter  
2026-08-12 16:48:31,568 | INFO | HTTP Request: POST https://openrouter.ai/api/v1/chat/completions "HTTP/1.1 200 OK"  
2026-08-12 16:48:34,134 | INFO | \[LLM:primary\] openrouter → SUCCESS  
\[TIMING\] generate                           2.91 sec

\======================================================================  
7\. HALLUCINATION CHECK  
\======================================================================  
2026-08-12 16:48:34,136 | INFO | \[LLM:fast\] Attempt 1/4 → openrouter  
2026-08-12 16:48:34,516 | INFO | HTTP Request: POST https://openrouter.ai/api/v1/chat/completions "HTTP/1.1 200 OK"  
2026-08-12 16:48:34,611 | INFO | \[LLM:fast\] openrouter → SUCCESS  
\[TIMING\] check\_hallucination                0.48 sec

\======================================================================  
GRAPH ROUTER: AFTER HALLUCINATION CHECK  
\======================================================================  
Hallucination grade: grounded  
Retry count: 0  
Maximum retries: 2  
ROUTE \-\> record\_turn  
2026-08-12 16:48:34,612 | INFO | \[route\_after\_hallucination\_check\] hallucination\_grade='grounded' | retry\_count='0' | decision='end'

\======================================================================  
8\. RECORD TURN  
\======================================================================

\======================================================================  
STRUCTURED TRACE SUMMARY (full request, end to end)  
\======================================================================  
\[  
  {  
    "stage": "check\_hallucination",  
    "raw\_grade": "grounded",  
    "normalized\_grade": "grounded",  
    "hallucination\_retry\_count": 0  
  },  
  {  
    "stage": "record\_turn",  
    "final\_route": "end",  
    "retry\_count": 1,  
    "retrieval\_decision": "generate",  
    "retrieval\_evidence\_strength": "strong",  
    "retrieval\_decision\_reason": "overview\_dominant\_with\_clear\_margin"  
  }  
\]

\======================================================================  
PERFORMANCE SUMMARY  
\======================================================================  
contextualize\_question            2.31 sec (  5.8%) \[4 call(s)\]  
    └─ Run \#1                         0.00 sec  
    └─ Run \#2                         1.34 sec  
    └─ Run \#3                         0.97 sec  
    └─ Run \#4                         0.00 sec  
retrieve                         12.22 sec ( 30.6%) \[5 call(s)\]  
    └─ Run \#1                         3.26 sec  
    └─ Run \#2                         2.25 sec  
    └─ Run \#3                         2.25 sec  
    └─ Run \#4                         2.21 sec  
    └─ Run \#5                         2.25 sec  
assess\_retrieval                  0.01 sec (  0.0%) \[5 call(s)\]  
    └─ Run \#1                         0.00 sec  
    └─ Run \#2                         0.00 sec  
    └─ Run \#3                         0.00 sec  
    └─ Run \#4                         0.00 sec  
    └─ Run \#5                         0.00 sec  
generate                         21.44 sec ( 53.7%) \[4 call(s)\]  
    └─ Run \#1                         2.28 sec  
    └─ Run \#2                        14.58 sec  
    └─ Run \#3                         1.68 sec  
    └─ Run \#4                         2.91 sec  
check\_hallucination               2.04 sec (  5.1%) \[4 call(s)\]  
    └─ Run \#1                         0.44 sec  
    └─ Run \#2                         0.58 sec  
    └─ Run \#3                         0.54 sec  
    └─ Run \#4                         0.48 sec  
grade\_documents                   1.45 sec (  3.6%) \[2 call(s)\]  
    └─ Run \#1                         0.45 sec  
    └─ Run \#2                         1.00 sec  
rewrite\_query                     0.49 sec (  1.2%) \[1 call(s)\]  
\----------------------------------------------------------------------  
TOTAL                            39.95 sec

BOTTLENECK: generate  
BOTTLENECK TIME: 21.44 sec  
\======================================================================  
INFO:     127.0.0.1:58040 \- "POST /query HTTP/1.1" 200 OK  
INFO:     127.0.0.1:58394 \- "GET /documents HTTP/1.1" 200 OK  
\[TIMING\] contextualize\_question             0.00 sec

\======================================================================  
2\. RETRIEVAL  
\======================================================================  
Query sent to retriever:  
I would like to stop asking any questions  
Document scope: 92f92d40c9b94deefa0d98d0c384a0402755d69cf7485641513fc8bbeb968d21

Overview chunks retrieved: 1  
Content chunks retrieved: 5

\------------------------------------------------------------  
DOCUMENT 1  
Similarity score: 0.131290451  
Metadata: {'author': 'Michael Munn & David Pitman', 'creationdate': '2023-02-11T09:02:57+00:00', 'creator': 'calibre 2.55.0 \[http://calibre-ebook.com\]', 'document\_id': '92f92d40c9b94deefa0d98d0c384a0402755d69cf7485641513fc8bbeb968d21', 'filename': 'Explainable-AI-for-Practitioners.pdf', 'moddate': '2023-02-11T10:04:57+01:00', 'page': 3.0, 'page\_label': '4', 'producer': '3-Heights(TM) PDF Optimization Shell 5.9.1.5 (http://www.pdf-tools.com)', 'source': 'Explainable-AI-for-Practitioners.pdf', 'title': 'Explainable AI for Practitioners', 'total\_pages': 74.0, 'type': 'content'}

Content preview:  
thereof complies        with    such    licenses        and/or  rights. 978-1-098-11913-3 \[LSI\]

\------------------------------------------------------------  
DOCUMENT 2  
Similarity score: 0.0922393873  
Metadata: {'author': 'Michael Munn & David Pitman', 'creationdate': '2023-02-11T09:02:57+00:00', 'creator': 'calibre 2.55.0 \[http://calibre-ebook.com\]', 'document\_id': '92f92d40c9b94deefa0d98d0c384a0402755d69cf7485641513fc8bbeb968d21', 'filename': 'Explainable-AI-for-Practitioners.pdf', 'moddate': '2023-02-11T10:04:57+01:00', 'page': 6.0, 'page\_label': '7', 'producer': '3-Heights(TM) PDF Optimization Shell 5.9.1.5 (http://www.pdf-tools.com)', 'source': 'Explainable-AI-for-Practitioners.pdf', 'title': 'Explainable AI for Practitioners', 'total\_pages': 74.0, 'type': 'content'}

Content preview:  
be      machine learning        algorithms.     Although        very    sophisticated,  these   techniques      are     all     “dumb”  in      the sense       that    we      cannot  interact with    them    in      a       two-way dialogue.       A       smart   explainability  technique       could adapt     to      our     queries,        learning        how     to       guide   us      towards the     best    explanation,    or      answer  the     question        we didn’t       know    we      were    asking. For     now,    if      we      want     to      try     and     obtain  more    information     about   a       prediction, the best    we      can     do      is      to      change  the     parameters      of      our      explanation     request,        or      try     a       differen

\------------------------------------------------------------  
DOCUMENT 3  
Similarity score: 0.0863046721  
Metadata: {'author': 'Michael Munn & David Pitman', 'creationdate': '2023-02-11T09:02:57+00:00', 'creator': 'calibre 2.55.0 \[http://calibre-ebook.com\]', 'document\_id': '92f92d40c9b94deefa0d98d0c384a0402755d69cf7485641513fc8bbeb968d21', 'filename': 'Explainable-AI-for-Practitioners.pdf', 'moddate': '2023-02-11T10:04:57+01:00', 'page': 73.0, 'page\_label': '74', 'producer': '3-Heights(TM) PDF Optimization Shell 5.9.1.5 (http://www.pdf-tools.com)', 'source': 'Explainable-AI-for-Practitioners.pdf', 'title': 'Explainable AI for Practitioners', 'total\_pages': 74.0, 'type': 'content'}

Content preview:  
About   the     Authors Michael Munn    is      an      ML      Solutions       Engineer        at      Google  where   he      works   with    customers       of      Google Cloud    on       helping them    design, implement,      and     deploy  machine learning        models. He      also    teaches an      ML Immersion    Program at      the     Advanced        Solutions        Lab.    Michael has     a       PhD     in      mathematics     from    the     City University of      New     York.   Before  joining Google, he      worked  as      aresearch        professor. David        Pitman  is      a       Senior  Engineering     Manager working in      Google  Cloud   on      the     AI      Platform,       where   he leadsthe      Explai

\------------------------------------------------------------  
DOCUMENT 4  
Similarity score: 0.0824709  
Metadata: {'author': 'Michael Munn & David Pitman', 'creationdate': '2023-02-11T09:02:57+00:00', 'creator': 'calibre 2.55.0 \[http://calibre-ebook.com\]', 'document\_id': '92f92d40c9b94deefa0d98d0c384a0402755d69cf7485641513fc8bbeb968d21', 'filename': 'Explainable-AI-for-Practitioners.pdf', 'moddate': '2023-02-11T10:04:57+01:00', 'page': 58.0, 'page\_label': '59', 'producer': '3-Heights(TM) PDF Optimization Shell 5.9.1.5 (http://www.pdf-tools.com)', 'source': 'Explainable-AI-for-Practitioners.pdf', 'title': 'Explainable AI for Practitioners', 'total\_pages': 74.0, 'type': 'content'}

Content preview:  
model   we      specify include\_top=True        to      get     the     final   prediction      layer   of      the     model   and     we      set weights='imagenet’  to      get     the      weights pre-trained     on      the     ImageNet        dataset. inception \= tf.keras.applications.InceptionV3(     include\_top=True, weights='imagenet') model \= tf.keras.models.Model(inception.inputs, inception.output) Now, given   an      image,  we      can     create  explanations    for     the     Inception       model’s prediction      by      creatinga LimeImageExplainer     object  and     then    calling the     explain\_instance        method. The     fol

\------------------------------------------------------------  
DOCUMENT 5  
Similarity score: 0.0711555555  
Metadata: {'author': 'Michael Munn & David Pitman', 'creationdate': '2023-02-11T09:02:57+00:00', 'creator': 'calibre 2.55.0 \[http://calibre-ebook.com\]', 'document\_id': '92f92d40c9b94deefa0d98d0c384a0402755d69cf7485641513fc8bbeb968d21', 'filename': 'Explainable-AI-for-Practitioners.pdf', 'moddate': '2023-02-11T10:04:57+01:00', 'page': 5.0, 'page\_label': '6', 'producer': '3-Heights(TM) PDF Optimization Shell 5.9.1.5 (http://www.pdf-tools.com)', 'source': 'Explainable-AI-for-Practitioners.pdf', 'title': 'Explainable AI for Practitioners', 'total\_pages': 74.0, 'type': 'content'}

Content preview:  
What    Are     Explanations? When      a       model   makes   a       prediction,     Explainable     AI      methods generate        an      explanation     that    gives   insight into     the     model’s behavior        as      it      arrived at      that    prediction.     When    we      seek    explanations,   we      are     trying  to understand   “why    did      X       happen?”        Figuring        out     this    “Why”   can     help    us      build   a       better  comprehension   of what influences      a       model,  how     that     influence       occurs, and     where   the     model   performs        (or     fails). As      part    of building     our     own     mental  models, we      often   find    apure    explanation     to      be

\------------------------------------------------------------  
DOCUMENT 6  
Similarity score: 0.0279455204  
Metadata: {'document\_id': '92f92d40c9b94deefa0d98d0c384a0402755d69cf7485641513fc8bbeb968d21', 'filename': 'Explainable-AI-for-Practitioners.pdf', 'source': 'Explainable-AI-for-Practitioners.pdf', 'type': 'overview'}

Content preview:  
This document covers the topic of Explainable AI for practitioners, focusing on designing and implementing explainable machine learning solutions. The excerpt provided appears to be from the first chapter, "An Overview of Explainability", which introduces the concept of explainability in AI and its importance. The chapter discusses the history of explainability, the different types of explanations, and the various consumers of explainability, including practitioners, observers, and end-users. Th  
2026-08-12 16:48:47,559 | INFO | RETRIEVAL | query='I would like to stop asking any questions' | scores=\[0.1313, 0.0922, 0.0863, 0.0825, 0.0712, 0.0279\] | top=0.1313 | second=0.0922 | gap=0.0391 | mean=0.0819 | top/mean=1.6030 | gap\_ratio=0.2974  
\[TIMING\] retrieve                           2.21 sec

\======================================================================  
3\. RETRIEVAL ASSESSMENT  
\======================================================================  
Top score: 0.1313  
Second score: 0.0922  
Top/mean ratio: 1.6030  
Gap ratio: 0.2974  
Top document type: content  
Overview dominant: False  
Evidence strength: strong  
Retrieval decision: generate  
Decision reason: strong\_score\_distribution  
\[TIMING\] assess\_retrieval                   0.00 sec

\======================================================================  
GRAPH ROUTER: AFTER RETRIEVAL ASSESSMENT  
\======================================================================  
Retrieval decision: generate  
ROUTE \-\> generate  
2026-08-12 16:48:47,561 | INFO | \[route\_after\_retrieval\_assessment\] retrieval\_decision='generate' | decision='generate'

\======================================================================  
6\. GENERATION  
\======================================================================  
2026-08-12 16:48:47,562 | INFO | \[LLM:primary\] Attempt 1/4 → openrouter  
2026-08-12 16:48:48,255 | INFO | HTTP Request: POST https://openrouter.ai/api/v1/chat/completions "HTTP/1.1 200 OK"  
2026-08-12 16:48:49,822 | INFO | \[LLM:primary\] openrouter → SUCCESS  
\[TIMING\] generate                           2.26 sec

\======================================================================  
7\. HALLUCINATION CHECK  
\======================================================================  
2026-08-12 16:48:49,823 | INFO | \[LLM:fast\] Attempt 1/4 → openrouter  
2026-08-12 16:48:50,196 | INFO | HTTP Request: POST https://openrouter.ai/api/v1/chat/completions "HTTP/1.1 200 OK"  
2026-08-12 16:48:50,332 | INFO | \[LLM:fast\] openrouter → SUCCESS  
\[TIMING\] check\_hallucination                0.51 sec

\======================================================================  
GRAPH ROUTER: AFTER HALLUCINATION CHECK  
\======================================================================  
Hallucination grade: hallucinated  
Retry count: 1  
Maximum retries: 2  
ROUTE \-\> generate  
2026-08-12 16:48:50,333 | INFO | \[route\_after\_hallucination\_check\] hallucination\_grade='hallucinated' | retry\_count='1' | decision='generate'

\======================================================================  
6\. GENERATION  
\======================================================================  
2026-08-12 16:48:50,334 | INFO | \[LLM:primary\] Attempt 1/4 → openrouter  
2026-08-12 16:48:50,664 | INFO | HTTP Request: POST https://openrouter.ai/api/v1/chat/completions "HTTP/1.1 200 OK"  
2026-08-12 16:48:52,648 | INFO | \[LLM:primary\] openrouter → SUCCESS  
\[TIMING\] generate                           2.31 sec

\======================================================================  
7\. HALLUCINATION CHECK  
\======================================================================  
2026-08-12 16:48:52,656 | INFO | \[LLM:fast\] Attempt 1/4 → openrouter  
2026-08-12 16:48:53,019 | INFO | HTTP Request: POST https://openrouter.ai/api/v1/chat/completions "HTTP/1.1 200 OK"  
2026-08-12 16:48:53,085 | INFO | \[LLM:fast\] openrouter → SUCCESS  
\[TIMING\] check\_hallucination                0.43 sec

\======================================================================  
GRAPH ROUTER: AFTER HALLUCINATION CHECK  
\======================================================================  
Hallucination grade: grounded  
Retry count: 1  
Maximum retries: 2  
ROUTE \-\> record\_turn  
2026-08-12 16:48:53,085 | INFO | \[route\_after\_hallucination\_check\] hallucination\_grade='grounded' | retry\_count='1' | decision='end'

\======================================================================  
8\. RECORD TURN  
\======================================================================

\======================================================================  
STRUCTURED TRACE SUMMARY (full request, end to end)  
\======================================================================  
\[  
  {  
    "stage": "check\_hallucination",  
    "raw\_grade": "grounded",  
    "normalized\_grade": "grounded",  
    "hallucination\_retry\_count": 1  
  },  
  {  
    "stage": "record\_turn",  
    "final\_route": "end",  
    "retry\_count": 0,  
    "retrieval\_decision": "generate",  
    "retrieval\_evidence\_strength": "strong",  
    "retrieval\_decision\_reason": "strong\_score\_distribution"  
  }  
\]

\======================================================================  
PERFORMANCE SUMMARY  
\======================================================================  
contextualize\_question            2.31 sec (  4.8%) \[5 call(s)\]  
    └─ Run \#1                         0.00 sec  
    └─ Run \#2                         1.34 sec  
    └─ Run \#3                         0.97 sec  
    └─ Run \#4                         0.00 sec  
    └─ Run \#5                         0.00 sec  
retrieve                         14.43 sec ( 30.3%) \[6 call(s)\]  
    └─ Run \#1                         3.26 sec  
    └─ Run \#2                         2.25 sec  
    └─ Run \#3                         2.25 sec  
    └─ Run \#4                         2.21 sec  
    └─ Run \#5                         2.25 sec  
    └─ Run \#6                         2.21 sec  
assess\_retrieval                  0.01 sec (  0.0%) \[6 call(s)\]  
    └─ Run \#1                         0.00 sec  
    └─ Run \#2                         0.00 sec  
    └─ Run \#3                         0.00 sec  
    └─ Run \#4                         0.00 sec  
    └─ Run \#5                         0.00 sec  
    └─ Run \#6                         0.00 sec  
generate                         26.02 sec ( 54.6%) \[6 call(s)\]  
    └─ Run \#1                         2.28 sec  
    └─ Run \#2                        14.58 sec  
    └─ Run \#3                         1.68 sec  
    └─ Run \#4                         2.91 sec  
    └─ Run \#5                         2.26 sec  
    └─ Run \#6                         2.31 sec  
check\_hallucination               2.98 sec (  6.3%) \[6 call(s)\]  
    └─ Run \#1                         0.44 sec  
    └─ Run \#2                         0.58 sec  
    └─ Run \#3                         0.54 sec  
    └─ Run \#4                         0.48 sec  
    └─ Run \#5                         0.51 sec  
    └─ Run \#6                         0.43 sec  
grade\_documents                   1.45 sec (  3.0%) \[2 call(s)\]  
    └─ Run \#1                         0.45 sec  
    └─ Run \#2                         1.00 sec  
rewrite\_query                     0.49 sec (  1.0%) \[1 call(s)\]  
\----------------------------------------------------------------------  
TOTAL                            47.68 sec

BOTTLENECK: generate  
BOTTLENECK TIME: 26.02 sec  
\======================================================================  
INFO:     127.0.0.1:58394 \- "POST /query HTTP/1.1" 200 OK

