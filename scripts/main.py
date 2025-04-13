import argparse
import pathlib

from actions import Actions

default_path = pathlib.Path(__file__).parents[1].resolve()
actions = Actions()

def main():
    parser = argparse.ArgumentParser(description="iBook Notes Exporter")
    parser.add_argument('-o', '--output', type=str, default=default_path, help='The path to save the markdown file.')
    parser.add_argument('-l', '--list', action='store_true', help='List all books available for export.')
    parser.add_argument('-s', '--search', type=str, help='Search for a specific book by title.')

    # 全部导出和单个导出不能同时操作
    group = parser.add_mutually_exclusive_group() # 不必须使用，参数不需要加上required=True
    group.add_argument('-t', '--title', type=str, help='The title of the book to export notes from.')
    group.add_argument('-a', '--all', action='store_true', help='Export all notes from all books.')

    args = parser.parse_args()

    if args.search:
        res = actions.search(args.search)
        print(res)

    if args.list:
        actions.getBooksLists()

    if args.title:
        actions.export(args.title, args.output)

    if args.all:
        actions.export('' ,args.output)



if __name__ == "__main__":
    main()