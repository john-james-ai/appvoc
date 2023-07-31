#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Appstore Ratings & Reviews Analysis                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.11                                                                             #
# Filename   : /appstore/data/acquisition/appdata/result.py                                        #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/appstore                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Wednesday May 3rd 2023 01:59:31 pm                                                  #
# Modified   : Sunday July 30th 2023 06:48:25 pm                                                   #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Defines the Result Object for AppData Requests"""
from dataclasses import dataclass
import pandas as pd

from appstore.data.acquisition.base import Result


# ------------------------------------------------------------------------------------------------ #
@dataclass
class AppDataResult(Result):
    page: int = 0  # The result page
    pages: int = 0  # The number of pages cumulatively processed up to this result
    size: int = 0  # Size of result in bytes
    results: int = 0  # The number of records returned
    content: pd.DataFrame = None  # The content of the response.
