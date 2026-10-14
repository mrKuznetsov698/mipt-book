# Trigonometric Equations, Systems, and Inequalities

An editable LaTeX transcription of all 244 problems from 19 photographs of pages
29–47. The layout replicates the structure of the printed book: identical page boundaries,
a compact two-line chapter heading, bottom page numbers with no running header,
mirrored margins, bold problem numbers, function notation matching the `Преобразования.pdf` reference sample, and exam ticket labels
to the right of the formulas. No photographs are embedded in place of text.

## Page Size and Fonts

The demo build uses a book format of 145 × 215 mm.
This is a close approximation rather than a physically measured size of a printed copy.
Based on the user's link, the title and ISBN of the publication were identified:
*"Методическое пособие по математике для старшеклассников и абитуриентов"* (*Study Guide in Mathematics for High School Students and University Applicants*),
6th edition, 2018, ISBN 978-5-89155-295-1.
The bibliographic record from the Ryazan Regional Library lists a
height of 22 cm, but no width. The cover size and trimmed page size may
differ. Unscaled photographs do not allow determining exact dimensions in millimeters.

Sources for size and identification:
- https://urss.ru/cgi-bin/db.pl?blang=ru&id=237712&lang=Ru&page=Book
- https://kraeved.rounb.ru/uploads/new/2020/new022020.pdf

The main text font is Nimbus Roman, metrically close to Times; the math font is
Computer Modern, matching the `Преобразования.pdf` reference sample. This is a visual match: the exact font names
used in the original book cannot be determined from photographs. The notations sin, cos, tg, ctg,
and inverse functions are set upright; variables are italicized. The font size is 10 pt with 11.5 pt leading.

## Files

- `trigonometry.tex` — includable chapter file, without preamble or `\begin{document}`.
- `trig-chapter.sty` — styling, page numbering, and mathematical operators.
- `main.tex` — sample build file configuring page dimensions and fonts.
- `trigonometry.pdf` — 19 sample pages, numbered 29–47.
- `Makefile` — build and verification rules.
- `check_layout.py` — script to verify page boundaries, problem numbers, and the placement of all exam ticket labels.

## Including in a Master Book with Matching Styling

Place `trig-chapter.sty` next to the master book file,
and `trigonometry.tex` in a subdirectory such as `chapters/`.
Use the preamble from `main.tex`. The following settings are essential:

```latex
\documentclass[10pt,twoside,openany]{book}
\usepackage{fontspec}
\setmainfont{NimbusRoman-Regular.otf}[
  BoldFont=NimbusRoman-Bold.otf,
  ItalicFont=NimbusRoman-Italic.otf,
  BoldItalicFont=NimbusRoman-BoldItalic.otf]
\newfontfamily\cyrillicfont{NimbusRoman-Regular.otf}[
  BoldFont=NimbusRoman-Bold.otf,
  ItalicFont=NimbusRoman-Italic.otf,
  BoldItalicFont=NimbusRoman-BoldItalic.otf,
  Script=Default]
\usepackage{polyglossia}
\setdefaultlanguage{russian}
\usepackage[
  paperwidth=145mm,paperheight=215mm,
  inner=14mm,outer=11mm,top=16mm,bottom=15mm,
  headheight=10pt,headsep=5pt]{geometry}
\usepackage{trig-chapter}
```

In the document body:

```latex
\input{chapters/trigonometry.tex}
```

The chapter file itself does not set fonts, geometry, language, or TeX engine, nor does it modify
the page counter. To match the intended layout, use the parameters from the sample file.
Hard page breaks matching the original pages are preserved inside the file:
changing the page dimensions or font size of the master book may require manual adjustment.

The chapter is numbered using the standard `chapter` counter; instead of the default large
heading, it uses `\TrigChapter`, which also adds the chapter entry
to the table of contents. By default, problem numbers are hardcoded as 2.1–2.244.
To bind them dynamically to the current chapter number:

```latex
\renewcommand{\TrigNumberPrefix}{\thechapter}

```

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

The output is `main.pdf`. Requires XeLaTeX, Nimbus Roman OpenType fonts
(typically provided by the `fonts-urw-base35` package), and the packages listed in the preamble. LuaLaTeX is also
compatible with a full TeX installation, though verification was performed with XeLaTeX.

The counters in `main.tex` are set strictly to demonstrate Chapter 2 starting on page
29. Remove those two counter assignments in the master book so numbering continues automatically.

## Preserved Inconsistencies from the Original

* Problems 2.229–2.232 state "Решить неравенство" ("Solve the inequality"), but are printed with an `=` sign.
* Problem 2.203 is labeled "Билет 10, 2009" ("Ticket 10, 2009"), duplicating the label of 2.202.
* Several equations and systems from 2010 share identical ticket numbers.

Mathematical problem statements were not altered by guesswork. During layout adjustments,
all 244 formulas were automatically verified against the initial transcription to ensure zero drift.
All 19 problem number ranges were checked against the original pages, and no formulas
overflow the margins. An exact facsimile match of fonts and coordinates
cannot be guaranteed from angled photographs; this is a reconstructed LaTeX typesetting.

## Formatting of Ticket Labels and Long Problem Statements

All exam ticket labels are anchored to their respective formulas, including in problems where the formula
is followed by additional conditions or sub-items. Any text following a formula is placed
separately from the ticket label. Long equations in 2.194 and 2.196 are split across two lines
so the ticket label fits to the right of the math block.

In 2.37–2.40, line breaks are placed between logical clauses of the problem statement, avoiding hyphenation
of the word "выполняется". Continuation lines are aligned with the start of the text following the problem number.
There is no running header; page numbers are centered at the bottom.
