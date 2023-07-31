#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Appstore Ratings & Reviews Analysis                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.11                                                                             #
# Filename   : /appstore/data/acquisition/rating/result.py                                         #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/appstore                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Wednesday May 3rd 2023 01:59:31 pm                                                  #
# Modified   : Sunday July 30th 2023 06:50:39 pm                                                   #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Defines the Result Object for Rating Responses"""
from __future__ import annotations
from dataclasses import dataclass, field
import logging

import pandas as pd
from appstore.data.acquisition.base import Result, Response


# ------------------------------------------------------------------------------------------------ #
@dataclass
class RatingResponse(Response):
    """Encapsulates a response from the RatingScraper.

    Inherits the following member from the Response base class:
        status: bool = True
    """

    id: str = None  # noqa
    name: str = None
    category_id: str = None
    category: str = None
    rating: float = 0
    reviews: int = 0
    ratings: int = 0
    onestar: int = 0
    twostar: int = 0
    threestar: int = 0
    fourstar: int = 0
    fivestar: int = 0

    @classmethod
    def create(cls, batch: dict, response: dict) -> RatingResponse:
        """Factory method creating a ReviewResponse object

        Args:
            response (dict): A dictionary containing ratings for a single app.
        """
        cls._logger = logging.getLogger(f"{cls.__class__.__name__}")

        # id has been validated by the calling scope.
        id = str(response["adamId"])  # noqa
        try:
            rating_response = cls(
                id=id,
                name=[app["name"] for app in batch if app["id"] == id][0],
                category_id=[str(app["category_id"]) for app in batch if app["id"] == id][0],
                category=[app["category"] for app in batch if app["id"] == id][0],
                rating=response["ratingAverage"],
                reviews=response["totalNumberOfReviews"],
                ratings=response["ratingCount"],
                onestar=response["ratingCountList"][0],
                twostar=response["ratingCountList"][1],
                threestar=response["ratingCountList"][2],
                fourstar=response["ratingCountList"][3],
                fivestar=response["ratingCountList"][4],
                status=True,
            )
            return rating_response  # noqa

        except Exception as e:
            msg = f"\nInvalid response. Encountered {type(e)} exception.\n{e}\n{response}"
            cls._logger.debug(msg)

            # Create  default rating response for the app.
            rating_response = cls(
                id=id,
                name=[app["name"] for app in batch if app["id"] == id][0],
                category_id=[str(app["category_id"]) for app in batch if app["id"] == id][0],
                category=[app["category"] for app in batch if app["id"] == id][0],
                status=False,
            )
            return rating_response  # noqa


# ------------------------------------------------------------------------------------------------ #
@dataclass
class RatingResult(Result):
    response: list[dict] = field(default_factory=list)
    apps: int = 0
    requests: int = 0
    successes: int = 0
    fails: int = 0

    def update_result(self, response: RatingResponse) -> None:
        """Adds a response to the result object

        Args:
           response (RatingResponse): A RatingResponse object
        """
        self.response.append(response.as_dict())
        self.requests += 1
        if response.status:
            self.apps += 1
            self.successes += 1
        else:
            self.fails += 1

    def as_df(self) -> pd.DataFrame:
        """Returns the RatingResult(s) as a dataframe"""
        return pd.DataFrame(self.response)

    def is_valid(self) -> bool:
        """Assesses and returns Result validity"""
        return self.successes > 0
