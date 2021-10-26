from ..challenges import Challenge
from .exceptions import *
from typing import Union
from collections import Mapping
import random
import redis

class Solver:
    def __init__(
        self,
        database: Union[redis.Redis, Mapping],
        min_answers: int = 3
        ):
        self._database = database
        self._min_answers = min_answers

    def _get_tile_score(self, tile):
        if isinstance(self._database, redis.Redis):
            return int(self._database.get(tile.custom_id) or 0)

        elif isinstance(self._database, Mapping):
            return self._database.get(tile.custom_id, 0)

    def _incr_tile_score(self, tile, incr_by):
        if isinstance(self._database, redis.Redis):
            self._database.incrby(tile.custom_id, incr_by)

        elif isinstance(self._database, Mapping):
            value = self._database.get(tile.custom_id, 0)
            self._database[tile.custom_id] += value + incr_by
    
    def solve(self, challenge: Challenge):
        prefix_text = "Please click each image containing a "

        if challenge.token:
            return challenge.token

        if challenge.mode != "image_label_binary":
            raise UnsupportedChallenge(
                f"Unsupported challenge mode: {challenge.mode}")

        if not challenge.question["en"].startswith(prefix_text):
            raise UnsupportedChallenge(
                f"Unsupported challenge question: {challenge.question['en']}")
        
        variation = challenge.question["en"] \
            .replace(prefix_text, "") \
            .rstrip(".") \
            .lower()
        
        for tile in challenge.tiles:
            image = tile.get_image(raw=True)
            image_hash = hash(image)
            tile.custom_id = f"{variation}|{image_hash}"
            tile.score = self._get_tile_score(tile)
            tile.selected = False

        challenge.tiles.sort(
            key=lambda tile: tile.score or random.uniform(0, 0.9),
            reverse=True)
        
        for index in range(max(
                self._min_answers,
                len([1 for tile in challenge.tiles if tile.score])
            )):
            tile = challenge.tiles[index]
            tile.selected = False
            challenge.answer(tile)

        challenge.submit()

        for tile in challenge.tiles:
            if not tile.selected: continue
            self._incr_tile_score(tile, 1)
        
        return challenge.token