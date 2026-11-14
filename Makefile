PAPER_DIR := paper
BUILD_DIR := build
MAIN      := main
PYTHON    ?= python3
SYNC_ARGS ?=

.PHONY: pdf sync clean

# Build paper/build/main.pdf
pdf:
	cd $(PAPER_DIR) && latexmk -pdf -interaction=nonstopmode -halt-on-error \
		-file-line-error -outdir=$(BUILD_DIR) $(MAIN).tex

# Copy result tables and figures from dx300-sim into results/
sync:
	$(PYTHON) scripts/sync_results.py $(SYNC_ARGS)

# Remove LaTeX build output (results/ is kept)
clean:
	rm -rf $(PAPER_DIR)/$(BUILD_DIR)
