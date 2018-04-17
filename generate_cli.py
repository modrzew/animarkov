import argparse

import generate

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--start_page', type=int)
    parser.add_argument('--end_page', type=int)
    args = parser.parse_args()
    generate.main(args.start_page, args.end_page)
