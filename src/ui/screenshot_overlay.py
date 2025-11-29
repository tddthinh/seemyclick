"""
Visual overlay for screenshot selection using PyQt5
"""
from PyQt5.QtWidgets import (QApplication, QDialog, QLabel, QLineEdit, 
                              QPushButton, QVBoxLayout, QHBoxLayout, QFrame)
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor, QFont, QImage
from PIL import ImageGrab, Image
from datetime import datetime
import os

class ModernInputDialog(QDialog):
    def __init__(self, parent, title, prompt, initial_value, x, y, preview_image=None):
        super().__init__(parent)
        self.result = None
        self.setWindowTitle(title)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground, False)
        
        self.drag_start_pos = None
        
        # Main widget with dark background
        main_widget = QFrame(self)
        main_widget.setStyleSheet("""
            QFrame {
                background-color: #2b2b2b;
                border: 1px solid #555555;
            }
        """)
        
        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(12)
        
        # Preview image if provided
        if preview_image:
            max_width = 400
            max_height = 300
            img_width, img_height = preview_image.size
            
            scale = min(max_width / img_width, max_height / img_height, 1.0)
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)
            
            thumbnail = preview_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Convert PIL image to QPixmap
            img_bytes = thumbnail.tobytes()
            qimage = QImage(img_bytes, thumbnail.width, thumbnail.height, 
                          thumbnail.width * 3, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qimage)
            
            img_label = QLabel()
            img_label.setPixmap(pixmap)
            img_label.setStyleSheet("border: 1px solid #555555;")
            img_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(img_label)
        
        # Prompt label
        label = QLabel(prompt)
        label.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-family: 'Segoe UI';
                font-size: 10pt;
                background: transparent;
            }
        """)
        layout.addWidget(label)
        
        # Input field
        self.entry = QLineEdit(initial_value)
        self.entry.setStyleSheet("""
            QLineEdit {
                background-color: #3c3c3c;
                color: #ffffff;
                font-family: 'Segoe UI';
                font-size: 10pt;
                border: 1px solid #555555;
                padding: 6px;
            }
            QLineEdit:focus {
                border: 1px solid #0078d4;
            }
        """)
        self.entry.setMinimumWidth(350)
        self.entry.selectAll()
        self.entry.setFocus()
        layout.addWidget(self.entry)
        
        # Button layout
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        # Save button
        ok_btn = QPushButton('Save')
        ok_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: #ffffff;
                font-family: 'Segoe UI';
                font-size: 9pt;
                font-weight: bold;
                border: none;
                padding: 6px 20px;
                cursor: pointer;
            }
            QPushButton:hover {
                background-color: #1084d8;
            }
        """)
        ok_btn.setCursor(Qt.PointingHandCursor)
        ok_btn.clicked.connect(self.ok)
        btn_layout.addWidget(ok_btn)
        
        # Cancel button
        cancel_btn = QPushButton('Cancel')
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #3c3c3c;
                color: #ffffff;
                font-family: 'Segoe UI';
                font-size: 9pt;
                border: none;
                padding: 6px 20px;
                cursor: pointer;
            }
            QPushButton:hover {
                background-color: #4c4c4c;
            }
        """)
        cancel_btn.setCursor(Qt.PointingHandCursor)
        cancel_btn.clicked.connect(self.cancel)
        btn_layout.addWidget(cancel_btn)
        
        layout.addLayout(btn_layout)
        
        # Set the main layout
        dialog_layout = QVBoxLayout(self)
        dialog_layout.setContentsMargins(0, 0, 0, 0)
        dialog_layout.addWidget(main_widget)
        
        # Position the dialog
        self.adjustSize()
        screen = QApplication.desktop().screenGeometry()
        
        pos_x = min(x, screen.width() - self.width() - 10)
        pos_y = min(y, screen.height() - self.height() - 10)
        pos_x = max(10, pos_x)
        pos_y = max(10, pos_y)
        
        self.move(pos_x, pos_y)
        
        # Connect Enter/Escape keys
        self.entry.returnPressed.connect(self.ok)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_pos = event.globalPos() - self.frameGeometry().topLeft()
    
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.drag_start_pos:
            self.move(event.globalPos() - self.drag_start_pos)
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.cancel()
        else:
            super().keyPressEvent(event)
    
    def ok(self):
        self.result = self.entry.text()
        self.accept()
    
    def cancel(self):
        self.result = None
        self.reject()
class ScreenshotDialog(QDialog):
    """Internal dialog class that does the actual screenshot UI"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowState(Qt.WindowFullScreen)
        self.setCursor(Qt.CrossCursor)
        
        # Take screenshot before showing overlay
        self.screenshot = ImageGrab.grab()
        
        self.start_pos = None
        self.current_pos = None
        self.result_path = None
        

    
    def capture(self):
        self.show()
        self.raise_()
        self.activateWindow()

    def mousePressEvent(self, event):
        """Start selection"""
        if event.button() == Qt.LeftButton:
            self.start_pos = event.pos()
            self.current_pos = event.pos()
            self.update()
        elif event.button() == Qt.RightButton:
            self.on_right_click()
    
    def mouseMoveEvent(self, event):
        """Update selection rectangle"""
        if self.start_pos:
            self.current_pos = event.pos()
            self.update()
    
    def mouseReleaseEvent(self, event):
        """Complete selection and save"""
        if event.button() == Qt.LeftButton and self.start_pos:
            x1 = min(self.start_pos.x(), event.pos().x())
            y1 = min(self.start_pos.y(), event.pos().y())
            x2 = max(self.start_pos.x(), event.pos().x())
            y2 = max(self.start_pos.y(), event.pos().y())
            
            if abs(x2 - x1) > 5 and abs(y2 - y1) > 5:
                cropped = self.screenshot.crop((x1, y1, x2, y2))
                
                self.hide()
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                
                dialog = ModernInputDialog(
                    None,
                    "Save Screenshot",
                    "Enter filename:",
                    f'screenshot_{timestamp}',
                    event.globalPos().x(),
                    event.globalPos().y(),
                    preview_image=cropped
                )
                
                dialog.exec_()
                filename = dialog.result
                
                if filename:
                    if not filename.endswith('.png'):
                        filename += '.png'
                    
                    os.makedirs('images', exist_ok=True)
                    filepath = f'images/{filename}'
                    cropped.save(filepath)
                    self.result_path = filepath
            
            self.accept()
    
    def on_right_click(self):
        """Reset selection or cancel if no selection"""
        if self.start_pos is None:
            self.result_path = None
            self.reject()
        else:
            self.start_pos = None
            self.current_pos = None
            self.update()
    
    def keyPressEvent(self, event):
        """Cancel on Escape"""
        if event.key() == Qt.Key_Escape:
            self.result_path = None
            self.reject()
    
    def paintEvent(self, event):
        """Draw selection rectangle and info text with transparent overlay"""
        painter = QPainter(self)
        
        # Draw semi-transparent dark overlay over entire screen
        painter.fillRect(self.rect(), QColor(0, 0, 0, 100))
        
        if self.start_pos and self.current_pos:
            # Draw selection rectangle
            rect = QRect(self.start_pos, self.current_pos).normalized()
            
            # Clear the selection area (make it transparent to show original screen)
            painter.setCompositionMode(QPainter.CompositionMode_Clear)
            painter.fillRect(rect, Qt.transparent)
            painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
            
            # Draw red outline around selection
            pen = QPen(QColor(255, 0, 0), 2)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)
            painter.drawRect(rect)
            
            # Draw info text
            width = abs(self.current_pos.x() - self.start_pos.x())
            height = abs(self.current_pos.y() - self.start_pos.y())
            
            info_text = f"{width} x {height} px"
            text_y = rect.top() - 25 if rect.top() > 35 else rect.bottom() + 25
            
            # Draw text background
            font = QFont('Arial', 12, QFont.Bold)
            painter.setFont(font)
            text_rect = painter.boundingRect(rect.left() + 5, text_y - 15, 200, 20, 
                                            Qt.AlignLeft, info_text)
            painter.fillRect(text_rect.adjusted(-5, -3, 5, 3), QColor(0, 0, 0, 180))
            
            # Draw text with white color
            painter.setPen(QColor(255, 255, 255))
            painter.drawText(rect.left() + 5, text_y, info_text)

