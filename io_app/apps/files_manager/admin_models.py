from django.contrib import admin


class FilesAdmin(admin.ModelAdmin):
    list_display = ("uuid", "name", "extension", "upload_date", "size", "owner_id")
    search_fields = ("owner_id", "uuid", "name", "extension")

    readonly_fields = ["uuid", "upload_date"]


class DirectoryAdmin(admin.ModelAdmin):
    list_display = ("uuid", "name", "creation_date", "owner_id")
    search_fields = ("owner_id", "uuid", "name")

    readonly_fields = ["uuid", "creation_date"]
