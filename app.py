import json
import webview
import os
import sys
from pathlib import Path
from PyQt5.QtWidgets import QFileDialog, QApplication

# Set WebView2 user data folder to avoid permission issues
webview_data_dir = os.path.join(os.getenv('TEMP'), 'webview_data')
os.makedirs(webview_data_dir, exist_ok=True)
os.environ['WEBVIEW2_USER_DATA_FOLDER'] = webview_data_dir
os.environ['WEBVIEW2_ADDITIONAL_BROWSER_ARGUMENTS'] = ' '.join([
    '--disable-gpu',
    '--disable-software-rasterizer',
    '--disable-extensions',
    '--disable-plugins',
    '--disable-dev-shm-usage',
    '--no-sandbox',
    '--disable-setuid-sandbox',
    '--js-flags=--max-old-space-size=512',
    '--disable-background-networking',
    '--disable-background-timer-throttling',
    '--disable-backgrounding-occluded-windows',
    '--disable-breakpad',
    '--disable-component-extensions-with-background-pages',
    '--disable-features=TranslateUI,BlinkGenPropertyTrees',
    '--disable-ipc-flooding-protection',
    '--disable-renderer-backgrounding',
])

_webview_window = None

class API:
    def __init__(self):
        self.data = [
            {"type": "click","step_number": 1,"disabled": True,"image": "images\\screenshot_20250913_230333.png","pre_delay": 0.0,"post_delay": 0.0,"can_fail": True,"timeout": 0.0,"try_times": 1,"confidence": 0.8,"offset": "0,0"},
            {"type": "remove_folder","step_number": 2,"disabled": False,"image": "images\\screenshot_20250913_230333.png","pre_delay": 0.0,"post_delay": 0.0,"can_fail": True,"try_times": 1,"confidence": 0.8,"offset": "0,0"},
            {"type": "click","step_number": 3,"disabled": False,"image": "images\\screenshot_20250913_230333.png","pre_delay": 0.0,"post_delay": 0.0,"can_fail": True,"try_times": 1,"confidence": 0.8,"offset": "0,0"},
            {"type": "click","step_number": 4,"disabled": False,"image": "images\\screenshot_20250913_230333.png","pre_delay": 0.0,"post_delay": 0.0,"can_fail": True,"try_times": 1,"confidence": 0.8,"offset": "0,0"},
            {"type": "click","step_number": 5,"disabled": False,"image": "images\\screenshot_20250913_230333.png","pre_delay": 0.0,"post_delay": 0.0,"can_fail": True,"try_times": 1,"confidence": 0.8,"offset": "0,0"},
            {"type": "click","step_number": 6,"disabled": False,"image": "images\\screenshot_20250913_230333.png","pre_delay": 0.0,"post_delay": 0.0,"can_fail": True,"try_times": 1,"confidence": 0.8,"offset": "0,0"},
            {"type": "click","step_number": 7,"disabled": False,"image": "images\\screenshot_20250913_230333.png","pre_delay": 0.0,"post_delay": 0.0,"can_fail": True,"try_times": 1,"confidence": 0.8,"offset": "0,0"},
            {"type": "click","step_number": 8,"disabled": False,"image": "images\\screenshot_20250913_230333.png","pre_delay": 0.0,"post_delay": 0.0,"can_fail": True,"try_times": 1,"confidence": 0.8,"offset": "0,0"},
        ]
    
    def response(self, success: bool, message: str = '', data: any = {}):
        return {
            'success': success,
            'message': message,
            'data': data
        }

    def get_data(self):
        return self.data
    
    def capture_screenshot(self):
        """Capture screenshot using overlay"""
        from src.ui.screenshot_overlay import ScreenshotDialog
        from PyQt5.QtWidgets import QApplication
        import sys
        try:
            app = QApplication.instance()
            if app is None:
                app = QApplication(sys.argv)
            dialog = ScreenshotDialog()
            dialog.capture()
            if dialog.exec_():
                if dialog.result_path:
                    return self.response(success=True, message='Image saved', data={'path': dialog.result_path})
            return self.response(success=False, message='No image saved')
        except Exception as e:
            return self.response(success=False, message='Failed to capture screenshot: ' + str(e))

    def open_folder(self, path):
        """
        Open the requested file or the nearest existing parent folder.
        Falls back gracefully if the target does not exist yet (e.g. pending screenshot).
        """
        target = Path(path)
        if not target.is_absolute():
            target = (APP_ROOT / target).resolve()

        # Always open a directory – if a file was requested, use its parent folder instead.
        candidate = target if target.is_dir() else target.parent

        # Walk up the tree until we find an existing folder.
        while candidate and not candidate.exists():
            parent = candidate.parent
            if parent == candidate:
                candidate = None
                break
            candidate = parent

        if not candidate:
            return self.response(success=False, message='Could not find an existing path for: ' + path)

        try:
            os.startfile(str(candidate))
            return self.response(success=True, message=None)
        except OSError as exc:
            print(f"[open_folder] Failed to open '{candidate}': {exc}")
            return self.response(success=False, message='Failed to open: ' + str(candidate))

    def load_file(self):
        try:
            app = QApplication.instance()
            if app is None:
                app = QApplication(sys.argv)

            initial_dir = (APP_ROOT / 'json_example').resolve()
            if not initial_dir.exists():
                initial_dir = APP_ROOT

            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getOpenFileName(
                None,
                'Select JSON file',
                str(initial_dir),
                'JSON Files (*.json);;All Files (*)',
                options=options
            )

            if not file_path:
                return self.response(success=False, message='No file selected')

            with open(file_path, 'r', encoding='utf-8') as json_file:
                loaded = json.load(json_file)

            self.file_path = file_path

            return self.response(success=True, message='File loaded', data={'path': file_path, 'content': loaded})
        except Exception as exc:
            return self.response(success=False, message=f'Failed to load file: {exc}')
    
    def save_file(self, content):
        path = self.file_path
        with open(path, 'w', encoding='utf-8') as json_file:
            self.dump_one_line_objects_per_line(content, out=json_file)
        return self.response(success=True, message='File saved', data={'path': path})
    
    def export_file(self, content):
        try:
            app = QApplication.instance()
            if app is None:
                app = QApplication(sys.argv)

            initial_dir = (APP_ROOT / 'json_example').resolve()
            if not initial_dir.exists():
                initial_dir = APP_ROOT
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(
                None,
                'Export JSON file',
                str(initial_dir),
                'JSON Files (*.json)',
                options=options
            )
            if not file_path:
                return self.response(success=False, message='No file selected')
            if not file_path.endswith('.json'):
                file_path += '.json'
            if not os.path.exists(os.path.dirname(file_path)):
                os.makedirs(os.path.dirname(file_path))

            with open(file_path, 'w', encoding='utf-8') as json_file:
                self.dump_one_line_objects_per_line(content, out=json_file)
            return self.response(success=True, message='File exported', data={'path': file_path})
        except Exception as exc:
            return self.response(success=False, message=f'Failed to export file: {exc}')
        
    def dump_one_line_objects_per_line(self, obj, indent=0, out=None):
        class PathEncoder(json.JSONEncoder):
            def default(self, obj):
                return super().default(obj)

            def encode(self, obj):
                if isinstance(obj, str):
                    # Preserve single backslashes in paths
                    return f'"{obj}"'
                return super().encode(obj)

        pad = " " * indent
        if isinstance(obj, dict):
            out.write("{\n")
            items = list(obj.items())
            for i, (k, v) in enumerate(items):
                out.write(
                    pad
                    + "  "
                    + json.dumps(k, ensure_ascii=False, cls=PathEncoder)
                    + ": "
                )
                if isinstance(v, list):
                    out.write("[\n")
                    for j, item in enumerate(v):
                        out.write(pad + "    ")
                        if isinstance(item, dict):
                            out.write(
                                json.dumps(
                                    item,
                                    ensure_ascii=False,
                                    separators=(",", ": "),
                                    cls=PathEncoder,
                                )
                            )
                        else:
                            out.write(
                                json.dumps(item, ensure_ascii=False, cls=PathEncoder)
                            )
                        if j < len(v) - 1:
                            out.write(",")
                        out.write("\n")
                    out.write(pad + "  ]")
                else:
                    out.write(json.dumps(v, ensure_ascii=False, cls=PathEncoder))
                if i < len(items) - 1:
                    out.write(",")
                out.write("\n")
            out.write(pad + "}")
        else:
            out.write(json.dumps(obj, ensure_ascii=False, cls=PathEncoder))

APP_ROOT = Path(__file__).parent
ENTRY = APP_ROOT / 'index.html'

def boot(window: webview.Window):
    entry_uri = ENTRY.resolve().as_uri()
    window.load_url(entry_uri)

def main():
    global _webview_window
    
    #Arguments
    test = False
    width = 800
    height = 800
    if "--test" in sys.argv:
        test = True
    if "--width" in sys.argv:
        width = int(sys.argv[sys.argv.index("--width") + 1])
    if "--height" in sys.argv:
        height = int(sys.argv[sys.argv.index("--height") + 1])

    print("Qt UI Manager started and ready")

    #Webview window
    api = API()
    loading_html = """
        <!doctype html><html><head>
        <meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
        <style>
        html,body{height:100%;margin:0;background:#fff;font:14px system-ui}
        .center{height:100%;display:grid;place-items:center}
        .spinner{width:32px;height:32px;border:3px solid #ddd;border-top-color:#555;border-radius:50%;animation:spin 1s linear infinite}
        @keyframes spin{to{transform:rotate(360deg)}}
        </style>
        </head><body><div class="center"><div class="spinner"></div></div></body></html>
    """
    _webview_window = webview.create_window(
        title='Seemyclick',
        width=width,
        height=height,
        resizable=True,
        background_color='#FFFFFF',
        html=loading_html,
        js_api=api
    )
    webview.start(func=boot, args=(_webview_window,), gui='edgechromium', http_server=True, private_mode=False, debug=test)

if __name__ == '__main__':
    main()