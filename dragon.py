import os
import sys
import psutil
import time
from groq import Groq
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.text import Text

# --- إعدادات الهوية والاتصال ---
USERNAME = "PyDragonX"
GITHUB_LINK = "https://github.com/PyDragonX"
API_KEY = "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"
client = Groq(api_key=API_KEY)
console = Console()

def get_sys_info():
    """جلب بيانات النظام الحية"""
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    return f"[bold magenta]CPU:[/bold magenta] {cpu}% | [bold magenta]RAM:[/bold magenta] {ram}%"

def save_to_history(prompt, response):
    with open("dragon_history.txt", "a", encoding="utf-8") as f:
        f.write(f"[{time.ctime()}]\nUser: {prompt}\nAI: {response}\n{'-'*40}\n")

def dragon_ai_query(system_prompt, user_input):
    """محرك الاستعلام الرئيسي"""
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=0.5,
            max_tokens=2048,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def display_menu():
    os.system('clear' if os.name == 'posix' else 'cls')
    stats = get_sys_info()
    
    console.print(Panel.fit(
        f"[bold cyan]🐉 {USERNAME} REVOLUTIONARY SYSTEM v3.0[/bold cyan]\n"
        f"[bold white]GitHub: {GITHUB_LINK}[/bold white]\n"
        f"{stats}",
        border_style="cyan",
        title="[bold red]VIRTUAL TERMINAL[/bold red]"
    ))
    
    table = Table(show_header=False, box=None)
    table.add_row("[1] 🧠 Neural Link (Chat)", "[2] 👁️ Dragon Eye (Code Audit)")
    table.add_row("[3] 📄 Doc Architect", "[4] ⚔️ Weapon Factory (Payloads)")
    table.add_row("[5] 📜 Archives (History)", "[6] 🔍 OSINT Search (Coming Soon)")
    table.add_row("[7] 💀 Stealth Exit", "")
    
    console.print(Panel(table, title="[bold yellow]Select Tool[/bold yellow]", border_style="blue"))

def main():
    while True:
        display_menu()
        choice = input(f"\n[{USERNAME}] @ Root:~$ ")

        if choice == '1':
            q = input("\n[?] Ask Dragon: ")
            res = dragon_ai_query("You are a cybersecurity expert.", q)
            console.print(Panel(res, title="Response", border_style="green"))
            save_to_history(q, res)
            input("\nPress Enter...")

        elif choice == '2':
            path = input("\n[?] Enter Path to .py file: ")
            if os.path.exists(path):
                with open(path, 'r') as f:
                    code = f.read()
                console.print("[yellow]Analyzing code for vulnerabilities...[/yellow]")
                res = dragon_ai_query("Analyze this Python code for security vulnerabilities, logic errors, and leaked credentials. Provide a detailed report.", code)
                console.print(Panel(res, title="Audit Report", border_style="red"))
                save_to_history(f"Audit: {path}", res)
            else:
                console.print("[red]File not found![/red]")
            input("\nPress Enter...")

        elif choice == '4':
            p_type = input("\n[?] What payload/tool do you need? (e.g. Reverse Shell): ")
            console.print("[yellow]Forging weapon in the factory...[/yellow]")
            res = dragon_ai_query("Write a clean, functional Python script for the following security tool/payload. Include comments on how it works.", p_type)
            console.print(Panel(res, title="Generated Weapon", border_style="magenta"))
            save_to_history(f"Payload Request: {p_type}", res)
            input("\nPress Enter...")

        elif choice == '5':
            if os.path.exists("dragon_history.txt"):
                with open("dragon_history.txt", "r") as f: console.print(f.read())
            else:
                console.print("Archives are empty.")
            input("\nPress Enter...")

        elif choice == '7':
            console.print("[bold red]Executing Stealth Exit... Cleaning History.[/bold red]")
            # مسح الـ Terminal History في كالي
            os.system('history -c') 
            time.sleep(1)
            break

        else:
            console.print("[red]Invalid Option![/red]")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[red]Session Aborted.[/red]")
        sys.exit()
