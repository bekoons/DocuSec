def upload_form() -> str:
    """Return a minimal HTML form for file uploads."""
    return (
        "<html><body><h1>Upload Document</h1>"
        "<form action='/ingest' method='post' enctype='multipart/form-data'>"
        "<input type='file' name='file'/>"
        "<input type='submit' value='Upload'/></form></body></html>"
    )

