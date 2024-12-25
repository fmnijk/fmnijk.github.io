import sys
from pathlib import Path
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QVBoxLayout, 
                             QWidget, QMenu, QSizePolicy)
from PySide6.QtGui import QPixmap, QKeyEvent, QWheelEvent, QMouseEvent, QAction
from PySide6.QtCore import Qt, QSize, QPoint, QRect

class InfoLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            background-color: rgba(0, 0, 0, 180);
            color: white;
            padding: 5px;
            font-size: 28px;
        """)
        self.setAlignment(Qt.AlignLeft)
        self.setMinimumHeight(50)

class ImageLabel(QLabel):
    def __init__(self, info_label):
        super().__init__()
        self.setStyleSheet("background-color: black;")
        self.setAlignment(Qt.AlignCenter)
        self._zoom = 1.0
        self._empty = True
        self._drag_start = None
        self._view_offset = QPoint(0, 0)
        self._info_label = info_label
        self._use_soften = True
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_context_menu)
        
    def _show_context_menu(self, pos):
        menu = QMenu(self)
        menu.setStyleSheet("QMenu { background-color: black; color: white; } QMenu::item:selected { background-color: #404040; }")
        no_filter = QAction("No Filter", self, checkable=True)
        no_filter.setChecked(not self._use_soften)
        soften = QAction("Soften", self, checkable=True)
        soften.setChecked(self._use_soften)
        
        no_filter.triggered.connect(lambda: self._set_soften(False))
        soften.triggered.connect(lambda: self._set_soften(True))
        
        menu.addAction(no_filter)
        menu.addAction(soften)
        menu.exec(self.mapToGlobal(pos))
        
    def _set_soften(self, soften):
        if self._use_soften != soften:
            self._use_soften = soften
            self._update_pixmap()
        
    def set_pixmap(self, pixmap, keep_state=False):
        self._empty = False
        self._original_pixmap = pixmap
        if not keep_state:
            self._zoom = 1.0
            self._view_offset = QPoint(0, 0)
        self._update_pixmap()
        
    def wheelEvent(self, event: QWheelEvent):
        if self._empty:
            return
        
        mouse_pos = event.position()
        rel_x = (self._view_offset.x() + mouse_pos.x()) / (self.scaled_pixmap.width())
        rel_y = (self._view_offset.y() + mouse_pos.y()) / (self.scaled_pixmap.height())
        
        old_zoom = self._zoom
        self._zoom *= 1.1 if event.angleDelta().y() > 0 else 0.9
        self._zoom = max(0.01, min(self._zoom, 100.0))
        
        if old_zoom != self._zoom:
            self._update_pixmap()
            
            new_x = int(rel_x * self.scaled_pixmap.width() - mouse_pos.x())
            new_y = int(rel_y * self.scaled_pixmap.height() - mouse_pos.y())
            self._update_offset(new_x, new_y)
        
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton and self._zoom > 1.0:
            self._drag_start = event.position().toPoint()
            self.setCursor(Qt.ClosedHandCursor)

    def mouseReleaseEvent(self, event: QMouseEvent):
        self._drag_start = None
        self.unsetCursor()
        
    def mouseMoveEvent(self, event: QMouseEvent):
        if self._drag_start and self._zoom > 1.0:
            delta = event.position().toPoint() - self._drag_start
            new_x = self._view_offset.x() - delta.x()
            new_y = self._view_offset.y() - delta.y()
            self._update_offset(new_x, new_y)
            self._drag_start = event.position().toPoint()
            
    def _update_offset(self, x, y):
        max_x = max(0, self.scaled_pixmap.width() - self.width())
        max_y = max(0, self.scaled_pixmap.height() - self.height())
        self._view_offset = QPoint(
            max(0, min(max_x, x)),
            max(0, min(max_y, y))
        )
        self._show_current_view()
        
    def _update_pixmap(self):
        if self._empty:
            return
            
        base_scale_w = self.width() / self._original_pixmap.width()
        base_scale_h = self.height() / self._original_pixmap.height()
        base_scale = min(base_scale_w, base_scale_h)
        
        total_scale = base_scale * self._zoom
        scaled_width = int(self._original_pixmap.width() * total_scale)
        scaled_height = int(self._original_pixmap.height() * total_scale)
        
        transform_mode = Qt.SmoothTransformation if self._use_soften else Qt.FastTransformation
        
        self.scaled_pixmap = self._original_pixmap.scaled(
            scaled_width,
            scaled_height,
            Qt.KeepAspectRatio,
            transform_mode
        )
        
        self._show_current_view()
        
    def _show_current_view(self):
        if hasattr(self, 'scaled_pixmap'):
            view = self.scaled_pixmap.copy(
                self._view_offset.x(),
                self._view_offset.y(),
                min(self.width(), self.scaled_pixmap.width()),
                min(self.height(), self.scaled_pixmap.height())
            )
            super().setPixmap(view)
            
            actual_scale = self.scaled_pixmap.width() / self._original_pixmap.width() * 100
            
            view_width = view.width()
            view_height = view.height()
            
            rel_x = self._view_offset.x() / max(0.1, (self.scaled_pixmap.width() - view_width)) * 100
            rel_y = self._view_offset.y() / max(0.1, (self.scaled_pixmap.height() - view_height)) * 100
            
            if self.scaled_pixmap.width() <= view_width:
                rel_x = 50
            if self.scaled_pixmap.height() <= view_height:
                rel_y = 50
                
            self._info_label.setText(
                f"Zoom: {actual_scale:.0f}%\n"
                f"Position: ({rel_x:.0f}%, {rel_y:.0f}%)"
            )

class PhotoViewer(QMainWindow):
    def __init__(self, path):
        super().__init__()
        self.setWindowTitle("Photo Viewer")
        self.setStyleSheet("background-color: black;")
        self.setMinimumSize(200, 200)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        self.info_label = InfoLabel()
        self.image_label = ImageLabel(self.info_label)
        
        layout.addWidget(self.image_label)
        layout.addWidget(self.info_label)
        
        path = Path(path).resolve()
        if not path.exists():
            self.image_label.setText(f"Path not found: {path}")
            return
            
        self.images = []
        search_path = path if path.is_dir() else path.parent
        for ext in ('*.jpg', '*.jpeg', '*.png', '*.gif'):
            self.images.extend(str(p) for p in search_path.glob(ext))
        
        if not self.images:
            self.image_label.setText(f"No images found in: {search_path}")
            return
            
        self.current_index = self.images.index(str(path)) if path.is_file() else 0
        self.show_image()
    
    def show_image(self):
        pixmap = QPixmap(self.images[self.current_index])
        self.image_label.set_pixmap(pixmap, keep_state=True)
        
    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, 'image_label'):
            self.image_label._update_pixmap()
        
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Left:
            self.current_index = (self.current_index - 1) % len(self.images)
            self.show_image()
        elif event.key() == Qt.Key_Right:
            self.current_index = (self.current_index + 1) % len(self.images)
            self.show_image()
        elif event.key() == Qt.Key_Home:
            self.current_index = 0
            self.show_image()
        elif event.key() == Qt.Key_End:
            self.current_index = len(self.images) - 1
            self.show_image()
        elif event.key() == Qt.Key_Escape:
            self.close()
        elif (event.key() == Qt.Key_0 and 
              (event.modifiers() == Qt.ControlModifier or 
               (event.modifiers() == Qt.KeypadModifier | Qt.ControlModifier))):
            self.image_label._zoom = 1.0
            self.image_label._view_offset = QPoint(0, 0)
            self.image_label._update_pixmap()

import os
from PySide6.QtCore import Qt
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QApplication

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("""
Photo Viewer Usage:
   python script.py <path>
   path: Image file or directory containing images

Controls:
   Mouse:
       Left Click + Drag: Pan image when zoomed
       Right Click: Show filter menu
       Scroll Wheel: Zoom in/out
   
   Keyboard:
       Left/Right: Previous/Next image
       Home/End: First/Last image
       Ctrl+0: Reset zoom to fit
       Esc: Exit viewer
       
Supported formats: jpg, jpeg, png, gif
""")
        sys.exit(1)
    
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
    os.environ["QT_SCALE_FACTOR"] = "1"

    app = QApplication(sys.argv)
    app.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    viewer = PhotoViewer(sys.argv[1])
    viewer.show()

    sys.exit(app.exec())
