(.rag\_project) PS F:\\Agentic\_Project\\agentic-rag\> uvicorn src.agentic\_rag.api.main:app \--reload | Out-File \-FilePath F:\\Agentic\_Project\\agentic-rag\\dot\_md\\console\_app\_output\_v1.md \-Encoding utf8  
INFO:     Will watch for changes in these directories: \['F:\\\\Agentic\_Project\\\\agentic-rag'\]  
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)  
INFO:     Started reloader process \[29988\] using WatchFiles  
2026-08-12 16:38:14,234 | INFO | LLM provider chain initialized (primary tier): \['openrouter', 'cerebras', 'groq', 'nvidia'\]  
2026-08-12 16:38:14,274 | INFO | LLM provider chain initialized (fast tier): \['openrouter', 'cerebras', 'groq', 'nvidia'\]  
2026-08-12 16:38:17,290 | INFO | No device provided, using cpu  
2026-08-12 16:38:17,567 | INFO | HTTP Request: HEAD https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/main/modules.json "HTTP/1.1 307 Temporary Redirect"  
Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF\_TOKEN to enable higher rate limits and faster downloads.  
2026-08-12 16:38:17,567 | WARNING | Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF\_TOKEN to enable higher rate limits and faster downloads.  
2026-08-12 16:38:17,591 | INFO | HTTP Request: HEAD https://huggingface.co/api/resolve-cache/models/sentence-transformers/all-MiniLM-L6-v2/1110a243fdf4706b3f48f1d95db1a4f5529b4d41/modules.json "HTTP/1.1 200 OK"  
2026-08-12 16:38:17,824 | INFO | HTTP Request: HEAD https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/main/config\_sentence\_transformers.json "HTTP/1.1 307 Temporary Redirect"  
2026-08-12 16:38:17,848 | INFO | HTTP Request: HEAD https://huggingface.co/api/resolve-cache/models/sentence-transformers/all-MiniLM-L6-v2/1110a243fdf4706b3f48f1d95db1a4f5529b4d41/config\_sentence\_transformers.json "HTTP/1.1 200 OK"  
2026-08-12 16:38:17,849 | INFO | Loading SentenceTransformer model from sentence-transformers/all-MiniLM-L6-v2.  
2026-08-12 16:38:18,070 | INFO | HTTP Request: HEAD https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/main/config\_sentence\_transformers.json "HTTP/1.1 307 Temporary Redirect"  
2026-08-12 16:38:18,093 | INFO | HTTP Request: HEAD https://huggingface.co/api/resolve-cache/models/sentence-transformers/all-MiniLM-L6-v2/1110a243fdf4706b3f48f1d95db1a4f5529b4d41/config\_sentence\_transformers.json "HTTP/1.1 200 OK"  
2026-08-12 16:38:18,317 | INFO | HTTP Request: HEAD https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/main/README.md "HTTP/1.1 307 Temporary Redirect"  
2026-08-12 16:38:18,340 | INFO | HTTP Request: HEAD https://huggingface.co/api/resolve-cache/models/sentence-transformers/all-MiniLM-L6-v2/1110a243fdf4706b3f48f1d95db1a4f5529b4d41/README.md "HTTP/1.1 200 OK"  
2026-08-12 16:38:18,560 | INFO | HTTP Request: HEAD https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/main/modules.json "HTTP/1.1 307 Temporary Redirect"  
2026-08-12 16:38:18,583 | INFO | HTTP Request: HEAD https://huggingface.co/api/resolve-cache/models/sentence-transformers/all-MiniLM-L6-v2/1110a243fdf4706b3f48f1d95db1a4f5529b4d41/modules.json "HTTP/1.1 200 OK"  
2026-08-12 16:38:18,817 | INFO | HTTP Request: HEAD https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/main/sentence\_bert\_config.json "HTTP/1.1 307 Temporary Redirect"  
2026-08-12 16:38:18,839 | INFO | HTTP Request: HEAD https://huggingface.co/api/resolve-cache/models/sentence-transformers/all-MiniLM-L6-v2/1110a243fdf4706b3f48f1d95db1a4f5529b4d41/sentence\_bert\_config.json "HTTP/1.1 200 OK"  
2026-08-12 16:38:19,062 | INFO | HTTP Request: HEAD https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/main/adapter\_config.json "HTTP/1.1 404 Not Found"  
2026-08-12 16:38:19,280 | INFO | HTTP Request: HEAD https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/main/config.json "HTTP/1.1 307 Temporary Redirect"  
2026-08-12 16:38:19,303 | INFO | HTTP Request: HEAD https://huggingface.co/api/resolve-cache/models/sentence-transformers/all-MiniLM-L6-v2/1110a243fdf4706b3f48f1d95db1a4f5529b4d41/config.json "HTTP/1.1 200 OK"  
Loading weights: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 103/103 \[00:00\<00:00, 10620.32it/s\]  
2026-08-12 16:38:19,631 | INFO | HTTP Request: HEAD https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/main/processor\_config.json "HTTP/1.1 404 Not Found"  
2026-08-12 16:38:19,852 | INFO | HTTP Request: HEAD https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/main/preprocessor\_config.json "HTTP/1.1 404 Not Found"  
2026-08-12 16:38:20,128 | INFO | HTTP Request: HEAD https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/main/video\_preprocessor\_config.json "HTTP/1.1 404 Not Found"  
2026-08-12 16:38:20,350 | INFO | HTTP Request: HEAD https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/main/preprocessor\_config.json "HTTP/1.1 404 Not Found"  
2026-08-12 16:38:20,571 | INFO | HTTP Request: HEAD https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/main/tokenizer\_config.json "HTTP/1.1 307 Temporary Redirect"  
2026-08-12 16:38:20,594 | INFO | HTTP Request: HEAD https://huggingface.co/api/resolve-cache/models/sentence-transformers/all-MiniLM-L6-v2/1110a243fdf4706b3f48f1d95db1a4f5529b4d41/tokenizer\_config.json "HTTP/1.1 200 OK"  
2026-08-12 16:38:20,815 | INFO | HTTP Request: HEAD https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/main/config.json "HTTP/1.1 307 Temporary Redirect"  
2026-08-12 16:38:20,838 | INFO | HTTP Request: HEAD https://huggingface.co/api/resolve-cache/models/sentence-transformers/all-MiniLM-L6-v2/1110a243fdf4706b3f48f1d95db1a4f5529b4d41/config.json "HTTP/1.1 200 OK"  
2026-08-12 16:38:21,073 | INFO | HTTP Request: HEAD https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/main/config.json "HTTP/1.1 307 Temporary Redirect"  
2026-08-12 16:38:21,101 | INFO | HTTP Request: HEAD https://huggingface.co/api/resolve-cache/models/sentence-transformers/all-MiniLM-L6-v2/1110a243fdf4706b3f48f1d95db1a4f5529b4d41/config.json "HTTP/1.1 200 OK"  
2026-08-12 16:38:21,336 | INFO | HTTP Request: HEAD https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/main/tokenizer\_config.json "HTTP/1.1 307 Temporary Redirect"  
2026-08-12 16:38:21,358 | INFO | HTTP Request: HEAD https://huggingface.co/api/resolve-cache/models/sentence-transformers/all-MiniLM-L6-v2/1110a243fdf4706b3f48f1d95db1a4f5529b4d41/tokenizer\_config.json "HTTP/1.1 200 OK"  
2026-08-12 16:38:21,598 | INFO | HTTP Request: GET https://huggingface.co/api/models/sentence-transformers/all-MiniLM-L6-v2/tree/main/additional\_chat\_templates?recursive=false\&expand=false "HTTP/1.1 404 Not Found"  
2026-08-12 16:38:21,824 | INFO | HTTP Request: GET https://huggingface.co/api/models/sentence-transformers/all-MiniLM-L6-v2/tree/main?recursive=true\&expand=false "HTTP/1.1 200 OK"  
2026-08-12 16:38:22,074 | INFO | HTTP Request: HEAD https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/main/1\_Pooling/config.json "HTTP/1.1 307 Temporary Redirect"  
2026-08-12 16:38:22,096 | INFO | HTTP Request: HEAD https://huggingface.co/api/resolve-cache/models/sentence-transformers/all-MiniLM-L6-v2/1110a243fdf4706b3f48f1d95db1a4f5529b4d41/1\_Pooling%2Fconfig.json "HTTP/1.1 200 OK"  
2026-08-12 16:38:22,321 | INFO | HTTP Request: GET https://huggingface.co/api/models/sentence-transformers/all-MiniLM-L6-v2 "HTTP/1.1 200 OK"  
INFO:     Started server process \[28540\]  
INFO:     Waiting for application startup.  
INFO:     Application startup complete.  
ERROR:    Exception in ASGI application  
Traceback (most recent call last):  
  File "F:\\Agentic\_Project\\agentic-rag\\.rag\_project\\Lib\\site-packages\\uvicorn\\protocols\\http\\httptools\_impl.py", line 422, in run\_asgi  
    result \= await app(  \# type: ignore\[func-returns-value\]  
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^  
        self.scope, self.receive, self.send  
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^  
    )  
    ^  
  File "F:\\Agentic\_Project\\agentic-rag\\.rag\_project\\Lib\\site-packages\\uvicorn\\middleware\\proxy\_headers.py", line 63, in \_\_call\_\_  
    return await self.app(scope, receive, send)  
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^  
  File "F:\\Agentic\_Project\\agentic-rag\\.rag\_project\\Lib\\site-packages\\fastapi\\applications.py", line 1163, in \_\_call\_\_  
    await super().\_\_call\_\_(scope, receive, send)  
  File "F:\\Agentic\_Project\\agentic-rag\\.rag\_project\\Lib\\site-packages\\starlette\\applications.py", line 90, in \_\_call\_\_  
    await self.middleware\_stack(scope, receive, send)  
  File "F:\\Agentic\_Project\\agentic-rag\\.rag\_project\\Lib\\site-packages\\starlette\\middleware\\errors.py", line 186, in \_\_call\_\_  
    raise exc  
  File "F:\\Agentic\_Project\\agentic-rag\\.rag\_project\\Lib\\site-packages\\starlette\\middleware\\errors.py", line 164, in \_\_call\_\_  
    await self.app(scope, receive, \_send)  
  File "F:\\Agentic\_Project\\agentic-rag\\.rag\_project\\Lib\\site-packages\\starlette\\middleware\\exceptions.py", line 63, in \_\_call\_\_  
    await wrap\_app\_handling\_exceptions(self.app, conn)(scope, receive, send)  
  File "F:\\Agentic\_Project\\agentic-rag\\.rag\_project\\Lib\\site-packages\\starlette\\\_exception\_handler.py", line 53, in wrapped\_app  
    raise exc  
  File "F:\\Agentic\_Project\\agentic-rag\\.rag\_project\\Lib\\site-packages\\starlette\\\_exception\_handler.py", line 42, in wrapped\_app  
    await app(scope, receive, sender)  
  File "F:\\Agentic\_Project\\agentic-rag\\.rag\_project\\Lib\\site-packages\\fastapi\\middleware\\asyncexitstack.py", line 18, in \_\_call\_\_  
    await self.app(scope, receive, send)  
  File "F:\\Agentic\_Project\\agentic-rag\\.rag\_project\\Lib\\site-packages\\starlette\\routing.py", line 660, in \_\_call\_\_  
    await self.middleware\_stack(scope, receive, send)  
  File "F:\\Agentic\_Project\\agentic-rag\\.rag\_project\\Lib\\site-packages\\fastapi\\routing.py", line 2734, in app  
    await route.handle(scope, receive, send)  
  File "F:\\Agentic\_Project\\agentic-rag\\.rag\_project\\Lib\\site-packages\\fastapi\\routing.py", line 1281, in handle  
    await super().handle(scope, receive, send)  
  File "F:\\Agentic\_Project\\agentic-rag\\.rag\_project\\Lib\\site-packages\\starlette\\routing.py", line 276, in handle  
    await self.app(scope, receive, send)  
  File "F:\\Agentic\_Project\\agentic-rag\\.rag\_project\\Lib\\site-packages\\fastapi\\routing.py", line 158, in app  
    await wrap\_app\_handling\_exceptions(app, request)(scope, receive, send)  
  File "F:\\Agentic\_Project\\agentic-rag\\.rag\_project\\Lib\\site-packages\\starlette\\\_exception\_handler.py", line 53, in wrapped\_app  
    raise exc  
  File "F:\\Agentic\_Project\\agentic-rag\\.rag\_project\\Lib\\site-packages\\starlette\\\_exception\_handler.py", line 42, in wrapped\_app  
    await app(scope, receive, sender)  
  File "F:\\Agentic\_Project\\agentic-rag\\.rag\_project\\Lib\\site-packages\\fastapi\\routing.py", line 144, in app  
    response \= await f(request)  
               ^^^^^^^^^^^^^^^^  
  File "F:\\Agentic\_Project\\agentic-rag\\.rag\_project\\Lib\\site-packages\\fastapi\\routing.py", line 706, in app  
    raw\_response \= await run\_endpoint\_function(  
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^  
    ...\<3 lines\>...  
    )  
    ^  
  File "F:\\Agentic\_Project\\agentic-rag\\.rag\_project\\Lib\\site-packages\\fastapi\\routing.py", line 354, in run\_endpoint\_function  
    return await run\_in\_threadpool(dependant.call, \*\*values)  
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^  
  File "F:\\Agentic\_Project\\agentic-rag\\.rag\_project\\Lib\\site-packages\\starlette\\concurrency.py", line 34, in run\_in\_threadpool  
    return await anyio.to\_thread.run\_sync(func)  
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^  
  File "F:\\Agentic\_Project\\agentic-rag\\.rag\_project\\Lib\\site-packages\\anyio\\to\_thread.py", line 65, in run\_sync  
    return await get\_async\_backend().run\_sync\_in\_worker\_thread(  
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^  
        func, args, abandon\_on\_cancel=abandon\_on\_cancel, limiter=limiter  
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^  
    )  
    ^  
  File "F:\\Agentic\_Project\\agentic-rag\\.rag\_project\\Lib\\site-packages\\anyio\\\_backends\\\_asyncio.py", line 2641, in run\_sync\_in\_worker\_thread  
    return await future  
           ^^^^^^^^^^^^  
  File "F:\\Agentic\_Project\\agentic-rag\\.rag\_project\\Lib\\site-packages\\anyio\\\_backends\\\_asyncio.py", line 1033, in run  
    result \= context.run(func, \*args)  
  File "F:\\Agentic\_Project\\agentic-rag\\src\\agentic\_rag\\api\\main.py", line 71, in query  
    result \= http\_request.app.state.rag\_graph.invoke(  
        initial\_state,  
        config=config,  
    )  
  File "F:\\Agentic\_Project\\agentic-rag\\.rag\_project\\Lib\\site-packages\\langgraph\\pregel\\main.py", line 3913, in invoke  
    for chunk in self.stream(  
                 \~\~\~\~\~\~\~\~\~\~\~^  
        input,  
        ^^^^^^  
    ...\<11 lines\>...  
        \*\*kwargs,  
        ^^^^^^^^^  
    ):  
    ^  
  File "F:\\Agentic\_Project\\agentic-rag\\.rag\_project\\Lib\\site-packages\\langgraph\\pregel\\main.py", line 2967, in stream  
    for \_ in runner.tick(  
             \~\~\~\~\~\~\~\~\~\~\~^  
        \[t for t in loop.tasks.values() if not t.writes\],  
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^  
    ...\<2 lines\>...  
        schedule\_task=loop.accept\_push,  
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^  
    ):  
    ^  
  File "F:\\Agentic\_Project\\agentic-rag\\.rag\_project\\Lib\\site-packages\\langgraph\\pregel\\\_runner.py", line 207, in tick  
    run\_with\_retry(  
    \~\~\~\~\~\~\~\~\~\~\~\~\~\~^  
        t,  
        ^^  
    ...\<10 lines\>...  
        },  
        ^^  
    )  
    ^  
  File "F:\\Agentic\_Project\\agentic-rag\\.rag\_project\\Lib\\site-packages\\langgraph\\pregel\\\_retry.py", line 617, in run\_with\_retry  
    return task.proc.invoke(task.input, config)  
           \~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~^^^^^^^^^^^^^^^^^^^^  
  File "F:\\Agentic\_Project\\agentic-rag\\.rag\_project\\Lib\\site-packages\\langgraph\\\_internal\\\_runnable.py", line 684, in invoke  
    input \= context.run(step.invoke, input, config, \*\*kwargs)  
  File "F:\\Agentic\_Project\\agentic-rag\\.rag\_project\\Lib\\site-packages\\langgraph\\\_internal\\\_runnable.py", line 426, in invoke  
    ret \= self.func(\*args, \*\*kwargs)  
  File "F:\\Agentic\_Project\\agentic-rag\\src\\agentic\_rag\\graph\\nodes.py", line 214, in retrieve  
    print(f"\\nContent preview:\\n{\_preview(doc.page\_content)}")  
    \~\~\~\~\~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^  
  File "C:\\Users\\USER\\AppData\\Roaming\\uv\\python\\cpython-3.13-windows-x86\_64-none\\Lib\\encodings\\cp1252.py", line 19, in encode  
    return codecs.charmap\_encode(input,self.errors,encoding\_table)\[0\]  
           \~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^  
UnicodeEncodeError: 'charmap' codec can't encode character '\\ufb01' in position 127: character maps to \<undefined\>  
During task with name 'retrieve' and id '2d8e5492-1750-56ae-b1dd-2e32a9184385'

