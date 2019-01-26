import argparse


class parser:
    """
    Parsing command line arguments with the argparse
    """

    def __init__(self):
        """
        Setting and Parsing arguments
        """
        self.parser = argparse.ArgumentParser(description='Document Converter')
        # sets the input file name argument
        self.parser.add_argument('input',
                                 type=str,
                                 help='Input CSV File Name')
        # sets the output file name argument
        self.parser.add_argument('output',
                                 type=str,
                                 help='Output File Name')
        # sets the output file format
        self.parser.add_argument('format',
                                 type=str,
                                 help='Output File Format')
        self.parser.add_argument('-v', '--verbose',
                                 help="increase output verbosity",
                                 action="store_true")
        self.args = self.parser.parse_args()

    def propagate_args(self) -> argparse:
        """
         Returns the custom logger for use in others classes
        :param self: Set and Parsed instance of argparse
        :return argparse: The arguments will be propagated to the caller
        """
        return self.args
