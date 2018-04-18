import argparse

from animarkov import fetch, generate


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['generate', 'fetch'])
    parser.add_argument('--start_page', type=int)
    parser.add_argument('--end_page', type=int)
    args = parser.parse_args()
    if args.command == 'generate':
        generate.main(args.start_page, args.end_page)
    elif args.command == 'fetch':
        fetch.main(args.start_page, args.end_page)
