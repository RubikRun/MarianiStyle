from logger import Logger

from PySide2.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QHeaderView
from PySide2.QtGui import QFont
from PySide2.QtCore import Qt

from ui.font_changer_widget import FontGlobal

class TableBase(QWidget):
    # name - string - Name of the table to be used for a QLabel above the table
    # vrows_count - int - Number of virtual rows
    # vrows_sizes - list[int] - Size of each virtual row, as a number of Qt rows that it takes up
    # qcols_count - int - Number of Qt columns
    # qcols_labels - list[string] - Labels of each Qt column
    # qcols_resize_modes - list[QHeaderView.Stretch / QHeaderView.ResizeToContents] - Resize modes of each Qt column
    # objs_map - dict{ int -> any } - Maps virtual rows to objects of any type
    # viewer_callback - func : any, column, vrow -> string - Function for retrieving the string content of each column.
    #                    The function can be called on each object from the map and each column to get a string from it for the corresponding column
    # bg_get_color_callback - func : any, column, vrow -> QColor - Function that returns a background QColor for each object and each of its columns
    # fg_get_color_callback - func : any, column, vrow -> QColor - Function that returns a foreground QColor for each object and each of its columns
    # deleter_callback - func : int, vrow -> None - Function to be called with an object's ID if the object is deleted in UI
    # updater_callback - func : int, int, string, vrow -> bool - Function to be called with an object's ID, column index and cell's updated string
    #                    if the object is updated in UI. Function should return true if the update was successful,
    #                    and false if the requested string value is invalid for that column meaning that it should be reverted to old value in UI
    def __init__(self, name, vrows_count, vrows_sizes, qcols_count, qcols_labels, qcols_resize_modes, objs_map,
                 viewer_callback, bg_get_color_callback, fg_get_color_callback, deleter_callback, updater_callback, on_obj_selected_callback = None):
        super().__init__()
        self.init_constants()

        self.name = name
        self.vrows_count = vrows_count
        self.vrows_sizes = vrows_sizes
        self.qcols_count = qcols_count
        self.qcols_labels = qcols_labels
        self.qcols_resize_modes = qcols_resize_modes
        self.objs_map = objs_map
        self.viewer_callback = viewer_callback
        self.bg_get_color_callback = bg_get_color_callback
        self.fg_get_color_callback = fg_get_color_callback
        self.deleter_callback = deleter_callback
        self.updater_callback = updater_callback
        self.on_obj_selected_callback = on_obj_selected_callback
        self.validate()

        self.qrows_count = sum(self.vrows_sizes)
        self.create_ui()

    def init_constants(self):
        self.STYLESHEET = """
            QTableWidget {
                background-color: #f0f0f0;
                alternate-background-color: #e0e0e0;
                selection-background-color: #a0a0a0;
            }
            QHeaderView::section {
                background-color: #606060;
                color: white;
                font-size: """ + str(FontGlobal.font.pointSize()) + """pt;
            }
        """

    def validate(self):
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
        if self.viewer_callback is None:
            Logger.log_error("TableBase created with viewer_callback that is None")
        if self.bg_get_color_callback is None:
            Logger.log_error("TableBase created with bg_get_color_callback that is None")
        if self.fg_get_color_callback is None:
            Logger.log_error("TableBase created with fg_get_color_callback that is None")
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

        if self.name is not None:
            self.label = QLabel(self.name)
            self.label.setFont(FontGlobal.font)
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
        self.table.setFont(FontGlobal.font)
        self.layout.addWidget(self.table)

        qrow_idx = 0
        for _, vrow_size in enumerate(self.vrows_sizes):
            if vrow_size > 1:
                for qcol_idx in range(self.qcols_count):
                    self.table.setSpan(qrow_idx, qcol_idx, vrow_size, 1)
            qrow_idx += vrow_size
        if qrow_idx != self.qrows_count:
            Logger.log_error("in TableBase qrow_idx doesn't match qrows_count after initializing the spans")
        self.table.itemSelectionChanged.connect(self.on_selection_changed)

    def fill_table(self):
        self.cells_cache = [[""] * self.qcols_count for _ in range(self.qrows_count)]
        for qrow in range(self.qrows_count):
            for qcol in range(self.qcols_count):
                self.set_item(qrow, qcol, "")
        for vrow, obj in self.objs_map.items():
            for qcol in range(self.qcols_count):
                obj_view = self.viewer_callback(obj, qcol, vrow)
                qrow = self.get_qrow_idx(vrow)
                self.set_item(qrow, qcol, obj_view)

                bg_color = self.bg_get_color_callback(obj, qcol, vrow)
                if bg_color is not None:
                    self.set_item_color(qrow, qcol, bg_color, True)
                fg_color = self.fg_get_color_callback(obj, qcol, vrow)
                if fg_color is not None:
                    self.set_item_color(qrow, qcol, fg_color, False)
        self.table.cellChanged.connect(self.on_cell_changed)

    def set_item(self, qrow, qcol, str_value):
        self.cells_cache[qrow][qcol] = str_value
        widget_item = QTableWidgetItem(str_value)
        widget_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.table.setItem(qrow, qcol, widget_item)

    def set_item_color(self, qrow, qcol, color, bg_fg):
        item = self.table.item(qrow, qcol)
        if item:
            if bg_fg:
                item.setBackground(color)
            else:
                item.setForeground(color)

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
                try:
                    deleted_obj_id = self.objs_map[vrow].id
                    self.deleter_callback(deleted_obj_id, vrow)
                except AttributeError:
                    # The objects in the table might not have ID, in this case ignore delete functionality
                    pass

    def on_cell_changed(self, qrow, qcol):
        item = self.table.item(qrow, qcol)
        do_revert = True
        if item:
            if item.text() == self.cells_cache[qrow][qcol]:
                return
            vrow = self.get_vrow_idx(qrow)
            if vrow in self.objs_map:
                try:
                    updated_obj_id = self.objs_map[vrow].id
                    if self.updater_callback(updated_obj_id, qcol, item.text(), vrow):
                        self.cells_cache[qrow][qcol] = item.text()
                        do_revert = False
                except AttributeError:
                    # The objects in the table might not have ID, in this case ignore update functionality
                    pass
        if do_revert:
            self.set_item(qrow, qcol, self.cells_cache[qrow][qcol])

    def on_selection_changed(self):
        if self.on_obj_selected_callback is None:
            return
        selected_items = self.table.selectedItems()
        if selected_items:
            qrow = selected_items[0].row()
            vrow = self.get_vrow_idx(qrow)
            if vrow in self.objs_map:
                try:
                    selected_obj_id = self.objs_map[vrow].id
                    self.on_obj_selected_callback(selected_obj_id)
                except AttributeError:
                    # The objects in the table might not have ID, in this case ignore select functionality
                    pass

    def set_spacing_and_margin(self, spacing, ml, mu, mr, md):
        self.layout.setSpacing(spacing)
        self.layout.setContentsMargins(ml, mu, mr, md)

    # Colors the currently selected cells of the table with the given color,
    # colors their background or foreground depending on the bg_fg parameter,
    # calls the given update_color_callback function on each colored column of an object,
    # so if column "column" of object with id "id" is colored then update_color_callback(id, column) will be called.
    def color_selected_cells(self, color, bg_fg, update_color_callback):
        selected_items = self.table.selectedItems()

        if selected_items:
            for item in selected_items:
                qrow = item.row()
                qcol = item.column()
                item = self.table.item(qrow, qcol)
                if item:
                    vrow = self.get_vrow_idx(qrow)
                    if vrow in self.objs_map:
                        try:
                            updated_obj_id = self.objs_map[vrow].id
                            update_color_callback(updated_obj_id, qcol)
                        except AttributeError:
                            # The objects in the table might not have ID, in this case ignore color functionality
                            pass
                    if bg_fg:
                        item.setBackground(color)
                    else:
                        item.setForeground(color)
                else:
                    Logger.log_error("Trying to paint a cell from TableBase with the color from clicked color button but item doesn't exist")
        self.table.clearSelection()

def join_table_base(first_table: TableBase, second_table: TableBase, name: str, qcols_labels: list):
    qcols_count = first_table.qcols_count
    if first_table.qcols_count != second_table.qcols_count:
        Logger.log_error("Trying to join two TableBase's with different number of column. The smaller number will be used.")
        qcols_count = min(first_table.qcols_count, second_table.qcols_count)
    qcols_resize_modes = first_table.qcols_resize_modes
    if len(first_table.qcols_resize_modes) != len(second_table.qcols_resize_modes):
        Logger.log_error("Trying to join two TableBase's with different number of column resize modes. The smaller number will be used.")
        if len(first_table.qcols_resize_modes) > len(second_table.qcols_resize_modes):
            qcols_resize_modes = second_table.qcols_resize_modes
    else:
        for idx in range(len(first_table.qcols_resize_modes)):
            if first_table.qcols_resize_modes[idx] != second_table.qcols_resize_modes[idx]:
                Logger.log_error("Trying to join two TableBase's but some of the column resize modes are different. The ones of the first table will be used.")

    objs_map = {}
    for vrow, obj in first_table.objs_map.items():
        objs_map[vrow] = obj
    for vrow, obj in second_table.objs_map.items():
        objs_map[vrow + first_table.vrows_count] = obj

    def viewer_callback(obj, column, vrow):
        if vrow < first_table.vrows_count:
            return first_table.viewer_callback(obj, column, vrow)
        else:
            return second_table.viewer_callback(obj, column, vrow)

    bg_get_color_callback = lambda obj, column, vrow : first_table.bg_get_color_callback(obj, column, vrow) if vrow < first_table.vrows_count \
        else second_table.bg_get_color_callback(obj, column, vrow)
    fg_get_color_callback = lambda obj, column, vrow : first_table.fg_get_color_callback(obj, column, vrow) if vrow < first_table.vrows_count \
        else second_table.fg_get_color_callback(obj, column, vrow)
    deleter_callback = lambda id, vrow : first_table.deleter_callback(id, vrow) if vrow < first_table.vrows_count \
        else second_table.deleter_callback(id, vrow)
    updater_callback = lambda id, column, s, vrow : first_table.updater_callback(id, column, s, vrow) if vrow < first_table.vrows_count \
        else second_table.updater_callback(id, column, s, vrow)

    table = TableBase(
        name,
        first_table.vrows_count + second_table.vrows_count,
        first_table.vrows_sizes + second_table.vrows_sizes,
        qcols_count,
        qcols_labels,
        qcols_resize_modes,
        objs_map,
        viewer_callback,
        bg_get_color_callback,
        fg_get_color_callback,
        deleter_callback,
        updater_callback
    )
    return table