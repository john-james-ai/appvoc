#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Appstore Ratings & Reviews Analysis                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.12                                                                             #
# Filename   : /appstore/data/dataset/appdata.py                                                   #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/appstore                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Sunday May 21st 2023 03:53:33 am                                                    #
# Modified   : Sunday August 20th 2023 01:07:50 am                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import pandas as pd
from d8analysis.data.dataset import Dataset

from appstore.data.entity.appdata import AppData


# ------------------------------------------------------------------------------------------------ #
class AppDataDataset(Dataset):
    """An in-memory dataset containing app data

    Args:
        repo (Repo): The dataset repository
    """

    def __init__(self, df: pd.DataFrame) -> None:
        super().__init__(df=df)

    def __getitem__(self, idx: int) -> AppData:
        df = self._df.iloc[[idx]]
        return AppData.from_df(df=df)

    def summary(self) -> None:
        """Summarizes the data"""

        summary = self._df["category"].value_counts().reset_index()
        summary.columns = ["category", "Examples"]
        df2 = self._df.groupby(by="category")["id"].nunique().to_frame()
        df3 = self._df.groupby(by="category")["rating"].mean().to_frame()
        df4 = self._df.groupby(by="category")["ratings"].sum().to_frame()

        summary = summary.join(df2, on="category")
        summary = summary.join(df3, on="category")
        summary = summary.join(df4, on="category")
        summary.columns = ["Category", "Examples", "Apps", "Average Rating", "Rating Count"]
        return summary
