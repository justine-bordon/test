from collections.abc import Sequence
from typing import Protocol

import pyxel

from model import MoleInfo


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
	def start_game(self, update_handler: UpdateHandler, draw_handler: DrawHandler) -> None:
		pyxel.run(update_handler.update, draw_handler.draw)
	def get_clicked_mole(self) -> int | None:
		if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
			for i in range(self._active_mole_count):
				col = i % 3
				row = i // 3
				cx = 40 + (col * 60)
				cy = 40 + (row*60)
				
				if (pyxel.mouse_x - cx)**2 + (pyxel.mouse_y - cy)**2 <= 400:
					return i
		return None
				
	def draw_moles(self, moles_info: Sequence[MoleInfo]) -> None:
		self._active_mole_count = len(moles_info)
		
		for i, mole in enumerate(moles_info):
			col = i % 3
			row = i // 3
			x = 40 + (col*60)
			y = 40 + (row*60)
			
			if mole.state == MoleState.ACTIVE:
				pyxel.circ(x,y,20,9)
			elif mole.state == MoleState.HIT:
				pyxel.circ(x,y,20,8)
			else:
				pyxel.circ(x,y,20,5)
		
		
		
	def draw_score(self, score: int) -> None:
		pyxel.text(5,5, f"SCORE: {score}", 7)
	def reset_screen(self) -> None:
		pyxel.cls(0)
