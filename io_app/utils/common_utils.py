from django.http import FileResponse


def send_file(file_path, attachment_name, as_attachment=True):
    response = FileResponse(open(file_path, "rb"), as_attachment=as_attachment, filename=attachment_name)

    return response


def serve_media_file(file_path, filename):
    response = FileResponse(open(file_path, "rb"), as_attachment=False,  filename=filename)
    response["Accept-Ranges"] = "bytes"

    return response
