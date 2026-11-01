from solar_hosting_capacity.constants import V_MAX, V_MIN


def plot_profile(profile_df, ax, label: str) -> None:
    """Voltage (V) vs distance (m) on the given axes. Does not create a figure."""
    ax.plot(profile_df["dist_m"], profile_df["volts"], marker="o", markersize=3, label=label)


def add_limits(ax) -> None:
    """Dashed horizontal lines at the V_MAX and V_MIN steady-state limits."""
    ax.axhline(V_MAX, color="red", linestyle="--", label=f"{V_MAX:.0f} V upper limit")
    ax.axhline(V_MIN, color="blue", linestyle="--", label=f"{V_MIN:.0f} V lower limit")
