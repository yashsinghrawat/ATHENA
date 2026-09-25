"""
CLI demo for the ATHENA AI core. This IS the Phase 1 milestone from the
roadmap: text -> LLM extraction -> embedding -> storage -> baseline/trend,
with no frontend/backend/auth wrapped around it yet.

Usage:
    python -m src.main add "some journal text" [--days-ago N]
    python -m src.main baseline
    python -m src.main trajectory <dimension>
    python -m src.main list
"""
import argparse
import sys

from rich.console import Console
from rich.table import Table

from src import emotion_engine, embedding_engine, storage, temporal_engine
from src.config import STATE_DIMENSIONS

console = Console()


def cmd_add(args):
    console.print(f"[dim]Analyzing entry...[/dim]")
    analysis = emotion_engine.analyze(args.text)
    embedding = embedding_engine.embed(args.text)
    entry_id = storage.save_entry(analysis, embedding=embedding, days_ago=args.days_ago)

    console.print(f"[green]Saved entry #{entry_id}[/green]")
    table = Table(title="Extracted state")
    table.add_column("Dimension")
    table.add_column("Score")
    for dim, score in analysis["emotional_state"].items():
        table.add_row(dim, f"{score:.2f}")
    console.print(table)
    console.print(f"[dim]Confidence: {analysis.get('confidence', 0):.2f}[/dim]")
    if analysis.get("topics"):
        console.print(f"[dim]Topics: {', '.join(analysis['topics'])}[/dim]")
    if analysis.get("context"):
        console.print(f"[dim]Context: {', '.join(analysis['context'])}[/dim]")


def cmd_baseline(args):
    entries = storage.get_entries()
    if len(entries) < 2:
        console.print("[yellow]Need at least a few entries first — run 'add' a few times.[/yellow]")
        return

    comparison = temporal_engine.compare_to_baseline(entries)
    table = Table(title="Personal baseline vs current window")
    table.add_column("Dimension")
    table.add_column("Baseline")
    table.add_column("Current")
    table.add_column("Delta")
    table.add_column("Flagged")
    for dim, stats in comparison.items():
        flag = "[red]YES[/red]" if stats["flagged"] else "no"
        table.add_row(dim, str(stats["baseline"]), str(stats["current"]), str(stats["delta"]), flag)
    console.print(table)


def cmd_trajectory(args):
    entries = storage.get_entries()
    if not entries:
        console.print("[yellow]No entries yet.[/yellow]")
        return
    points = temporal_engine.trajectory(entries, args.dimension)
    table = Table(title=f"Trajectory: {args.dimension}")
    table.add_column("Timestamp")
    table.add_column("Score")
    for ts, score in points:
        table.add_row(ts, f"{score:.2f}")
    console.print(table)


def cmd_list(args):
    entries = storage.get_entries()
    if not entries:
        console.print("[yellow]No entries yet.[/yellow]")
        return
    table = Table(title="All entries")
    table.add_column("ID")
    table.add_column("Timestamp")
    table.add_column("Text")
    for e in entries:
        preview = e["text"][:60] + ("..." if len(e["text"]) > 60 else "")
        table.add_row(str(e["id"]), e["timestamp"], preview)
    console.print(table)


def main():
    parser = argparse.ArgumentParser(description="ATHENA AI core CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="Analyze and store a new entry")
    p_add.add_argument("text")
    p_add.add_argument("--days-ago", type=int, default=0, help="Backdate for demo purposes")
    p_add.set_defaults(func=cmd_add)

    p_baseline = sub.add_parser("baseline", help="Compare current window to personal baseline")
    p_baseline.set_defaults(func=cmd_baseline)

    p_traj = sub.add_parser("trajectory", help="Show a dimension's history over time")
    p_traj.add_argument("dimension", choices=STATE_DIMENSIONS)
    p_traj.set_defaults(func=cmd_trajectory)

    p_list = sub.add_parser("list", help="List all stored entries")
    p_list.set_defaults(func=cmd_list)

    args = parser.parse_args()
    try:
        args.func(args)
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
