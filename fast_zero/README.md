# Resolução de erros que surgiram

## 1) Configuração de PATH do Poetry | fastapi[standard] - Não reconhece o diretório de binários
```python
(fast-zero-py3.12) ➜  fast_zero git:(main) ✗ fastapi --help

To use the fastapi command, please install "fastapi[standard]":

        pip install "fastapi[standard]"

Traceback (most recent call last):
  File "/home/alunaris/.cache/pypoetry/virtualenvs/fast-zero-3leACWDJ-py3.12/bin/fastapi", line 8, in <module>
    sys.exit(main())
             ^^^^^^
  File "/home/alunaris/.cache/pypoetry/virtualenvs/fast-zero-3leACWDJ-py3.12/lib/python3.12/site-packages/fastapi/cli.py", line 12, in main
    raise RuntimeError(message)  # noqa: B904
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^
RuntimeError: To use the fastapi command, please install "fastapi[standard]":

        pip install "fastapi[standard]"
```

Mesmo instalando o fastapi corretamente, ele ainda não conseguia reconhecer o PATH do local de instalação, então era necessário exportar o diretório de binários do Poetry no PATH (usando o ./zshrc):

```python
export PATH="$HOME/.cache/pypoetry/virtualenvs/fast-zero-3leACWDJ-py3.12/bin:$PATH"
```

Depois, é salvo o arquivo zshrc, recarregando o terminal:

```python
source ~/.zshrc
```

Após isso, é executado o comando abaixo para rodar o servidor:

```python
fastapi dev fast_zero/app.py
```

