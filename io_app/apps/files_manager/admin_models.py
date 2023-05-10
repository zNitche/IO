from django.contrib import admin


class FilesAdmin(admin.ModelAdmin):
    list_display = ("uuid", "name", "extension", "upload_date", "size", "owner_id")
    search_fields = ("owner_id", "uuid", "name", "extension")

    readonly_fields = ["uuid", "upload_date"]
