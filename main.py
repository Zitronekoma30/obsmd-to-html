import argparse
import obsidian_to_html.md_html as md_html
import os
import hashlib
import time
from http.server import HTTPServer, SimpleHTTPRequestHandler

def check_for_changes(md_path, file_ids):
    new_file_ids = []
    for root, _, files in os.walk(md_path):
        for file in files:
            if file.endswith(".md"):
                full_path_to_file = md_path + os.sep + file
                new_file_ids.append(generate_dynamic_id(full_path_to_file))
    for key in file_ids:
        if key not in new_file_ids:
            return True
        if file_ids[key] != new_file_ids[key]:
            return True
    return False

class CustomHTTPRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        super().end_headers()

def serve_output_html(output_path, md_path, file_ids):
    os.chdir(output_path)
    httpd = HTTPServer(('localhost', 80), CustomHTTPRequestHandler)
    print(f"Serving HTTP on localhost port 80 (http://localhost:80/) ...")
    
    while True:
        httpd.handle_request()
        if check_for_changes(md_path, file_ids):
            print("Changes detected, rebuilding html files")
            file_ids = convert_all_md_files(output_path, md_path)
            time.sleep(1)


def generate_dynamic_id(file_path):
    mtime = os.path.getmtime(file_path)
    hash_input = f"{file_path}-{mtime}".encode('utf-8')
    return hashlib.md5(hash_input).hexdigest()

def convert_all_md_files(output_path, md_path):
    # remove all files in output path
    for root, _, files in os.walk(output_path):
        for file in files:
            os.remove(output_path + os.sep + file)
    
    # Convert all md files to html
    file_dynamic_ids = {}
    for root, _, files in os.walk(md_path):
        for file in files:
            if file.endswith(".md"):
                full_path_to_file = md_path + os.sep + file
                print("Converting", full_path_to_file)
                md_html.md_to_html(full_path_to_file, output_path)
                file_dynamic_ids[file] = generate_dynamic_id(full_path_to_file)
    return file_dynamic_ids

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert markdown file to html and maintain a directory of html files to serve as a website")
    # add arguments for md input file directory and output dir
    parser.add_argument("md", help="Markdown files to convert to html")
    parser.add_argument("output", help="Output directory for html files")
    args = parser.parse_args()
    
    md_path = args.md
    output_path = args.output

    # convert md files to html
    ids = convert_all_md_files(output_path, md_path)

    # serve html files
    serve_output_html(output_path, md_path, ids)
