"""Optional plotting utilities for live Smartline data visualization."""

from typing import Any, Sequence, Tuple


def _get_pyplot():
    """Import and return ``matplotlib.pyplot``.

    Raises
    ------
    ModuleNotFoundError
        If matplotlib is not installed.
    """
    try:
        import matplotlib.pyplot as plt
    except ModuleNotFoundError as exc:  # pragma: no cover - optional dependency
        raise ModuleNotFoundError(
            "matplotlib is required for plotting utilities. Install with 'pip install matplotlib'."
        ) from exc
    return plt


def create_realtime_plot(
    title: str = "Smartline Signal",
    xlabel: str = "Time (s)",
    ylabel: str = "Refractive Index (mRIU)",
) -> Tuple[Any, Any, Any]:
    """Create a simple real-time plot scaffold.

    Returns
    -------
    tuple
        ``(fig, ax, line)`` matplotlib objects used for live updates.
    """
    plt = _get_pyplot()

    fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
    line, = ax.plot([], [], marker="o", linestyle="", markersize=2, color="purple")
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    return fig, ax, line


def update_realtime_plot(line: Any, ax: Any, times: Sequence[float], values: Sequence[float]) -> None:
    """Update an existing line plot with the latest time-series values."""
    line.set_data(times, values)
    ax.relim()
    ax.autoscale_view()
    line.figure.canvas.draw_idle()
    line.figure.canvas.flush_events()
