from logic.z5 import flatten_list


def test_flatten_list1():
    assert flatten_list([1, 2, 3]) == [1, 2, 3]


def test_flatten_list2():
    assert flatten_list([1, [2, 3], [4, [5]]]) == [1, 2, 3, 4, 5]


def test_flatten_list3():
    assert flatten_list([]) == []


def test_flatten_list4():
    assert flatten_list([[[1]]]) == [1]


def test_flatten_list5():
    assert flatten_list([1, [2, [3, [4]]]]) == [1, 2, 3, 4]
