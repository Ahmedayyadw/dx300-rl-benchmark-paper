# Is Reinforcement Learning Worth It? A Benchmark-Driven Design Study of Learned Control for an Excavator Boom

Paper repository (LaTeX sources and result snapshots). Experiments live in
[dx300-sim](https://github.com/Ahmedayyadw/dx300-sim).

## Summary

This paper asks when reinforcement learning is worth using on a hydraulic machine, and
answers with a benchmark on the DX300 excavator boom. Learned controllers (SAC, and the
Lab 13 set: PPO, TD3, BC, CQL, IQL) are compared against an economical payload-aware PID
on a validated plant model, in tip accuracy and in energy. Working thesis, to be confirmed
once Lab 13 finishes: no learned controller beats that PID on both accuracy and energy, so
the contribution is a design procedure for deciding, with evidence, whether learning is
justified. Written for the Design of AI Systems course (Okan University).

| | |
|---|---|
| Target venue | ICEEE 2027, Ankara, Track 2 (Control Systems, Automation & Computing Technologies) |
| Format | IEEEtran conference, 4-8 double-column pages |
| Submission deadline | 1 December 2026 |
| Experiments | [github.com/Ahmedayyadw/dx300-sim](https://github.com/Ahmedayyadw/dx300-sim) |

## Repository layout

```
paper/
  main.tex            IEEEtran conference skeleton, one \input per section
  refs.bib            bibliography
  sections/           one file per section
results/              tables and figures copied from dx300-sim (see SOURCE.md)
scripts/
  sync_results.py     copies results from dx300-sim, writes results/SOURCE.md
Makefile              pdf, sync, clean
```

## Build the PDF

Requirements: TeX Live with `latexmk` and the `IEEEtran` class.

```bash
make pdf
```

Output: `paper/build/main.pdf`. `make clean` removes `paper/build/`.

The bibliography lines at the end of `paper/main.tex` are commented out until the first
`\cite`, because BibTeX fails on a document with no citations.

## Sync results

No experiment runs in this repository. Result tables and figures are copied from a local
dx300-sim checkout:

```bash
make sync
```

- Source: `~/ahmed/dx300-sim` by default. Override with the `DX300_SIM` environment
  variable or `make sync SYNC_ARGS="--src /path/to/dx300-sim"`.
- The list of files is `SOURCES` in [scripts/sync_results.py](scripts/sync_results.py).
- Files that do not exist yet (for example the Lab 13 benchmark) are skipped with a warning.
- `results/SOURCE.md` records the dx300-sim commit hash, and for each file whether it
  matched that commit when it was copied.
- The sync only reads from dx300-sim. It never writes there.

Do not edit files in `results/` by hand. Change them in dx300-sim, then sync and commit.

## Section status

| # | Section | File | Status |
|---|---------|------|--------|
| - | Abstract | [00_abstract.tex](paper/sections/00_abstract.tex) | Not started |
| I | Introduction | [01_introduction.tex](paper/sections/01_introduction.tex) | Not started |
| II | Design requirements | [02_design_requirements.tex](paper/sections/02_design_requirements.tex) | Not started |
| III | Method selection (on/off-policy, online/offline) | [03_method_selection.tex](paper/sections/03_method_selection.tex) | Not started |
| IV | Benchmark protocol | [04_benchmark_protocol.tex](paper/sections/04_benchmark_protocol.tex) | Not started |
| V | Results | [05_results.tex](paper/sections/05_results.tex) | Not started |
| VI | Why learning lost and when it would win | [06_why_learning_lost.tex](paper/sections/06_why_learning_lost.tex) | Not started |
| VII | Design lessons | [07_design_lessons.tex](paper/sections/07_design_lessons.tex) | Not started |
| VIII | Conclusion | [08_conclusion.tex](paper/sections/08_conclusion.tex) | Not started |

Each section file starts with a TODO comment that lists the dx300-sim files feeding it.

## Contributing

- Commits follow [Conventional Commits](https://www.conventionalcommits.org/).
- Optional hooks: `pre-commit install` (trailing whitespace, end of file, YAML check).

## Citation

See [CITATION.cff](CITATION.cff).

## License

MIT. See [LICENSE](LICENSE).
