import argparse
import ast
import codecs

parser = argparse.ArgumentParser()
parser.add_argument("input_file")
parser.add_argument("scores_file")
args = parser.parse_args()


def get_names(astparse):
    """
    :param astparse: AST node
    :return: cписок названий всех функций классов и переменных
    """
    return sorted({node.id for node in ast.walk(astparse) if isinstance(node, ast.Name)})


def levinstein(a, b):
    dp = [[(i + j) if i * j == 0 else 0 for j in range(len(b) + 1)] for i in range(len(a) + 1)]

    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]) + 1
    return dp[len(a)][len(b)]


def compare_files(path1, path2):
    with codecs.open(path1, 'r', 'utf-8') as f1, codecs.open(path2, 'r', 'utf-8') as f2:
        txt1 = f1.read()
        txt2 = f2.read()
        names1 = get_names(ast.parse(txt1))
        names2 = get_names(ast.parse(txt2))
        return levinstein(str(names1), str(names2))


with open(args.input_file, 'r') as files, open(args.scores_file, 'w') as scores:
    for line in files:
        file1, file2 = line.split()
        scores.writelines(str(compare_files(file1, file2)) + '\n')

