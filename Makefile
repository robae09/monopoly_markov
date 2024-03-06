all: rapport

repport: rapport

rapport:
	@cd Rapport; \
	pdflatex Rapport.tex -interaction=nonstopmode > /dev/null
	@# Compile deux fois pour les bibliothèques
	@cd Rapport; \
	pdflatex Rapport.tex -interaction=nonstopmode > /dev/null

install:
	sudo apt-get install python3 python3-tk python3-numpy

clean: cleanLatex cleanPython

cleanPython:
	@find . | grep -E "\(__pycache__|\.pyc|\.pyo$\)" | xargs -I{} rm {}

cleanLatex:
	@rm -f Rapport/Rapport.aux Rapport/Rapport.log Rapport/Rapport.out Rapport/Rapport.pdf Rapport/Rapport.dvi

