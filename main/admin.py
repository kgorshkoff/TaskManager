from django.contrib import admin

from main.models import Tag, Task, User


class TaskManagerAdminSite(admin.AdminSite):
    pass


task_manager_admin_site = TaskManagerAdminSite(name="Task manager admin")


@admin.register(Tag, site=task_manager_admin_site)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Task, site=task_manager_admin_site)
class TaskAdmin(admin.ModelAdmin):
    pass


class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "role")


task_manager_admin_site.register(User, UserAdmin)
