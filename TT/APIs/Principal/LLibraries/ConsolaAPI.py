from rich.console import Console
console = Console()

def mensaje_consola_plano(mensaje):
    global console
    console.print(f'    {mensaje}')
def mensaje_consola(mensaje,programa:str='API'):
    global console
    console.print(f'[bold cyan]{programa}:[/]      {mensaje}')
def error_consola(mensaje):
    global console
    console.print(f'[bold red]ERROR:[/]     {mensaje}')
def advertencia_consola(mensaje):
    global console
    console.print(f'[bold gold1]ADVERTENCIA:        {mensaje}')