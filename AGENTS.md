# Agents

## Building the PDF

Always use the compile script to build the PDF:

```
./build.sh
```

Rebuild after making any changes to `slides.tex` or any other LaTeX source files.

## Citations

Citations use `biblatex` with a `biber` backend. The bibliography file is `refs.bib`, copied from the companion paper repo at `/Users/ianturner/research/qserver-report/`.

When adding content to a slide that corresponds to a section of the paper, mirror the citations used in that section of `main.tex`. Use `\cite{key}` inline (with a non-breaking space before it: `word~\cite{key}`). The References slide at the end is populated automatically via `\printbibliography`.
