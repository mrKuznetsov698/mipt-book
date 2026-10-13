.PHONY: all check

all: trigonometry.pdf

trigonometry.pdf: main.tex trigonometry.tex trig-chapter.sty
	xelatex -interaction=nonstopmode -halt-on-error main.tex
	xelatex -interaction=nonstopmode -halt-on-error main.tex
	cp main.pdf trigonometry.pdf

check: trigonometry.pdf
	python3 check_layout.py trigonometry.pdf
