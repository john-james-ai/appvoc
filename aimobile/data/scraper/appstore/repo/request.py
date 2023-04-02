#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/data/scraper/appstore/repo/request.py                                     #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Friday March 31st 2023 06:11:19 am                                                  #
# Modified   : Saturday April 1st 2023 12:14:06 am                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import logging

import pandas as pd

from aimobile.data.scraper.appstore.repo.base import Repo
from aimobile.data.database.database import SQLiteDatabase


# ------------------------------------------------------------------------------------------------ #
class RequestRepo(Repo):
    """Repository of HTTP requests from the scraping projects.

    Args:
        database (SQLiteDatabase): Appstore Database
    """

    def __init__(self, database: SQLiteDatabase) -> None:
        self._database = database
        self._logger = logging.getLogger(f"{self.__module__}.{self.__class__.__name__}")

    def get(self, category_name: str) -> pd.DataFrame:
        """Retrieves AppData by category

        Args:
            category_name (str): A category_name from AppStoreCategories
        """
        query = "SELECT * FROM request WHERE category_name = ?;"
        params = (category_name,)
        return self._database.read(query=query, params=params)

    def add(self, data: pd.DataFrame) -> None:
        """Adds a DataFrame to the Database

        Args:
            data (pd.DataFrame): The data
        """
        self._database.create(data=data, tablename="request")

    def update(self, data: pd.DataFrame) -> None:
        """Updates the table with the existing data.

        Args:
            data (pd.DataFrame): The data to replace existing data

        """
        raise NotImplementedError("Request data are immutable. Update is not implemented.")

    def remove(self, category_name: str = None, project_id: str = None) -> None:
        """Removes rows from the database

        Args:
            category_name (str): Category from AppStoreCategories. Optional.
            project_id (str): Identifier for a scrape project. Optional.
        """
        if category_name is not None and project_id is not None:
            query = "DELETE FROM request WHERE category_name = ? AND project_id = ?;"
            params = (
                category_name,
                project_id,
            )
        elif category_name is not None:
            query = "DELETE FROM request WHERE category_name = ?;"
            params = (category_name,)
        elif project_id is not None:
            query = "DELETE FROM request WHERE project_id = ?;"
            params = (project_id,)
        else:
            msg = "Remove method missing parameters."
            self._logger.error(msg)
            raise ValueError(msg)

        self._database.delete(query=query, params=params)
