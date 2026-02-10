# smartsort-gl

A tiny Python package that canonicalizes **GL Strings** by *smart sorting*:
- recursively sorts within delimiter levels in precedence: `^`, `|`, `+`, `~`, `/`
- orders blocks by **gene/locus** (left of `*`)
- orders alleles **numerically** (not lexically) within a locus (e.g., `A*01:11` before `A*01:103`)
- strips suffixes for numeric comparison (e.g., `01:01N` compares as `01:01`)

This is a Python port of `SmartSort.pm` (2012-11-14).

## Install (local)

From the project directory:

```bash
python -m pip install -U pip
python -m pip install -e .
```

## Usage (Python)

```python
from smartsort_gl import smart_sort

print(smart_sort("A*01:103+A*01:11"))
# A*01:11+A*01:103
```

## Usage (CLI)

Sort a single GL string:

```bash
gl-smartsort "B*07:02^A*02:01"
```

Or sort from stdin (one per line):

```bash
cat gl.txt | gl-smartsort
```

## License

MIT
