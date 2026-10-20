# Trigonometric Equations, Systems, and Inequalities

An editable LaTeX transcription of all 244 problems from 19 photographs of pages
29–47. The demo uses the shared [Fi_tex preamble](https://github.com/sstellariaa/Fi_tex):
landscape A4 with two columns. Problem numbers, formulas, and exam ticket labels
are preserved as editable text; no photographs are embedded in their place.

## Page Size, Fonts, and Languages

The demo uses landscape A4 (297 × 210 mm), with 1 cm side margins and 1.5 cm
top/bottom margins. Two columns are separated by a 2 cm gap and a 0.4 pt rule.
Text is 10 pt with 12 pt leading so consecutive lines and formulas remain legible.
The original template's unsupported `14pt` option for `article` is replaced by
an explicit `10pt` setting; the sample's 8 pt leading is not used.

Fonts and localization are configured together in `preamble.tex`:

```latex
\usepackage{amsmath,amsthm}
\usepackage[regular]{newcomputermodern}
\usepackage{polyglossia}
\setmainlanguage{russian}
\setotherlanguage{english}
```

New Computer Modern provides Cyrillic text and Unicode math. Trigonometric
operators are upright; variables are italic. There is no Babel/fontenc/inputenc
configuration and no `amssymb` dependency. Install Russian hyphenation patterns
as part of the TeX distribution; both Russian and English are available.

The shared preamble also includes `\fr`, `\pd`, `\limm`, `\vect`, the
`Proof` environment, and the `Ex`, `Th`, `Def`, and `Ax` theorem environments
from Fi_tex. Placeholder body text from that repository is not included.

The source book is *Методическое пособие по математике для старшеклассников и
абитуриентов*, 6th edition, 2018, ISBN 978-5-89155-295-1. Its original page
numbers remain as source markers in `trigonometry.tex`; they do not force page
breaks in the two-column build.

Sources for the original publication:
- https://urss.ru/cgi-bin/db.pl?blang=ru&id=237712&lang=Ru&page=Book
- https://kraeved.rounb.ru/uploads/new/2020/new022020.pdf

## Files

- `trigonometry.tex` — includable chapter file, without preamble or `\begin{document}`.
- `trig-chapter.sty` — styling, page numbering, and mathematical operators.
- `main.tex` — sample article that loads the preamble and starts two columns.
- `preamble.tex` — Fi_tex layout and commands, with New Computer Modern and Polyglossia.
- `trigonometry.pdf` — compiled chapter in the current two-column layout.
- `Makefile` — build and verification rules.
- `check_layout.py` — script to verify page boundaries, problem numbers, and the placement of all exam ticket labels.

## Including in a Master Document

Place `preamble.tex` and `trig-chapter.sty` next to the main file,
and `trigonometry.tex` in the same directory or a subdirectory such as `chapters/`.

```latex
\documentclass[10pt,a4paper,landscape]{article}
\input{preamble.tex}
\usepackage[continuous]{trig-chapter}
\usepackage[unicode,hidelinks]{hyperref}
\pdfstringdefDisableCommands{\def\\{ }}

\begin{document}
\pagestyle{trigbook}
\fontsize{10}{12}\selectfont
\setcounter{section}{1}
\begin{multicols}{2}
\input{chapters/trigonometry.tex}
\end{multicols}
\end{document}
```

The `continuous` option removes the old source-page breaks and keeps each
problem together when a column fills. Page numbers are centered at the bottom;
there is no running header. The chapter file does not select fonts or languages.

`\TrigChapter` uses the `section` counter in `article` and the `chapter`
counter in `book`. It also adds an entry to the table of contents. The counter
assignment in the example makes the heading number 2. Problem numbers remain
2.1–2.244 by default. To bind them to the current heading number:

```latex
\renewcommand{\TrigNumberPrefix}{\thesection} % article
% \renewcommand{\TrigNumberPrefix}{\thechapter} % book
```

Without the `continuous` option, the package retains the original fixed
page boundaries for a single-column book. Its geometry must be configured
separately (the previous demo used approximately 145 × 215 mm). Do not use
that mode inside `multicols`.

Cross-references: `\ref{trig:17}`, `\ref{trig:244}`, `\ref{chap:trigonometry}`.
All trigonometric function commands are prefixed with `trig`; global macros
such as `\sin`, `\cos`, and others in the master book are not overridden.

## Building

From the source directory:

```sh
make
make check

```

Verification requires Python 3 with PyMuPDF (`python3-pymupdf` in Debian).
The check validates all 244 exam ticket labels, including their alignment next to the formula
when followed by additional text, as well as line-break alignment in problems 2.37–2.40.
After building, the PDF pages should also be inspected visually.

Manual build commands:

```sh
xelatex -interaction=nonstopmode -halt-on-error main.tex
xelatex -interaction=nonstopmode -halt-on-error main.tex

```

The generated files are `main.pdf` and, after `make`, `trigonometry.pdf`.
Use XeLaTeX with New Computer Modern, fontsetup, Polyglossia, Russian hyphenation
patterns, and the other packages in `preamble.tex`. For TeX Live, the relevant
packages include `newcomputermodern`, `fontsetup`, `polyglossia`, and
`hyphen-russian`; a complete installation already includes them.
The document is Unicode and should not be compiled with pdfLaTeX.

## Preserved Inconsistencies from the Original

* Problems 2.229–2.232 state "Решить неравенство" ("Solve the inequality"), but are printed with an `=` sign.
* Problem 2.203 is labeled "Билет 10, 2009" ("Ticket 10, 2009"), duplicating the label of 2.202.
* Several equations and systems from 2010 share identical ticket numbers.

Mathematical problem statements were not altered by guesswork. During layout adjustments,
all 244 formulas were automatically verified against the initial transcription to ensure zero drift.
The source-page markers and all 244 problem numbers are retained. The layout check
verifies reading order across columns, all ticket labels, and language/layout warnings. An exact facsimile match of fonts and coordinates
cannot be guaranteed from angled photographs; this is a reconstructed LaTeX typesetting.

## Formatting of Ticket Labels and Long Problem Statements

All exam ticket labels are anchored to their respective formulas, including in problems where the formula
is followed by additional conditions or sub-items. Any text following a formula is placed
separately from the ticket label. Long equations in 2.194 and 2.196 are split across two lines
so the ticket label fits to the right of the math block.

In 2.37–2.40, line breaks are placed between logical clauses of the problem statement, avoiding hyphenation
of the word "выполняется". Continuation lines are aligned with the start of the text following the problem number.
There is no running header; page numbers are centered at the bottom.
