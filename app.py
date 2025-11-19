import webview
import os
import sys
from pathlib import Path


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
        
    def get_data(self):
        return self.data
    
    def capture_screenshot(self):
        pass


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