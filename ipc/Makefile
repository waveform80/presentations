DOT_FILES=$(wildcard *.dot)
SVG_FILES=$(DOT_FILES:%.dot=%.svg)

all: $(SVG_FILES)

%.svg: %.dot
	dot -Tsvg -o$@ $<
