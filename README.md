# OptimizerU

**Version: Alpha 1.0**  
**Created by: CrackDroid926**

OptimizerU is a lightweight, open-source Windows optimization tool built for users with older or low-spec hardware—such as systems with Intel Celeron/Pentium CPUs, 2–4 GB of RAM, and traditional HDDs. It helps improve system responsiveness by applying safe, reversible tweaks to Windows settings, services, and caches.

Unlike many "system optimizers," this tool is transparent, does not hide its actions, and never modifies critical system files without your explicit consent.

---

## 🔒 This Is Not a Virus

OptimizerU is **completely safe** and **100% open-source**.  
- All source code is publicly available for inspection.
- It uses only standard Windows utilities: **PowerShell** and **Command Prompt**.
- No data is collected, transmitted, or stored.
- No advertisements, toolbars, cryptocurrency miners, or hidden payloads.

When you run the program, you may see PowerShell windows appear briefly. This is normal—these are the system commands executing cleanup or configuration tasks (e.g., `ipconfig /flushdns`, `sfc /scannow`). You can review every command in the source code.

Files `INFO_ES.txt` and `INFO_EN.txt` are automatically created on first launch to explain this behavior in your preferred language.

---

## 🛠️ What It Does

OptimizerU performs practical optimizations such as:

- **Cleaning**: temporary files, DNS cache, thumbnail cache, Prefetch, and font caches
- **Disabling**: unnecessary background services (e.g., SysMain on HDDs), telemetry, and diagnostic tracking
- **Tuning**: visual effects for performance (disabling animations, transparency, and shadows)
- **Managing**: startup apps, Windows Update bandwidth, and delivery optimization
- **Protecting**: automatically creates a system restore point before major changes
- **Adapting**: detects your hardware (RAM, disk type, GPU) and suggests relevant optimizations

Every option is labeled with a risk level: **Low**, **Medium**, or **High**. High-risk actions are hidden by default and require explicit confirmation.

---

## 🌐 Features

- Bilingual interface: **English** and **Spanish**
- Two modes:  
  - **Recommended**: safe, hardware-aware optimizations  
  - **Custom**: full manual control
- Dark and Light themes
- Saves your settings and applied optimizations to `config.json`
- Optional debug mode (`debug.log` + console) for developers
- Weekly updates planned (approximately 3 per week), regardless of popularity

---

## ⚙️ Requirements

To run from source:
- Windows 10 or 11 (64-bit recommended)
- Python 3.7 or newer
- Dependencies: customtkinter and psutil
-  Install with:
```bash
pip install -r requirements.txt
```
- Run with:
```bash
python OptimizerU.py
```
A standalone executable (OptimizerU.exe) is available in the Releases section.

---

### 💡 For Developers
This project was inspired by tools like OptiJuegos but rebuilt from scratch in Python to ensure transparency and simplicity.

The code is functional but not perfect—I am still learning Python and GUI development. You may notice minor visual bugs, especially on very low screen resolutions (e.g., 800x600). I am actively working to improve stability and UI smoothness.

Contributions, bug reports, and suggestions are welcome—but never expected.

---

### 📜 License & Ownership
OptimizerU is released without a formal license.

When you download this software, it becomes yours.
You are free to use, modify, redistribute, or even claim it as your own.
No attribution is required. No restrictions apply. 

This is a personal choice to give users complete freedom. If you find this tool helpful, the best thanks is to help someone else with an old computer.

---

## 🛠️ Known Issues
- Brief UI stutter when loading optimization lists (due to dynamic widget creation)
- Minor layout issues on screens below 1024x768 resolution
- Some optimizations require a system restart to take full effect

I will continue fixing these issues because this tool exists to help real people—not to chase popularity.

---

## 🔗 Useful Links
- Releases: https://github.com/Crackdroid926/OptimizerU/releases
- Report a bug: https://github.com/Crackdroid926/OptimizerU/issues
- Source code: https://github.com/Crackdroid926/OptimizerU
