import customtkinter as ctk
from tkinter import messagebox

# Set the visual theme
ctk.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class BookingAppUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Window Configuration ---
        self.title("Service Scheduler Pro")
        self.geometry("1100x650")

        # --- Layout Grid ---
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Sidebar Frame ---
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="RESERVE IT", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.btn_dashboard = ctk.CTkButton(self.sidebar_frame, text="Booking Home", command=self.nav_home)
        self.btn_dashboard.grid(row=1, column=0, padx=20, pady=10)

        self.btn_history = ctk.CTkButton(self.sidebar_frame, text="My Appointments", command=self.nav_history)
        self.btn_history.grid(row=2, column=0, padx=20, pady=10)

        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 20))

        # --- Header Frame ---
        self.header_frame = ctk.CTkFrame(self, height=60, corner_radius=0, fg_color="transparent")
        self.header_frame.grid(row=0, column=1, sticky="new", padx=20, pady=10)
        
        self.search_bar = ctk.CTkEntry(self.header_frame, placeholder_text="Search services...", width=400)
        self.search_bar.pack(side="left", padx=10)

        self.user_profile = ctk.CTkLabel(self.header_frame, text="Guest User 👤")
        self.user_profile.pack(side="right", padx=20)

        # --- Main Content Area (Where the Web Wrapper or Logic goes) ---
        self.main_view = ctk.CTkFrame(self, corner_radius=15)
        self.main_view.grid(row=0, column=1, sticky="nsew", padx=(20, 20), pady=(80, 20))
        
        self.welcome_label = ctk.CTkLabel(self.main_view, text="Ready to book?", font=ctk.CTkFont(size=24))
        self.welcome_label.pack(pady=40)

        self.action_btn = ctk.CTkButton(self.main_view, text="Launch 10to8 Booking Window", 
                                        height=50, width=250, font=ctk.CTkFont(size=16),
                                        command=self.launch_booking_logic)
        self.action_btn.pack(pady=20)

        self.info_text = ctk.CTkLabel(self.main_view, text="This will open a secure, direct connection to the scheduling server.", 
                                      font=ctk.CTkFont(size=12), text_color="gray")
        self.info_text.pack(pady=10)

    # --- UI Logic Methods ---
    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def nav_home(self):
        print("Navigating to Home...")

    def nav_history(self):
        messagebox.showinfo("History", "Appointment history feature coming soon!")

    def launch_booking_logic(self):
        # This is where your back-end script/logic hooks in
        print("Triggering external web view for: https://app.10to8.com/booking/5bf4ba81-9fd4-48f4-9cf9-3d4106e4a75f/")
        # Call your function here

if __name__ == "__main__":
    app = BookingAppUI()
    app.mainloop()