from model import Model
from view import View


class Controller:
    def __init__(self, model: Model, view: View):
        self._model = model
        self._view = view

    def start_game(self):
        self._view.start_game(self, self)

    def update(self):
        if not self._model.is_game_over:
            click_idx = self._view.get_clicked_mole()
            self._model.update(click_idx)

    def draw(self):
        # moles
        # score
        self._view.reset_screen()
        self._view.draw_moles(self._model.moles_info)
        self._view.draw_score(self._model.score)
