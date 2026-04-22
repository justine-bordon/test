from __future__ import annotations
from abc import ABC, abstractmethod
from collections.abc import Sequence
from enum import Enum, auto
from typing import Protocol


class MoleState(Enum):
    INACTIVE = auto()
    ACTIVE = auto()
    HIT = auto()


class MoleInfo(ABC):
    @property
    @abstractmethod
    def base_hit_points(self) -> int: ...

    @property
    @abstractmethod
    def base_active_ticks(self) -> int: ...

    @property
    @abstractmethod
    def base_cooldown_ticks(self) -> int: ...

    @property
    @abstractmethod
    def hit_points(self) -> int: ...

    @property
    @abstractmethod
    def cooldown_ticks(self) -> int: ...

    @property
    @abstractmethod
    def points(self) -> int: ...

    @property
    @abstractmethod
    def is_active(self) -> bool: ...

    @property
    @abstractmethod
    def is_dead(self) -> bool: ...

    @property
    @abstractmethod
    def state(self) -> MoleState:
        ...


class Mole(MoleInfo):
    @abstractmethod
    def pop_up(self) -> None:
        ...
    
    @abstractmethod
    def hide(self) -> None:
        ...

    @abstractmethod
    def receive_hit(self, damage: int) -> None:
        ...

    @abstractmethod
    def start_tick(self) -> None:
        ...

    @abstractmethod
    def end_tick(self) -> None:
        ...

    @abstractmethod
    def affect_moles(self, moles: Sequence[Mole]) -> None:
        ...


class SimpleMole(Mole):
    def __init__(self):
        self._hit_points = self.base_hit_points
        self._active_ticks = self.base_active_ticks
        self._cooldown_ticks = 0
        self._state = MoleState.INACTIVE
        super().__init__()

    @property
    def is_active(self) -> bool:
        return self.state == MoleState.ACTIVE

    @property
    def is_dead(self) -> bool:
        return self.state == MoleState.HIT and self.hit_points <= 0 

    @property
    def base_hit_points(self) -> int:
        return 1

    @property
    def base_active_ticks(self) -> int:
        return 40

    @property
    def base_cooldown_ticks(self) -> int:
        return 30

    @property
    def cooldown_ticks(self) -> int:
        return self._cooldown_ticks

    @property
    def hit_points(self) -> int:
        return self._hit_points

    @property
    def points(self) -> int:
        return 1

    @property
    def state(self) -> MoleState:
        return self._state

    def pop_up(self) -> None:
        if self._state == MoleState.INACTIVE and self._cooldown_ticks <= 0:
            self._state = MoleState.ACTIVE
            self._active_ticks = self.base_active_ticks
    
    def hide(self) -> None:
        self._state = MoleState.INACTIVE
        self._cooldown_ticks = self.base_cooldown_ticks

    def receive_hit(self, damage: int) -> None:
        if self.state == MoleState.ACTIVE:
            self._hit_points -= damage
            self._state = MoleState.HIT

    def start_tick(self) -> None:
        pass

    def end_tick(self) -> None:
        match self.state:
            case MoleState.INACTIVE:
                self._cooldown_ticks = max(0, self._cooldown_ticks - 1)
            case MoleState.ACTIVE:
                self._active_ticks -= 1
                if self._active_ticks == 0:
                    self.hide()
            case MoleState.HIT:
                if self.hit_points <= 0:
                    self.hide()
                else:
                    self._state = MoleState.ACTIVE

    def affect_moles(self, moles: Sequence[Mole]) -> None:
        pass


class MolePopupPlan(Protocol):
    def choose_moles_to_popup(self, current_tick: int, moles: Sequence[MoleInfo], rng: Random) -> list[int]:
        ...


class GameOverCondition(Protocol):
    def is_game_over(self, moles: Sequence[MoleInfo], current_tick: int, points: int) -> bool:
        ...
