#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Enter Project Name in Workspace Settings                                            #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.11                                                                             #
# Filename   : /appstore/data/storage/rating.py                                                    #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : Enter URL in Workspace Settings                                                     #
# ------------------------------------------------------------------------------------------------ #
# Created    : Saturday April 29th 2023 05:56:28 am                                                #
# Modified   : Saturday July 29th 2023 02:11:50 pm                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import logging

import pandas as pd
import numpy as np

from appstore.data.storage.base import Repo
from appstore.infrastructure.database.base import Database
from sqlalchemy.dialects.mysql import (
    BIGINT,
    TINYINT,
    VARCHAR,
    FLOAT,
)

# ------------------------------------------------------------------------------------------------ #
#                                    DATAFRAME DATA TYPES                                          #
# ------------------------------------------------------------------------------------------------ #
DATAFRAME_DTYPES = {
    "id": "string",
    "name": "string",
    "category_id": "category",
    "category": "category",
    "rating": np.float64,
    "reviews": np.int64,
    "ratings": np.int64,
    "onestar": np.int64,
    "twostar": np.int64,
    "threestar": np.int64,
    "fourstar": np.int64,
    "fivestar": np.int64,
    "status": bool,
}

# ------------------------------------------------------------------------------------------------ #
#                                      DATABASE DATA TYPES                                         #
# ------------------------------------------------------------------------------------------------ #
DATABASE_DTYPES = {
    "id": VARCHAR(24),
    "name": VARCHAR(128),
    "category_id": VARCHAR(8),
    "category": VARCHAR(64),
    "rating": FLOAT,
    "reviews": BIGINT,
    "ratings": BIGINT,
    "onestar": BIGINT,
    "twostar": BIGINT,
    "threestar": BIGINT,
    "fourstar": BIGINT,
    "fivestar": BIGINT,
    "status": TINYINT,
}


# ------------------------------------------------------------------------------------------------ #
class RatingRepo(Repo):
    """Repository for rating data

    Args:
        database(Database): Database containing data to access.
    """

    __name = "rating"

    def __init__(self, database: Database) -> None:
        super().__init__(name=self.__name, database=database)
        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    def add(self, data: pd.DataFrame) -> None:
        """Adds the dataframe rows to the designated table.

        Args:
            data (pd.DataFrame): DataFrame containing rows to add to the table.
        """
        self._database.insert(
            data=data, tablename=self._name, dtype=DATABASE_DTYPES, if_exists="append"
        )
        msg = f"Added {data.shape[0]} rows to the {self._name} repository."
        self._logger.debug(msg)

    def get(
        self, id: str, dtypes: dict = DATAFRAME_DTYPES, parse_dates: dict = None  # noqa
    ) -> pd.DataFrame:
        """Returns data for the entity designated by the 'id' parameter.

        Args:
            id (Union[str,int]): The entity id.
            dtypes (dict): Dictionary mapping of column to data types
            parse_dates (dict): Dictionary of columns and keyword arguments for datetime parsing.
        """
        return super().get(id=id, dtypes=dtypes, parse_dates=parse_dates)

    def getall(self) -> pd.DataFrame:
        """Returns all data in the repository."""

        return super().getall(dtypes=DATAFRAME_DTYPES)

    def replace(self, data: pd.DataFrame) -> None:
        """Replaces the data in a repository with that of the data parameter.

        Args:
            data (pd.DataFrame): DataFrame containing rows to add to the table.
        """
        self._database.insert(
            data=data, tablename=self._name, dtype=DATABASE_DTYPES, if_exists="replace"
        )
        msg = f"Replace {self._name} repository data with {data.shape[0]} rows."
        self._logger.debug(msg)

    @property
    def summary(self) -> pd.DataFrame:
        """Summarizes the app data by category"""
        df = self.getall()
        summary = df["category"].value_counts().reset_index()
        df2 = df.groupby(by="category")["id"].nunique().to_frame()
        df3 = df.groupby(by="category")["rating"].mean().to_frame()
        summary = summary.join(df2, on="category")
        summary = summary.join(df3, on="category")
        summary.columns = ["Category", "Reviews", "Apps", "Average Rating"]
        return summary