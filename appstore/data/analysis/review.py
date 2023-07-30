#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Enter Project Name in Workspace Settings                                            #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.11                                                                             #
# Filename   : /appstore/data/analysis/review.py                                                   #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : Enter URL in Workspace Settings                                                     #
# ------------------------------------------------------------------------------------------------ #
# Created    : Sunday May 21st 2023 03:53:33 am                                                    #
# Modified   : Saturday July 29th 2023 07:59:15 pm                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from dependency_injector.wiring import Provide, inject
import pandas as pd

from appstore.data.storage.base import Repo
from appstore.data.analysis.base import Dataset
from appstore.container import AppstoreContainer

# ------------------------------------------------------------------------------------------------ #
DTYPES = [
    "Nominal",
    "Nominal",
    "Nominal",
    "Categorical",
    "Categorical",
    "Nominal",
    "Continuous",
    "Nominal",
    "Text",
    "Discrete",
    "Discrete",
    "Interval",
]


# ------------------------------------------------------------------------------------------------ #
class ReviewDataset(Dataset):
    """An in-memory dataset containing review data

    Args:
        repo (Repo): The dataset repository
    """

    @inject
    def __init__(self, repo: Repo = Provide[AppstoreContainer.data.review_repo]) -> None:
        super().__init__(repo=repo)

    @property
    def structure(self) -> pd.DataFrame:
        """Describes dataset structure, in terms of shape, size, and data type."""
        return super().structure

    @property
    def dtypes(self) -> pd.DataFrame:
        """Summarizes the data types in the dataset."""

        d = {
            "Number of Nominal Data Types": sum(1 for i in DTYPES if i == "Nominal"),
            "Number of Categorical Data Types": sum(1 for i in DTYPES if i == "Categorical"),
            "Number of Discrete Data Types": sum(1 for i in DTYPES if i == "Discrete"),
            "Number of Interval Data Types": sum(1 for i in DTYPES if i == "Interval"),
            "Number of Text Data Types": sum(1 for i in DTYPES if i == "Text"),
        }
        dtypes = pd.DataFrame.from_dict(data=d, orient="index").reset_index()
        dtypes.columns = ["Data Type", "Number of Features"]
        return dtypes

    @property
    def quality(self) -> pd.DataFrame:
        """Provides statistical information at the variable level."""
        quality = self._df.dtypes.to_frame().reset_index()
        quality.columns = ["Column", "Format"]
        quality["Data Type"] = DTYPES
        quality["Valid"] = self._df.count().values
        quality["Null"] = self._df.isna().sum().values
        quality["Validity"] = quality["Valid"] / self._df.shape[0]
        quality["Cardinality"] = self._df.nunique().values
        quality["Percent Unique"] = self._df.nunique().values / self._df.shape[0]
        quality["Size"] = self._df.memory_usage(deep=True, index=False).to_frame().reset_index()[0]
        quality = round(quality, 2)
        return quality

    @property
    def summary(self) -> None:
        """Summarizes the data"""
        return self._repo.summary