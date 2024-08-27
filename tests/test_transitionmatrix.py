import pytest
import math
from modules.file import File
from modules.transtition_matrix import TransitionMatrix

@pytest.mark.parametrize("key, value", [
    (('a', 'b'), ['c', 'd']),
    (('b', 'c'), ['a', None]),
    (('c', 'a'), ['b']),
    (('b', 'd'), ['a']),
    (('d', 'a'), ['b']),
])
def test_prefix_stat(key, value):
    matrix = TransitionMatrix(['a', 'b', 'c', 'a', 'b', 'd', 'a', 'b', 'c'], 2)
    prefixes = matrix.make_matrix()
    assert key in prefixes.keys(), f"Префикс {key} отсутствует"
    suffixes = [key for key in prefixes[key].keys()]
    assert value == suffixes, f"Для префикса {key}, ожидалось {value} но получено {suffixes}"

@pytest.mark.parametrize("key, value", [
    (('a', 'b'), {'c': 0.66, 'd': 0.33}),
    (('b', 'c'), {'a': 0.5, None: 0.5}),
    (('c', 'a'), {'b': 1.0}),
    (('b', 'd'), {'a': 1.0}),
    (('d', 'a'), {'b': 1.0}),
])
def test_matrix_data(key, value):
    matrix = TransitionMatrix(['a', 'b', 'c', 'a', 'b', 'd', 'a', 'b', 'c'], 2)
    prefixes = matrix.make_matrix()
    assert key in prefixes.keys(), f"Префикс {key} отсутствует"
    suffixes = prefixes[key]
    for suffix, probability in suffixes.items():
        assert suffix in value.keys(), f"Суффикс {suffix} не найден {suffixes.keys()}"
        assert math.isclose(probability, value[suffix], rel_tol=1e-2), f"Ожидалось {value[suffix]} но получено {probability}"

@pytest.mark.parametrize("path", [
    ("./texts/text_eng.txt"),
    ("./texts/text_bigeng.txt")
])
def test_matrix_probabilities(path):
    data = File.get_data_from_file(path)
    matrix = TransitionMatrix(File.split_data(data), 2)
    prefixes = matrix.make_matrix()
    for prefix, suffixes in prefixes.items():
        total_probability = sum(suffixes.values())
        assert math.isclose(total_probability, 1.0, abs_tol=1e-9), \
            f"Сумма вероятностей для {prefix} меньше 1.0: {total_probability}"

def test_generated_text_length_more_zero():
    matrix = TransitionMatrix(['a', 'b', 'c', 'a', 'b', 'd', 'a', 'b', 'c'], 2)
    generated_text = matrix.generate_text_by_matrix()
    assert len(generated_text) > 0

def test_empty_corpus():
    with pytest.raises(SystemExit):
        TransitionMatrix([], 2)

def test_str_prefix_length():
    with pytest.raises(SystemExit):
        TransitionMatrix(['a'], 'a')

def test_length_prefix_more_than_corpus_length():
    with pytest.raises(SystemExit):
        TransitionMatrix(['a', 'b'], 5)