from logger import Logger

from PySide2.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QHeaderView
from PySide2.QtGui import QFont
from PySide2.QtCore import Qt

class TableBase(QWidget):
    # name - string - Name of the table to be used for a QLabel above the table
    # vrows_count - int - Number of virtual rows
    # vrows_sizes - list[int] - Size of each virtual row, as a number of Qt rows that it takes up
    # qcols_count - int - Number of Qt columns
    # qcols_labels - list[string] - Labels of each Qt column
    # qcols_resize_modes - list[QHeaderView.Stretch / QHeaderView.ResizeToContents] - Resize modes of each Qt column
    # objs_map - dict{ int -> any } - Maps virtual rows to objects of any type
    # viewer_callbacks - list[func : any -> string] - Functions for retrieving the string content of each column.
    #                    Each function can be called on each object from the map to get a string from it for the corresponding column
    # deleter_callback - func : int -> None - Function to be called with an object's ID if the object is deleted in UI
    # updater_callback - func : int, int, string -> bool - Function to be called with an object's ID, column index and cell's updated string
    #                    if the object is updated in UI. Function should return true if the update was successful,
    #                    and false if the requested string value is invalid for that column meaning that it should be reverted to old value in UI
    def __init__(self, name, vrows_count, vrows_sizes, qcols_count, qcols_labels, qcols_resize_modes, objs_map, viewer_callbacks, deleter_callback, updater_callback):
        super().__init__()
        self.init_constants()

        self.name = name
        self.vrows_count = vrows_count
        self.vrows_sizes = vrows_sizes
        self.qcols_count = qcols_count
        self.qcols_labels = qcols_labels
        self.qcols_resize_modes = qcols_resize_modes
        self.objs_map = objs_map
        self.viewer_callbacks = viewer_callbacks
        self.deleter_callback = deleter_callback
        self.updater_callback = updater_callback
        self.validate()

        self.qrows_count = sum(self.vrows_sizes)
        self.create_ui()

    def init_constants(self):
        self.FONT = QFont("Verdana", 12)
        self.STYLESHEET = """
            QTableWidget {
                background-color: #f0f0f0;
                alternate-background-color: #e0e0e0;
                selection-background-color: #a0a0a0;
            }
            QHeaderView::section {
                background-color: #606060;
                color: white;
                font-size: """ + str(self.FONT.pointSize()) + """pt;
            }
        """

    def validate(self):
        if self.vrows_count < 1:
            Logger.log_error("TableBase created with vrows_count < 1")
        if len(self.vrows_sizes) != self.vrows_count:
            Logger.log_error("in TableBase the given vrows_sizes list doesn't match the vrows_count. It will be forced to match.")
            if len(self.vrows_sizes) < self.vrows_count:
                self.vrows_sizes += [1] * (self.vrows_count - len(self.vrows_sizes))
            else:
                self.vrows_sizes = self.vrows_sizes[:self.vrows_count]
        if self.qcols_count < 1:
            Logger.log_error("TableBase created with qcols_count < 1")
        if len(self.qcols_labels) != self.qcols_count:
            Logger.log_error("TableBase created with qcols_labels list that doesn't match the qcols_count. It will be forced to match.")
            if len(self.qcols_labels) < self.qcols_count:
                self.qcols_labels += [""] * (self.qcols_count - len(self.qcols_labels))
            else:
                self.qcols_labels = self.qcols_labels[:self.qcols_count]
        if len(self.qcols_resize_modes) != self.qcols_count:
            Logger.log_error("TableBase created with qcols_resize_modes list that doesn't match the qcols_count. It will be forced to match.")
            if len(self.qcols_resize_modes) < self.qcols_count:
                self.qcols_resize_modes += [QHeaderView.Stretch] * (self.qcols_count - len(self.qcols_resize_modes))
            else:
                self.qcols_resize_modes = self.qcols_resize_modes[:self.qcols_count]
        for vrow_idx, obj in self.objs_map.items():
            if vrow_idx < 0 or vrow_idx >= self.vrows_count:
                Logger.log_error("TableBase created with objs_map containing an entry with a vrow_idx out of bounds.")
            if obj is None:
                Logger.log_error("TableBase created with objs_map containing a None object")
        if len(self.viewer_callbacks) != self.qcols_count:
            Logger.log_error("TableBase created with viewer_callbacks list that doesn't match the qcols_count. It will be forced to match.")
            if len(self.viewer_callbacks) < self.qcols_count:
                self.viewer_callbacks += [lambda x : "missing viewer"] * (self.qcols_count - len(self.viewer_callbacks))
            else:
                self.viewer_callbacks = self.viewer_callbacks[:self.qcols_count]
        if self.deleter_callback is None:
            Logger.log_error("TableBase created with deleter_callback that is None")
        if self.updater_callback is None:
            Logger.log_error("TableBase created with updater_callback that is None")

    def get_qrow_idx(self, vrow_idx):
        return sum(self.vrows_sizes[:vrow_idx])

    def get_vrow_idx(self, qrow_idx):
        if qrow_idx < 0 or qrow_idx >= self.qrows_count:
            Logger.log_error("in TableBase trying to get_vrow_idx() with a qrow_idx out of bounds.")
            return -1
        qrow_sum = 0
        for vrow_idx, vrow_size in enumerate(self.vrows_sizes):
            qrow_sum += vrow_size
            if qrow_sum > qrow_idx:
                return vrow_idx
        Logger.log_error("in TableBase cannot find vrow_idx in get_vrow_idx(). Something wrong with vrow/qrow logic.")
        return -1

    def create_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.label = QLabel(self.name)
        self.label.setFont(self.FONT)
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(self.label)

        self.create_table()
        self.fill_table()

    def create_table(self):
        self.table = QTableWidget(self.qrows_count, self.qcols_count)
        self.table.setHorizontalHeaderLabels(self.qcols_labels)
        for qcol_idx, resize_mode in enumerate(self.qcols_resize_modes):
            self.table.horizontalHeader().setSectionResizeMode(qcol_idx, resize_mode)
        self.table.verticalHeader().hide()
        self.table.setStyleSheet(self.STYLESHEET)
        self.table.setFont(self.FONT)
        self.layout.addWidget(self.table)

        qrow_idx = 0
        for _, vrow_size in enumerate(self.vrows_sizes):
            if vrow_size > 1:
                for qcol_idx in range(self.qcols_count):
                    self.table.setSpan(qrow_idx, qcol_idx, vrow_size, 1)
            qrow_idx += vrow_size
        if qrow_idx != self.qrows_count:
            Logger.log_error("in TableBase qrow_idx doesn't match qrows_count after initializing the spans")

    def fill_table(self):
        self.cells_cache = [[""] * self.qcols_count for _ in range(self.qrows_count)]
        for vrow_idx, obj in self.objs_map.items():
            for qcol_idx, viewer_callback in enumerate(self.viewer_callbacks):
                obj_view = viewer_callback(obj)
                qrow_idx = self.get_qrow_idx(vrow_idx)
                self.set_item(qrow_idx, qcol_idx, obj_view)
        self.table.cellChanged.connect(self.on_cell_changed)

    def set_item(self, qrow, qcol, str_value):
        self.cells_cache[qrow][qcol] = str_value
        widget_item = QTableWidgetItem(str_value)
        widget_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.table.setItem(qrow, qcol, widget_item)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            self.delete_selected_row()
        else:
            super().keyPressEvent(event)

    def delete_selected_row(self):
        selected_items = self.table.selectedItems()
        if selected_items:
            qrow = selected_items[0].row()
            for qcol in range(self.table.columnCount()):
                self.set_item(qrow, qcol, "")
            vrow = self.get_vrow_idx(qrow)
            if vrow in self.objs_map:
                deleted_obj_id = self.objs_map[vrow].id
                self.deleter_callback(deleted_obj_id)

    def on_cell_changed(self, qrow, qcol):
        item = self.table.item(qrow, qcol)
        do_revert = True
        if item:
            if item.text() == self.cells_cache[qrow][qcol]:
                return
            vrow = self.get_vrow_idx(qrow)
            if vrow in self.objs_map:
                updated_obj_id = self.objs_map[vrow].id
                if self.updater_callback(updated_obj_id, qcol, item.text()):
                    self.cells_cache[qrow][qcol] = item.text()
                    do_revert = False
        if do_revert:
            self.set_item(qrow, qcol, self.cells_cache[qrow][qcol])

    def set_spacing_and_margin(self, spacing, ml, mu, mr, md):
        self.layout.setSpacing(spacing)
        self.layout.setContentsMargins(ml, mu, mr, md)