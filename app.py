import customtkinter as ctk
import webbrowser
from engine import BookingEngine

# ── Theme ──────────────────────────────────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

BG       = "#080D18"
PANEL    = "#0F1724"
CARD     = "#161F30"
BORDER   = "#1E2D45"
ACCENT   = "#06B6D4"       # cyan
ACCENT2  = "#F59E0B"       # amber
TEXT     = "#E2E8F0"
MUTED    = "#4A6080"
SUCCESS  = "#10B981"
WARN     = "#F59E0B"

class Divider(ctk.CTkFrame):
    def __init__(self, parent, **kw):
        super().__init__(parent, height=1, fg_color=BORDER, **kw)


class StatusBar(ctk.CTkFrame):
    """Tiny coloured dot + label at the bottom of the sidebar."""

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self._dot   = ctk.CTkLabel(self, text="●", font=ctk.CTkFont(size=9))
        self._label = ctk.CTkLabel(self, text="Ready", font=FONT_SMALL, text_color=MUTED)
        self._dot.pack(side="left", padx=(0, 5))
        self._label.pack(side="left")
        self.set("Ready", SUCCESS)

    def set(self, msg: str, color: str = SUCCESS):
        self._dot.configure(text_color=color)
        self._label.configure(text=msg)


class NavButton(ctk.CTkButton):
    def __init__(self, parent, **kw):
        defaults = dict(
            anchor="w", height=40, corner_radius=6,
            fg_color="transparent", hover_color=BORDER,
            text_color=TEXT, font=FONT_BODY,
        )
        defaults.update(kw)
        super().__init__(parent, **defaults)


class BookingApp(ctk.CTk):

    def __init__(self):
        super().__init__()
        global FONT_HEAD, FONT_TITLE, FONT_BODY, FONT_SMALL, FONT_LOGO, FONT_MONO
        FONT_HEAD  = ctk.CTkFont("Trebuchet MS", 26, "bold")
        FONT_TITLE = ctk.CTkFont("Trebuchet MS", 15, "bold")
        FONT_BODY  = ctk.CTkFont("Trebuchet MS", 12)
        FONT_SMALL = ctk.CTkFont("Trebuchet MS", 11)
        FONT_LOGO  = ctk.CTkFont("Trebuchet MS", 17, "bold")
        FONT_MONO  = ctk.CTkFont("Courier New",  11)

        self.engine     = BookingEngine()
        self._win_open  = False        # guard against double-open

        self.title("GTC Student Services Scheduler")
        self.geometry("1080x660")
        self.minsize(820, 500)
        self.configure(fg_color=BG)

        self._build_sidebar()
        self._build_main()
        self.show_home()

    # ── Sidebar ────────────────────────────────────────────────────────────────

    def _build_sidebar(self):
        sb = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color=PANEL)
        sb.pack(side="left", fill="y")
        sb.pack_propagate(False)

        # Logo block
        logo_box = ctk.CTkFrame(sb, fg_color="transparent")
        logo_box.pack(fill="x", padx=18, pady=(28, 8))

        # Accent stripe
        stripe = ctk.CTkFrame(logo_box, width=3, height=42, corner_radius=2, fg_color=ACCENT)
        stripe.pack(side="left", padx=(0, 12))

        txt_block = ctk.CTkFrame(logo_box, fg_color="transparent")
        txt_block.pack(side="left")
        ctk.CTkLabel(txt_block, text="GTC SCHEDULER", font=FONT_LOGO, text_color=TEXT).pack(anchor="w")
        ctk.CTkLabel(txt_block, text="Student Services Portal", font=FONT_SMALL, text_color=MUTED).pack(anchor="w")

        Divider(sb).pack(fill="x", padx=14, pady=14)

        # Navigation
        nav = ctk.CTkFrame(sb, fg_color="transparent")
        nav.pack(fill="x", padx=10)

        self._nav_btns = {}
        items = [
            ("home",    "🏠  Home",               self.show_home),
            ("book",    "📆  Book Appointment",    self._open_booking),
            ("portal",  "📋  My Appointments",     self._open_portal),
            ("contact", "📞  Contact",             self.show_contact),
            ("about",   "ℹ️   About",               self.show_about),
        ]
        for key, label, cmd in items:
            b = NavButton(nav, text=label, command=cmd)
            b.pack(fill="x", pady=2)
            self._nav_btns[key] = b

        # Status bar pinned to bottom
        Divider(sb).pack(fill="x", padx=14, pady=14, side="bottom")
        self.status = StatusBar(sb)
        self.status.pack(side="bottom", padx=18, pady=(0, 14))

    def _set_active(self, key: str):
        for k, b in self._nav_btns.items():
            b.configure(fg_color=BORDER if k == key else "transparent")

    # ── Main frame ─────────────────────────────────────────────────────────────

    def _build_main(self):
        self.main = ctk.CTkScrollableFrame(self, fg_color=BG, corner_radius=0)
        self.main.pack(side="right", expand=True, fill="both")

    def _clear(self):
        for w in self.main.winfo_children():
            w.destroy()

    def _header(self, title: str, subtitle: str = ""):
        box = ctk.CTkFrame(self.main, fg_color="transparent")
        box.pack(fill="x", padx=30, pady=(28, 6))

        # Accent line
        ctk.CTkFrame(box, width=32, height=3, corner_radius=2, fg_color=ACCENT).pack(anchor="w")
        ctk.CTkLabel(box, text=title, font=FONT_HEAD, text_color=TEXT).pack(anchor="w", pady=(6, 0))
        if subtitle:
            ctk.CTkLabel(box, text=subtitle, font=FONT_BODY, text_color=MUTED).pack(anchor="w")

    def _card(self, parent=None, **kw) -> ctk.CTkFrame:
        p = parent or self.main
        defaults = dict(fg_color=CARD, corner_radius=10, border_width=1, border_color=BORDER)
        defaults.update(kw)
        return ctk.CTkFrame(p, **defaults)

    # ── Views ──────────────────────────────────────────────────────────────────

    def show_home(self):
        self._clear()
        self._set_active("home")
        self._header("Welcome Back", "Gateway Technical College — Student Services")

        # Quick-action cards
        cards_row = ctk.CTkFrame(self.main, fg_color="transparent")
        cards_row.pack(fill="x", padx=30, pady=(10, 6))
        cards_row.columnconfigure((0, 1, 2), weight=1, uniform="col")

        cards = [
            (0, "📆", "Book Appointment",
             "Schedule a virtual advising\nsession via Zoom",
             ACCENT, self._open_booking),
            (1, "📋", "My Appointments",
             "View or cancel your\nexisting bookings",
             "#8B5CF6", self._open_portal),
            (2, "📞", "Contact Us",
             "1-800-247-7122\nsscontactcenter@gtc.edu",
             ACCENT2, self.show_contact),
        ]
        for col, icon, title, desc, color, cmd in cards:
            c = ctk.CTkFrame(cards_row, fg_color=CARD, corner_radius=10,
                             border_width=1, border_color=BORDER)
            c.grid(row=0, column=col, sticky="nsew", padx=5, pady=4)

            inner = ctk.CTkFrame(c, fg_color="transparent")
            inner.pack(padx=18, pady=18, fill="both", expand=True)

            # colour top-bar
            ctk.CTkFrame(inner, height=3, corner_radius=2, fg_color=color).pack(fill="x", pady=(0, 12))
            ctk.CTkLabel(inner, text=icon, font=ctk.CTkFont(size=26)).pack(anchor="w")
            ctk.CTkLabel(inner, text=title, font=FONT_TITLE, text_color=TEXT).pack(anchor="w", pady=(6, 2))
            ctk.CTkLabel(inner, text=desc, font=FONT_SMALL, text_color=MUTED,
                         justify="left").pack(anchor="w")
            ctk.CTkButton(inner, text="Open →", height=30, corner_radius=6,
                          fg_color=color, hover_color=color,
                          font=FONT_SMALL, command=cmd).pack(anchor="w", pady=(14, 0))

        # Info card
        info = self._card()
        info.pack(fill="x", padx=30, pady=8)

        info_inner = ctk.CTkFrame(info, fg_color="transparent")
        info_inner.pack(padx=20, pady=16, fill="x")

        ctk.CTkLabel(info_inner, text="About These Appointments",
                     font=FONT_TITLE, text_color=TEXT).pack(anchor="w")
        ctk.CTkLabel(info_inner,
                     text="Virtual Zoom sessions for students applying to academic programs at Gateway Technical College.\n"
                          "Learn about admission requirements, available support services, complete your application, and more.\n"
                          "A computer with a reliable internet connection is recommended for all Zoom appointments.",
                     font=FONT_BODY, text_color=MUTED,
                     wraplength=680, justify="left").pack(anchor="w", pady=(6, 0))

        # Cancellation note
        note = self._card()
        note.pack(fill="x", padx=30, pady=(4, 20))
        n_inner = ctk.CTkFrame(note, fg_color="transparent")
        n_inner.pack(padx=20, pady=12, fill="x")
        ctk.CTkLabel(n_inner, text="⚠  Cancellation Policy", font=FONT_TITLE, text_color=WARN).pack(anchor="w")
        ctk.CTkLabel(n_inner,
                     text="If you need to cancel, call 1-800-247-7122 immediately or use the cancel link "
                          "in your confirmation email.",
                     font=FONT_BODY, text_color=MUTED, wraplength=680, justify="left").pack(anchor="w", pady=(4, 0))

    def show_contact(self):
        self._clear()
        self._set_active("contact")
        self._header("Contact Student Services")

        card = self._card()
        card.pack(fill="x", padx=30, pady=16)
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(padx=24, pady=20, fill="x")

        rows = [
            ("📞  Phone",   "1-800-247-7122"),
            ("✉️  Email",   "sscontactcenter@gtc.edu"),
            ("🌐  Website", "gtc.edu"),
        ]
        for label, value in rows:
            row = ctk.CTkFrame(inner, fg_color="transparent")
            row.pack(fill="x", pady=6)
            ctk.CTkLabel(row, text=label, font=FONT_TITLE, width=130, anchor="w").pack(side="left")
            ctk.CTkLabel(row, text=value, font=FONT_MONO, text_color=ACCENT).pack(side="left")

        Divider(inner).pack(fill="x", pady=14)

        ctk.CTkButton(inner, text="Open Booking Page in Browser",
                      fg_color="transparent", border_width=1, border_color=BORDER,
                      font=FONT_BODY, text_color=TEXT,
                      command=lambda: webbrowser.open(
                          "https://app.10to8.com/booking/5bf4ba81-9fd4-48f4-9cf9-3d4106e4a75f/"
                      )).pack(anchor="w", pady=(0, 4))

        ctk.CTkButton(inner, text="View Terms & Conditions",
                      fg_color="transparent", border_width=1, border_color=BORDER,
                      font=FONT_BODY, text_color=TEXT,
                      command=lambda: webbrowser.open("https://signinapp.com/legal/")).pack(anchor="w")

    def show_about(self):
        self._clear()
        self._set_active("about")
        self._header("About")

        card = self._card()
        card.pack(fill="x", padx=30, pady=16)
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(padx=24, pady=24, fill="x")

        ctk.CTkLabel(inner, text="GTC Student Services Scheduler",
                     font=FONT_TITLE, text_color=TEXT).pack(anchor="w")
        ctk.CTkLabel(inner,
                     text="A clean-room wrapper around the Gateway Technical College 10to8 booking portal.\n"
                          "Strips all the unnecessary chrome and branding from the original page so you "
                          "can focus on what matters: booking your appointment.",
                     font=FONT_BODY, text_color=MUTED, wraplength=680, justify="left").pack(anchor="w", pady=(8, 0))

        Divider(inner).pack(fill="x", pady=14)
        ctk.CTkLabel(inner, text="Built with  CustomTkinter  +  pywebview",
                     font=FONT_MONO, text_color=MUTED).pack(anchor="w")

    # ── Webview launchers ─────────────────────────────────────────────────────

    def _open_booking(self):
        if self._win_open:
            self.status.set("Window already open", WARN)
            return
        self._win_open = True
        self.status.set("Booking window open", SUCCESS)
        self._nav_btns["book"].configure(fg_color=BORDER)

        def on_close():
            self._win_open = False
            self.status.set("Ready", SUCCESS)
            self._nav_btns["book"].configure(fg_color="transparent")

        self.engine.launch(on_close_cb=on_close)

    def _open_portal(self):
        if self._win_open:
            self.status.set("Window already open", WARN)
            return
        self._win_open = True
        self.status.set("Portal open", SUCCESS)
        self._nav_btns["portal"].configure(fg_color=BORDER)

        def on_close():
            self._win_open = False
            self.status.set("Ready", SUCCESS)
            self._nav_btns["portal"].configure(fg_color="transparent")

        self.engine.launch_portal(on_close_cb=on_close)


if __name__ == "__main__":
    app = BookingApp()
    app.mainloop()
