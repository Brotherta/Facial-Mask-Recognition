def load_stylesheet(css_file):
    with open(css_file, 'r') as f:
        content = f.read()
    return content
