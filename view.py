from collections.abc import Sequence
from typing import Protocol

import pyxel

from model import MoleInfo, MoleState
from moles import *


class UpdateHandler(Protocol):
    def update(self):
        ...


class DrawHandler(Protocol):
    def draw(self):
        ...


# Controller <: UpdateHandler
# Controller <: DrawHandler


class View:
	def __init__(self, width, height):
		self.width = width
		self.height = height
		pyxel.init(self.width, self.height, title="Whac-A-Mole (Pyxel Version)")
		pyxel.mouse(True)
		self._active_mole_count = 0
		self._LOCS = {
		6:[(100,100), (100,50), (50,100), (75,150), (125,150), (150,100)],
		7:[(100,100), (100,50), (50,75), (50,125), (100,150), (150,125), (150,75)],
		8:[(100,100), (100,50), (60,75), (50, 116), (80,150), (120,150), (150,116), (140, 75)]
		}
	def start_game(self, update_handler: UpdateHandler, draw_handler: DrawHandler) -> None:
		pyxel.run(update_handler.update, draw_handler.draw)
	def get_clicked_mole(self) -> int | None:
		if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
			total = self._active_mole_count
			locs = self._LOCS.get(total)
			
			if locs:
				for i in range(total):
					cx, cy = locs[i]
					if (pyxel.mouse_x - cx)**2 + (pyxel.mouse_y - cy)**2 <= 100:
						return i
		return None
				
	def draw_moles(self, moles_info: Sequence[MoleInfo]) -> None:
		self._active_mole_count = len(moles_info)
		total = self._active_mole_count
		locs = self._LOCS.get(total)
		
		for i, mole in enumerate(moles_info):
			x, y = locs[i]
			
			pyxel.circ(x,y,15,0)
			
			if (mole.state == MoleState.ACTIVE) and (isinstance(mole, BombMole)):
				pyxel.circ(x,y,10,4)
			elif (mole.state == MoleState.ACTIVE) and isinstance(mole, LuckyMole):
				pyxel.circ(x,y,10,11)
			elif (mole.state == MoleState.ACTIVE) and isinstance(mole, RichMole):
				pyxel.circ(x,y,10,10)
			elif (mole.state == MoleState.ACTIVE) and isinstance(mole, ScaredyMole):
				pyxel.circ(x,y,10,2)
			elif (mole.state == MoleState.ACTIVE) and isinstance(mole, SimpleMole):
				pyxel.circ(x,y,10,9)
			elif mole.state == MoleState.HIT:
				pyxel.circ(x,y,10,8)
			else:
				pyxel.circ (x,y,10,0)
		
		
		
	def draw_score(self, score: int) -> None:
		pyxel.text(5,5, f"SCORE: {score}", 7)
	def reset_screen(self) -> None:
		pyxel.cls(15)
