# Keystroke Logger - Educational Security Project

A Python-based keystroke logging application designed for **security research and educational purposes** to understand input monitoring, system intrusion detection, and endpoint security mechanisms.

## ⚠️ Disclaimer

This tool captures keyboard input and logs application context. **Unauthorized use of keyloggers is illegal.** This project is intended exclusively for:
- Security professionals in controlled lab environments
- Cybersecurity students studying system monitoring and detection
- Personal research on systems you own and have permission to test

Unauthorized interception of keystrokes on systems you do not own or without explicit consent violates computer fraud and privacy laws in most jurisdictions.

---

## Project Overview

This keylogger demonstrates fundamental concepts in:
- **Input device monitoring** — How operating systems capture and forward input events
- **Window/application context tracking** — Understanding active process detection
- **Logging mechanisms** — Persistent data recording and analysis
- **Detection evasion identification** — Learning what endpoint protection solutions look for

**Educational use cases:**
- Understand how endpoint detection and response (EDR) solutions identify suspicious input monitoring
- Learn reverse-engineering defensive security tools
- Analyze system behavior patterns for intrusion detection
- Study data exfiltration methodologies

---

## Features

### Current Implementation
- **Keystroke Capture** — Logs every key press with timestamp
- **Active Application Context** — Records which window/application has focus at each keystroke
- **File Logging** — Persistent storage to `keylog.txt`
- **Non-blocking Listener** — Runs in background without blocking main thread

### Logged Data Format
```
[2024-09-14 14:23:45,123]:App:Google Chrome | Key:h
[2024-09-14 14:23:45,234]:App:Google Chrome | Key:e
[2024-09-14 14:23:45,345]:App:Visual Studio Code | Key:l
```

---

## Requirements

### Dependencies
- **Python 3.7+**
- `pynput` — Cross-platform input device monitoring
- `pywinctl` — Window/application context detection (Windows-specific in current implementation)

### System Requirements
- **Windows 10/11** (pywinctl currently optimized for Windows)
- Administrator/elevated privileges (some protected applications may block key capture)

### Installation

```bash
# Clone or download the project
cd keystroke-logger

# Install dependencies
pip install pynput pywinctl

# Run the logger
python main.py
```

---

## Usage

### Basic Operation
```bash
python main.py
```
The script will:
1. Start listening for keyboard input
2. Detect the active window on each keystroke
3. Log to `keylog.txt` in the current directory
4. Run until manually stopped (Ctrl+C)

### Output File
- **Location:** `keylog.txt` (created in working directory)
- **Format:** Timestamped entries with application context
- **Permissions:** Ensure appropriate file access controls

---

## Technical Details

### How It Works

1. **Keyboard Listener** (`pynput.keyboard.Listener`)
   - Hooks keyboard events at the OS level
   - Triggers `on_press()` callback for each keystroke
   - Non-intrusive; doesn't modify input stream

2. **Window Detection** (`pywinctl.getActiveWindow()`)
   - Queries OS for currently focused window
   - Returns window title (application name)
   - Handles exceptions for protected/system windows

3. **Logging System** (Python `logging` module)
   - Uses standard logging with file handler
   - Includes millisecond-precision timestamps
   - DEBUG level captures all events

### Key Code Structure
```python
# Listener callback for each key press
def on_press(key):
    app_name = get_active_app()           # Get active window
    logging.info(f"App:{app_name} | Key:{key}")  # Log with timestamp
```

---

## Limitations & Detection Vectors

### Current Weaknesses
- **Plain-text logging** — No obfuscation; trivial to detect on filesystem
- **No anti-forensics** — Logs preserved in standard locations with metadata
- **Obvious resource usage** — Process visible in Task Manager
- **No anti-debugging** — Can be inspected with process monitoring tools
- **Cross-app visibility** — Protected applications (Windows Hello, password managers) may block access
- **No persistence mechanism** — Dies when script terminates

### How EDR/Security Tools Detect This
- **Input device hook detection** — Monitor for `SetWindowsHookEx()` or pynput equivalents
- **File access monitoring** — Detect unusual file creation/modification (keylog.txt)
- **Process behavior analysis** — Identify keystroke capture pattern signatures
- **Registry/config scanning** — Look for known keylogger configurations
- **Memory inspection** — Scan loaded DLLs and hook tables

---

## Potential Learning Extensions

### Defensive/Detection Features
```python
# Add these to understand attack/defense tradeoffs:
- Keystroke pattern analysis (identify unusual typing rhythms)
- Log encryption (practice securing sensitive captures)
- Rotating/compressing log files (evasion techniques)
- Network transmission simulation (understand C2 callbacks)
- Process tree inspection (learn parent-child relationships)
- Clipboard monitoring (expand beyond keyboard)
```

### Companion Projects
- **Keylogger Detector** — Build a script that identifies keystroke logging patterns
- **Behavior Analysis** — Analyze captured logs for patterns (e.g., password entry rhythms)
- **EDR Evasion Analysis** — Identify detection signatures and understand defensive responses

---

## Ethical Use Guidelines

✅ **Permitted:**
- Testing on systems you own in isolated environments
- Academic research with proper authorization
- Authorized penetration testing (with written scope)
- Security tool evaluation and comparison

❌ **Not Permitted:**
- Capturing keystrokes on systems without owner consent
- Monitoring others' input devices
- Credential theft or information gathering
- Workplace monitoring without legal compliance/notification

---

## Platform Support

| Platform | Status | Notes |
|----------|--------|-------|
| Windows 10/11 | ✅ Full | Primary target; requires admin |
| Linux | ⚠️ Partial | pynput works; pywinctl needs adaptation |
| macOS | ⚠️ Partial | pynput compatible; window detection varies |

### Linux/macOS Adaptation
Replace `pywinctl` with platform-specific alternatives:
```python
# Linux: Use wmctrl or xdotool
# macOS: Use native Cocoa APIs or open source alternatives
```

---

## Security Hardening (for authorized use)

If deploying in legitimate security testing:

```python
# 1. Encrypt logs
from cryptography.fernet import Fernet
cipher = Fernet(key)
encrypted = cipher.encrypt(log_data)

# 2. Use secure deletion
import shutil
shutil.disk_usage('keylog.txt')  # Verify before cleanup

# 3. Add authentication
# Require credentials before accessing logs

# 4. Implement log rotation
import logging.handlers
handler = logging.handlers.RotatingFileHandler(
    'keylog.txt', maxBytes=5*1024*1024, backupCount=5
)
```

---

## Troubleshooting

### Script Won't Capture Keys
- **Solution:** Run with administrator/elevated privileges
- **Check:** Verify pynput installation: `python -c "from pynput import keyboard; print('OK')"`

### Window Title Shows "Unknown Application"
- **Cause:** Protected windows or system processes blocking access
- **Solution:** Add try-except handling or filter by process ID instead

### High CPU Usage
- **Cause:** Listener callback executing heavy operations
- **Solution:** Move logging to separate thread or queue

### keylog.txt Growing Too Large
- **Solution:** Implement log rotation (see Security Hardening section)

---

## Dependencies & Attribution

- **pynput** — Cross-platform Python library for controlling and monitoring input devices
- **pywinctl** — Pythonic window control for Windows/Linux/macOS
- **Python logging** — Standard library for structured logging

---

## Learning Outcomes

After working with this project, you should understand:
- ✓ How keyloggers interact with operating system input mechanisms
- ✓ Window/application context detection at the OS level
- ✓ Detection techniques used by endpoint protection solutions
- ✓ Logging strategies and data persistence
- ✓ Ethical implications of input device monitoring
- ✓ Legal frameworks governing system monitoring

---

## Related Topics to Explore

- **Endpoint Detection & Response (EDR)** — How tools detect this activity
- **Operating System Security** — Input device protection mechanisms
- **Forensic Analysis** — Recovering/analyzing logs post-incident
- **Anti-debugging** — Techniques to evade analysis tools
- **Secure Logging** — Encryption and tamper-proofing of audit trails

---

## References

- [pynput Documentation](https://pynput.readthedocs.io/)
- [pywinctl Documentation](https://pywinctl.readthedocs.io/)
- [MITRE ATT&CK - Input Capture](https://attack.mitre.org/techniques/T1056/004/)
- [CIS Controls - Detailed Logging](https://www.cisecurity.org/cis-controls)

---

## License

Educational use only. See disclaimer above.

---

**Last Updated:** September 2024  
**Maintained for:** Cybersecurity education and security research
