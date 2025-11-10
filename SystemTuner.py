"""
SystemTuner - Alpha 1.1 (Enhanced)
Created by: CrackDroid926
GitHub: https://github.com/Crackdroid926/

Enhanced because I had a few errors in the normal version, but this is the improved version that includes some new libraries and better documentation in the code, an advanced developer mode that I don't have because it was just a test that I can't delete now due to the errors I had, but there are some improvements. I want it to look like OptimizerX but without viruses and without using the source code, but the interface is still missing and I'm just getting started with the code.
"""

import os
import sys
import json
import ctypes
import subprocess
import threading
import webbrowser
import logging
import traceback
from datetime import datetime, timedelta
from pathlib import Path
import platform
import customtkinter as ctk
from tkinter import messagebox

# ================================
# GLOBAL CONFIGURATION & PATHS
# ================================

# Developer mode activation
DEVELOPER_MODE = "-devmode" in sys.argv or "-crack" in sys.argv

# Directories
BASE_DIR = Path(__file__).parent.resolve()
DATA_DIR = BASE_DIR / "SystemTuner_Data"
ASSETS_DIR = BASE_DIR / "assets"
DATA_DIR.mkdir(exist_ok=True)

# File paths
CONFIG_FILE = DATA_DIR / "config.json"
SYSTEM_INFO_FILE = DATA_DIR / "system_info.json"
DEBUG_LOG_FILE = DATA_DIR / "debug.log"

# Info files (created on first run)
INFO_FILES = {
    "es": BASE_DIR / "INFO_ES.txt",
    "en": BASE_DIR / "INFO_EN.txt"
}

# ================================
# DEBUG & LOGGING SETUP
# ================================

def setup_logging():
    """Initialize debug logging if enabled."""
    if not DEVELOPER_MODE and getattr(sys, 'frozen', False):
        return

    logging.basicConfig(
        filename=DEBUG_LOG_FILE,
        level=logging.DEBUG,
        format="%(asctime)s | %(levelname)-8s | %(funcName)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        force=True
    )
    logging.info("=== SYSTEMTUNER DEBUG MODE ACTIVATED ===")
    logging.info(f"Python {sys.version}, Platform: {platform.platform()}")
    logging.info(f"Base Dir: {BASE_DIR}")

def log_exception(exc: Exception):
    """Log full exception with traceback."""
    if logging.getLogger().hasHandlers():
        logging.error("Unhandled exception:\n%s", traceback.format_exc())

# ================================
# UTILITY FUNCTIONS
# ================================

def is_admin() -> bool:
    """Check if the process has administrator privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """Relaunch the application with elevated privileges."""
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1
    )

def run_powershell(cmd: str, timeout: int = 30) -> tuple[bool, str]:
    """Execute a PowerShell command and return (success, output)."""
    try:
        result = subprocess.run(
            ["powershell", "-Command", cmd],
            capture_output=True, text=True, timeout=timeout, cwd=BASE_DIR
        )
        return result.returncode == 0, result.stdout.strip()
    except Exception as e:
        if logging.getLogger().hasHandlers():
            logging.error(f"PowerShell failed: {e}")
        return False, str(e)

def resource_path(relative_path: str) -> Path:
    """Get absolute path to resource, works for dev and PyInstaller."""
    try:
        base_path = Path(sys._MEIPASS)
    except:
        base_path = BASE_DIR
    return base_path / relative_path

# ================================
# CONFIGURATION MANAGEMENT
# ================================

def load_config() -> dict:
    """Load user configuration from JSON file."""
    if CONFIG_FILE.exists():
        try:
            return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        except Exception as e:
            log_exception(e)
    return {
        "language": "es",
        "expert_mode": False,
        "dark_mode": True,
        "window_size": "1050x780",
        "applied_optimizations": []
    }

def save_config(config: dict):
    """Save user configuration to JSON file."""
    try:
        # Ensure developer mode flag is consistent
        config["developer_mode"] = DEVELOPER_MODE
        CONFIG_FILE.write_text(json.dumps(config, indent=4, ensure_ascii=False), encoding="utf-8")
    except Exception as e:
        log_exception(e)

# ================================
# INTERNATIONALIZATION (I18N)
# ================================

class Translator:
    """Bilingual translator for UI strings."""
    def __init__(self, lang: str = "es"):
        self.lang = lang
        self._strings = {
            "es": {
                "window_title": "SystemTuner | Creado por CrackDroid926",
                "main_title": "Optimizar Sistema",
                "detecting": "Detectando hardware y sistema...",
                "create_restore_point": "Crear Punto de Restauración",
                "apply_optimizations": "✅ Aplicar Optimizaciones Seleccionadas",
                "recommended_tab": "Recomendado para mi PC",
                "custom_tab": "Personalizar Optimizaciones",
                "hardware_info": "Sistema: {os} • RAM: {ram} GB • Disco: {disk} • GPU: {gpu}",
                "restore_success": "[ÉXITO] Punto de restauración creado.",
                "restore_fail": "[ADVERTENCIA] No se pudo crear el punto de restauración.",
                "no_selection": "Seleccione al menos una optimización.",
                "executing": "EJECUTANDO OPTIMIZACIONES...",
                "done": "✅ ¡Optimización completada!",
                "options": "⚙️ Opciones",
                "expert_mode": "Soy un usuario experto",
                "language": "Idioma",
                "check_updates": "Buscar actualizaciones",
                "dark_mode": "Modo oscuro",
                "light_mode": "Modo claro",
                "debug_mode": "Activar modo debug (desarrolladores)",
                "admin_required": "¿Ejecutar como administrador?",
                "github_url": "https://github.com/Crackdroid926/OptimizerU",
                "risk_low": "Nivel de riesgo: Bajo",
                "risk_medium": "Nivel de riesgo: Medio",
                "risk_high": "Nivel de riesgo: Alto",
                "description": "Descripción: {}",
                "config_dev": "🔧 Configuración para Desarrolladores",
                "error_report": "Si encuentras un error, por favor repórtalo en GitHub. ¡Estoy aprendiendo Python y tu ayuda mejora este proyecto! Gracias por usar SystemTuner.",
                "error_report_en": "If you find a bug, please report it on GitHub. I'm learning Python, and your help makes this project better! Thank you for using SystemTuner."
            },
            "en": {
                "window_title": "SystemTuner | Created by CrackDroid926",
                "main_title": "Optimize System",
                "detecting": "Detecting hardware and OS...",
                "create_restore_point": "Create Restore Point",
                "apply_optimizations": "✅ Apply Selected Optimizations",
                "recommended_tab": "Recommended for My PC",
                "custom_tab": "Customize Optimizations",
                "hardware_info": "System: {os} • RAM: {ram} GB • Disk: {disk} • GPU: {gpu}",
                "restore_success": "[SUCCESS] Restore point created.",
                "restore_fail": "[WARNING] Failed to create restore point.",
                "no_selection": "Please select at least one optimization.",
                "executing": "EXECUTING OPTIMIZATIONS...",
                "done": "✅ Optimization completed!",
                "options": "⚙️ Options",
                "expert_mode": "I am an expert user",
                "language": "Language",
                "check_updates": "Check for Updates",
                "dark_mode": "Dark Mode",
                "light_mode": "Light Mode",
                "debug_mode": "Enable Debug Mode (Developers)",
                "admin_required": "Run as administrator?",
                "github_url": "https://github.com/Crackdroid926/OptimizerU",
                "risk_low": "Risk Level: Low",
                "risk_medium": "Risk Level: Medium",
                "risk_high": "Risk Level: High",
                "description": "Description: {}",
                "config_dev": "🔧 Developer Configuration",
                "error_report": "If you find a bug, please report it on GitHub. I'm learning Python, and your help makes this project better! Thank you for using SystemTuner.",
                "error_report_en": "If you find a bug, please report it on GitHub. I'm learning Python, and your help makes this project better! Thank you for using SystemTuner."
            }
        }

    def set_language(self, lang: str):
        if lang in self._strings:
            self.lang = lang

    def tr(self, key: str) -> str:
        return self._strings[self.lang].get(key, key)

# ================================
# OPTIMIZATION DISCOVERY & METADATA
# ================================

def get_risk_level(filename: str) -> str:
    """Determine risk level based on filename keywords."""
    name_lower = filename.lower()
    high_risk = ["defender", "delete", "remove", "uninstall", "disable windows defender"]
    medium_risk = ["telemetry", "telemetria", "privacy", "services", "servicios", "compression", "compresion"]
    
    if any(kw in name_lower for kw in high_risk):
        return "High"
    elif any(kw in name_lower for kw in medium_risk):
        return "Medium"
    return "Low"

def get_description(filename: str, lang: str = "es") -> str:
    """Generate accurate description based on filename."""
    name_lower = filename.lower()
    if lang == "es":
        descriptions = {
            "transparencia": "Desactiva el efecto de transparencia en la barra de tareas y ventanas.",
            "cortana": "Desactiva el asistente de voz Cortana.",
            "telemetria": "Reduce la telemetría y los diagnósticos enviados a Microsoft.",
            "temporales": "Elimina archivos temporales del usuario y del sistema.",
            "servicios": "Optimiza servicios en segundo plano para mejorar el rendimiento.",
            "energia": "Configura el plan de energía para máximo rendimiento.",
            "ram": "Optimiza el uso de la memoria RAM.",
            "ssd": "Optimiza la configuración para unidades SSD.",
            "hdd": "Optimiza la configuración para discos duros tradicionales (HDD).",
            "prefetch": "Limpia la caché de Prefetch para mejorar el tiempo de carga.",
            "dns": "Limpia la caché DNS para resolver problemas de red.",
            "recycle": "Vacía la papelera de reciclaje del sistema.",
            "thumbcache": "Limpia la caché de miniaturas del Explorador de archivos."
        }
    else:
        descriptions = {
            "transparency": "Disables transparency effect on taskbar and windows.",
            "cortana": "Disables Cortana voice assistant.",
            "telemetry": "Reduces telemetry and diagnostics sent to Microsoft.",
            "temp": "Deletes temporary user and system files.",
            "services": "Optimizes background services to improve performance.",
            "power": "Sets power plan to high performance.",
            "ram": "Optimizes RAM usage.",
            "ssd": "Optimizes settings for SSD drives.",
            "hdd": "Optimizes settings for traditional hard disk drives (HDD).",
            "prefetch": "Cleans Prefetch cache to improve load times.",
            "dns": "Flushes DNS cache to resolve network issues.",
            "recycle": "Empties the system Recycle Bin.",
            "thumbcache": "Cleans thumbnail cache in File Explorer."
        }

    for keyword, desc in descriptions.items():
        if keyword in name_lower:
            return desc
    
    return "Optimización específica para mejorar el rendimiento del sistema." if lang == "es" \
        else "Specific optimization to improve system performance."

def discover_optimizations() -> dict:
    """Scan assets/Tweaks/ and return structured optimization metadata."""
    tweaks_dir = resource_path("assets/Tweaks")
    optimizations = {}

    if not tweaks_dir.exists():
        return optimizations

    for root, _, files in os.walk(tweaks_dir):
        rel_path = Path(root).relative_to(tweaks_dir)
        category = str(rel_path) if rel_path != Path(".") else "General"

        for file in files:
            if file.endswith((".bat", ".cmd", ".reg")):
                full_path = Path(root) / file
                risk = get_risk_level(file)
                lang = "es"  # Default to Spanish for descriptions
                desc = get_description(file, lang)
                file_type = "reg" if file.endswith(".reg") else "bat"
                
                if category not in optimizations:
                    optimizations[category] = []
                optimizations[category].append((file, str(full_path), file_type, risk, desc))

    return optimizations

def execute_optimization(file_path: str, file_type: str) -> bool:
    """Execute a .bat, .cmd, or .reg file securely."""
    try:
        if file_type == "reg":
            result = subprocess.run(["reg", "import", file_path], shell=True, capture_output=True, text=True, cwd=BASE_DIR)
        else:
            result = subprocess.run([file_path], shell=True, capture_output=True, text=True, cwd=BASE_DIR)
        
        if logging.getLogger().hasHandlers():
            logging.info(f"Executed: {file_path} | Exit code: {result.returncode}")
        return result.returncode == 0
    except Exception as e:
        log_exception(e)
        return False

# ================================
# SYSTEM DETECTION
# ================================

def detect_system_info() -> dict:
    """Detect comprehensive system information."""
    info = {
        "os_name": "Windows",
        "os_version": "Unknown",
        "os_build": "Unknown",
        "architecture": "x64",
        "ram_gb": 0,
        "disk_type": "HDD",
        "gpu": "Unknown",
        "detected_at": datetime.now().isoformat()
    }

    try:
        # OS Info
        info["os_version"] = platform.version()
        info["os_build"] = platform.release()
        info["architecture"] = "x64" if platform.machine().endswith("64") else "x86"
        
        import psutil
        info["ram_gb"] = max(1, round(psutil.virtual_memory().total / (1024**3)))
        
        # Disk type (HDD/SSD)
        success, output = run_powershell("Get-PhysicalDisk | Select-Object -First 1 -ExpandProperty MediaType")
        info["disk_type"] = "SSD" if (success and "SSD" in output) else "HDD"
        
        # GPU
        success, output = run_powershell("(Get-WmiObject Win32_VideoController).Name | Select-Object -First 1")
        if success and output:
            info["gpu"] = output[:45]
    except Exception as e:
        log_exception(e)
    
    return info

def load_or_detect_system() -> dict:
    """Load cached system info or perform fresh detection."""
    if SYSTEM_INFO_FILE.exists():
        try:
            data = json.loads(SYSTEM_INFO_FILE.read_text(encoding="utf-8"))
            detected_at = datetime.fromisoformat(data.get("detected_at", "1970-01-01T00:00:00"))
            if datetime.now() - detected_at < timedelta(days=7):
                return data
        except Exception as e:
            log_exception(e)
    
    # Perform fresh detection
    info = detect_system_info()
    try:
        SYSTEM_INFO_FILE.write_text(json.dumps(info, indent=4, ensure_ascii=False), encoding="utf-8")
    except Exception as e:
        log_exception(e)
    return info

# ================================
# MAIN APPLICATION CLASS
# ================================

class SystemTunerApp(ctk.CTk):
    """Main application window for SystemTuner."""
    
    def __init__(self):
        super().__init__()
        self.config = load_config()
        self.translator = Translator(self.config.get("language", "es"))
        self.title(self.translator.tr("window_title"))
        
        # Apply saved theme
        theme = "Dark" if self.config.get("dark_mode", True) else "Light"
        ctk.set_appearance_mode(theme)
        ctk.set_default_color_theme("blue")
        
        # Window setup
        self._setup_window()
        self._create_ui()
        self._load_system_info()

    def _setup_window(self):
        """Configure window size and behavior."""
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Parse saved size or use default
        try:
            width, height = map(int, self.config.get("window_size", "1050x780").split("x"))
        except:
            width, height = 1050, 780
            
        # Constrain to screen size
        width = min(width, screen_width - 50)
        height = min(height, screen_height - 100)
        if screen_width < 1024 or screen_height < 768:
            width, height = min(800, screen_width), min(600, screen_height)
            
        self.geometry(f"{width}x{height}")
        self.minsize(750, 550)
        self.resizable(True, True)

    def _create_ui(self):
        """Create the main user interface."""
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=12, pady=12)

        # Title
        title_label = ctk.CTkLabel(main_frame, text=self.translator.tr("main_title"), font=("Segoe UI", 24, "bold"))
        title_label.pack(pady=(5, 10))

        # System info
        self.system_info_label = ctk.CTkLabel(main_frame, text=self.translator.tr("detecting"), font=("Segoe UI", 11), text_color="gray")
        self.system_info_label.pack()

        # Top buttons
        top_btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        top_btn_frame.pack(pady=8, fill="x")

        self.restore_btn = ctk.CTkButton(
            top_btn_frame, 
            text=self.translator.tr("create_restore_point"), 
            width=190, 
            command=self._create_restore_point
        )
        self.restore_btn.pack(side="left", padx=5)

        self.options_btn = ctk.CTkButton(
            top_btn_frame, 
            text=self.translator.tr("options"), 
            width=140, 
            command=self._open_options
        )
        self.options_btn.pack(side="right", padx=5)

        # Developer button (only in dev mode)
        if DEVELOPER_MODE:
            self.dev_btn = ctk.CTkButton(
                top_btn_frame, 
                text=self.translator.tr("config_dev"), 
                width=180, 
                fg_color="purple", 
                command=self._open_dev_config
            )
            self.dev_btn.pack(side="right", padx=5)

        # Tabs
        self.tabview = ctk.CTkTabview(main_frame, height=0)
        self.tabview.pack(fill="both", expand=True, pady=(10, 0))
        self.tabview.add(self.translator.tr("recommended_tab"))
        self.tabview.add(self.translator.tr("custom_tab"))

        # Tab content frames
        self.recommended_frame = ctk.CTkScrollableFrame(self.tabview.tab(self.translator.tr("recommended_tab")), fg_color="transparent")
        self.recommended_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.custom_frame = ctk.CTkScrollableFrame(self.tabview.tab(self.translator.tr("custom_tab")), fg_color="transparent")
        self.custom_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Bottom controls
        bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        bottom_frame.pack(fill="x", padx=15, pady=(0, 12))

        self.apply_btn = ctk.CTkButton(
            bottom_frame,
            text=self.translator.tr("apply_optimizations"),
            font=("Segoe UI", 14, "bold"),
            height=42,
            fg_color="green",
            hover_color="#005000",
            command=self._execute_optimizations
        )
        self.apply_btn.pack(pady=(0, 8), fill="x")

        self.log_area = ctk.CTkTextbox(bottom_frame, height=100, font=("Consolas", 10))
        self.log_area.pack(fill="x", pady=(5, 0))
        self.log_area.configure(state="disabled")

        # Version and error report
        version_frame = ctk.CTkFrame(self, fg_color="transparent")
        version_frame.pack(fill="x", padx=15, pady=(0, 5))

        self.version_label = ctk.CTkLabel(version_frame, text="Alpha 1.1", font=("Segoe UI", 10), text_color="gray")
        self.version_label.pack(side="left")

        error_msg = self.translator.tr("error_report_en") if self.translator.lang == "en" else self.translator.tr("error_report")
        self.error_label = ctk.CTkLabel(version_frame, text=error_msg, font=("Segoe UI", 9), text_color="gray", justify="right")
        self.error_label.pack(side="right", padx=(0, 15))

    def _load_system_info(self):
        """Load system information and populate UI."""
        self.system_info = load_or_detect_system()
        
        os_name = f"Windows {self.system_info['os_build']}"
        ram = self.system_info['ram_gb']
        disk = self.system_info['disk_type']
        gpu = self.system_info['gpu'][:40] + ("..." if len(self.system_info['gpu']) > 40 else "")
        
        self.system_info_label.configure(
            text=self.translator.tr("hardware_info").format(
                os=os_name, ram=ram, disk=disk, gpu=gpu
            )
        )
        
        # Populate tabs
        self._populate_recommended_tab()
        self._populate_custom_tab()

    def _populate_recommended_tab(self):
        """Populate the recommended optimizations tab."""
        for widget in self.recommended_frame.winfo_children():
            widget.destroy()

        optimizations = discover_optimizations()
        recommended = set()
        safe_keywords = ["temporales", "dns", "iconos", "miniaturas", "transparencia", "cortana", "telemetria", "servicios", "prefetch"]

        for category, items in optimizations.items():
            for name, path, ftype, risk, desc in items:
                if risk == "High" and not self.config.get("expert_mode", False):
                    continue
                    
                name_lower = name.lower()
                # Always recommend safe items
                if any(kw in name_lower for kw in safe_keywords):
                    recommended.add((name, path, ftype, risk, desc))
                # Hardware-specific recommendations
                elif self.system_info["disk_type"] == "HDD" and ("hdd" in name_lower or "compresion" in name_lower):
                    recommended.add((name, path, ftype, risk, desc))
                elif self.system_info["ram_gb"] <= 4 and ("ram" in name_lower or "mem" in name_lower):
                    recommended.add((name, path, ftype, risk, desc))
                elif "ssd" in name_lower and self.system_info["disk_type"] == "SSD":
                    recommended.add((name, path, ftype, risk, desc))

        if not recommended:
            msg = ctk.CTkLabel(self.recommended_frame, text="No recommended optimizations found.", font=("Segoe UI", 12))
            msg.pack(pady=30)
            return

        # Display recommendations
        cat_label = ctk.CTkLabel(self.recommended_frame, text="🔹 Recommended Optimizations", font=("Segoe UI", 14, "bold"), anchor="w")
        cat_label.pack(pady=(10, 6), padx=10, anchor="w")

        for name, path, ftype, risk, desc in sorted(recommended):
            self._create_optimization_item(self.recommended_frame, name, path, risk, desc, True)

    def _populate_custom_tab(self):
        """Populate the custom optimizations tab."""
        for widget in self.custom_frame.winfo_children():
            widget.destroy()

        optimizations = discover_optimizations()
        if not optimizations:
            msg = ctk.CTkLabel(self.custom_frame, text="No optimizations found in assets/Tweaks/", font=("Segoe UI", 12))
            msg.pack(pady=30)
            return

        for category in sorted(optimizations.keys()):
            items = optimizations[category]
            if not items:
                continue

            display_cat = category.replace("\\", " → ").replace(".", "")
            cat_label = ctk.CTkLabel(self.custom_frame, text=f"🔹 {display_cat}", font=("Segoe UI", 14, "bold"), anchor="w")
            cat_label.pack(pady=(12, 6), padx=10, anchor="w")

            for name, path, ftype, risk, desc in items:
                if risk == "High" and not self.config.get("expert_mode", False):
                    continue
                self._create_optimization_item(self.custom_frame, name, path, risk, desc, False)

    def _create_optimization_item(self, parent, name: str, path: str, risk: str, desc: str, selected_by_default: bool):
        """Create a single optimization item widget."""
        var = ctk.BooleanVar(value=selected_by_default)
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        
        # Checkbox
        chk = ctk.CTkCheckBox(
            frame,
            text=name,
            variable=var,
            font=("Segoe UI", 12, "bold"),
            checkbox_width=18,
            checkbox_height=18,
            fg_color="#2CC985",
            hover_color="#3FCB9A"
        )
        chk.pack(anchor="w")
        
        # Description
        desc_label = ctk.CTkLabel(
            frame, 
            text=self.translator.tr("description").format(desc), 
            font=("Segoe UI", 10), 
            text_color="gray70", 
            wraplength=720, 
            justify="left"
        )
        desc_label.pack(anchor="w", pady=(2, 4))
        
        # Risk level
        risk_colors = {"Low": "#4CAF50", "Medium": "#FF9800", "High": "#F44336"}
        risk_label = ctk.CTkLabel(
            frame, 
            text=self.translator.tr(f"risk_{risk.lower()}"), 
            text_color=risk_colors.get(risk, "gray"), 
            font=("Segoe UI", 10, "bold")
        )
        risk_label.pack(anchor="w")
        
        frame.pack(pady=6, padx=15, fill="x")
        
        # Store variable reference
        if selected_by_default:
            self.__dict__.setdefault("check_vars_recommended", {})[path] = var
        else:
            self.__dict__.setdefault("check_vars_custom", {})[path] = var

    def _open_options(self):
        """Open the options dialog."""
        options_window = ctk.CTkToplevel(self)
        options_window.title("Options" if self.translator.lang == "en" else "Opciones")
        options_window.geometry("430x380")
        options_window.resizable(False, False)
        options_window.transient(self)
        options_window.grab_set()

        # Expert mode
        expert_var = ctk.BooleanVar(value=self.config.get("expert_mode", False))
        expert_checkbox = ctk.CTkCheckBox(
            options_window, 
            text=self.translator.tr("expert_mode"), 
            variable=expert_var, 
            font=("Segoe UI", 12)
        )
        expert_checkbox.pack(pady=(20, 12), padx=25, anchor="w")

        # Language
        lang_label = ctk.CTkLabel(options_window, text=self.translator.tr("language"), font=("Segoe UI", 13, "bold"))
        lang_label.pack(pady=(10, 5), padx=25, anchor="w")
        
        lang_display = {"es": "Español", "en": "English"}
        lang_internal = {"Español": "es", "English": "en"}
        current_display = lang_display.get(self.translator.lang, "Español")
        lang_var = ctk.StringVar(value=current_display)
        lang_menu = ctk.CTkOptionMenu(options_window, variable=lang_var, values=list(lang_display.values()), width=200)
        lang_menu.pack(pady=(0, 15), padx=25, anchor="w")

        # Theme
        current_theme = ctk.get_appearance_mode()
        theme_var = ctk.StringVar(value="Modo Oscuro" if current_theme == "Dark" else "Modo Claro")
        theme_label = ctk.CTkLabel(options_window, text="Tema / Theme", font=("Segoe UI", 13, "bold"))
        theme_label.pack(pady=(5, 5), padx=25, anchor="w")
        theme_menu = ctk.CTkOptionMenu(options_window, variable=theme_var, values=["Modo Oscuro", "Modo Claro"], width=200)
        theme_menu.pack(pady=(0, 15), padx=25, anchor="w")

        # Check updates
        update_btn = ctk.CTkButton(
            options_window,
            text=self.translator.tr("check_updates"),
            command=lambda: webbrowser.open("https://github.com/Crackdroid926/OptimizerU")
        )
        update_btn.pack(pady=8, padx=25, fill="x")

        # Debug mode (dev only)
        if not getattr(sys, 'frozen', False):
            debug_var = ctk.BooleanVar(value=logging.getLogger().hasHandlers())
            debug_checkbox = ctk.CTkCheckBox(
                options_window, 
                text=self.translator.tr("debug_mode"), 
                variable=debug_var, 
                font=("Segoe UI", 12)
            )
            debug_checkbox.pack(pady=(10, 12), padx=25, anchor="w")

        # Apply button
        def apply_options():
            # Update config
            self.config.update({
                "expert_mode": expert_var.get(),
                "language": lang_internal.get(lang_var.get(), "es"),
                "dark_mode": theme_var.get() == "Modo Oscuro"
            })
            save_config(self.config)
            
            # Apply changes
            self.translator.set_language(self.config["language"])
            ctk.set_appearance_mode("Dark" if self.config["dark_mode"] else "Light")
            self._refresh_ui()
            options_window.destroy()
            
            # Enable debug if needed
            if not getattr(sys, 'frozen', False) and debug_var.get():
                setup_logging()
                messagebox.showinfo("Debug Mode", "Debug mode enabled. Logs saved to SystemTuner_Data/debug.log")

        apply_btn = ctk.CTkButton(options_window, text="Apply / Aplicar", command=apply_options, height=36)
        apply_btn.pack(pady=20, padx=25, fill="x")

    def _open_dev_config(self):
        """Open developer configuration window."""
        if not DEVELOPER_MODE:
            return
            
        dev_window = ctk.CTkToplevel(self)
        dev_window.title("Developer Configuration")
        dev_window.geometry("520x480")
        dev_window.resizable(False, False)
        dev_window.transient(self)
        dev_window.grab_set()

        title = ctk.CTkLabel(dev_window, text="🔧 Developer Configuration", font=("Segoe UI", 16, "bold"))
        title.pack(pady=15)

        # Theme color
        theme_frame = ctk.CTkFrame(dev_window, fg_color="transparent")
        theme_frame.pack(pady=8, padx=20, fill="x")
        ctk.CTkLabel(theme_frame, text="UI Theme Color", font=("Segoe UI", 12, "bold")).pack(anchor="w")
        theme_var = ctk.StringVar(value="blue")
        theme_menu = ctk.CTkOptionMenu(theme_frame, variable=theme_var, values=["blue", "green", "dark-blue"])
        theme_menu.pack(pady=5, fill="x")

        # Window size
        size_frame = ctk.CTkFrame(dev_window, fg_color="transparent")
        size_frame.pack(pady=8, padx=20, fill="x")
        ctk.CTkLabel(size_frame, text="Window Size", font=("Segoe UI", 12, "bold")).pack(anchor="w")
        size_var = ctk.StringVar(value=self.config.get("window_size", "1050x780"))
        size_menu = ctk.CTkOptionMenu(size_frame, variable=size_var, values=["800x600", "1024x768", "1050x780", "1280x800"])
        size_menu.pack(pady=5, fill="x")

        # Log viewer
        def open_log():
            if DEBUG_LOG_FILE.exists():
                os.startfile(DEBUG_LOG_FILE)
            else:
                messagebox.showinfo("Debug Log", "No debug log found. Enable debug mode first.")
                
        log_btn = ctk.CTkButton(dev_window, text="View Debug Log", command=open_log)
        log_btn.pack(pady=8, padx=20, fill="x")

        # Reset config
        def reset_config():
            if messagebox.askyesno("Reset Config", "Reset all settings and system info?"):
                try:
                    CONFIG_FILE.unlink(missing_ok=True)
                    SYSTEM_INFO_FILE.unlink(missing_ok=True)
                    messagebox.showinfo("Reset", "Configuration reset. Please restart the application.")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to reset: {e}")

        reset_btn = ctk.CTkButton(dev_window, text="Reset Configuration", fg_color="red", command=reset_config)
        reset_btn.pack(pady=15, padx=20, fill="x")

        # Apply dev settings
        def apply_dev():
            try:
                ctk.set_default_color_theme(theme_var.get())
                self.geometry(size_var.get())
                self.config["window_size"] = size_var.get()
                save_config(self.config)
            except Exception as e:
                log_exception(e)
            dev_window.destroy()

        apply_btn = ctk.CTkButton(dev_window, text="Apply Developer Settings", command=apply_dev, height=36)
        apply_btn.pack(pady=15, padx=20, fill="x")

    def _refresh_ui(self):
        """Refresh the entire UI with new settings."""
        self.title(self.translator.tr("window_title"))
        for widget in self.winfo_children():
            widget.destroy()
        self._create_ui()
        self._load_system_info()

    def _create_restore_point(self):
        """Create a system restore point."""
        self._log(self.translator.tr("detecting"))
        success, _ = run_powershell("Checkpoint-Computer -Description 'Before SystemTuner Optimization' -RestorePointType MODIFY_SETTINGS")
        msg = self.translator.tr("restore_success") if success else self.translator.tr("restore_fail")
        self._log(msg)

    def _execute_optimizations(self):
        """Execute selected optimizations."""
        current_tab = self.tabview.get()
        if current_tab == self.translator.tr("recommended_tab"):
            selected = [path for path, var in getattr(self, "check_vars_recommended", {}).items() if var.get()]
        else:
            selected = [path for path, var in getattr(self, "check_vars_custom", {}).items() if var.get()]
        
        if not selected:
            messagebox.showwarning("Warning", self.translator.tr("no_selection"))
            return

        self.config["applied_optimizations"] = selected
        save_config(self.config)

        threading.Thread(target=self._run_optimizations, args=(selected,), daemon=True).start()

    def _run_optimizations(self, selected_files: list):
        """Background thread to run optimizations."""
        self._log("\n" + "="*60)
        self._log(self.translator.tr("executing"))
        success_count = 0
        
        for file_path in selected_files:
            ext = Path(file_path).suffix.lower()
            file_type = "reg" if ext == ".reg" else "bat"
            if execute_optimization(file_path, file_type):
                success_count += 1
            else:
                self._log(f"[!] Failed: {Path(file_path).name}")
                
        self._log(f"\n{self.translator.tr('done')} ({success_count}/{len(selected_files)} successful)")
        self._log("💡 Some changes may require a system restart to take effect.")

    def _log(self, message: str):
        """Log a message to the log area."""
        self.log_area.configure(state="normal")
        self.log_area.insert("end", message + "\n")
        self.log_area.configure(state="disabled")
        self.log_area.see("end")

# ================================
# APPLICATION ENTRY POINT
# ================================

def main():
    """Main entry point with error handling."""
    try:
        # Setup logging if in dev mode
        if DEVELOPER_MODE:
            setup_logging()
        
        # Create info files
        for lang, path in INFO_FILES.items():
            if not path.exists():
                content = (
                    "Información sobre SystemTuner (Alpha 1.1)\n\n"
                    "¿Por qué se abre PowerShell?\n"
                    "- Este programa usa comandos de Windows para optimizar tu sistema.\n"
                    "- PowerShell es una herramienta oficial de Microsoft.\n"
                    "- NO es un virus. Todos los comandos son visibles en los archivos .bat/.reg.\n\n"
                    "Creado por: CrackDroid926\n"
                    "GitHub: https://github.com/Crackdroid926/OptimizerU"
                ) if lang == "es" else (
                    "About SystemTuner (Alpha 1.1)\n\n"
                    "Why does PowerShell open?\n"
                    "- This tool uses Windows commands to optimize your system.\n"
                    "- PowerShell is an official Microsoft tool.\n"
                    "- It is NOT a virus. All commands are visible in .bat/.reg files.\n\n"
                    "Created by: CrackDroid926\n"
                    "GitHub: https://github.com/Crackdroid926/OptimizerU"
                )
                path.write_text(content, encoding="utf-8")

        # Check admin rights
        if not is_admin():
            if messagebox.askyesno("Admin Required", "Administrator rights are recommended for full functionality.\nRun as administrator?"):
                run_as_admin()
                return

        # Start application
        app = SystemTunerApp()
        app.mainloop()

    except Exception as e:
        log_exception(e)
        error_msg = (
            "An unexpected error occurred.\n"
            "Details have been saved to SystemTuner_Data/debug.log\n"
            "Please report this issue on GitHub."
        )
        messagebox.showerror("SystemTuner Error", error_msg)
        raise

if __name__ == "__main__":
    main()