import json
import os
import time
import requests
import sys
import socket as s
import colorama
from instaloader import Instaloader, Profile
import phonenumbers
import geocoder
from phonenumbers import carrier, geocoder

# Nombre del archivo JSON donde se guardarán los datos de los usuarios
USERS_FILE = 'users.json'


def load_users():
    """Carga los usuarios desde el archivo JSON."""
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as file:
            return json.load(file)
    return {}


def save_users(users):
    """Guarda los usuarios en el archivo JSON."""
    with open(USERS_FILE, 'w') as file:
        json.dump(users, file, indent=4)


def register():
    """Permite a un nuevo usuario registrarse."""
    users = load_users()
    username = input('Ingrese un nombre de usuario: ')
    if username in users.get('usuarios', {}):
        print('El nombre de usuario ya existe. Intenta con otro.')
        return
    password = input('Ingrese una contraseña: ')
    users.setdefault('usuarios', {})[username] = password
    ip_autorizada = input('¿Desea agregar la IP actual como autorizada para este usuario? sí/no: ').strip().lower()
    if ip_autorizada == "sí":
        local_ip = get_local_ip()
        users.setdefault('ips_autorizadas', {})[username] = local_ip
        print(f'IP {local_ip} agregada como autorizada para {username}.')
    save_users(users)
    print('Registro exitoso.')


def login():
    """Permite al usuario iniciar sesión."""
    users = load_users()
    username = input('Ingrese su nombre de usuario: ')
    if username not in users.get('usuarios', {}):
        print('El nombre de usuario no existe.')
        return False
    password = input('Ingrese su contraseña: ')
    if users['usuarios'][username] == password:
        print('Inicio de sesión exitoso.')
        return username  # Devuelve el nombre de usuario en lugar de True
    else:
        print('Contraseña incorrecta.')
        return False


def change_password():
    """Permite al usuario cambiar su contraseña antes de iniciar sesión."""
    users = load_users()
    username = input('Ingrese su nombre de usuario: ')
    if username not in users.get('usuarios', {}):
        print('El nombre de usuario no existe.')
        return
    old_password = input('Ingrese su contraseña actual: ')
    if users['usuarios'][username] != old_password:
        print('Contraseña incorrecta.')
        return
    new_password = input('Ingrese su nueva contraseña: ')
    users['usuarios'][username] = new_password
    save_users(users)
    print('Contraseña cambiada exitosamente.')


def banner():
    print(colorama.Fore.LIGHTBLACK_EX + """
          / _ \\/ __|_ _| \\| |_   _|
         | (_) \\__ \\| || .` | | |  
          \\___/|___/___|_|\\_| |_|  
          """)
    print(colorama.Fore.RESET + "")


def get_local_ip():
    """Obtiene la IP local del ordenador."""
    hostname = s.gethostname()
    local_ip = s.gethostbyname(hostname)
    return local_ip


def auto_login_by_ip():
    """Inicia sesión automáticamente si la IP local coincide con una autorizada."""
    users_data = load_users()  # Carga los datos de users.json
    local_ip = get_local_ip()  # Obtén la IP local del ordenador

    # Verifica si la IP está autorizada
    for username, ip_autorizada in users_data.get('ips_autorizadas', {}).items():
        if local_ip == ip_autorizada:
            print(f'Inicio de sesión automático para {username}')
            return username  # Devuelve el nombre de usuario
    return None


from instaloader import Instaloader, Profile  # Importar Instaloader y Profile


def instagram_account_osint():
    x = Instaloader()  # Instancia de Instaloader
    try:
        uname = input("Enter a username: ")
        if uname == "":
            print("Unknown command!")
            sys.exit()

        # Usar correctamente Profile para acceder al perfil
        f = Profile.from_username(x.context, uname)

        # Mostrar la información del perfil
        print("Username:", f.username)
        print("ID:", f.userid)
        print("Full name:", f.full_name)
        print("Biography:", f.biography)
        print("Business category name:", f.business_category_name)
        print("External URL:", f.external_url)
        print("Followed by viewer:", f.followed_by_viewer)
        print("Followees:", f.followees)
        print("Followers:", f.followers)
        print("Follows viewer:", f.follows_viewer)
        print("Blocked by viewer:", f.blocked_by_viewer)
        print("Has blocked viewer:", f.has_blocked_viewer)
        print("Has highlight reels:", f.has_highlight_reels)
        print("Has public story:", f.has_public_story)
        print("Has requested viewer:", f.has_requested_viewer)
        print("Requested by viewer:", f.requested_by_viewer)
        print("Has viewable story:", f.has_viewable_story)
        print("Igtvcount:", f.igtvcount)
        print("Is business account:", f.is_business_account)
        print("Is private:", f.is_private)
        print("Is verified:", f.is_verified)
        print("Mediacount:", f.mediacount)
        print("Profile pic url:", f.profile_pic_url)

    except KeyboardInterrupt:
        print("I understand!")

    except EOFError:
        print("Why?")


def get_ip_location(ip):
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json")
        response.raise_for_status()
        data = response.json()
        if 'bogon' in data:
            return {"Error": "IP privada o reservada, no se puede localizar."}
        location_data = {
            "IP": data.get("ip", "N/A"),
            "Ciudad": data.get("city", "N/A"),
            "Región": data.get("region", "N/A"),
            "País": data.get("country", "N/A"),
            "Ubicación": data.get("loc", "N/A"),
            "Organización": data.get("org", "N/A")
        }
        return location_data
    except requests.RequestException as e:
        return {"Error": f"Error al obtener los datos de la IP: {e}"}


def ip_info():
    ip = input("Introduce la dirección IP: ").strip()
    location_data = get_ip_location(ip)
    print("Información de la IP:")
    for key, value in location_data.items():
        print(f"{key}: {value}")


def web_code():
    url = input("Introduce la URL para scrapear: ").strip()
    check_url = input(f"¿Es esta la URL: {url}, sí/no: ").strip().lower()
    if check_url == "sí":
        response = requests.get(url)
        soup = response.text
        print(soup)
    else:
        web_code()

    txt = input("¿Deseas guardar el código en un archivo txt? sí/no: ").strip().lower()
    if txt == "sí":
        with open("WEB_CODE.txt", "w") as file:
            file.write(soup)
    else:
        sys.exit()


def ip():
    web = input("Introduce el dominio: ").strip()
    print(f"IP de {web} es: {s.gethostbyname(web)}")


def numchecker():
    print("El formato del número es: +34612345678")
    phone = input("Introduce el número de teléfono: ").strip()
    info = []
    number = phonenumbers.parse(phone)
    info.append(geocoder.description_for_number(number, "es"))
    info.append(carrier.name_for_number(number, "es"))
    print(info)


def selection_tool():
    tools = [
        "WEB CODE", "IP ADDRESS", "NUMBER INFO", "IP INFO", "INSTAGRAM OSINT"
    ]
    print("Herramientas disponibles:", tools)

    tool = input("¿Qué herramienta quieres usar? ").strip().upper()

    if tool == "WEB CODE":
        web_code()
    elif tool == "IP ADDRESS":
        ip()
    elif tool == "NUMBER INFO":
        numchecker()
    elif tool == "IP INFO":
        ip_info()
    elif tool == "INSTAGRAM OSINT":
        instagram_account_osint()
    else:
        print("Selección no válida. Por favor, elige una herramienta válida.")
        selection_tool()


def main():
    """Función principal que gestiona el flujo del programa."""
    colorama.init()
    auto_login_user = auto_login_by_ip()

    if auto_login_user:
        # Si el login automático es exitoso
        print(f"Inicio de sesión automático exitoso para {auto_login_user}")
        banner()
        time.sleep(2)
        os.system("cls" if os.name == 'nt' else 'clear')
        banner()
        selection_tool()
        return

    while True:
        print('\n--- Menú Principal ---')
        print('1. Registrarse')
        print('2. Iniciar sesión')
        print('3. Cambiar contraseña')
        print('4. Salir')

        choice = input('Seleccione una opción: ')
        if choice == '1':
            register()
        elif choice == '2':
            username = login()
            if username:
                banner()
                time.sleep(2)
                os.system("cls" if os.name == 'nt' else 'clear')
                banner()
                selection_tool()
        elif choice == '3':
            change_password()
        elif choice == '4':
            print('Saliendo...')
            break
        else:
            print('Opción no válida. Intente de nuevo.')


if __name__ == "__main__":
    main()
