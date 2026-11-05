# Site Take 1 Comunicação

Site estático em HTML + CSS (Tailwind compilado) + JS puro.

## Publicar

Suba para o servidor:

- `index.html` e as pastas das páginas (`quem-somos/`, `publicidade/`, `comunicacao-empresarial/`,
  `marketing-digital/`, `design-grafico/`, `videos-de-treinamento/`, `regulamentacao-de-rifas/`,
  `clientes/`, `fale-conosco/`);
- `assets/`, `sitemap.xml` e `robots.txt`.

**Não** suba `src/`, `tailwind.config.js` nem este `README.md`.

> Antes de publicar, troque todos os quadros marcados "Imagem a definir" por imagens reais
> (procure `reservado` em `src/paginas/` e em `src/build.py`).

## Editar

O HTML publicado é **gerado**. Não edite `index.html` nem `*/index.html` à mão.

- `src/build.py` — cabeçalho, rodapé, menu, contatos, metadados de SEO, perguntas frequentes,
  lista de clientes e o conteúdo das 6 páginas de serviço (`SERVICO_DADOS`).
- `src/paginas/*.html` — miolo das páginas Início, Quem somos, Clientes e Fale conosco.
- `src/input.css` e `tailwind.config.js` — estilos e paleta oficial (`vinho` #aa2845).

Depois de editar, rode na raiz:

```bash
python3 src/build.py
npx tailwindcss@3.4 -i ./src/input.css -o ./assets/css/style.css --minify
```

## Ver localmente

Os links usam endereços de pasta (`/quem-somos/`), então abra por um servidor:

```bash
python3 -m http.server 8123
```

e acesse http://127.0.0.1:8123/
