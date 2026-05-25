from __future__ import annotations

import os
import signal
import subprocess
import sys
import time
import atexit
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlencode

from ._paths import browser_profile_dir
from .registry import process_exists, upsert_bridge


@dataclass
class WindowHandle:
    port: int
    url: str
    pid: int | None
    owned: bool

    @property
    def alive(self) -> bool:
        return bool(self.owned and self.pid and process_exists(self.pid))

    def wait(self, poll_interval: float = 0.5) -> None:
        if not self.owned or not self.pid:
            return
        while process_exists(self.pid):
            time.sleep(poll_interval)

    def close(self) -> None:
        if not self.owned or not self.pid:
            return
        close_process_tree(self.pid)


def window(
    port: int = 1146,
    *,
    token: str | None = None,
    close_on_exit: bool = True,
    web_url: str | None = None,
    mode: str = "mini",
    width: int = 420,
    height: int = 340,
    profile: str | None = None,
) -> WindowHandle:
    base_url = web_url or discover_web_url(port)
    query = {"bridgePort": str(port)}
    if token:
        query["pairingToken"] = token
    if mode:
        query["mode"] = mode
    separator = "&" if "?" in base_url else "?"
    url = f"{base_url}{separator}{urlencode(query)}"
    browser = find_chromium()
    if browser:
        process = subprocess.Popen(
            [
                str(browser),
                f"--app={url}",
                f"--user-data-dir={browser_profile_dir(port, profile)}",
                f"--window-size={width},{height}",
                "--disable-background-timer-throttling",
                "--disable-backgrounding-occluded-windows",
                "--disable-renderer-backgrounding",
                "--no-first-run",
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            close_fds=os.name != "nt",
        )
        upsert_bridge(port, window_pid=process.pid, window_url=url)
        handle = WindowHandle(port=port, url=url, pid=process.pid, owned=True)
        if close_on_exit:
            atexit.register(handle.close)
        return handle

    import webbrowser

    webbrowser.open(url)
    upsert_bridge(port, window_pid=None, window_url=url)
    return WindowHandle(port=port, url=url, pid=None, owned=False)


def discover_web_url(port: int) -> str:
    override = os.environ.get("XLOCLLM_WEB_URL")
    if override:
        return override.rstrip("/")
    for candidate in (f"http://127.0.0.1:{port}/ui/", "http://127.0.0.1:5173", "http://localhost:5173"):
        try:
            with urllib.request.urlopen(candidate, timeout=0.5) as response:
                if response.status < 500:
                    return candidate
        except (OSError, urllib.error.URLError):
            continue
    return "http://127.0.0.1:5173"


def find_chromium() -> Path | None:
    candidates: list[Path] = []
    if os.name == "nt":
        roots = [
            os.environ.get("PROGRAMFILES"),
            os.environ.get("PROGRAMFILES(X86)"),
            os.environ.get("LOCALAPPDATA"),
        ]
        for root in roots:
            if not root:
                continue
            base = Path(root)
            candidates.extend(
                [
                    base / "Microsoft" / "Edge" / "Application" / "msedge.exe",
                    base / "Google" / "Chrome" / "Application" / "chrome.exe",
                    base / "Chromium" / "Application" / "chrome.exe",
                ]
            )
    elif sys.platform == "darwin":
        candidates.extend(
            [
                Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
                Path("/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"),
                Path("/Applications/Chromium.app/Contents/MacOS/Chromium"),
            ]
        )
    else:
        for name in ("google-chrome", "microsoft-edge", "chromium", "chromium-browser"):
            path = shutil_which(name)
            if path:
                candidates.append(Path(path))
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def close_process_tree(pid: int) -> None:
    if os.name == "nt":
        subprocess.run(["taskkill", "/PID", str(pid), "/T", "/F"], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return
    try:
        os.kill(pid, signal.SIGTERM)
    except OSError:
        return
    time.sleep(0.2)


def shutil_which(name: str) -> str | None:
    import shutil

    return shutil.which(name)
