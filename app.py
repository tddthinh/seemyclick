import webview
import json
import os


# Set WebView2 user data folder to avoid permission issues
webview_data_dir = os.path.join(os.getcwd(), 'webview_data')
os.makedirs(webview_data_dir, exist_ok=True)
os.environ['WEBVIEW2_USER_DATA_FOLDER'] = webview_data_dir


class API:
    def __init__(self):
        self.data = [
            {"type": "click","step_number": 1,"disabled": True,"image": "images\\screenshot_20250913_230333.png","pre_delay": 0.0,"post_delay": 0.0,"can_fail": True,"try_times": 1,"confidence": 0.8,"offset": "0,0"},
            {"type": "click","step_number": 2,"disabled": False,"image": "images\\screenshot_20250913_230333.png","pre_delay": 0.0,"post_delay": 0.0,"can_fail": True,"try_times": 1,"confidence": 0.8,"offset": "0,0"},
            {"type": "click","step_number": 3,"disabled": False,"image": "images\\screenshot_20250913_230333.png","pre_delay": 0.0,"post_delay": 0.0,"can_fail": True,"try_times": 1,"confidence": 0.8,"offset": "0,0"},
            {"type": "click","step_number": 4,"disabled": False,"image": "images\\screenshot_20250913_230333.png","pre_delay": 0.0,"post_delay": 0.0,"can_fail": True,"try_times": 1,"confidence": 0.8,"offset": "0,0"},
            {"type": "click","step_number": 5,"disabled": False,"image": "images\\screenshot_20250913_230333.png","pre_delay": 0.0,"post_delay": 0.0,"can_fail": True,"try_times": 1,"confidence": 0.8,"offset": "0,0"},
            {"type": "click","step_number": 6,"disabled": False,"image": "images\\screenshot_20250913_230333.png","pre_delay": 0.0,"post_delay": 0.0,"can_fail": True,"try_times": 1,"confidence": 0.8,"offset": "0,0"},
            {"type": "click","step_number": 7,"disabled": False,"image": "images\\screenshot_20250913_230333.png","pre_delay": 0.0,"post_delay": 0.0,"can_fail": True,"try_times": 1,"confidence": 0.8,"offset": "0,0"},
            {"type": "click","step_number": 8,"disabled": False,"image": "images\\screenshot_20250913_230333.png","pre_delay": 0.0,"post_delay": 0.0,"can_fail": True,"try_times": 1,"confidence": 0.8,"offset": "0,0"},
        ]
        self.next_id = 11
    
    def get_data(self):
        print(f"Python: get_data called, returning {len(self.data)} rows")
        return self.data
    
    def update_row(self, row_index, row_data):
        try:
            print(f"Python: update_row called with index={row_index}, data={row_data}")
            
            # Find and update the row by ID
            row_id = row_data.get('id')
            if row_id:
                for i, item in enumerate(self.data):
                    if item['id'] == row_id:
                        self.data[i] = row_data
                        print(f"Python: Row with id={row_id} updated successfully")
                        return {'success': True, 'message': 'Row updated successfully'}
            else:
                # If no ID, use index
                if 0 <= row_index < len(self.data):
                    self.data[row_index] = row_data
                    print(f"Python: Row at index={row_index} updated successfully")
                    return {'success': True, 'message': 'Row updated successfully'}
            
            return {'success': False, 'message': 'Row not found'}
        except Exception as e:
            print(f"Python: Error updating row: {e}")
            return {'success': False, 'message': str(e)}
    
    def add_row(self, row_data):
        try:
            print(f"Python: add_row called with data={row_data}")

            if 'id' not in row_data or row_data['id'] is None:
                row_data['id'] = self.next_id
                self.next_id += 1
            
            self.data.append(row_data)
            print(f"Python: Row added successfully, new row count: {len(self.data)}")
            return {'success': True, 'message': 'Row added successfully', 'row': row_data}
        except Exception as e:
            print(f"Python: Error adding row: {e}")
            return {'success': False, 'message': str(e)}
    
    def delete_row(self, row_index):
        try:
            print(f"Python: delete_row called with index={row_index}")
            
            if 0 <= row_index < len(self.data):
                deleted_row = self.data.pop(row_index)
                print(f"Python: Row deleted successfully: {deleted_row}")
                return {'success': True, 'message': 'Row deleted successfully'}
            else:
                return {'success': False, 'message': 'Invalid row index'}
        except Exception as e:
            print(f"Python: Error deleting row: {e}")
            return {'success': False, 'message': str(e)}
    
    def delete_row_by_id(self, row_id):
        try:
            print(f"Python: delete_row_by_id called with id={row_id}")
            
            for i, item in enumerate(self.data):
                if item['id'] == row_id:
                    deleted_row = self.data.pop(i)
                    print(f"Python: Row with id={row_id} deleted successfully: {deleted_row}")
                    return {'success': True, 'message': 'Row deleted successfully'}
            
            return {'success': False, 'message': 'Row not found'}
        except Exception as e:
            print(f"Python: Error deleting row: {e}")
            return {'success': False, 'message': str(e)}


def main():
    """Main function to initialize and start the pywebview application."""
    api = API()
    
    # Create the webview window
    window = webview.create_window(
        title='Seemymacro',
        url='index.html',
        js_api=api,
        width=1200,
        height=800,
        resizable=True,
        background_color='#FFFFFF'
    )
    
    print("Starting PyWebView application...")
    print("Python backend is ready to communicate with JavaScript frontend")
    
    # Start the webview
    webview.start(debug=True)


if __name__ == '__main__':
    main()

