from rich.console import Console
from rich.table import Table

from src import storage, temporal_engine
from src.config import STATE_DIMENSIONS


console = Console()


def main():
    entries = storage.get_entries()

    if not entries:
        console.print("[yellow]No demo data found.[/yellow]")
        console.print("Run: python -m src.demo_data")
        return

    console.print("\n[bold]ATHENA — Longitudinal State Analysis[/bold]\n")

    console.print(
        f"[dim]Analyzing {len(entries)} longitudinal entries...[/dim]\n"
    )

    # Baseline comparison
    comparison = temporal_engine.compare_to_baseline(entries)

    table = Table(title="Personal Baseline vs Current State")
    table.add_column("Dimension")
    table.add_column("Baseline")
    table.add_column("Current")
    table.add_column("Delta")
    table.add_column("Signal")

    for dim in STATE_DIMENSIONS:
        stats = comparison[dim]

        signal = (
            "[red]SIGNIFICANT CHANGE[/red]"
            if stats["flagged"]
            else "[green]Stable[/green]"
        )

        table.add_row(
            dim.replace("_", " ").title(),
            f"{stats['baseline']:.3f}",
            f"{stats['current']:.3f}",
            f"{stats['delta']:+.3f}",
            signal,
        )

    console.print(table)

    # Stress trajectory
    console.print("\n[bold]Stress Trajectory[/bold]")

    stress_points = temporal_engine.trajectory(entries, "stress")

    for i, (_, score) in enumerate(stress_points, start=1):
        bar = "█" * int(score * 20)
        console.print(
            f"Day {i:<2} {bar:<20} {score:.2f}"
        )

    # Motivation trajectory
    console.print("\n[bold]Motivation Trajectory[/bold]")

    motivation_points = temporal_engine.trajectory(entries, "motivation")

    for i, (_, score) in enumerate(motivation_points, start=1):
        bar = "█" * int(score * 20)
        console.print(
            f"Day {i:<2} {bar:<20} {score:.2f}"
        )

    console.print(
        "\n[bold green]ATHENA analysis complete.[/bold green]"
    )


if __name__ == "__main__":
    main()
