import math

from .base import BaseChart
from .data import normalize_series, value_range


def _catmull_rom_points(points, samples_per_segment=12):
    """Return a smooth curve that passes through every supplied point."""
    if len(points) < 3:
        return list(points)

    result = []
    for index in range(len(points) - 1):
        p0 = points[index - 1] if index > 0 else points[index]
        p1 = points[index]
        p2 = points[index + 1]
        p3 = points[index + 2] if index + 2 < len(points) else p2

        for step in range(samples_per_segment):
            t = step / samples_per_segment
            t2 = t * t
            t3 = t2 * t
            x = 0.5 * (
                2 * p1[0]
                + (-p0[0] + p2[0]) * t
                + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2
                + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3
            )
            y = 0.5 * (
                2 * p1[1]
                + (-p0[1] + p2[1]) * t
                + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2
                + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3
            )
            result.append((x, y))

    result.append(points[-1])
    return result


class LineChart(BaseChart):
    def draw(self):
        self.draw_title()
        all_values = [value for _, values in self._series.values() for value in values]
        low, high = value_range(all_values)
        left, top, right, bottom = self._chart_bounds(low, high)
        self.draw_grid(low, high, left, top, right, bottom)
        span_x = max(1, right - left)
        span_y = max(1, bottom - top)
        count = max(1, len(self._data_labels) - 1)
        palette = self.theme.palette
        for series_index, (series_name, (labels, values)) in enumerate(self._series.items()):
            color = palette[series_index % len(palette)]
            points = []
            baseline = 0.0 if low <= 0 <= high else low
            for i, value in enumerate(values):
                x = left + span_x * i / count
                animated = baseline + (value - baseline) * self._progress
                y = bottom - ((animated - low) / (high - low)) * span_y
                points.append((x, y))
            if len(points) >= 2:
                curve_points = _catmull_rom_points(points)
                self.create_line(
                    *[coord for point in curve_points for coord in point],
                    fill=color,
                    width=4,
                    smooth=False,
                    joinstyle="round",
                    capstyle="round",
                )
            for i, (x, y) in enumerate(points):
                hovered = i == self._hover_index and series_index == self._hover_series_index()
                radius = 6 if hovered else 4
                fill = self.theme.text if hovered else color
                self.create_oval(x - radius, y - radius, x + radius, y + radius, fill=fill, outline=self.theme.plot_background, width=2)
            if series_index == 0:
                for label_index in self._x_label_indices(len(labels), span_x):
                    x_label = left + span_x * label_index / count
                    self.create_text(x_label, bottom + 18, text=str(labels[label_index]), fill=self.theme.muted_text, font=("TkDefaultFont", 8), anchor="n")
        self._draw_legend(palette[: len(self._series)], left, top, right)

    def _draw_legend(self, colors, left, top, right):
        if not self.show_legend:
            return
        x = left
        for (name, _), color in zip(self._series.items(), colors):
            self.create_text(x, top - 20, text=f"● {name}", anchor="w", fill=color, font=("TkDefaultFont", 8, "bold"))
            x += max(60, 8 * len(str(name)) + 30)
            if x >= right:
                break

    def _hover_series_index(self):
        return getattr(self, "_hover_series", -1)

    def _hit_test(self, x, y):
        if not self._series:
            return -1, -1
        left, top, right, bottom = self._chart_bounds()
        all_values = [value for _, values in self._series.values() for value in values]
        low, high = value_range(all_values)
        span_x, span_y = max(1, right - left), max(1, bottom - top)
        count = max(1, len(self._data_labels) - 1)
        nearest = -1
        nearest_series = -1
        nearest_distance = 16
        baseline = 0.0 if low <= 0 <= high else low
        for series_index, (_, (_, values)) in enumerate(self._series.items()):
            for i, value in enumerate(values):
                px = left + span_x * i / count
                animated = baseline + (value - baseline) * self._progress
                py = bottom - ((animated - low) / (high - low)) * span_y
                distance = math.hypot(x - px, y - py)
                if distance <= nearest_distance:
                    nearest, nearest_series = i, series_index
                    nearest_distance = distance
        return nearest, nearest_series


class BarChart(BaseChart):
    def draw(self):
        self.draw_title()
        all_values = [value for _, values in self._series.values() for value in values]
        low, high = value_range(all_values)
        low, high = min(0, low), max(0, high)
        left, top, right, bottom = self._chart_bounds(low, high)
        if low == high:
            high = low + 1
        self.draw_grid(low, high, left, top, right, bottom)
        zero_y = bottom - ((0 - low) / (high - low)) * (bottom - top)
        slot = (right - left) / len(self._data_labels)
        series_count = max(1, len(self._series))
        group_width = slot * 0.72
        bar_width = group_width / series_count
        palette = self.theme.palette
        for series_index, (_, (_, values)) in enumerate(self._series.items()):
            color = palette[series_index % len(palette)]
            for i, value in enumerate(values):
                x = left + i * slot + (slot - group_width) / 2 + series_index * bar_width
                animated = value * self._progress
                if animated >= 0:
                    y1 = zero_y - (animated / (high - low)) * (bottom - top)
                    y2 = zero_y
                else:
                    y1 = zero_y
                    y2 = zero_y - (animated / (high - low)) * (bottom - top)
                hovered = i == self._hover_index and series_index == self._hover_series_index()
                self.create_rectangle(x, min(y1, y2), x + bar_width * 0.86, max(y1, y2), fill=self.theme.text if hovered else color, outline="")
                if self._progress >= 0.9 and len(self._series) == 1:
                    self.create_text(x + bar_width * 0.43, min(y1, y2) - 10, text=self._format_value(value), fill=self.theme.text, font=("TkDefaultFont", 8, "bold"))
            if series_index == 0:
                label_indices = self._x_label_indices(len(self._data_labels), right - left)
                for i in label_indices:
                    self.create_text(left + i * slot + slot / 2, bottom + 18, text=str(self._data_labels[i]), fill=self.theme.muted_text, font=("TkDefaultFont", 8), anchor="n")
        self._draw_legend(palette[: len(self._series)], left, top, right)

    def _draw_legend(self, colors, left, top, right):
        if not self.show_legend or len(self._series) == 1:
            return
        x = left
        for (name, _), color in zip(self._series.items(), colors):
            self.create_text(x, top - 20, text=f"● {name}", anchor="w", fill=color, font=("TkDefaultFont", 8, "bold"))
            x += max(60, 8 * len(str(name)) + 30)
            if x >= right:
                break

    def _hover_series_index(self):
        return getattr(self, "_hover_series", -1)

    def _hit_test(self, x, y):
        if not self._series:
            return -1, -1
        left, top, right, bottom = self._chart_bounds()
        low, high = value_range([value for _, values in self._series.values() for value in values])
        low, high = min(0, low), max(0, high)
        if low == high:
            high = low + 1
        zero_y = bottom - ((0 - low) / (high - low)) * (bottom - top)
        slot = (right - left) / len(self._data_labels)
        series_count = max(1, len(self._series))
        group_width = slot * 0.72
        bar_width = group_width / series_count
        for i in range(len(self._data_labels)):
            for series_index, (_, (_, values)) in enumerate(self._series.items()):
                value = values[i]
                animated = value * self._progress
                if animated >= 0:
                    y1, y2 = zero_y - (animated / (high - low)) * (bottom - top), zero_y
                else:
                    y1, y2 = zero_y, zero_y - (animated / (high - low)) * (bottom - top)
                x1 = left + i * slot + (slot - group_width) / 2 + series_index * bar_width
                x2 = x1 + bar_width * 0.86
                if x1 <= x <= x2 and min(y1, y2) <= y <= max(y1, y2):
                    return i, series_index
        return -1, -1


class ScatterChart(BaseChart):
    def set_data(self, data, *, animate=None):
        series = normalize_series(data)
        if len(series) > 1:
            raise ValueError("ScatterChart currently supports one series only")
        return super().set_data(data, animate=animate)

    def draw(self):
        self.draw_title()
        low, high = value_range(self._data_values)
        left, top, right, bottom = self._chart_bounds(low, high)
        self.draw_grid(low, high, left, top, right, bottom)
        span_x = max(1, right - left)
        span_y = max(1, bottom - top)
        count = max(1, len(self._data_values) - 1)
        baseline = 0.0 if low <= 0 <= high else low
        label_indices = set(self._x_label_indices(len(self._data_values), span_x))
        for i, value in enumerate(self._data_values):
            x = left + span_x * i / count
            animated = baseline + (value - baseline) * self._progress
            y = bottom - ((animated - low) / (high - low)) * span_y
            size = 5 + min(7, abs(value) / max(abs(high), 1) * 6)
            fill = self.theme.accent_2 if i == self._hover_index else self.theme.accent
            self.create_oval(x - size, y - size, x + size, y + size, fill=fill, outline=self.theme.plot_background, width=2)
            if i in label_indices:
                self.create_text(x, bottom + 18, text=str(self._data_labels[i]), fill=self.theme.muted_text, font=("TkDefaultFont", 8), anchor="n")

    def _hit_test(self, x, y):
        if not self._data_values:
            return -1, -1
        left, top, right, bottom = self._chart_bounds()
        low, high = value_range(self._data_values)
        span_x, span_y = max(1, right - left), max(1, bottom - top)
        count = max(1, len(self._data_values) - 1)
        nearest = -1
        distance_limit = 14
        baseline = 0.0 if low <= 0 <= high else low
        for i, value in enumerate(self._data_values):
            px = left + span_x * i / count
            animated = baseline + (value - baseline) * self._progress
            py = bottom - ((animated - low) / (high - low)) * span_y
            distance = math.hypot(x - px, y - py)
            if distance <= distance_limit:
                nearest = i
                distance_limit = distance
        return nearest, -1


class PieChart(BaseChart):
    def set_data(self, data, *, animate=None):
        series = normalize_series(data)
        if len(series) > 1:
            raise ValueError("PieChart supports one series only")
        return super().set_data(data, animate=animate)

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("show_legend", True)
        super().__init__(*args, **kwargs)

    def _slices(self):
        if any(value < 0 for value in self._data_values):
            raise ValueError("pie chart values cannot be negative")
        total = sum(self._data_values)
        if total <= 0:
            raise ValueError("pie chart values must sum to a positive number")
        slices = []
        start = 0.0
        for label, value in zip(self._data_labels, self._data_values):
            extent = 360.0 * value / total
            slices.append((label, value, start, extent))
            start += extent
        return slices

    def draw(self):
        self.draw_title()
        width, height = max(1, self.winfo_width()), max(1, self.winfo_height())
        legend_width = 150 if self.show_legend else 0
        diameter = max(20, min(width - 30 - legend_width, height - 80))
        x0 = 15 + max(0, (width - legend_width - diameter - 30) / 2)
        y0 = 48 + max(0, (height - 70 - diameter) / 2)
        bounds = (x0, y0, x0 + diameter, y0 + diameter)
        slices = self._slices()
        for i, (_, _, start, extent) in enumerate(slices):
            extent *= self._progress
            fill = self.theme.text if i == self._hover_index else self._slice_color(i)
            self.create_arc(*bounds, start=start, extent=extent, fill=fill, outline=self.theme.plot_background, width=2)
        if self.show_legend:
            lx, ly = width - legend_width + 12, 62
            total = sum(self._data_values)
            for i, (label, value, _, _) in enumerate(slices):
                color = self._slice_color(i)
                self.create_rectangle(lx, ly - 5, lx + 10, ly + 5, fill=color, outline="")
                percent = 100 * value / total
                self.create_text(lx + 16, ly, text=f"{label} · {self._format_value(value)} ({percent:.0f}%)", anchor="w", fill=self.theme.text, font=("TkDefaultFont", 8))
                ly += 22

    def _slice_color(self, index):
        palette = self.theme.palette
        return palette[index % len(palette)]

    def _hit_test(self, x, y):
        slices = self._slices() if self._data_values else []
        width, height = max(1, self.winfo_width()), max(1, self.winfo_height())
        legend_width = 150 if self.show_legend else 0
        diameter = max(20, min(width - 30 - legend_width, height - 80))
        x0 = 15 + max(0, (width - legend_width - diameter - 30) / 2)
        y0 = 48 + max(0, (height - 70 - diameter) / 2)
        cx, cy = x0 + diameter / 2, y0 + diameter / 2
        if math.hypot(x - cx, y - cy) > diameter / 2:
            return -1, -1
        angle = (math.degrees(math.atan2(-(y - cy), x - cx)) + 360) % 360
        visible = self._progress
        for i, (_, _, start, extent) in enumerate(slices):
            visible_extent = extent * visible
            if visible_extent > 0 and start <= angle <= start + visible_extent:
                return i, -1
        return -1, -1


class DonutChart(PieChart):
    def __init__(self, *args, hole=0.56, center_text=None, **kwargs):
        self.hole = min(0.9, max(0.15, float(hole)))
        self.center_text = center_text
        super().__init__(*args, **kwargs)

    def draw(self):
        super().draw()
        width, height = max(1, self.winfo_width()), max(1, self.winfo_height())
        legend_width = 150 if self.show_legend else 0
        diameter = max(20, min(width - 30 - legend_width, height - 80))
        x0 = 15 + max(0, (width - legend_width - diameter - 30) / 2)
        y0 = 48 + max(0, (height - 70 - diameter) / 2)
        inner = diameter * self.hole
        cx, cy = x0 + diameter / 2, y0 + diameter / 2
        self.create_oval(cx - inner / 2, cy - inner / 2, cx + inner / 2, cy + inner / 2, fill=self.theme.plot_background, outline="")
        text = self.center_text if self.center_text is not None else self._format_value(sum(self._data_values))
        self.create_text(cx, cy, text=text, fill=self.theme.text, font=("TkDefaultFont", 11, "bold"))

    def _hit_test(self, x, y):
        index, series_index = super()._hit_test(x, y)
        if index < 0:
            return -1, -1
        width, height = max(1, self.winfo_width()), max(1, self.winfo_height())
        legend_width = 150 if self.show_legend else 0
        diameter = max(20, min(width - 30 - legend_width, height - 80))
        x0 = 15 + max(0, (width - legend_width - diameter - 30) / 2)
        y0 = 48 + max(0, (height - 70 - diameter) / 2)
        inner = diameter * self.hole
        cx, cy = x0 + diameter / 2, y0 + diameter / 2
        if math.hypot(x - cx, y - cy) < inner / 2:
            return -1, -1
        return index, series_index
