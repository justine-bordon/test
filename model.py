from __future__ import annotations
from abc import ABC, abstractmethod
from collections.abc import Sequence
from random import Random
from typing import Protocol

from moles import (
    MoleState, MoleInfo, Mole,
    MolePopupPlan, GameOverCondition,
    SimpleMole, BombMole, LuckyMole, RichMole
)


class SimpleMolePopupPlan:
    def choose_moles_to_popup(self, current_tick: int, moles: Sequence[MoleInfo], rng: Random) -> list[int]:
        if current_tick % 30 == 0:
            li = [idx for (idx, m) in enumerate(moles) if m.state == MoleState.INACTIVE and m.cooldown_ticks == 0]
            x = len(li)
            min_moles = 1
            if li:
                return rng.sample(li, rng.randint(min_moles, max(1, 2 * x // 3)))
            return li
        return []


class SimpleGameOverCondition:
    def is_game_over(self, moles: Sequence[MoleInfo], current_tick: int, points: int) -> bool:
        return points >= 20


class Model:
    def __init__(self,
                 moles: Sequence[Mole],
                 popup_plan: MolePopupPlan,
                 game_over_condition: GameOverCondition,
                 rng: Random):
        self._moles: list[Mole] = list(moles)
        self._popup_plan: MolePopupPlan = popup_plan
        self._game_over_condition: GameOverCondition = game_over_condition
        self._rng: Random = rng
        self._total_points: int = 0
        self._is_game_over: bool = False

        self._current_tick = 1


    @property
    def is_game_over(self) -> bool:
        return self._is_game_over

    @property
    def moles_info(self) -> Sequence[MoleInfo]:
        return self._moles

    @property
    def score(self) -> int:
        return self._total_points


    def update(self, click_idx: None | int) -> None:
        if not self._is_game_over:
            self._current_tick += 1

            mole_idxs = self._popup_plan.choose_moles_to_popup(self._current_tick, self._moles,  self._rng)
            for idx in mole_idxs:
                self._moles[idx].pop_up()

            if click_idx is not None:
                mole = self._moles[click_idx]
                if mole.is_active:
                    mole.receive_hit(1)
                    if mole.is_dead:
                        self._total_points += mole.points
                        mole.end_tick()

            for mole in self._moles:
                mole.affect_moles(self._moles)

            for mole in self._moles:
                mole.end_tick()

            self._is_game_over = self._game_over_condition.is_game_over(self._moles, self._current_tick, self.score)

    @classmethod
    def get_simple_model(cls):
        rng = Random()
        simple_popup = SimpleMolePopupPlan()
        simple_game_over = SimpleGameOverCondition()
        moles = [SimpleMole() for _ in range(5)] + [BombMole()] + [LuckyMole()] + [RichMole()]
        return cls(moles, simple_popup, simple_game_over, rng)
