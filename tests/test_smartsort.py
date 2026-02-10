\
from smartsort_gl import smart_sort

def test_basic_numeric_order():
    assert smart_sort("A*01:103+A*01:11") == "A*01:11+A*01:103"

def test_locus_ordering_blocks():
    assert smart_sort("B*07:02^A*02:01") == "A*02:01^B*07:02"

def test_suffix_stripping():
    assert smart_sort("A*01:01N+A*01:01") == "A*01:01+A*01:01N"

def test_nested_delims():
    # + inside ^
    assert smart_sort("A*02:01+A*01:01^B*08:01+B*07:02") == "A*01:01+A*02:01^B*07:02+B*08:01"
