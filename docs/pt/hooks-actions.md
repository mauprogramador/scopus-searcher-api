# Hooks e Actions

Ao desenvolver uma aplicação, é comum utilizar diferentes tecnologias para assegurar  uma boa condição do código e seu funcionamento. Para isso, podemos utilizar ferramentas de verificação e integração quando ocorrem certas ações importantes no {{abbr.versioningPt}} do código.

## Git Hooks

Abaixo esta o script do [Git Hook](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks){:target="\_blank"} do {{abbr.clientSidePt}} usado nesta aplicação, é chamado de `pre-commit` porque é o primeiro que será executado automaticamente localmente quando ocorrer um {{abbr.commit}}, e irá executar determinadas ações de checagem dependendo dos arquivos que foram alterados e que estão sendo comitados.

- Executa o {{abbr.lint}} quando arquivos da pasta `app` forem comitados.
- Executa o {{abbr.lint}} quando arquivos da pasta `tests` forem comitados.
- Executa a **Auditoria de Vulnerabilidade** quando arquivos da pasta `requirements` forem comitados, o que significa que novas bibliotecas, pacotes ou dependências foram instalados.
- Executa os **Testes** de qualquer forma, garantindo que tudo esteja funcionando.

```sh title="pre-commit" linenums="1"
#!/bin/bash

make format

if git diff --cached --name-only | grep -q '^app/'; then
  make lint
fi

if git diff --cached --name-only | grep -q '^tests/'; then
  make lint-tests
fi

if git diff --cached --name-only | grep -q '^requirements/'; then
  make audit
fi

make test
```

!!! tip

    Não se esqueça de conceder as permissões necessárias para os arquivos de hook.
    ```zsh
    chmod +x .git/hooks/pre-commit
    ```

## GitHub Actions

No {{abbr.serverSidePt}}, esta aplicação usa o [GitHub Actions](https://github.com/features/actions){:target="\_blank"} para criar {{abbr.workflows}} que serão acionados automaticamente quando ocorrer um evento `push` no repositório remoto do [GitHub](https://github.com/){:target="\_blank"}, automatizando a execução automática dos trabalhos de verificação e implantação.

### [Trabalho de Verificação :octicons-link-external-16:]({{links.workflows}}/verification.yml){:target="\_blank"}

Para **{{abbr.linting}} and Testes**, ele verificará o repositório, configurará o [Python](https://www.python.org/){:target="\_blank"}, instalará o [Poetry](https://python-poetry.org/){:target="\_blank"}, carregará o {{abbr.venv}} em cache e instalará todas as dependências necessárias, como [Pytest](https://docs.pytest.org/en/8.0.x/contents.html){:target="\_blank"} e [Pylint](https://pylint.readthedocs.io/en/stable/){:target="\_blank"}, para realizar operações de *lint* e teste no código, garantindo que tudo esteja bem.

### [Trabalho de Documentação :octicons-link-external-16:]({{links.workflows}}/documentation.yml){:target="\_blank"}

Ele verificará o repositório, configurará o [Python](https://www.python.org/){:target="\_blank"}, carregará o {{abbr.venv}} em cache, e instalará as bibliotecas [MkDocs](https://www.mkdocs.org/){:target="\_blank"} e [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/){:target="\_blank"} para configurar, fazer o {{abbr.deploy}} e [publicar](https://squidfunk.github.io/mkdocs-material/publishing-your-site/){:target="\_blank"} a página web estática da documentação da aplicação, escrita em [Markdown](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax){:target="\_blank"}, e que será hospedada no [GitHub Pages](https://pages.github.com/){:target="\_blank"} no domínio `github.io` do [GitHub](https://github.com/){:target="\_blank"}.
