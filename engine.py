"""
engine.py — BookingEngine
Launches _launcher.py in a subprocess via subprocess.Popen.
This avoids multiprocessing pickle issues and keeps webview on its own
main thread while the CTk window stays fully responsive.
"""

import os
import sys
import subprocess
import threading
from pathlib import Path


def get_profile_dir() -> str:
    path = Path(__file__).parent.resolve() / "browser_profile"
    path.mkdir(exist_ok=True)
    return str(path)


def get_launcher() -> str:
    return str(Path(__file__).parent.resolve() / "_launcher.py")


class BookingEngine:
    BOOKING_URL = "https://app.10to8.com/booking/5bf4ba81-9fd4-48f4-9cf9-3d4106e4a75f/"
    PORTAL_URL  = "https://app.10to8.com/portal/#/"

    def launch(self, service_id: str = "", on_close_cb=None):
        url = self.BOOKING_URL + service_id
        self._spawn("booking", url, on_close_cb)

    def launch_portal(self, on_close_cb=None):
        self._spawn("portal", self.PORTAL_URL, on_close_cb)

    @staticmethod
    def _spawn(mode: str, url: str, on_close_cb):
        profile  = get_profile_dir()
        launcher = get_launcher()

        p = subprocess.Popen(
            [sys.executable, launcher, mode, url, profile],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        if on_close_cb:
            def _watch():
                stdout, stderr = p.communicate()
                if stderr:
                    print(f"[launcher/{mode} stderr]\n{stderr.decode(errors='replace')}")
                on_close_cb()

            t = threading.Thread(target=_watch, daemon=True)
            t.start()
