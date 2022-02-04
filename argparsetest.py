import argparse

card_search_parser = argparse.ArgumentParser(description='Argument parser for basic card search')
card_search_parser.add_argument('-lb', '--lower-bound', type=int, default=1, help='A lower level bound for card searching' )
card_search_parser.add_argument('-l', '--level', type=int, default=None, help='A level bound for card searching' )
card_search_parser.add_argument('-ub', '--upper-bound', type=int, default=10, help='An upper level bound for card searching' )
card_search_parser.add_argument('-c', '--colour', type=str, default=None, help='A colour to search' )
# card_search_parser.add_argument('-s', '--search', metavar='SEARCH_TERM', type=str, default=None, help='A lower level bound for card searching' )
card_search_parser.add_argument('-s', '--search', metavar='SEARCH_TERM', type=str, default=None, nargs='+', help='A lower level bound for card searching' )


args = card_search_parser.parse_args(['-s', 'name', 'nah'])
print(args)