from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Create a Django module using the mini-finance project structure."

    def add_arguments(self, parser):
        parser.add_argument(
            "name",
            type=str,
            help="Module name, e.g. delivery",
        )

    def handle(self, *args, **options):
        name = options["name"].strip().lower()

        if not name.isidentifier():
            raise CommandError(
                f"Invalid module name: {name}"
            )

        base_dir = Path(settings.BASE_DIR)
        module_dir = base_dir / name

        if module_dir.exists():
            raise CommandError(
                f"Module '{name}' already exists."
            )

        directories = [
            module_dir,
            module_dir / "migrations",
            module_dir / "models",
            module_dir / "serializers",
            module_dir / "services",
            module_dir / "views",
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

        files = {
            module_dir / "__init__.py": "",
            module_dir / "migrations" / "__init__.py": "",
            module_dir / "models" / "__init__.py": "",
            module_dir / "serializers" / "__init__.py": "",
            module_dir / "services" / "__init__.py": "",
            module_dir / "views" / "__init__.py": "",

            module_dir / "admin.py": "",
            module_dir / "constants.py": "",
            module_dir / "tests.py": "",
            module_dir / "urls.py": "",

            module_dir / "models" / f"{name}.py": "",
            module_dir / "serializers" / f"{name}_serializer.py": "",
            module_dir / "services" / f"{name}_service.py": "",
            module_dir / "views" / f"{name}_view_set.py": "",

            module_dir / "apps.py": f"""from django.apps import AppConfig


class {self.class_name(name)}Config(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "{name}"
""",
        }

        for file_path, content in files.items():
            file_path.write_text(content, encoding="utf-8")

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created module '{name}'."
            )
        )

        self.stdout.write("")
        self.stdout.write("Created structure:")

        for path in sorted(module_dir.rglob("*")):
            if path.is_file():
                self.stdout.write(
                    f"  {path.relative_to(base_dir)}"
                )

    @staticmethod
    def class_name(name):
        return "".join(part.capitalize() for part in name.split("_"))