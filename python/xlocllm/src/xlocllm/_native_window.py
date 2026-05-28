from __future__ import annotations

import argparse
import json
import tkinter as tk
import urllib.error
import urllib.request
from typing import Any


BG = "#f6faf9"
SURFACE = "#ffffff"
CARD = "#eef6f5"
CARD_DARK = "#e5f0ef"
TEXT = "#122027"
MUTED = "#60727b"
GREEN = "#2fbf7b"
GREEN_SOFT = "#dff7e9"
RED = "#c53b49"
BORDER = "#d9e6e5"


class NativeDashboard:
    def __init__(self, root: tk.Tk, *, port: int, width: int, height: int) -> None:
        self.root = root
        self.port = port
        self.base_url = f"http://127.0.0.1:{port}"
        self.root.title("xlocllm")
        self.root.geometry(f"{width}x{height}")
        self.root.minsize(420, 400)
        self.root.configure(bg=BG)
        self.root.option_add("*Font", "Segoe UI 10")
        self.values: dict[str, tk.StringVar] = {
            "gpu": tk.StringVar(value="--"),
            "cpu": tk.StringVar(value="--"),
            "ram": tk.StringVar(value="--"),
            "models": tk.StringVar(value="0"),
            "queue": tk.StringVar(value="0"),
            "status": tk.StringVar(value="offline"),
            "logs": tk.StringVar(value="Waiting for native runtime..."),
        }
        self._build()

    def _build(self) -> None:
        shell = tk.Frame(self.root, bg=BG, padx=18, pady=18)
        shell.pack(fill="both", expand=True)

        header = tk.Frame(shell, bg=BG)
        header.pack(fill="x", pady=(0, 14))
        tk.Label(
            header,
            text="xlocllm",
            bg=BG,
            fg=TEXT,
            font=("Segoe UI", 24, "bold"),
        ).pack(side="left")
        tk.Label(
            header,
            text="native",
            bg=GREEN_SOFT,
            fg="#176f48",
            font=("Segoe UI", 12, "bold"),
            padx=16,
            pady=8,
        ).pack(side="right")

        gauges = tk.Frame(shell, bg=BG)
        gauges.pack(fill="x", pady=(0, 12))
        for key, label in (("gpu", "GPU"), ("cpu", "CPU"), ("ram", "RAM")):
            card = tk.Frame(gauges, bg=CARD, padx=12, pady=12, highlightthickness=1, highlightbackground="#e0eceb")
            card.pack(side="left", fill="x", expand=True, padx=5)
            tk.Label(card, text=label, bg=CARD, fg=MUTED, font=("Segoe UI", 10, "bold")).pack(anchor="w")
            tk.Label(card, textvariable=self.values[key], bg=CARD, fg=TEXT, font=("Segoe UI", 22, "bold")).pack(anchor="w", pady=(8, 0))

        middle = tk.Frame(shell, bg=SURFACE, padx=14, pady=12, highlightthickness=1, highlightbackground=BORDER)
        middle.pack(fill="x", pady=(0, 12))
        top_line = tk.Frame(middle, bg=SURFACE)
        top_line.pack(fill="x")
        tk.Label(top_line, text="DISK", bg=SURFACE, fg=MUTED, font=("Segoe UI", 9, "bold")).pack(side="left")
        tk.Label(top_line, textvariable=self.values["status"], bg=SURFACE, fg=GREEN, font=("Segoe UI", 9, "bold")).pack(side="right")
        self.disk_canvas = tk.Canvas(middle, height=9, bg=SURFACE, highlightthickness=0)
        self.disk_canvas.pack(fill="x", pady=(9, 0))
        self.disk_value = 0.0

        counters = tk.Frame(shell, bg=BG)
        counters.pack(fill="x", pady=(0, 12))
        self._counter(counters, "models", "models").pack(side="left", fill="x", expand=True, padx=(0, 6))
        self._counter(counters, "queue", "queue").pack(side="left", fill="x", expand=True, padx=(6, 0))

        actions = tk.Frame(shell, bg=BG)
        actions.pack(fill="x", pady=(0, 12))
        self._button(actions, "Start", "#122027", "#ffffff", lambda: self.post("/xlocllm/v1/runtime/heatup")).pack(side="left", fill="x", expand=True, padx=(0, 6))
        self._button(actions, "Pause", SURFACE, TEXT, lambda: self.post("/xlocllm/v1/runtime/hibernate")).pack(side="left", fill="x", expand=True, padx=6)
        self._button(actions, "Clear", SURFACE, TEXT, lambda: self.post("/xlocllm/v1/models/delete_all")).pack(side="left", fill="x", expand=True, padx=(6, 0))

        log_card = tk.Frame(shell, bg=CARD, padx=12, pady=10, highlightthickness=1, highlightbackground="#e0eceb")
        log_card.pack(fill="both", expand=True)
        tk.Label(log_card, text="EVENTS", bg=CARD, fg=MUTED, font=("Segoe UI", 9, "bold")).pack(anchor="w")
        tk.Label(
            log_card,
            textvariable=self.values["logs"],
            bg=CARD,
            fg="#36515b",
            justify="left",
            anchor="nw",
            wraplength=360,
        ).pack(fill="both", expand=True, pady=(8, 0))

    def _counter(self, parent: tk.Frame, key: str, label: str) -> tk.Frame:
        frame = tk.Frame(parent, bg=SURFACE, padx=12, pady=10, highlightthickness=1, highlightbackground=BORDER)
        tk.Label(frame, textvariable=self.values[key], bg=SURFACE, fg=TEXT, font=("Segoe UI", 20, "bold")).pack(side="left")
        tk.Label(frame, text=label, bg=SURFACE, fg=MUTED).pack(side="left", padx=(8, 0), pady=(8, 0))
        return frame

    def _button(
        self,
        parent: tk.Frame,
        text: str,
        bg: str,
        fg: str,
        command: Any,
    ) -> tk.Button:
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg,
            fg=fg,
            activebackground=GREEN if bg != SURFACE else CARD_DARK,
            activeforeground=fg,
            relief="flat",
            borderwidth=0,
            highlightthickness=1,
            highlightbackground=BORDER,
            padx=12,
            pady=10,
            cursor="hand2",
            font=("Segoe UI", 10, "bold"),
        )

    def poll(self) -> None:
        try:
            data = self.get("/xlocllm/v1/status")
            runtime = data.get("runtime") if isinstance(data.get("runtime"), dict) else {}
            metrics = runtime.get("metrics") if isinstance(runtime.get("metrics"), dict) else {}
            self.values["gpu"].set(fmt_percent(metrics.get("gpu")))
            self.values["cpu"].set(fmt_percent(metrics.get("cpu")))
            self.values["ram"].set(fmt_percent(metrics.get("ram")))
            self.disk_value = float(metrics.get("disk") or 0)
            models = runtime.get("models") if isinstance(runtime.get("models"), list) else []
            active_count = len([item for item in models if isinstance(item, dict) and item.get("active")])
            requests = runtime.get("requests") if isinstance(runtime.get("requests"), dict) else {}
            self.values["models"].set(str(active_count))
            self.values["queue"].set(str(requests.get("queued") or 0))
            self.values["status"].set("running" if runtime.get("running") else "ready")
            logs = runtime.get("logs") if isinstance(runtime.get("logs"), list) else []
            self.values["logs"].set("\n".join(format_log(item) for item in logs[-5:]) or "No runtime events yet.")
        except Exception as error:  # noqa: BLE001
            self.disk_value = 0.0
            self.values["status"].set("offline")
            self.values["logs"].set(f"offline - {error}")
        self.draw_disk_bar()
        self.root.after(1000, self.poll)

    def draw_disk_bar(self) -> None:
        self.disk_canvas.delete("all")
        width = max(1, self.disk_canvas.winfo_width())
        height = max(1, self.disk_canvas.winfo_height())
        fill_width = int(width * max(0.0, min(self.disk_value, 100.0)) / 100.0)
        self.disk_canvas.create_rectangle(0, 0, width, height, fill="#e7eeee", outline="")
        color = RED if self.disk_value >= 90 else GREEN
        self.disk_canvas.create_rectangle(0, 0, fill_width, height, fill=color, outline="")

    def get(self, path: str) -> dict[str, Any]:
        with urllib.request.urlopen(self.base_url + path, timeout=2) as response:
            return json.loads(response.read().decode("utf-8"))

    def post(self, path: str) -> None:
        request = urllib.request.Request(
            self.base_url + path,
            data=b"{}",
            method="POST",
            headers={"Content-Type": "application/json"},
        )
        try:
            urllib.request.urlopen(request, timeout=5).read()
        except urllib.error.URLError:
            return
        self.poll()


def fmt_percent(value: Any) -> str:
    if value is None:
        return "--"
    try:
        return f"{round(float(value))}%"
    except (TypeError, ValueError):
        return "--"


def format_log(item: Any) -> str:
    if not isinstance(item, dict):
        return str(item)
    return f"{item.get('level', 'info')} - {item.get('message', '')}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=1146)
    parser.add_argument("--token", default="")
    parser.add_argument("--width", type=int, default=440)
    parser.add_argument("--height", type=int, default=430)
    args = parser.parse_args()
    root = tk.Tk()
    dashboard = NativeDashboard(root, port=args.port, width=args.width, height=args.height)
    dashboard.poll()
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
