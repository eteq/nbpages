# Standard library
from os import path

# Third-party
from astropy import log as logger
logger.setLevel('INFO')

from nbconvert.preprocessors import ExecutePreprocessor, CellExecutionError
from nbconvert.exporters import RSTExporter
from nbconvert.writers import FilesWriter
import nbformat

IPYTHON_VERSION = 4

class NBConverter(object):

    def __init__(self, nb_path):
        self.nb_path = path.abspath(nb_path)
        fn = path.basename(self.nb_path)
        self.path_only = path.dirname(self.nb_path)
        self.nb_name, _ = path.splitext(fn)

        # the executed notebook
        self._executed_nb_path = path.join(self.path_only,
                                           'exec_{0}'.format(fn))

        logger.info('Processing notebook {0} (in {1})'.format(fn,
                                                              self.path_only))

    def execute(self, write=True):
        """
        Execute the specified notebook file, and optionally write out the
        executed notebook to a new file.

        Parameters
        ----------
        write : bool, optional
            Write the executed notebook to a new file, or not.

        Returns
        -------
        executed_nb_path : str, ``None``
            The path to the executed notebook path, or ``None`` if
            ``write=False``.

        """

        # Execute the notebook
        logger.debug('Executing notebook...')
        executor = ExecutePreprocessor(timeout=900, kernel_name='python3')
        with open(self.nb_path) as f:
            nb = nbformat.read(f, as_version=IPYTHON_VERSION)

        try:
            executor.preprocess(nb, {'metadata': {'path': self.path_only}})
        except CellExecutionError:
            # TODO: should we fail fast and raies, or record all errors?
            raise

        if write:
            logger.debug('Writing executed notebook to file {0}...'
                         .format(self._executed_nb_path))
            with open(self._executed_nb_path, 'w') as f:
                nbformat.write(nb, f)

            return self._executed_nb_path

    def convert(self):
        """
        Convert the executed notebook to a restructured text (RST) file.
        """

        if not path.exists(self._executed_nb_path):
            raise IOError("Executed notebook file doesn't exist! Expected: {0}"
                          .format(self._executed_nb_path))

        # Initialize the resources dict - see:
        # https://github.com/jupyter/nbconvert/blob/master/nbconvert/nbconvertapp.py#L327
        resources = {}
        resources['config_dir'] = '' # we don't need to specify config
        resources['unique_key'] = self.nb_name

        # path to store extra files, like plots generated
        resources['output_files_dir'] = path.join(self.path_only, 'nboutput')

        # Exports the notebook to RST
        logger.debug('Exporting notebook to RST...')
        exporter = RSTExporter()
        output, resources = exporter.from_filename(self._executed_nb_path,
                                                   resources=resources)

        # Write the output RST file
        writer = FilesWriter()
        output_file_path = writer.write(output, resources,
                                        notebook_name=self.nb_name)

        return output_file_path

if __name__ == "__main__":
    from argparse import ArgumentParser
    import logging

    # Define parser object
    parser = ArgumentParser(description="")

    vq_group = parser.add_mutually_exclusive_group()
    vq_group.add_argument('-v', '--verbose', action='count', default=0,
                          dest='verbosity')
    vq_group.add_argument('-q', '--quiet', action='count', default=0,
                          dest='quietness')

    parser.add_argument('-o', '--overwrite', action='store_true',
                        dest='overwrite', default=False,
                        help='Re-run and overwrite any existing executed '
                             'notebook or RST files.')

    parser.add_argument('nbfile_or_path', default=None,
                        help='Path to a specific notebook file, or the '
                             'top-level path to a directory containing '
                             'notebook files to process.')

    args = parser.parse_args()

    # Set logger level based on verbose flags
    if args.verbosity != 0:
        if args.verbosity == 1:
            logger.setLevel(logging.DEBUG)
        else: # anything >= 2
            logger.setLevel(1)

    elif args.quietness != 0:
        if args.quietness == 1:
            logger.setLevel(logging.WARNING)
        else: # anything >= 2
            logger.setLevel(logging.ERROR)

    if path.isdir(args.nbfile_or_path):
        # It's a path, so we need to walk through recursively and find any
        # notebook files

        # TODO:

        # nbc = NBConverter(args.nbfile_or_path)
        # nbc.execute()
        # nbc.convert()

        pass

    else:
        # It's a single file, so convert it
        nbc = NBConverter(args.nbfile_or_path)
        nbc.execute()
        nbc.convert()
