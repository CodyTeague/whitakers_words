import argparse
import abc
from argparse import ArgumentParser
from whitakers_words.parse import Parser
import json


class Command:
    @abc.abstractproperty
    def name(self):
        pass

    @abc.abstractproperty
    def help(self):
        pass

    def add_parser(self, subparsers: argparse._SubParsersAction):
        command_parser = subparsers.add_parser(self.name, help=self.help)
        command_parser.set_defaults(func=self.execute_command)
        self.contribute_to_parser(command_parser)

    def contribute_to_parser(self, argument_parser: ArgumentParser):
        pass

    @abc.abstractmethod
    def execute_command(self, args: argparse.Namespace):
        pass


class ParseCommand(Command):
    name = "parse"
    help = "Parse the string as a Latin word and look it up in the Words dictionary"

    def contribute_to_parser(self, argument_parser: ArgumentParser):
        argument_parser.add_argument('word', help='latin word to look up')
        argument_parser.add_argument(
            '--json', '-j', action='store_true', default=False, help='output in json format')

    def execute_command(self, args: argparse.Namespace):
        result = Parser().parse(args.word)
        if args.json:
            print(json.dumps(result, indent=4))
        else:
            self.pretty_print(args.word, result)

    @staticmethod
    def pretty_print(word, result):
        print(word)
        print('TODO: Implement')


commands = [ParseCommand()]


def execute():
    arg_parser = argparse.ArgumentParser('open_words')
    subparsers = arg_parser.add_subparsers()

    for command in commands:
        command.add_parser(subparsers)

    args = arg_parser.parse_args()

    if 'func' in args:
        args.func(args)
    else:
        arg_parser.print_help()
