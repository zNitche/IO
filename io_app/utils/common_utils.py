from django.http import FileResponse


def send_file(file_path, attachment_name, as_attachment=True):
    response = FileResponse(open(file_path, "rb"), as_attachment=as_attachment, filename=attachment_name)

    return response
