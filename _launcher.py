"""
_launcher.py — Invoked by engine.py via subprocess.Popen.
Never run this directly. Arguments: <mode> <url> <profile_path>
"""

import sys
import os

if len(sys.argv) < 4:
    print("Usage: _launcher.py <mode> <url> <profile_path>")
    sys.exit(1)

mode    = sys.argv[1]   # "booking" or "portal"
url     = sys.argv[2]
profile = sys.argv[3]

os.makedirs(profile, exist_ok=True)

import webview

BOOKING_CSS = """
.t28-nav-container, .t28-header, .t28-footer, .t28-branding,
.t28-booking-page-header, .t28-cookie-consent,
.t28-about, .t28-contact, .t28-social,
nav, header, footer,
[class*="nav-container"], [class*="page-header"],
[class*="site-header"], [class*="site-footer"],
[class*="branding"], [class*="cookie"],
[class*="language-"], [class*="lang-select"],
[class*="terms-link"], [class*="legal-link"],
[class*="social-"], .about-section, .contact-section,
.social-section, .language-section,
[class*="banner"], [class*="hero"],
img[class*="header"], a[href*="gtc"], a > img[alt="Home"] {
    display: none !important;
}
html, body {
    background: #080D18 !important;
    color: #E2E8F0 !important;
    margin: 0 !important; padding: 0 !important;
    font-family: 'Trebuchet MS', 'Segoe UI', sans-serif !important;
}
.t28-booking-page, [class*="booking-page"],
[class*="booking-container"], [class*="booking-wrapper"] {
    border: none !important; box-shadow: none !important;
    background: #080D18 !important; max-width: 100% !important;
}
[class*="calendar"], [class*="date-picker"] {
    background: #0F1724 !important; border: 1px solid #1E2D45 !important;
    border-radius: 8px !important; color: #E2E8F0 !important;
}
[class*="time-slot"], [class*="timeslot"] {
    background: #161F30 !important; border: 1px solid #1E2D45 !important;
    color: #06B6D4 !important; border-radius: 6px !important;
}
[class*="time-slot"]:hover { background: #06B6D4 !important; color: #080D18 !important; }
input, select, textarea {
    background: #161F30 !important; border: 1px solid #1E2D45 !important;
    color: #E2E8F0 !important; border-radius: 6px !important; padding: 8px 12px !important;
}
input::placeholder { color: #4A6080 !important; }
[class*="btn-primary"], button[type="submit"] {
    background: #06B6D4 !important; color: #080D18 !important;
    border: none !important; border-radius: 6px !important; font-weight: 600 !important;
}
label, h1, h2, h3, h4, p { color: #E2E8F0 !important; }
[class*="selected"], [class*="active"] {
    background: #06B6D4 !important; color: #080D18 !important;
}
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #080D18; }
::-webkit-scrollbar-thumb { background: #1E2D45; border-radius: 3px; }
"""

PORTAL_CSS = """
html, body {
    background: #080D18 !important; color: #E2E8F0 !important;
    margin: 0 !important; padding: 0 !important;
    font-family: 'Trebuchet MS', 'Segoe UI', sans-serif !important;
}
nav, header, footer,
[class*="nav"], [class*="site-header"], [class*="site-footer"],
[class*="branding"], [class*="cookie"] { display: none !important; }
input, select, textarea {
    background: #161F30 !important; border: 1px solid #1E2D45 !important;
    color: #E2E8F0 !important; border-radius: 6px !important; padding: 8px 12px !important;
}
input::placeholder { color: #4A6080 !important; }
label, h1, h2, h3, p { color: #E2E8F0 !important; }
[class*="btn-primary"], button[type="submit"] {
    background: #06B6D4 !important; color: #080D18 !important;
    border: none !important; border-radius: 6px !important; font-weight: 600 !important;
}
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #080D18; }
::-webkit-scrollbar-thumb { background: #1E2D45; border-radius: 3px; }
"""

css   = BOOKING_CSS if mode == "booking" else PORTAL_CSS
title = ("Book Appointment — GTC Student Services" if mode == "booking"
         else "My Appointments — GTC Portal")

window = webview.create_window(
    title, url,
    width=1060, height=900,
    background_color="#080D18",
    min_size=(640, 520),
)

webview.start(
    lambda w: w.load_css(css),
    window,
    private_mode=False,
    storage_path=profile,
)
