import os
import time
import argparse
import google.generativeai as genai
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

# إعداد الواجهة
console = Console()

# إعداد المفتاح - تأكد من تحديثه إذا قمت بتغييره
genai.configure(api_key="AIzaSyC3Nyp_aH0DfQAoYqCdbvA5mhBVlTt1wNs")

def banner():
    os.system('clear')
    banner_text = """
    ██████  ██████   █████   ██████   ██████  ███    ██ 
    ██   ██ ██   ██ ██   ██ ██       ██    ██ ████   ██ 
    ██   ██ ██████  ███████ ██   ███ ██    ██ ██ ██  ██ 
    ██   ██ ██   ██ ██   ██ ██    ██ ██    ██ ██  ██ ██ 
    ██████  ██   ██ ██   ██  ██████   ██████  ██   ████ 
    """
    console.print(f"[bold red]{banner_text}[/bold red]")
    console.print(Panel("[bold cyan]COMMANDER: toolss0824828402 | SYSTEM: DRAGON AI[/bold cyan]", expand=False))

def get_ai_response(prompt, persona="expert"):
    configs = {
        "expert": "Professional technical expert. Deep English analysis.",
        "simple": "Explain like I'm five (ELI5). Simple English.",
        "code": "Coding assistant. Provide clean code snippets in English.",
        "readme": "Documentation expert. Write a professional GitHub README.md in English."
    }
    
    # إصلاح مشكلة الموديل عبر استخدام التسمية المباشرة
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    system_instruction = f"Instruction: {configs.get(persona)}. ALWAYS respond in English only."
    
    try:
        response = model.generate_content(f"{system_instruction}\n\nUser: {prompt}")
        return response.text
    except Exception as e:
        return f"Error occurred: {str(e)}"

def read_local_file(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    return None

def save_output(content, prefix="search"):
    if not os.path.exists("outputs"):
        os.makedirs("outputs")
    filename = f"outputs/{prefix}_{int(time.time())}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    return filename

def main():
    banner()
    
    console.print("\n[bold white]Choose Mode:[/bold white]")
    console.print("1. [red]Expert Search[/red] | 2. [green]Simple Explain[/green] | 3. [blue]Code Assistant[/blue]")
    console.print("4. [magenta]Analyze Local File[/magenta] | 5. [yellow]Generate README[/yellow]")
    
    mode = input("\nSelect (1-5): ")
    
    persona_map = {"1": "expert", "2": "simple", "3": "code", "5": "readme"}
    
    if mode == "4":
        path = input("[?] Enter file path (e.g., dragon.py): ")
        file_content = read_local_file(path)
        if file_content:
            query = f"Analyze this code for errors and explain it:\n\n{file_content}"
            selected_persona = "expert"
        else:
            console.print("[red]File not found![/red]")
            return
    elif mode in persona_map:
        selected_persona = persona_map[mode]
        query = input(f"\n[?] Enter your prompt (English): ")
    else:
        return

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        progress.add_task(description="Dragon is processing...", total=None)
        answer = get_ai_response(query, selected_persona)

    console.print("\n")
    console.print(Panel(answer, title="[bold green]DRAGON AI RESPONSE[/bold green]", border_style="red"))
    
    # الحفظ التلقائي
    save_type = "readme" if mode == "5" else "log"
    saved_path = save_output(answer, prefix=save_type)
    console.print(f"\n[dim]✔ File saved to: {saved_path}[/dim]")

if __name__ == "__main__":
    main()
