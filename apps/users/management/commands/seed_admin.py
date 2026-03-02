from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os


class Command(BaseCommand):

    help = "Crea o verifica el usuario ADMIN inicial usando el campo role"

    def add_arguments(self, parser):
        # puedes usarlo para poder definir otros atributos
        parser.add_argument("--name", type=str) 
        parser.add_argument("--last_name", type=str) 
        parser.add_argument("--email", type=str) 
        parser.add_argument("--password", type=str)

        # forzar el cambio de una contraseña cuando el admin ya existe   
        #usa force ==> true
        #sin ==> false
        parser.add_argument("--force", action="store_true")

    def handle(self, *args, **options):

        #.get se encarga de leer mediante *options* ("--email, --password",...)-> de add_arguments
        #se optiene y si ne caso no esita pasa os.getenv..  lee "example@gmail.com"
        email = "perrito1@gmail.com"
        username = "perrito1@gmail.com"
        #email = options.get("email") or os.getenv("ADMIN_EMAIL")
        #password = options.get("password") or os.getenv("ADMIN_PASSWORD")
        password = "caquita123"
        #force = bool(options.get("force"))
        #if not email: #si no encontro email entonces creamos pesss

            ##stderr => usado para errores
            #stdout => para mensajes normales
        #    self.stderr.write("Email requerido")
        #    return

        #normalizamos
        email = email.strip().lower()

        #usamos nuestro modelo personalizado
        User = get_user_model()

        #.objescts es una instancia de django que sirve como manager para
        #poder trabajar con los  atributos de User(un modelo)
        #tiene varios metodos ocmo get_or_create => busca(en DB) o crea 
        user, created = User.objects.get_or_create(email=email)
        if not created:
            #actualiza algo
            self.stderr.write(f"El gmail ya esta registrado{email}")
        
        user.username = username
        user.role = "admin"
        user.set_password(password)

        user.save()

        if created:
            self.stdout.write(f"Admin creado: {email}")
