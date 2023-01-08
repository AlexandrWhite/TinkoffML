import argparse
import ast
import codecs

parser = argparse.ArgumentParser()
parser.add_argument("input_file")
parser.add_argument("scores_file")
args = parser.parse_args()


def get_func_names(astparse):
    function_definitions = [node for node in ast.walk(astparse) if isinstance(node, ast.FunctionDef)]
    return [f.name for f in function_definitions]


def get_class_names(astparse):
    class_definitions = [node for node in ast.walk(astparse) if isinstance(node, ast.ClassDef)]
    return [f.name for f in class_definitions]


def get_docstrings(astparse):
    function_definitions = [node for node in ast.walk(astparse) if isinstance(node, ast.FunctionDef)]
    return [ast.get_docstring(f) for f in function_definitions]


def levinstein(a, b, replace_price=1, insert_price=1, remove_price=1):
    dp = [[(i + j) * insert_price if i * j == 0 else 0 for j in range(len(b) + 1)] for i in range(len(a) + 1)]

    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = min(
                    dp[i - 1][j] + remove_price,
                    dp[i][j - 1] + insert_price,
                    dp[i - 1][j - 1] + replace_price)
    return dp[len(a)][len(b)]


def compare_list(list1, list2):
    print(list1)
    print(list2)
    if (not list1) and (not list2):
        return 0
    elif not list1:
        return sum([len(i) for i in list2])
    elif not list2:
        return sum([len(i) for i in list1])
    else:
        max_d = max(
            max([len(i) for i in list1]),
            max([len(i) for i in list2]))  # самое большое расстояние между строками из двух массивов
        distance = 0
        for i in list1:
            d = max_d
            for j in list2:
                d = min(d, levinstein(i, j))
            distance += d
        return distance


def compare_files(path1, path2):
    with codecs.open(path1, 'r', 'utf-8') as f1, codecs.open(path2, 'r', 'utf-8') as f2:
        p1 = ast.parse(f1.read())
        p2 = ast.parse(f2.read())

        scores = 0

        scores += compare_list(get_func_names(p1), get_func_names(p2))
        scores += compare_list(get_class_names(p1), get_class_names(p2))
        scores += compare_list(get_docstrings(p1), get_docstrings(p2))

        return scores



with open(args.input_file, 'r') as files, open(args.scores_file, 'w') as scores:
    for line in files:
        file1, file2 = line.split()
        scores.writelines(str(compare_files(file1, file2)) + '\n')
