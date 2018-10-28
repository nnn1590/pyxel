import pyxel
from pyxel.ui import ScrollBar, Widget


class ImagePanel(Widget):
    def __init__(self, parent, *, is_tilemap_mode):
        y, height = (80, 66) if is_tilemap_mode else (16, 130)
        super().__init__(parent, 157, y, 66, height)

        self._is_tilemap_mode = is_tilemap_mode
        self.viewport_x = 0
        self.viewport_y = 0
        self.select_x = 0
        self.select_y = 0
        self._select_width = 8 if is_tilemap_mode else 16
        self._select_height = 8 if is_tilemap_mode else 16
        self._drag_offset_x = 0
        self._drag_offset_y = 0
        self._h_scroll_bar = ScrollBar(
            self, 157, 145, 66, ScrollBar.HORIZONTAL, 32, 8, 0
        )
        self._v_scroll_bar = (
            ScrollBar(self, 222, 80, 66, ScrollBar.VERTICAL, 32, 8, 0)
            if is_tilemap_mode
            else ScrollBar(self, 222, 16, 130, ScrollBar.VERTICAL, 32, 16, 0)
        )

        self.add_event_handler("mouse_down", self.__on_mouse_down)
        self.add_event_handler("mouse_drag", self.__on_mouse_drag)
        self.add_event_handler("mouse_hover", self.__on_mouse_hover)
        self.add_event_handler("update", self.__on_update)
        self.add_event_handler("draw", self.__on_draw)
        self._h_scroll_bar.add_event_handler("change", self.__on_h_scroll_bar_change)
        self._v_scroll_bar.add_event_handler("change", self.__on_v_scroll_bar_change)

    def _screen_to_view(self, x, y):
        x += self.viewport_x - self.x - 1
        y += self.viewport_y - self.y - 1

        x = (x - (self._select_width - 8) // 2) // 8 * 8
        y = (y - (self._select_height - 8) // 2) // 8 * 8

        x = min(max(x, 0), 256 - self._select_width)
        y = min(max(y, 0), 256 - self._select_height)

        return x, y

    def __on_mouse_down(self, key, x, y):
        if key == pyxel.KEY_LEFT_BUTTON:
            self.select_x, self.select_y = self._screen_to_view(x, y)

            if not self._is_tilemap_mode:
                self.parent.drawing_x = self.select_x
                self.parent.drawing_y = self.select_y

        if key == pyxel.KEY_RIGHT_BUTTON:
            self._drag_offset_x = 0
            self._drag_offset_y = 0

    def __on_mouse_drag(self, key, x, y, dx, dy):
        if key == pyxel.KEY_LEFT_BUTTON:
            self.__on_mouse_down(key, x, y)
        elif key == pyxel.KEY_RIGHT_BUTTON:
            self._drag_offset_x -= dx
            self._drag_offset_y -= dy

            if abs(self._drag_offset_x) >= 8:
                offset = (self._drag_offset_x // 8) * 8
                self._drag_offset_x -= offset
                self.viewport_x += offset

            if abs(self._drag_offset_y) >= 8:
                offset = (self._drag_offset_y // 8) * 8
                self._drag_offset_y -= offset
                self.viewport_y += offset

            self.viewport_x = min(max(self.viewport_x, 0), 192)
            self.viewport_y = min(
                max(self.viewport_y, 0), 192 if self._is_tilemap_mode else 128
            )

    def __on_mouse_hover(self, x, y):
        x, y = self._screen_to_view(x, y)
        s = "VIEW:R-DRAG" if self._is_tilemap_mode else "TARGET:CURSOR VIEW:R-DRAG"
        self.parent.help_message = s + " ({},{})".format(x, y)

    def __on_update(self):
        if not self._is_tilemap_mode:
            self.select_x = self.parent.drawing_x
            self.select_y = self.parent.drawing_y

        self._h_scroll_bar.value = self.viewport_x // 8
        self._v_scroll_bar.value = self.viewport_y // 8

    def __on_draw(self):
        self.draw_panel(self.x, self.y, self.width, self.height)

        pyxel.blt(
            self.x + 1,
            self.y + 1,
            self.parent.image,
            self.viewport_x,
            self.viewport_y,
            self.width - 2,
            self.height - 2,
        )

        pyxel.clip(
            self.x + 1, self.y + 1, self.x + self.width - 2, self.y + self.height - 2
        )

        x1 = self.x + self.select_x - self.viewport_x
        y1 = self.y + self.select_y - self.viewport_y
        x2 = x1 + self._select_width + 1
        y2 = y1 + self._select_height + 1

        pyxel.rectb(x1, y1, x2, y2, 0)
        pyxel.rectb(x1 - 1, y1 - 1, x2 + 1, y2 + 1, 7)
        pyxel.rectb(x1 - 2, y1 - 2, x2 + 2, y2 + 2, 0)

        pyxel.clip()

    def __on_h_scroll_bar_change(self, value):
        self.viewport_x = value * 8

    def __on_v_scroll_bar_change(self, value):
        self.viewport_y = value * 8