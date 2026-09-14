from dataclasses import dataclass


@dataclass(frozen=True)
class Theme:
    background: str
    plot_background: str
    text: str
    muted_text: str
    grid: str
    axis: str
    accent: str
    accent_2: str
    tooltip_background: str
    tooltip_border: str
    tooltip_text: str
    positive: str
    negative: str

    @property
    def palette(self):
        return (
            self.accent,
            self.accent_2,
            self.positive,
            self.negative,
            "#F59E0B",
            "#EC4899",
            "#8B5CF6",
        )


LIGHT = Theme(
    background="#FFFFFF",
    plot_background="#FFFFFF",
    text="#1F2937",
    muted_text="#6B7280",
    grid="#E5E7EB",
    axis="#9CA3AF",
    accent="#4F46E5",
    accent_2="#0EA5E9",
    tooltip_background="#111827",
    tooltip_border="#374151",
    tooltip_text="#F9FAFB",
    positive="#16A34A",
    negative="#DC2626",
)

DARK = Theme(
    background="#0D1117",
    plot_background="#161B22",
    text="#F0F6FC",
    muted_text="#8B949E",
    grid="#30363D",
    axis="#8B949E",
    accent="#58A6FF",
    accent_2="#2DD4BF",
    tooltip_background="#21262D",
    tooltip_border="#58A6FF",
    tooltip_text="#F0F6FC",
    positive="#3FB950",
    negative="#F85149",
)


def resolve_theme(theme):
    if isinstance(theme, Theme):
        return theme
    if theme == "dark":
        return DARK
    if theme in (None, "light"):
        return LIGHT
    raise ValueError("theme must be 'light', 'dark', or a Theme instance")
