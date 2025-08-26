"""Module interface.py"""
import logging

import config
import src.elements.s3_parameters as s3p
import src.s3.directives
import src.s3.unload


class Interface:
    """
    Notes<br>
    ------<br>

    An interface to the data/artefacts retrieval class.  <b>Beware, sometimes dask
    will be unnecessary, edit accordingly.</b>
    """

    def __init__(self, s3_parameters: s3p.S3Parameters):
        """

        :param s3_parameters: The overarching S3 (Simple Storage Service) parameters
                              settings of this project, e.g., region code name, buckets, etc.
        """

        self.__s3_parameters: s3p.S3Parameters = s3_parameters
        self.__source_bucket = self.__s3_parameters.external

        # Directives
        self.__directives = src.s3.directives.Directives()

    def __get_assets(self, source_bucket: str, origin: str, target: str):
        """

        :param source_bucket:
        :param origin:
        :param target:
        :return:
        """

        return self.__directives.synchronise(
            source_bucket=source_bucket, origin=origin, target=target)

    def exc(self):
        """

        :return:
        """

        try:
            state = self.__get_assets(
                source_bucket=self.__source_bucket,
                origin='warehouse/numerics/best',
                target=config.Config().data_)
        except RuntimeError as err:
            raise err from err

        logging.info(state)
