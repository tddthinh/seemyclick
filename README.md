# ParamQuery Grid - PyWebView Desktop Application

A desktop application built with PyWebView that demonstrates an editable ParamQuery grid with bidirectional communication between Python backend and JavaScript frontend.

## Features

- ✅ **Editable Grid**: Double-click cells to edit data
- ✅ **Sorting & Filtering**: Built-in column sorting and filtering
- ✅ **Add/Delete Rows**: Add new rows or delete selected rows
- ✅ **Bidirectional Communication**: Python ↔ JavaScript data synchronization
- ✅ **Modern UI**: Beautiful gradient design with smooth animations
- ✅ **Local Dependencies**: All libraries bundled locally (no internet required)

## Project Structure

```
testpywebview/
├── app.py                      # Python backend with API
├── index.html                  # HTML frontend with ParamQuery grid
├── requirements.txt            # Python dependencies
├── assets/
│   ├── js/
│   │   ├── jquery-3.7.1.min.js
│   │   ├── jquery-ui.min.js
│   │   └── pqgrid.min.js
│   └── css/
│       ├── jquery-ui.css
│       ├── pqgrid.min.css
│       └── pqgrid.ui.min.css
└── README.md
```

## Installation

1. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Verify dependencies** (all JS/CSS files should be in `assets/` folder):
   - The required JavaScript and CSS libraries are already downloaded in the `assets/` directory

## Usage

1. **Run the application**:
   ```bash
   python app.py
   ```

2. **Use the grid**:
   - **Edit cells**: Double-click any cell to edit (except ID column)
   - **Add row**: Click "➕ Add Row" button to add a new row
   - **Delete row**: Select a row and click "🗑️ Delete Selected" button
   - **Refresh**: Click "🔄 Refresh Data" to reload data from Python backend
   - **Sort**: Click column headers to sort
   - **Filter**: Use the filter inputs in column headers

## Python API Methods

The Python backend exposes the following methods to JavaScript:

### `get_data()`
Returns the current grid data as a list of dictionaries.

```python
# Returns: [{'id': 1, 'company': '...', 'revenues': ..., 'profits': ...}, ...]
```

### `update_row(row_index, row_data)`
Updates a row in the data.

```python
# Parameters:
#   - row_index (int): Index of the row to update
#   - row_data (dict): Updated row data
# Returns: {'success': True/False, 'message': '...'}
```

### `add_row(row_data)`
Adds a new row to the data.

```python
# Parameters:
#   - row_data (dict): New row data
# Returns: {'success': True/False, 'message': '...', 'row': {...}}
```

### `delete_row(row_index)`
Deletes a row by index.

```python
# Parameters:
#   - row_index (int): Index of the row to delete
# Returns: {'success': True/False, 'message': '...'}
```

### `delete_row_by_id(row_id)`
Deletes a row by ID.

```python
# Parameters:
#   - row_id (int): ID of the row to delete
# Returns: {'success': True/False, 'message': '...'}
```

## JavaScript API Usage

From JavaScript, call Python methods using `pywebview.api`:

```javascript
// Get data
const data = await pywebview.api.get_data();

// Update row
const result = await pywebview.api.update_row(0, {
    id: 1,
    company: 'Updated Company',
    revenues: 100000,
    profits: 5000
});

// Add row
const result = await pywebview.api.add_row({
    company: 'New Company',
    revenues: 50000,
    profits: 2000
});

// Delete row
const result = await pywebview.api.delete_row_by_id(1);
```

## Technologies Used

- **Backend**: Python 3.x with PyWebView
- **Frontend**: 
  - jQuery 3.7.1
  - jQuery UI 1.12.1
  - ParamQuery Grid (free version)
- **UI**: Custom CSS with gradient design

## Customization

### Modify Grid Columns

Edit the `colModel` array in `index.html` to add/remove/modify columns:

```javascript
const colModel = [
    { 
        title: "Column Title", 
        dataIndx: "fieldName", 
        width: 150,
        dataType: "string",
        editable: true
    },
    // Add more columns...
];
```

### Change Initial Data

Modify the `self.data` array in the `API.__init__()` method in `app.py`.

### Customize Window Size

Edit the `width` and `height` parameters in `webview.create_window()` in `app.py`:

```python
window = webview.create_window(
    title='Your Title',
    url='index.html',
    js_api=api,
    width=1400,  # Change width
    height=900,  # Change height
    resizable=True
)
```

## Troubleshooting

### PyWebView not starting
- Ensure you have installed pywebview: `pip install pywebview`
- On Windows, pywebview uses Edge WebView2 runtime (usually pre-installed)
- On Linux, you may need to install additional dependencies

### Grid not displaying
- Check browser console for JavaScript errors
- Ensure all files in `assets/` directory are present
- Verify that `pywebviewready` event is firing

### Data not syncing
- Check Python console for error messages
- Ensure JavaScript is calling `pywebview.api` methods correctly
- Verify that API methods are returning proper response format

## License

This project is provided as a sample/demo application. ParamQuery Grid is subject to its own license terms.

## References

- [PyWebView Documentation](https://pywebview.flowrl.com/)
- [ParamQuery Grid Tutorial](https://paramquery.com/tutorial/index#topic-firstgrid)
- [jQuery Documentation](https://jquery.com/)
- [jQuery UI Documentation](https://jqueryui.com/)

