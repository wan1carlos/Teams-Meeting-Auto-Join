import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry  # Install with 'pip install tkcalendar'
from tkinter import ttk
import datetime
import threading
import schedule
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os

# Path to Chromedriver - update this with your path
chromedriver_path = "PATH TO CHROMEDRIVER"

# Function to join Teams meeting
def join_teams_meeting(teams_link):
    try:
        
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        # Initialize Chrome driver
        service = Service(chromedriver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(teams_link)

        # Add code to sign in if prompted or you may add an existing chrome profile for better experience
        # This part assumes manual login since we are not using a saved profile

        # Click "Join meeting from this browser" button
        join_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn.primary[data-tid="joinOnWeb"]'))
        )
        join_button.click()

        # Toggle microphone if it's on
        mic_toggle = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-tid="toggle-mute"]'))
        )
        if mic_toggle.get_attribute("aria-checked") == "true":
            mic_toggle.click()

        # Click "Join now" button
        join_now_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "prejoin-join-button"))
        )
        join_now_button.click()

        # Keep the driver instance open until manually closed by the user
        print("Meeting joined.")
        while True:  # Keeps the program running, allowing user to interact with Chrome
            time.sleep(1)

    except Exception as e:
        print("An error occurred:", e)

# Schedule function to run at specified time
def schedule_meeting(teams_link, schedule_datetime):
    def job():
        join_teams_meeting(teams_link)

    schedule.clear()  # Clear any previous schedules
    schedule.every().day.at(schedule_datetime.strftime("%H:%M")).do(job)

    # Start a background thread to check the schedule
    def run_schedule():
        while True:
            schedule.run_pending()
            time.sleep(1)

    threading.Thread(target=run_schedule, daemon=True).start()

# GUI Setup
def start_gui():
    def submit():
        teams_link = entry_link.get()
        schedule_date = calendar.get_date()
        schedule_hour = hour_combobox.get()
        schedule_minute = minute_combobox.get()
        am_pm = am_pm_combobox.get()

        # Validate inputs
        if not teams_link:
            messagebox.showerror("Input Error", "Please enter a Teams link.")
            return
        if not schedule_hour or not schedule_minute or am_pm == "Select":
            messagebox.showerror("Input Error", "Please select hour, minute, and AM/PM.")
            return

        # Convert hour to 24-hour format if PM is selected
        if am_pm == "PM" and schedule_hour != "12":
            schedule_hour = str(int(schedule_hour) + 12)
        elif am_pm == "AM" and schedule_hour == "12":
            schedule_hour = "00"

        # Combine date and time into a single datetime object
        schedule_time_str = f"{schedule_hour}:{schedule_minute}"
        schedule_datetime = datetime.datetime.combine(schedule_date, datetime.datetime.strptime(schedule_time_str, "%H:%M").time())

        # Schedule the meeting
        schedule_meeting(teams_link, schedule_datetime)
        messagebox.showinfo("Meeting Scheduled", f"Meeting scheduled on {schedule_datetime.strftime('%Y-%m-%d at %I:%M %p')}.")

    # Create the main window
    window = tk.Tk()
    window.title("Teams Meeting Scheduler")
    window.geometry("400x500")
    window.configure(bg="#2E3440")

    # Title Label
    lbl_title = tk.Label(window, text="Teams Meeting Scheduler", font=("Arial", 16, "bold"), bg="#2E3440", fg="#D8DEE9")
    lbl_title.pack(pady=10)

    # Teams Link Label and Entry
    lbl_link = tk.Label(window, text="Teams Meeting Link:", font=("Arial", 12), bg="#2E3440", fg="#D8DEE9")
    lbl_link.pack(pady=5)
    entry_link = tk.Entry(window, width=40, font=("Arial", 12))
    entry_link.pack(pady=5)

    # Schedule Date Label and DateEntry
    lbl_date = tk.Label(window, text="Schedule Date:", font=("Arial", 12), bg="#2E3440", fg="#D8DEE9")
    lbl_date.pack(pady=5)
    calendar = DateEntry(window, width=16, font=("Arial", 12), background="#5E81AC", foreground="#D8DEE9", borderwidth=2)
    calendar.pack(pady=5)

    # Schedule Time Label
    lbl_time = tk.Label(window, text="Schedule Time:", font=("Arial", 12), bg="#2E3440", fg="#D8DEE9")
    lbl_time.pack(pady=5)

    # Hour Combobox
    lbl_hour = tk.Label(window, text="Hour:", font=("Arial", 10), bg="#2E3440", fg="#D8DEE9")
    lbl_hour.pack(pady=2)
    hour_combobox = ttk.Combobox(window, width=5, font=("Arial", 12), values=[f"{h}" for h in range(1, 13)])  # 1 to 12 for 12-hour format
    hour_combobox.pack(pady=2)
    hour_combobox.set("12")  # Default hour

    # Minute Combobox
    lbl_minute = tk.Label(window, text="Minute:", font=("Arial", 10), bg="#2E3440", fg="#D8DEE9")
    lbl_minute.pack(pady=2)
    minute_combobox = ttk.Combobox(window, width=5, font=("Arial", 12), values=[f"{m:02d}" for m in range(0, 60)])  # 0 to 59
    minute_combobox.pack(pady=2)
    minute_combobox.set("00")  # Default minute

    # AM/PM Combobox
    lbl_am_pm = tk.Label(window, text="AM/PM:", font=("Arial", 10), bg="#2E3440", fg="#D8DEE9")
    lbl_am_pm.pack(pady=2)
    am_pm_combobox = ttk.Combobox(window, width=5, font=("Arial", 12), values=["AM", "PM"])
    am_pm_combobox.pack(pady=2)
    am_pm_combobox.set("AM")  # Default AM

    # Submit Button
    btn_submit = tk.Button(window, text="Schedule Meeting", font=("Arial", 12, "bold"), bg="#5E81AC", fg="#ECEFF4", command=submit)
    btn_submit.pack(pady=20)

    # Run the GUI loop
    window.mainloop()

# Run the GUI application
start_gui()
