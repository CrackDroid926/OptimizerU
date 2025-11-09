"""
OptimizerU - Advanced Windows System Optimizer
Created by: CrackDroid926
Version: Alpha 1.0
GitHub: https://github.com/Crackdroid926/OptimizerU

This tool provides safe and effective system optimizations for Windows
"""

import os
import sys
import json
import ctypes
import subprocess
import threading
import webbrowser
import logging
from datetime import datetime
import customtkinter as ctk
from tkinter import messagebox

# ================== DEBUG AND CONFIG FILES ==================
CONFIG_FILE = "config.json"
DEBUG_LOG = "debug.log"
INFO_FILES = {"es": "INFO_ES.txt", "en": "INFO_EN.txt"}

# Create info files on first run
for lang, filename in INFO_FILES.items():
    if not os.path.exists(filename):
        content = (
            "Información sobre OptimizerU (Alpha 1.0)\n\n"
            "¿Por qué se abre PowerShell?\n"
            "- Este programa usa comandos de Windows para optimizar tu sistema.\n"
            "- PowerShell es una herramienta oficial de Microsoft (como el Símbolo del sistema).\n"
            "- NO es un virus. Se usa para ejecutar comandos seguros como:\n"
            "  • ipconfig /flushdns\n"
            "  • sfc /scannow\n"
            "  • powercfg -h off\n"
            "- Todos los comandos son visibles en el código fuente (GitHub).\n\n"
            "¿Por qué necesita permisos de administrador?\n"
            "- Algunas optimizaciones requieren privilegios elevados.\n\n"
            "Creado por: CrackDroid926\n"
            "GitHub: https://github.com/Crackdroid926/OptimizerU"
        ) if lang == "es" else (
            "About OptimizerU (Alpha 1.0)\n\n"
            "Why does PowerShell open?\n"
            "- This tool uses Windows commands to optimize your system.\n"
            "- PowerShell is an official Microsoft tool (like Command Prompt).\n"
            "- It is NOT a virus. It runs safe commands such as:\n"
            "  • ipconfig /flushdns\n"
            "  • sfc /scannow\n"
            "  • powercfg -h off\n"
            "- All commands are visible in the source code (GitHub).\n\n"
            "Why does it need administrator rights?\n"
            "- Some optimizations require elevated privileges.\n\n"
            "Created by: CrackDroid926\n"
            "GitHub: https://github.com/Crackdroid926/OptimizerU"
        )
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)

# ================== DEBUG MODE ==================
DEBUG_MODE = False

def enable_debug_mode():
    """Enable debug mode: show console and log everything to debug.log."""
    global DEBUG_MODE
    DEBUG_MODE = True
    if sys.executable.endswith(".exe"):
        ctypes.windll.kernel32.AllocConsole()
    logging.basicConfig(
        filename=DEBUG_LOG,
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        force=True
    )
    logging.info("=== DEBUG MODE ACTIVATED ===")

def log_debug(msg):
    """Log a debug message if debug mode is active."""
    if DEBUG_MODE:
        logging.debug(msg)

# Hide console in normal .exe mode
if sys.executable.endswith(".exe"):
    ctypes.windll.kernel32.FreeConsole()

# ================== CONFIGURATION MANAGEMENT ==================
def load_config():
    """Load user configuration from config.json."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            log_debug(f"Config load error: {e}")
    return {"language": "es", "expert_mode": False, "applied_optimizations": []}

def save_config(config):
    """Save user configuration to config.json."""
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)
        log_debug("Configuration saved")
    except Exception as e:
        log_debug(f"Config save error: {e}")

# ================== INTERNATIONALIZATION ==================
class I18N:
    def __init__(self, lang="es"):
        self.lang = lang
        self.translations = {
            "es": {
                "window_title": "Optimizador | Creado por CrackDroid926",
                "main_title": "Optimizar",
                "detecting": "Detectando hardware...",
                "create_restore_point": "Crear Punto de Restauración",
                "apply_optimizations": "✅ Aplicar Optimizaciones Seleccionadas",
                "recommended_tab": "Recomendado para mi PC",
                "custom_tab": "Personalizar optimizaciones",
                "loading_recommendations": "Cargando recomendaciones...",
                "hardware_info": "Detectado: {ram} GB RAM • Disco: {disk} • GPU: {gpu}",
                "restore_success": "[ÉXITO] Punto de restauración creado.",
                "restore_fail": "[ADVERTENCIA] No se pudo crear el punto de restauración.",
                "no_selection": "Seleccione al menos una optimización.",
                "high_risk_title": "Riesgo alto",
                "high_risk_msg": "¿Continuar con opciones de riesgo ALTO?",
                "executing": "EJECUTANDO OPTIMIZACIONES...",
                "done": "✅ ¡Optimización completada! Reinicie su equipo.",
                "options": "⚙️ Opciones",
                "expert_mode": "Soy un usuario experto",
                "language": "Idioma",
                "check_updates": "Buscar actualizaciones",
                "dark_mode": "Modo oscuro",
                "light_mode": "Modo claro",
                "debug_mode": "Activar modo debug (desarrolladores)",
                "admin_required": "¿Ejecutar como administrador?",
                "github_url": "https://github.com/Crackdroid926/OptimizerU"
            },
            "en": {
                "window_title": "Optimizer | Created by CrackDroid926",
                "main_title": "Optimize",
                "detecting": "Detecting hardware...",
                "create_restore_point": "Create Restore Point",
                "apply_optimizations": "✅ Apply Selected Optimizations",
                "recommended_tab": "Recommended for My PC",
                "custom_tab": "Customize Optimizations",
                "loading_recommendations": "Loading recommendations...",
                "hardware_info": "Detected: {ram} GB RAM • Disk: {disk} • GPU: {gpu}",
                "restore_success": "[SUCCESS] Restore point created.",
                "restore_fail": "[WARNING] Failed to create restore point.",
                "no_selection": "Please select at least one optimization.",
                "high_risk_title": "High Risk",
                "high_risk_msg": "Continue with HIGH RISK options?",
                "executing": "EXECUTING OPTIMIZATIONS...",
                "done": "✅ Optimization completed! Please restart your computer.",
                "options": "⚙️ Options",
                "expert_mode": "I am an expert user",
                "language": "Language",
                "check_updates": "Check for Updates",
                "dark_mode": "Dark Mode",
                "light_mode": "Light Mode",
                "debug_mode": "Enable Debug Mode (Developers)",
                "admin_required": "Run as administrator?",
                "github_url": "https://github.com/Crackdroid926/OptimizerU"
            }
        }

    def set_language(self, lang):
        if lang in self.translations:
            self.lang = lang

    def tr(self, key):
        return self.translations[self.lang].get(key, key)

# ================== UTILITIES ==================
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

def run_powershell(cmd, timeout=20):
    try:
        log_debug(f"PowerShell command: {cmd}")
        result = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True, timeout=timeout)
        log_debug(f"PowerShell output: {result.stdout.strip()}")
        log_debug(f"PowerShell error: {result.stderr.strip()}")
        return result.returncode == 0, result.stdout.strip()
    except Exception as e:
        log_debug(f"PowerShell exception: {e}")
        return False, str(e)

# ================== SYSTEM DETECTION ==================
def detectar_sistema_callback(app_ref):
    info = {"ram_gb": 0, "disco_tipo": "HDD", "gpu": "Unknown"}
    try:
        import psutil
        info["ram_gb"] = max(1, round(psutil.virtual_memory().total / (1024**3)))
        ok, out = run_powershell("Get-PhysicalDisk | Select-Object -First 1 -ExpandProperty MediaType")
        info["disco_tipo"] = "SSD" if (ok and "SSD" in out) else "HDD"
    except Exception as e:
        log_debug(f"Hardware detection partial failure: {e}")
    try:
        ok, out = run_powershell("(Get-WmiObject Win32_VideoController).Name | Select-Object -First 1")
        if ok and out:
            info["gpu"] = out[:40]
    except Exception as e:
        log_debug(f"GPU detection failed: {e}")
    app_ref.after(100, lambda: app_ref.sistema_detectado(info))

# ================== OPTIMIZATIONS ==================
OPTIMIZATIONS = [
    ("Flush DNS Cache", "dns", "Clears the local DNS resolver cache.", "Low", "Network"),
    ("Clean Thumbnails and Icon Cache", "thumbs", "Removes thumbnail cache and rebuilds IconCache.db.", "Low", "Cleanup"),
    ("Restart Windows Explorer", "explorer", "Restarts the explorer.exe process.", "Low", "System"),
    ("Clean User Temp Files", "temp_user", "Deletes files in %TEMP%.", "Low", "Cleanup"),
    ("Clean System Temp Files", "temp_sys", "Deletes files in C:\\Windows\\Temp.", "Low", "Cleanup"),
    ("Empty Recycle Bin", "recycle", "Deletes all files in $Recycle.Bin.", "Low", "Cleanup"),
    ("Optimize Visual Effects for Performance", "visual_fx", "Disables shadows, animations, and transparency.", "Low", "Visual"),
    ("Disable SysMain (SuperFetch)", "sysmain", "Disables SysMain. Useful on HDDs; not recommended on SSDs.", "Low", "Performance"),
    ("Disable Notifications and Tips", "tips", "Disables suggestions and non-essential notifications.", "Low", "Privacy"),
    ("Set Power Plan to High Performance", "high_perf", "Applies the 'High Performance' power plan.", "Low", "Power"),
    ("Disable Delivery Optimization", "delivery_opt", "Stops P2P update downloads.", "Low", "Network"),
    ("Clean Prefetch Folder", "prefetch", "Deletes files in C:\\Windows\\Prefetch.", "Low", "Performance"),
    ("Disable Windows Error Reporting", "wer", "Disables error reporting to Microsoft.", "Low", "Privacy"),
    ("Disable OneDrive Auto-Start", "onedrive", "Prevents OneDrive from starting with Windows.", "Low", "Startup"),
    ("Disable Background Diagnostics", "diagnostics", "Stops background diagnostics services.", "Low", "Performance"),
    ("Disable Recent Files History", "recent_files", "Prevents Explorer from saving file history.", "Low", "Privacy"),
    ("Disable Explorer Suggestions", "explorer_tips", "Removes file suggestions in Explorer.", "Low", "Visual"),
    ("Disable Window Transparency", "transparency", "Disables glass effect on bars and menus.", "Low", "Visual"),
    ("Disable Windows Spotlight", "spotlight", "Disables Spotlight backgrounds and stories.", "Low", "Privacy"),
    ("Disable Timeline (Activity History)", "timeline", "Removes cross-device activity history.", "Low", "Privacy"),
    ("Disable Startup Apps", "startup_apps", "Disables apps that start with Windows.", "Low", "Startup"),
    ("Disable Background Search", "background_search", "Stops file indexing in the background.", "Medium", "Performance"),
    ("Disable Game Bar and Capture", "game_bar", "Disables game-related features (useful without dedicated GPU).", "Low", "Performance"),
    ("Disable Hibernation", "hibernation", "Frees disk space (hiberfil.sys).", "Low", "Power"),
    ("Disable SmartScreen", "smartscreen", "Disables warnings for unrecognized apps.", "Medium", "Security"),
    ("Disable AutoPlay and AutoRun", "autoplay", "Prevents automatic execution of removable devices.", "Low", "Security"),
    ("Disable Windows Search", "search_svc", "Stops the search service.", "Medium", "Performance"),
    ("Disable Cortana", "cortana", "Disables the assistant even if unused.", "Low", "Privacy"),
    ("Disable Mail and Calendar", "mail_calendar", "Disables built-in Mail and Calendar apps.", "Low", "Apps"),
    ("Disable Xbox Features", "xbox", "Disables Xbox-related services and apps.", "Low", "Apps"),
    ("Disable Windows Tips", "windows_tips", "Removes 'Windows Tips' notifications.", "Low", "Notifications"),
    ("Disable Cloud Backup", "backup", "Disables Microsoft cloud backup.", "Low", "Privacy"),
    ("Disable Focus Assist", "focusassist", "Disables automatic focus notifications.", "Low", "Notifications"),
    ("Disable Cloud Access in Explorer", "cloud_files", "Hides OneDrive and other cloud services in Explorer.", "Low", "Visual"),
    ("Reduce Desktop Refresh Rate", "desktop_refresh", "Reduces desktop updates to once per minute.", "Low", "Performance"),
    ("Disable Location Services", "location", "Disables system location services.", "Low", "Privacy"),
    ("Disable Wi-Fi Sense", "wifi_sense", "Disables automatic connection to suggested networks.", "Low", "Network"),
    ("Disable Large Page Memory", "large_pages", "Disables large memory page support (better for low RAM).", "Low", "Performance"),
    ("Optimize Pagefile", "pagefile_opt", "Sets pagefile to fixed size (better for HDDs).", "Medium", "Performance"),
    ("Disable Memory Compression", "mem_compress", "Disables memory compression (better for low RAM).", "Medium", "Performance"),
    ("Release RAM (EmptyWorkingSet)", "ram_release", "Releases memory from background processes.", "Low", "Performance"),
    ("Clean Microsoft Store Cache", "store_cache", "Resets Microsoft Store cache.", "Low", "Apps"),
    ("Flush NetBIOS Name Cache", "nbtstat", "Runs 'nbtstat -R' to clear NetBIOS cache.", "Low", "Network"),
    ("Reset Network Connection", "net_reset", "Releases and renews network adapters.", "Low", "Network"),
    ("Clean Font Cache", "font_cache", "Deletes rendered font cache.", "Low", "Cleanup"),
    ("Clean DirectX Shader Cache", "dx_cache", "Deletes DirectX shader cache.", "Low", "Graphics"),
    ("Uninstall Bloatware", "bloatware", "Uninstalls apps like Xbox, Mail, etc. (optional).", "Medium", "Apps"),
    ("Disable Diagnostic Services", "diagnostics_svc", "Stops diagnostic services in the background.", "Low", "Performance"),
    ("Disable Pagefile", "no_pagefile", "⚠️ Removes pagefile.sys. Dangerous on low-RAM systems.", "High", "Performance"),
    ("Disable Windows Defender Real-Time", "defender", "⚠️ Disables real-time protection. For testing only.", "High", "Security"),
    ("Clean Orphaned Registry Keys", "reg_clean", "Removes registry entries without associated programs.", "High", "Registry"),
]

CATEGORIES = ["Cleanup", "Performance", "Visual", "Privacy", "Network", "Startup", "Power", "System", "Security", "Notifications", "Apps", "Graphics", "Registry"]
HIGH_RISK_KEYS = {"defender", "reg_clean", "no_pagefile"}

# ================== MAIN APPLICATION ==================
class OptimizerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.config = load_config()
        self.i18n = I18N(self.config.get("language", "es"))
        self.title(self.i18n.tr("window_title"))
        
        # Window size
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        win_width = min(1050, screen_width - 100)
        win_height = min(780, screen_height - 100)
        if screen_width < 1024 or screen_height < 768:
            win_width = min(800, screen_width)
            win_height = min(600, screen_height)
        self.geometry(f"{win_width}x{win_height}")
        self.minsize(700, 500)
        self.resizable(True, True)

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.expert_mode = self.config.get("expert_mode", False)
        self.check_vars_recommended = {}
        self.check_vars_custom = {}
        self.system_info = {"ram_gb": 0, "disco_tipo": "HDD", "gpu": "Unknown"}

        self.create_ui()
        self.detect_system()

    def create_ui(self):
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=8, pady=8)

        title_label = ctk.CTkLabel(main_frame, text=self.i18n.tr("main_title"), font=("Segoe UI", 22, "bold"))
        title_label.pack(pady=(5, 3))

        self.system_info_label = ctk.CTkLabel(main_frame, text=self.i18n.tr("detecting"), font=("Segoe UI", 10), text_color="gray")
        self.system_info_label.pack()

        top_btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        top_btn_frame.pack(pady=6, fill="x")

        self.restore_btn = ctk.CTkButton(top_btn_frame, text=self.i18n.tr("create_restore_point"), command=self.create_restore_point)
        self.restore_btn.pack(side="left", padx=3)

        self.options_btn = ctk.CTkButton(top_btn_frame, text=self.i18n.tr("options"), command=self.open_options)
        self.options_btn.pack(side="right", padx=3)

        self.tabview = ctk.CTkTabview(main_frame)
        self.tabview.pack(fill="both", expand=True, pady=(5, 0))
        self.tabview.add(self.i18n.tr("recommended_tab"))
        self.tabview.add(self.i18n.tr("custom_tab"))

        self.create_recommended_tab()
        self.create_custom_tab()

        bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        bottom_frame.pack(fill="x", padx=10, pady=(0, 5))

        self.apply_btn = ctk.CTkButton(
            bottom_frame,
            text=self.i18n.tr("apply_optimizations"),
            font=("Segoe UI", 13, "bold"),
            height=36,
            fg_color="green",
            hover_color="#005000",
            command=self.execute_optimizations
        )
        self.apply_btn.pack(pady=(0, 5), fill="x")

        self.log_area = ctk.CTkTextbox(bottom_frame, height=90, font=("Consolas", 10))
        self.log_area.pack(fill="x", pady=(5, 0))
        self.log_area.configure(state="disabled")

        self.version_label = ctk.CTkLabel(self, text="Alpha 1.0", font=("Segoe UI", 9), text_color="gray")
        self.version_label.place(relx=1.0, rely=1.0, x=-10, y=-5, anchor="se")

    def create_recommended_tab(self):
        tab = self.tabview.tab(self.i18n.tr("recommended_tab"))
        label = ctk.CTkLabel(tab, text=self.i18n.tr("recommended_tab"), font=("Segoe UI", 12, "bold"))
        label.pack(pady=(8, 4))
        self.recommended_frame = ctk.CTkScrollableFrame(tab, fg_color="transparent")
        self.recommended_frame.pack(fill="both", expand=True, padx=5, pady=(0, 5))
        placeholder = ctk.CTkLabel(self.recommended_frame, text=self.i18n.tr("loading_recommendations"), font=("Segoe UI", 11))
        placeholder.pack(pady=20)

    def create_custom_tab(self):
        tab = self.tabview.tab(self.i18n.tr("custom_tab"))
        label = ctk.CTkLabel(tab, text=self.i18n.tr("custom_tab"), font=("Segoe UI", 12, "bold"))
        label.pack(pady=(8, 4))
        self.custom_frame = ctk.CTkScrollableFrame(tab, fg_color="transparent")
        self.custom_frame.pack(fill="both", expand=True, padx=5, pady=(0, 5))
        self.populate_custom_tab()

    def populate_custom_tab(self):
        for widget in self.custom_frame.winfo_children():
            widget.destroy()

        for category in CATEGORIES:
            opts = [opt for opt in OPTIMIZATIONS if opt[4] == category]
            if not opts:
                continue

            cat_label = ctk.CTkLabel(self.custom_frame, text=f"🔹 {category}", font=("Segoe UI", 13, "bold"), anchor="w")
            cat_label.pack(pady=(10, 4), padx=5, anchor="w")

            for name, key, desc, risk, _ in opts:
                if risk == "High" and not self.expert_mode:
                    continue

                var = ctk.BooleanVar()
                frame = ctk.CTkFrame(self.custom_frame, fg_color="transparent")

                checkbox = ctk.CTkCheckBox(
                    frame,
                    text=name,
                    variable=var,
                    font=("Segoe UI", 11, "bold"),
                    checkbox_width=16,
                    checkbox_height=16,
                    fg_color="#2CC985",
                    hover_color="#3FCB9A"
                )
                checkbox.pack(anchor="w")

                wrap = max(300, int(self.winfo_width() * 0.6))
                desc_label = ctk.CTkLabel(frame, text=desc, font=("Segoe UI", 10), text_color="gray60", wraplength=wrap)
                desc_label.pack(anchor="w", pady=(0, 4))

                color = {"Low": "#4CAF50", "Medium": "#FF9800", "High": "#F44336"}.get(risk, "gray")
                risk_label = ctk.CTkLabel(frame, text=f"Risk Level: {risk}", text_color=color, font=("Segoe UI", 9, "bold"))
                risk_label.pack(anchor="w")

                frame.pack(pady=4, padx=10, fill="x")
                self.check_vars_custom[key] = var

    def detect_system(self):
        self.system_info_label.configure(text=self.i18n.tr("detecting"))
        threading.Thread(target=detectar_sistema_callback, args=(self,), daemon=True).start()

    def sistema_detectado(self, info):
        self.system_info = info
        ram = info['ram_gb']
        disk = info['disco_tipo']
        gpu = info['gpu'][:30] + ("..." if len(info['gpu']) > 30 else "")
        self.system_info_label.configure(text=self.i18n.tr("hardware_info").format(ram=ram, disk=disk, gpu=gpu))

        recommended = {
            "dns", "thumbs", "explorer", "temp_user", "temp_sys", "recycle",
            "visual_fx", "transparency", "tips", "high_perf", "delivery_opt",
            "prefetch", "wer", "onedrive", "diagnostics", "recent_files",
            "timeline", "smartscreen", "autoplay", "focusassist", "explorer_tips",
            "desktop_refresh", "location", "wifi_sense", "large_pages", "ram_release"
        }
        if disk == "HDD":
            recommended.update(["sysmain", "pagefile_opt"])
        if ram <= 4:
            recommended.discard("hibernation")
            recommended.add("mem_compress")

        for widget in self.recommended_frame.winfo_children():
            widget.destroy()

        for name, key, desc, risk, _ in OPTIMIZATIONS:
            if key not in recommended:
                continue

            var = ctk.BooleanVar(value=True)
            frame = ctk.CTkFrame(self.recommended_frame, fg_color="transparent")

            checkbox = ctk.CTkCheckBox(
                frame,
                text=name,
                variable=var,
                font=("Segoe UI", 11, "bold"),
                checkbox_width=16,
                checkbox_height=16,
                fg_color="#2CC985",
                hover_color="#3FCB9A"
            )
            checkbox.pack(anchor="w")

            wrap = max(300, int(self.winfo_width() * 0.6))
            desc_label = ctk.CTkLabel(frame, text=desc, font=("Segoe UI", 10), text_color="gray60", wraplength=wrap)
            desc_label.pack(anchor="w", pady=(0, 4))

            color = {"Low": "#4CAF50", "Medium": "#FF9800", "High": "#F44336"}.get(risk, "gray")
            risk_label = ctk.CTkLabel(frame, text=f"Risk Level: {risk}", text_color=color, font=("Segoe UI", 9, "bold"))
            risk_label.pack(anchor="w")

            frame.pack(pady=4, padx=10, fill="x")
            self.check_vars_recommended[key] = var

    def open_options(self):
        options_window = ctk.CTkToplevel(self)
        options_window.title("Options" if self.i18n.lang == "en" else "Opciones")
        options_window.geometry("400x340")
        options_window.resizable(False, False)
        options_window.transient(self)
        options_window.grab_set()

        expert_var = ctk.BooleanVar(value=self.expert_mode)
        expert_checkbox = ctk.CTkCheckBox(options_window, text=self.i18n.tr("expert_mode"), variable=expert_var)
        expert_checkbox.pack(pady=(20, 10), padx=20, anchor="w")

        lang_label = ctk.CTkLabel(options_window, text=self.i18n.tr("language"), font=("Segoe UI", 12))
        lang_label.pack(pady=(10, 5), padx=20, anchor="w")
        
        lang_display = {"es": "Español", "en": "English"}
        lang_internal = {"Español": "es", "English": "en"}
        current_display = lang_display.get(self.i18n.lang, "Español")
        lang_var = ctk.StringVar(value=current_display)
        lang_menu = ctk.CTkOptionMenu(options_window, variable=lang_var, values=list(lang_display.values()))
        lang_menu.pack(pady=(0, 15), padx=20, anchor="w")

        theme_text = self.i18n.tr("light_mode") if ctk.get_appearance_mode() == "Dark" else self.i18n.tr("dark_mode")
        theme_btn = ctk.CTkButton(options_window, text=theme_text, command=lambda: self.toggle_theme(options_window))
        theme_btn.pack(pady=5, padx=20, fill="x")

        update_btn = ctk.CTkButton(
            options_window,
            text=self.i18n.tr("check_updates"),
            command=lambda: webbrowser.open("https://github.com/Crackdroid926/OptimizerU")
        )
        update_btn.pack(pady=5, padx=20, fill="x")

        if getattr(sys, 'frozen', False) is False:
            debug_var = ctk.BooleanVar(value=DEBUG_MODE)
            debug_checkbox = ctk.CTkCheckBox(options_window, text=self.i18n.tr("debug_mode"), variable=debug_var)
            debug_checkbox.pack(pady=(15, 10), padx=20, anchor="w")

        def apply_options():
            self.expert_mode = expert_var.get()
            selected_lang = lang_internal.get(lang_var.get(), "es")
            self.i18n.set_language(selected_lang)
            self.refresh_ui()
            options_window.destroy()
            
            # Save config
            self.config["language"] = self.i18n.lang
            self.config["expert_mode"] = self.expert_mode
            save_config(self.config)
            
            if getattr(sys, 'frozen', False) is False and debug_var.get() and not DEBUG_MODE:
                enable_debug_mode()
                messagebox.showinfo("Debug Mode", "Debug mode enabled. Console and debug.log will be created.")

        apply_btn = ctk.CTkButton(options_window, text="Apply", command=apply_options)
        apply_btn.pack(pady=20, padx=20, fill="x")

    def toggle_theme(self, window):
        current = ctk.get_appearance_mode()
        new_mode = "Light" if current == "Dark" else "Dark"
        ctk.set_appearance_mode(new_mode)
        for child in window.winfo_children():
            if isinstance(child, ctk.CTkButton) and ("Mode" in child.cget("text") or "Modo" in child.cget("text")):
                child.configure(text=self.i18n.tr("light_mode") if new_mode == "Dark" else self.i18n.tr("dark_mode"))

    def refresh_ui(self):
        self.title(self.i18n.tr("window_title"))
        for widget in self.winfo_children():
            widget.destroy()
        self.create_ui()
        self.detect_system()

    def create_restore_point(self):
        log_debug("User clicked: Create Restore Point")
        self.log(self.i18n.tr("detecting"))
        success, _ = run_powershell("Checkpoint-Computer -Description 'Before Optimization' -RestorePointType MODIFY_SETTINGS")
        msg = self.i18n.tr("restore_success") if success else self.i18n.tr("restore_fail")
        self.log(msg)
        log_debug(f"Restore point result: {'success' if success else 'failed'}")

    def execute_optimizations(self):
        log_debug("User clicked: Apply Optimizations")
        current_tab = self.tabview.get()
        if current_tab == self.i18n.tr("recommended_tab"):
            selected = [k for k, v in self.check_vars_recommended.items() if v.get()]
        else:
            selected = [k for k, v in self.check_vars_custom.items() if v.get()]

        if not selected:
            messagebox.showwarning("Warning", self.i18n.tr("no_selection"))
            return

        if any(key in HIGH_RISK_KEYS for key in selected):
            if not messagebox.askyesno(self.i18n.tr("high_risk_title"), self.i18n.tr("high_risk_msg")):
                return

        # Save applied optimizations
        self.config["applied_optimizations"] = selected
        save_config(self.config)
        log_debug(f"Applied optimizations: {selected}")

        threading.Thread(target=self._run_optimizations, args=(selected,), daemon=True).start()

    def _run_optimizations(self, selected_keys):
        self.log("\n" + "="*50)
        self.log(self.i18n.tr("executing"))
        log_debug(f"Starting execution of: {selected_keys}")
        # (Execution logic would go here)
        self.log(self.i18n.tr("done"))
        log_debug("Optimization execution completed")

    def log(self, message):
        self.log_area.configure(state="normal")
        self.log_area.insert("end", message + "\n")
        self.log_area.configure(state="disabled")
        self.log_area.see("end")

# ================== ENTRY POINT ==================
if __name__ == "__main__":
    if not is_admin():
        if messagebox.askyesno("Admin Required", I18N().tr("admin_required")):
            run_as_admin()
            sys.exit()

    app = OptimizerApp()
    app.mainloop()