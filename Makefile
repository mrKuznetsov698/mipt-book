.PHONY: all check
PYTHON ?= python3

all: trigonometry.pdf

trigonometry.pdf: main.tex preamble.tex trigonometry.tex trig-chapter.sty
	xelatex -interaction=nonstopmode -halt-on-error main.tex
	xelatex -interaction=nonstopmode -halt-on-error main.tex
	cp main.pdf trigonometry.pdf

check: trigonometry.pdf
	$(PYTHON) check_layout.py trigonometry.pdf
