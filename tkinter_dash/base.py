import math
import tkinter as tk
import tkinter.font as tkfont

from .data import normalize_series
from .theme import resolve_theme


class BaseChart(tk.Canvas):
    """Common Tkinter Canvas behavior shared by chart widgets."""

    def __init__(
        self,
        master,
        data=None,
        *,
        title=None,
        theme="light",
        animate=True,
        duration=350,
        tooltip=True,
        show_legend=True,
        **kwargs,
    ):
        self.theme = resolve_theme(theme)
        super().__init__(
            master,
            bg=self.theme.plot_background,
            highlightthickness=0,
            bd=0,
            **kwargs,
        )
        self.title = title
        self.animate_enabled = bool(animate)
        self.animation_duration = max(1, int(duration))
        self.tooltip_enabled = bool(tooltip)
        self.show_legend = bool(show_legend)
        self._progress = 1.0 if not self.animate_enabled else 0.0
        self._animation_after_id = None
        self._tooltip = None
        self._hover_index = -1
        self.last_clicked_index = -1
        self.last_clicked_series = None
        self._data_labels = []
        self._data_values = []
        self._series = {}
        self._configure_id = None
        self._destroyed = False

        self.bind("<Configure>", self._on_configure)
        self.bind("<Motion>", self._on_motion)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)

        if data is not None:
            self.set_data(data, animate=self.animate_enabled)

    @property
    def data(self):
        if len(self._series) <= 1:
            return list(zip(self._data_labels, self._data_values))
        return {name: dict(zip(labels, values)) for name, (labels, values) in self._series.items()}

    def set_data(self, data, *, animate=None):
        series = normalize_series(data)
        if animate is None:
            animate = self.animate_enabled
        first_labels, first_values = next(iter(series.values()))
        self._series = series
        self._data_labels = first_labels
        self._data_values = first_values
        self._hover_index = -1
        self._hover_series = -1
        self._destroy_tooltip()
        self._start_animation() if animate else self._finish_animation()
        return self

    def update(self, data, *, animate=None):
        return self.set_data(data, animate=animate)

    def configure_theme(self, theme):
        self.theme = resolve_theme(theme)
        super().configure(bg=self.theme.plot_background)
        self.redraw()
        return self

    def _start_animation(self):
        self._cancel_animation()
        if not self.animate_enabled:
            self._finish_animation()
            return
        self._progress = 0.0
        self.redraw()
        steps = max(1, self.animation_duration // 16)
        self._animation_step = 1.0 / steps
        self._animation_after_id = self.after(16, self._animate)

    def _finish_animation(self):
        self._cancel_animation()
        self._progress = 1.0
        self.redraw()

    def _animate(self):
        if self._destroyed:
            self._animation_after_id = None
            return
        self._animation_after_id = None
        self._progress = min(1.0, self._progress + self._animation_step)
        self.redraw()
        if self._progress < 1.0:
            self._animation_after_id = self.after(16, self._animate)

    def _cancel_animation(self):
        if self._animation_after_id is not None:
            try:
                self.after_cancel(self._animation_after_id)
            except tk.TclError:
                pass
            self._animation_after_id = None

    def _on_configure(self, event):
        if self._configure_id is not None:
            try:
                self.after_cancel(self._configure_id)
            except tk.TclError:
                pass
        self._configure_id = self.after(10, self._redraw_debounced)

    def _redraw_debounced(self):
        self._configure_id = None
        if not self._destroyed:
            self.redraw()

    def _on_motion(self, event):
        index, series_index = self._hit_test(event.x, event.y)
        if index != self._hover_index or series_index != self._hover_series:
            self._hover_index = index
            self._hover_series = series_index
            self._destroy_tooltip()
            if index >= 0 and self.tooltip_enabled:
                self._show_tooltip(event.x, event.y, index)
            self.redraw()

    def _on_leave(self, _event):
        if self._hover_index != -1:
            self._hover_index = -1
            self._hover_series = -1
            self._destroy_tooltip()
            self.redraw()

    def _on_click(self, event):
        index, series_index = self._hit_test(event.x, event.y)
        if index >= 0:
            self.last_clicked_index = index
            self.last_clicked_series = series_index
            self.event_generate("<<DataPointClick>>")

    def _show_tooltip(self, x, y, index):
        self._show_custom_tooltip(
            x,
            y,
            str(self._data_labels[index]),
            self._format_value(self._data_values[index]),
        )

    def _show_custom_tooltip(self, x, y, label, value_text):
        self._tooltip = tk.Toplevel(self)
        self._tooltip.overrideredirect(True)
        self._tooltip.configure(bg=self.theme.tooltip_border)
        body = tk.Frame(self._tooltip, bg=self.theme.tooltip_background)
        body.pack(padx=1, pady=1)
        tk.Label(
            body,
            text=label,
            bg=self.theme.tooltip_background,
            fg=self.theme.muted_text,
            font=("TkDefaultFont", 9),
            padx=10,
            pady=7,
        ).pack(anchor="w")
        tk.Label(
            body,
            text=value_text,
            bg=self.theme.tooltip_background,
            fg=self.theme.tooltip_text,
            font=("TkDefaultFont", 12, "bold"),
            padx=10,
            pady=7,
        ).pack(anchor="w")
        self._tooltip.update_idletasks()
        tooltip_width = self._tooltip.winfo_width()
        tooltip_height = self._tooltip.winfo_height()
        screen_x = self.winfo_rootx() + x - tooltip_width // 2
        screen_y = self.winfo_rooty() + y - tooltip_height - 12

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        if screen_y < 0:
            screen_y = self.winfo_rooty() + y + 12
        screen_x = max(0, min(screen_x, screen_width - tooltip_width))
        screen_y = max(0, min(screen_y, screen_height - tooltip_height))
        self._tooltip.geometry(f"+{screen_x}+{screen_y}")

    def _destroy_tooltip(self):
        if self._tooltip is not None:
            try:
                self._tooltip.destroy()
            except tk.TclError:
                pass
            self._tooltip = None

    @staticmethod
    def _format_value(value):
        if float(value).is_integer():
            return str(int(value))
        return f"{value:.2f}".rstrip("0").rstrip(".")

    def _chart_bounds(self, low=None, high=None):
        width = max(1, self.winfo_width())
        height = max(1, self.winfo_height())
        right = 24
        top = 48
        bottom = 54
        left = 64
        if low is not None and high is not None:
            font = self._axis_font()
            values = [high, low + (high - low) * 0.8, low + (high - low) * 0.6,
                      low + (high - low) * 0.4, low + (high - low) * 0.2, low]
            label_width = max(font.measure(self._format_value(value)) for value in values)
            left = max(left, label_width + 18)
        return left, top, max(left + 10, width - right), max(top + 10, height - bottom)

    @staticmethod
    def _axis_font():
        return tkfont.nametofont("TkDefaultFont")

    @staticmethod
    def _x_label_indices(count, width, min_spacing=80):
        if count <= 0:
            return []
        if count == 1:
            return [0]
        max_labels = max(2, int(max(1, width - 20) // min_spacing) + 1)
        if count <= max_labels:
            return list(range(count))
        step = max(1, math.ceil((count - 1) / (max_labels - 1)))
        indices = list(range(0, count, step))
        if indices[-1] != count - 1:
            indices.append(count - 1)
        return indices

    @property
    def series(self):
        return {name: list(zip(labels, values)) for name, (labels, values) in self._series.items()}

    def redraw(self):
        self.delete("all")
        if not self._data_values:
            self.create_text(
                max(1, self.winfo_width()) / 2,
                max(1, self.winfo_height()) / 2,
                text="No data",
                fill=self.theme.muted_text,
                font=("TkDefaultFont", 11),
            )
            return
        self.draw()

    def draw_title(self):
        if self.title:
            width = max(1, self.winfo_width())
            self.create_text(
                width / 2,
                20,
                text=self.title,
                fill=self.theme.text,
                font=("TkDefaultFont", 13, "bold"),
            )

    def draw_grid(self, low, high, left, top, right, bottom):
        self.create_rectangle(left, top, right, bottom, fill=self.theme.plot_background, outline="")
        ticks = 5
        span = high - low
        for i in range(ticks + 1):
            ratio = i / ticks
            y = bottom - ratio * (bottom - top)
            value = low + span * ratio
            self.create_line(left, y, right, y, fill=self.theme.grid)
            self.create_text(
                left - 10,
                y,
                text=self._format_value(value),
                anchor="e",
                fill=self.theme.muted_text,
                font=("TkDefaultFont", 8),
            )

        self.create_line(left, top, left, bottom, fill=self.theme.axis)
        self.create_line(left, bottom, right, bottom, fill=self.theme.axis)

    def _hit_test(self, x, y):
        return -1, -1

    def hit_test(self, x, y):
        """Return the data-point index under the given canvas coordinates."""
        index, _ = self._hit_test(x, y)
        return index

    def destroy(self):
        self._destroyed = True
        self._cancel_animation()
        if self._configure_id is not None:
            try:
                self.after_cancel(self._configure_id)
            except tk.TclError:
                pass
            self._configure_id = None
        self._destroy_tooltip()
        return super().destroy()
