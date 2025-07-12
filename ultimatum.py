import cv2
import numpy as np
import pyautogui
import time
import threading
import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime
import os

# Şablon görselin dosya adı
TEMPLATE_PATH = 'accept_trial.png'
TAKE_REWARDS_TEMPLATE_PATH = 'take_rewards.png'

# Threshold değeri
ACCEPT_TRIAL_THRESHOLD = 0.75

try:
    template = cv2.imread(TEMPLATE_PATH, cv2.IMREAD_GRAYSCALE)
    w, h = template.shape[::-1]
except Exception as e:
    template = None
    w, h = 0, 0

LOG_FILE = 'log.txt'
auto_clicking = False
click_count = 0

def find_take_rewards_button():
    template = cv2.imread(TAKE_REWARDS_TEMPLATE_PATH, cv2.IMREAD_GRAYSCALE)
    if template is None:
        return None
    tw, th = template.shape[::-1]
    screenshot = pyautogui.screenshot()
    screenshot_gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
    res = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        return pt[0] + tw // 2, pt[1] + th // 2  # Butonun ortası
    return None

def log_message(msg):
    log_entry = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {msg}"
    log_text.config(state='normal')
    log_text.insert(tk.END, log_entry + '\n')
    log_text.see(tk.END)
    log_text.config(state='disabled')
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_entry + '\n')

def clear_logs():
    log_text.config(state='normal')
    log_text.delete(1.0, tk.END)
    log_text.config(state='disabled')
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        f.write('')
    log_message('Loglar temizlendi.')

def find_and_click_accept_trial():
    if template is None:
        #log_message("accept_trial.png bulunamadı veya okunamadı!")
        return False
    screenshot = pyautogui.screenshot()
    screenshot_gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
    res = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= ACCEPT_TRIAL_THRESHOLD)
    for pt in zip(*loc[::-1]):
        try:
            x, y = pt[0] + w // 2, pt[1] + h // 2
            pyautogui.moveTo(x, y, duration=0.1)
            for _ in range(3):
                pyautogui.click()
                time.sleep(0.08)
            for _ in range(20):
                time.sleep(0.5)
                screenshot2 = pyautogui.screenshot()
                screenshot2_gray = cv2.cvtColor(np.array(screenshot2), cv2.COLOR_RGB2GRAY)
                res2 = cv2.matchTemplate(screenshot2_gray, template, cv2.TM_CCOEFF_NORMED)
                if not np.any(res2 >= ACCEPT_TRIAL_THRESHOLD):
                    return True
            return False
        except Exception as e:
            log_message(f"Tıklama hatası: {e}")
            return False
    return False

def auto_click():
    global auto_clicking, click_count
    while auto_clicking:
        clicked = find_and_click_accept_trial()
        if clicked:
            click_count += 1
            #log_message(f"Accept Trial butonuna tıklandı! Toplam tıklama: {click_count}")
            click_label.config(text=f"Tıklama Sayısı: {click_count}")
        time.sleep(0.5)

def start_clicking():
    global auto_clicking
    if not auto_clicking:
        auto_clicking = True
        log_message("Otomasyon başlatıldı.")
        threading.Thread(target=auto_click, daemon=True).start()

def stop_clicking():
    global auto_clicking
    auto_clicking = False
    log_message("Otomasyon durduruldu.")

# Tkinter UI
root = tk.Tk()
root.title("Ultimatum Otomasyon")
root.geometry("500x400")

start_btn = tk.Button(root, text="Başlat", command=start_clicking, bg='green', fg='white', font=('Arial', 12, 'bold'))
start_btn.pack(pady=10)

stop_btn = tk.Button(root, text="Durdur", command=stop_clicking, bg='red', fg='white', font=('Arial', 12, 'bold'))
stop_btn.pack(pady=5)

clear_log_btn = tk.Button(root, text="Logları Temizle", command=clear_logs, bg='gray', fg='white', font=('Arial', 11))
clear_log_btn.pack(pady=5)

click_label = tk.Label(root, text="Tıklama Sayısı: 0", font=('Arial', 12))
click_label.pack(pady=5)

log_text = scrolledtext.ScrolledText(root, width=60, height=15, state='disabled', font=('Consolas', 10))
log_text.pack(pady=10)

root.mainloop()
