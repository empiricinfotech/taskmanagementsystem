# Generated by Django 4.1.7 on 2023-03-16 11:36

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                ("otp", models.PositiveIntegerField(blank=True, null=True)),
                (
                    "email",
                    models.EmailField(
                        max_length=254, unique=True, verbose_name="email address"
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Task",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "task_title",
                    models.CharField(max_length=400, verbose_name="task_title"),
                ),
                (
                    "startDate",
                    models.DateField(blank=True, default=django.utils.timezone.now),
                ),
                (
                    "endDate",
                    models.DateField(blank=True, default=django.utils.timezone.now),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Done", "Done"),
                            ("Pending", "Pending"),
                            ("InProgress", "InProgress"),
                            ("Open", "Open"),
                        ],
                        default="Open",
                        max_length=20,
                    ),
                ),
                (
                    "progress",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("0%", "0%"),
                            ("10%", "10%"),
                            ("20%", "20%"),
                            ("30%", "30%"),
                            ("40%", "40%"),
                            ("50%", "50%"),
                            ("60%", "60%"),
                            ("70%", "70%"),
                            ("80%", "80%"),
                            ("90%", "90%"),
                        ],
                        default="0%",
                        max_length=20,
                        null=True,
                    ),
                ),
                (
                    "description",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "priority",
                    models.CharField(
                        choices=[
                            ("Highest", "Highest"),
                            ("High", "High"),
                            ("Midium", "Midium"),
                            ("Low", "Low"),
                        ],
                        default="Low",
                        max_length=20,
                    ),
                ),
                (
                    "assign_To",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="assigneduser",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "created_By",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="createduser",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("dependency", models.ManyToManyField(blank=True, to="TaskApp.task")),
            ],
        ),
    ]
