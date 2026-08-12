UVICORN ERROR : 

INFO:     127.0.0.1:59716 \- "POST /query HTTP/1.1" 500 Internal Server Error  
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
  File "F:\\Agentic\_Project\\agentic-rag\\src\\agentic\_rag\\api\\main.py", line 23, in query  
    result \= rag\_graph.invoke({"question": request.question, "retry\_count": 0})  
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
  File "F:\\Agentic\_Project\\agentic-rag\\src\\agentic\_rag\\graph\\nodes.py", line 9, in retrieve  
    retriever \= get\_retriever()  
  File "F:\\Agentic\_Project\\agentic-rag\\src\\agentic\_rag\\retrieval\\vectorstore.py", line 21, in get\_retriever  
    return get\_vectorstore().as\_retriever(search\_kwargs={"k": k})  
           \~\~\~\~\~\~\~\~\~\~\~\~\~\~\~^^  
  File "F:\\Agentic\_Project\\agentic-rag\\src\\agentic\_rag\\retrieval\\vectorstore.py", line 13, in get\_vectorstore  
    return PineconeVectorStore(  
        index\_name=settings.pinecone\_index\_name,  
        embedding=\_embeddings,  
        pinecone\_api\_key=settings.pinecone\_api\_key,  
    )  
  File "F:\\Agentic\_Project\\agentic-rag\\.rag\_project\\Lib\\site-packages\\langchain\_pinecone\\vectorstores.py", line 262, in \_\_init\_\_  
    \_index \= client.Index(name=\_index\_name)  
  File "F:\\Agentic\_Project\\agentic-rag\\.rag\_project\\Lib\\site-packages\\pinecone\\pinecone.py", line 490, in Index  
    index\_host \= self.db.index.\_get\_host(name)  
  File "F:\\Agentic\_Project\\agentic-rag\\.rag\_project\\Lib\\site-packages\\pinecone\\db\_control\\resources\\sync\\index.py", line 245, in \_get\_host  
    return self.\_index\_host\_store.get\_host(  
           \~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~^  
        api=self.\_index\_api, config=self.config, index\_name=name  
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^  
    )  
    ^  
  File "F:\\Agentic\_Project\\agentic-rag\\.rag\_project\\Lib\\site-packages\\pinecone\\db\_control\\index\_host\_store.py", line 47, in get\_host  
    description \= api.describe\_index(index\_name)  
  File "F:\\Agentic\_Project\\agentic-rag\\.rag\_project\\Lib\\site-packages\\pinecone\\openapi\_support\\endpoint.py", line 102, in \_\_call\_\_  
    return self.callable(self, \*args, \*\*kwargs)  
           \~\~\~\~\~\~\~\~\~\~\~\~\~^^^^^^^^^^^^^^^^^^^^^^^  
  File "F:\\Agentic\_Project\\agentic-rag\\.rag\_project\\Lib\\site-packages\\pinecone\\core\\openapi\\db\_control\\api\\manage\_indexes\_api.py", line 883, in \_\_describe\_index  
    return self.call\_with\_http\_info(\*\*kwargs)  
           \~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~^^^^^^^^^^  
  File "F:\\Agentic\_Project\\agentic-rag\\.rag\_project\\Lib\\site-packages\\pinecone\\openapi\_support\\endpoint.py", line 134, in call\_with\_http\_info  
    return self.api\_client.call\_api(  
           \~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~^  
        self.settings\["endpoint\_path"\],  
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^  
    ...\<16 lines\>...  
        collection\_formats=params\["collection\_format"\],  
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^  
    )  
    ^  
  File "F:\\Agentic\_Project\\agentic-rag\\.rag\_project\\Lib\\site-packages\\pinecone\\openapi\_support\\api\_client.py", line 306, in call\_api  
    return self.\_\_call\_api(  
           \~\~\~\~\~\~\~\~\~\~\~\~\~\~\~^  
        resource\_path,  
        ^^^^^^^^^^^^^^  
    ...\<14 lines\>...  
        \_check\_type,  
        ^^^^^^^^^^^^  
    )  
    ^  
  File "F:\\Agentic\_Project\\agentic-rag\\.rag\_project\\Lib\\site-packages\\pinecone\\openapi\_support\\api\_client.py", line 182, in \_\_call\_api  
    raise e  
  File "F:\\Agentic\_Project\\agentic-rag\\.rag\_project\\Lib\\site-packages\\pinecone\\openapi\_support\\api\_client.py", line 170, in \_\_call\_api  
    response\_data \= self.request(  
        method,  
    ...\<6 lines\>...  
        \_request\_timeout=\_request\_timeout,  
    )  
  File "F:\\Agentic\_Project\\agentic-rag\\.rag\_project\\Lib\\site-packages\\pinecone\\openapi\_support\\api\_client.py", line 360, in request  
    return self.rest\_client.GET(  
           \~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~^  
        url,  
        ^^^^  
    ...\<3 lines\>...  
        headers=headers,  
        ^^^^^^^^^^^^^^^^  
    )  
    ^  
  File "F:\\Agentic\_Project\\agentic-rag\\.rag\_project\\Lib\\site-packages\\pinecone\\openapi\_support\\rest\_utils.py", line 75, in GET  
    return self.request(  
           \~\~\~\~\~\~\~\~\~\~\~\~^  
        "GET",  
        ^^^^^^  
    ...\<4 lines\>...  
        query\_params=query\_params,  
        ^^^^^^^^^^^^^^^^^^^^^^^^^^  
    )  
    ^  
  File "F:\\Agentic\_Project\\agentic-rag\\.rag\_project\\Lib\\site-packages\\pinecone\\openapi\_support\\rest\_urllib3.py", line 267, in request  
    return raise\_exceptions\_or\_return(r)  
  File "F:\\Agentic\_Project\\agentic-rag\\.rag\_project\\Lib\\site-packages\\pinecone\\openapi\_support\\rest\_utils.py", line 44, in raise\_exceptions\_or\_return  
    raise NotFoundException(http\_resp=r)  
pinecone.exceptions.exceptions.NotFoundException: (404)  
Reason: Not Found  
HTTP response headers: HTTPHeaderDict({'content-type': 'text/plain; charset=utf-8', 'vary': 'origin, access-control-request-method, access-control-request-headers', 'access-control-allow-origin': '\*', 'access-control-expose-headers': '\*', 'x-pinecone-api-version': '2025-04', 'x-cloud-trace-context': '5740c17926c0e3081d548ded3293d2ef', 'date': 'Tue, 04 Aug 2026 08:03:25 GMT', 'server': 'Google Frontend', 'Content-Length': '86', 'Via': '1.1 google', 'Alt-Svc': 'h3=":443"; ma=2592000'})  
HTTP response body: {"error":{"code":"NOT\_FOUND","message":"Resource agentic-rag not found"},"status":404}

During task with name 'retrieve' and id '9ba23e7c-cbb3-e322-bea7-4d2613093537'

STREAMLIT ERROR:

────────────────────────── Traceback (most recent call last) ───────────────────────────  
  F:\\Agentic\_Project\\agentic-rag\\.rag\_project\\Lib\\site-packages\\streamlit\\runtime\\scri    
  ptrunner\\exec\_code.py:129 in exec\_func\_with\_error\_handling                              
                                                                                          
  F:\\Agentic\_Project\\agentic-rag\\.rag\_project\\Lib\\site-packages\\streamlit\\runtime\\scri    
  ptrunner\\script\_runner.py:807 in code\_to\_exec                                           
                                                                                          
  F:\\Agentic\_Project\\agentic-rag\\app\\streamlit\_app.py:18 in \<module\>                      
                                                                                          
    15 if question:                                                                       
    16 │   with st.spinner("Thinking..."):                                                
    17 │   │   response \= requests.post(f"{API\_URL}/query", json={"question": question    
  ❱ 18 │   │   response.raise\_for\_status()                                                
    19 │   │   data \= response.json()                                                     
    20 │                                                                                  
    21 │   st.markdown(data\["answer"\])                                                    
                                                                                          
  F:\\Agentic\_Project\\agentic-rag\\.rag\_project\\Lib\\site-packages\\requests\\models.py:116    
  7 in raise\_for\_status                                                                   
                                                                                          
    1164 │   │   │   )                                                                    
    1165 │   │                                                                            
    1166 │   │   if http\_error\_msg:                                                       
  ❱ 1167 │   │   │   raise HTTPError(http\_error\_msg, response=self)                       
    1168 │                                                                                
    1169 │   def close(self) \-\> None:                                                     
    1170 │   │   """Releases the connection back to the pool. Once this method has bee    
────────────────────────────────────────────────────────────────────────────────────────  
HTTPError: 500 Server Error: Internal Server Error for url: http://localhost:8000/query  
