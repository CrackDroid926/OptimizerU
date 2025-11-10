# SystemTuner

**Version: Alpha 1.1**  
**Created by: CrackDroid926**

SystemTuner is a lightweight, open-source Windows optimization tool built for users with older or low-spec hardware—such as systems with Intel Celeron/Pentium CPUs, 2–4 GB of RAM, and traditional HDDs. It helps improve system responsiveness by applying safe, reversible tweaks to Windows settings, services, and caches.

Unlike many "system optimizers," this tool is transparent, does not hide its actions, and never modifies critical system files without your explicit consent.

This project is the result of continuous learning in Python and GUI development. If you find a bug, please report it—your feedback helps make this tool better for everyone with an older PC.

---

## This Is Not a Virus

SystemTuner is completely safe and 100% open-source.  
- All source code is publicly available for inspection.  
- It uses only standard Windows utilities: PowerShell and Command Prompt.  
- No data is collected, transmitted, or stored.  
- No advertisements, toolbars, cryptocurrency miners, or hidden payloads.  

When you run the program, you may see PowerShell windows appear briefly. This is normal—these are the system commands executing cleanup or configuration tasks (e.g., `ipconfig /flushdns`, `sfc /scannow`). You can review every command in the source code.

Files `INFO_ES.txt` and `INFO_EN.txt` are automatically created on first launch to explain this behavior in your preferred language.

---

## What It Does

SystemTuner performs practical optimizations such as:

- **Cleaning**: temporary files, DNS cache, thumbnail cache, Prefetch, and font caches  
- **Disabling**: unnecessary background services (e.g., SysMain on HDDs), telemetry, and diagnostic tracking  
- **Tuning**: visual effects for performance (disabling animations, transparency, and shadows)  
- **Managing**: startup apps and Windows Update settings  
- **Protecting**: automatically creates a system restore point before major changes  
- **Adapting**: detects your hardware (RAM, disk type, GPU, Windows version) and suggests relevant optimizations  

Every option is labeled with a risk level: Low, Medium, or High. High-risk actions are hidden by default and require explicit confirmation.

---

## Features

- Bilingual interface: English and Spanish  
- Two modes:  
  - Recommended: safe, hardware-aware optimizations  
  - Custom: full manual control  
- Dark and Light themes  
- Saves your settings and applied optimizations to `config.json`  
- Automatic system information caching to avoid repeated scans  
- Clean file organization: all runtime data stored in a dedicated folder  
- Weekly updates planned (approximately 3 per week), regardless of popularity  

---

## Requirements

- Windows 10 or 11 (64-bit recommended)  
- Python 3.7 or newer  
- Dependencies: `customtkinter`, `psutil`

---

## For Developers

This project was inspired by existing optimization tools but rebuilt from scratch in Python to ensure full transparency and user control. All optimizations are executed from external `.bat` and `.reg` files—no hidden logic inside the launcher.

The code includes detailed documentation, modular design, and hardware-aware logic. While functional, it is still evolving as I continue to learn and improve. Contributions and bug reports are welcome, but never expected.

---

## License & Ownership

SystemTuner is released without a formal license.

When you download this software, it becomes yours.  
You are free to use, modify, redistribute, or even claim it as your own.  
No attribution is required. No restrictions apply.

This is a personal choice to give users complete freedom. If you find this tool helpful, the best thanks is to help someone else with an old computer.

---

## Known Issues

- Brief UI stutter when loading optimization lists  
- Minor layout issues on screens below 1024x768 resolution  
- Some optimizations require a system restart to take full effect  

I will continue fixing these issues because this tool exists to help real people—not to chase popularity.

---

## Useful Links

- Releases: https://github.com/Crackdroid926/SystemTuner/releases  
- Report a bug: https://github.com/Crackdroid926/SystemTuner/issues  
- Source code: https://github.com/Crackdroid926/SystemTuner  

Thank you for using SystemTuner. Your trust means a lot.
