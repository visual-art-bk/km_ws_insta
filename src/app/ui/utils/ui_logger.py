def log_status(ui_element, message):
    ui_element.append(f"[상태] {message}")


def log_error_to_ui(ui_element, message, trace=""):
    ui_element.append(f"<span style='color:red;'>[오류]</span> {message}")
    if trace:
        ui_element.append(f"<pre>{trace}</pre>")
