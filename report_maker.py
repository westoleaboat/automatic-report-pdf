import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from PyQt5 import QtPrintSupport as qtps



class ReportForm(qtw.QWidget):

    submitted = qtc.pyqtSignal(dict) # carry form's values

    def __init__(self):
        super().__init__()
        self.setLayout(qtw.QFormLayout())

        self.inputs = dict()
        self.inputs['Batch Name'] = qtw.QLineEdit()
        self.inputs['Batch Number'] = qtw.QLineEdit()
        self.inputs['Production Date'] = qtw.QDateEdit(
            date=qtc.QDate.currentDate(), calendarPopup=True)
        self.inputs['Production Due'] = qtw.QSpinBox(
            minimum=0, maximum=60, value=30)

        for label, widget in self.inputs.items():
            self.layout().addRow(label, widget)
        



        # Timer inside GroupBox widget
        self.timer_box = qtw.QGroupBox('Timer', self)
        self.timer_box.setCheckable(True)
        self.timer_box.setChecked(False)
        self.timer_box.setAlignment(qtc.Qt.AlignHCenter)
        self.timer_box.setFlat(False)

        # Timer layout
        timer_layout = qtw.QVBoxLayout()

        # Timer label
        self.timer_label = qtw.QLabel('00:00:00', self.timer_box)
        timer_layout.addWidget(self.timer_label)

        # Timer buttons
        self.start_button = qtw.QPushButton('Start Timer', self.timer_box, clicked=self.start_timer)
        self.stop_button = qtw.QPushButton('Stop Timer', self.timer_box, clicked=self.stop_timer)
        self.reset_button = qtw.QPushButton('Reset Timer', self.timer_box, clicked=self.reset_timer)
        timer_layout.addWidget(self.start_button)
        timer_layout.addWidget(self.stop_button)
        timer_layout.addWidget(self.reset_button)

        # Set layout for the timer group box
        self.timer_box.setLayout(timer_layout)
        self.layout().addRow(self.timer_box)

        # Timer setup
        self.timer = qtc.QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.timer_start_time = None
        self.elapsed_time = 0

        # Line items table
        self.line_items = qtw.QTableWidget(
            # rowCount=10, columnCount=3)
            rowCount=15, columnCount=3)
        self.line_items.setFixedWidth(350)
        self.line_items.setHorizontalHeaderLabels(
            ['Time', 'Description', 'Check'])
        self.line_items.horizontalHeader().setSectionResizeMode(
            1, qtw.QHeaderView.Stretch)


        
        self.layout().addRow(self.line_items)

        for row in range(self.line_items.rowCount()):
            for col in range(self.line_items.columnCount()):
                if col < 2:
                    w = qtw.QLineEdit()

                    # if col == 0:
                    #     w.setReadOnly(True)

                    self.line_items.setCellWidget(row, col, w)
                elif col == 2:
                # else:
                    w_check = qtw.QCheckBox('Time Set')
                    # self.line_items.setCellWidget(row, col, w_check)
                    w_check.stateChanged.connect(lambda state, row=row: self.on_checkbox_state_changed(state, row))
                    self.line_items.setCellWidget(row, col, w_check)



        submit = qtw.QPushButton('Generate Report', clicked=self.on_submit)
        self.layout().addRow(submit)

        # self.on_submit()

    ### TIMER
    def start_timer(self):
        if not self.timer.isActive():
            self.timer_start_time = qtc.QTime.currentTime()
            self.timer.start(1000)

    def stop_timer(self):
        if self.timer.isActive():
            self.elapsed_time += self.timer_start_time.secsTo(qtc.QTime.currentTime())
            self.timer.stop()

    def reset_timer(self):
        self.timer.stop()
        self.elapsed_time = 0
        self.timer_label.setText('00:00:00')

    def update_timer(self):
        if self.timer_start_time:
            current_time = qtc.QTime.currentTime()
            elapsed_seconds = self.elapsed_time + self.timer_start_time.secsTo(current_time)
            hours, remainder = divmod(elapsed_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.timer_label.setText(f'{hours:02}:{minutes:02}:{seconds:02}')
    
    def get_elapsed_time(self):
        if self.timer.isActive():
            current_time = qtc.QTime.currentTime()
            elapsed_seconds = self.elapsed_time + self.timer_start_time.secsTo(current_time)
            hours, remainder = divmod(elapsed_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            elapsed_time = f'{hours:02}:{minutes:02}:{seconds:02}'
        else:
            elapsed_time = self.elapsed_time
        return elapsed_time
    ###


    ### SLOT FOR CHECKBOX ###
    def on_checkbox_state_changed(self, state, row):
        
        if state == qtc.Qt.Checked:
            current_time = qtc.QTime.currentTime().toString('HH:mm:ss')
            time_widget = self.line_items.cellWidget(row, 0)
            if isinstance(time_widget, qtw.QLineEdit):
                # time_widget.setText(f"{current_time}" + "\n" + f"{self.get_elapsed_time()}")
                time_widget.setText(f"{current_time}")
                time_widget.setEnabled(False)

            # for col in range(1,2):
            #     widget = self.line_items.cellWidget(row, col)
            #     if widget:
            #         widget.setEnabled(False)

            # for col in range(self.line_items.columnCount()):
            #     self.line_items.cellWidget(row, col).setEnabled(True)

        else:
            for col in range(self.line_items.columnCount()):
                widget = self.line_items.cellWidget(row, col).setEnabled(True)
                # if widget:
                #     widget.setEnabled(True)

    def on_submit(self):
        elapsed_time = self.get_elapsed_time()
        data = {
            'b_name': self.inputs['Batch Name'].text(),
            'b_num': self.inputs['Batch Number'].text(),
            'p_date': self.inputs['Production Date'].date().toString(),
            'p_due': self.inputs['Production Date'].date().addDays(
                self.inputs['Production Due'].value()).toString(),
            'p_terms': '{} days'.format(self.inputs['Production Due'].value()),
            'elapsed_time': elapsed_time
        }


        data['line_items'] = list()

        for row in range(self.line_items.rowCount()):
             # Retrieve the job from the first column
            job_widget = self.line_items.cellWidget(row, 0)
            if isinstance(job_widget, qtw.QLineEdit):
                job = job_widget.text().strip()
            else:
                job = ''

            # Retrieve the description from the second column
            description_widget = self.line_items.cellWidget(row, 1)
            if isinstance(description_widget, qtw.QLineEdit):
                description = description_widget.text().strip()
            else:
                description = ''

            # Append the row data if either job or description has content
            if job or description:
                row_data = [job, description]
                data['line_items'].append(row_data)

        data['total_due'] = elapsed_time
        self.submitted.emit(data)


class ReportView(qtw.QTextEdit):

    dpi = 72
    doc_width = 8.5 * dpi
    doc_height = 11 * dpi

    def __init__(self):
        super().__init__(readOnly=True)
        self.setFixedSize(qtc.QSize(int(self.doc_width), int(self.doc_height)))


    def set_page_size(self, qrect):
        self.doc_width = qrect.width()
        self.doc_height = qrect.height()
        self.setFixedSize(qtc.QSize(int(self.doc_width), int(self.doc_height)))
        self.document().setPageSize(
            qtc.QSizeF(self.doc_width, self.doc_height))

    def build_report(self, data):
        document = qtg.QTextDocument()
        self.setDocument(document)
        document.setPageSize(qtc.QSizeF(self.doc_width, self.doc_height))
        cursor = qtg.QTextCursor(document)
        root = document.rootFrame()
        cursor.setPosition(root.lastPosition())

        # Insert top-level frames
        logo_frame_fmt = qtg.QTextFrameFormat()
        logo_frame_fmt.setBorder(2)
        logo_frame_fmt.setPadding(10)
        logo_frame = cursor.insertFrame(logo_frame_fmt)

        cursor.setPosition(root.lastPosition())
        cust_addr_frame_fmt = qtg.QTextFrameFormat()
        cust_addr_frame_fmt.setWidth(self.doc_width * .3)
        cust_addr_frame_fmt.setPosition(qtg.QTextFrameFormat.FloatRight)
        cust_addr_frame = cursor.insertFrame(cust_addr_frame_fmt)

        cursor.setPosition(root.lastPosition())
        terms_frame_fmt = qtg.QTextFrameFormat()
        terms_frame_fmt.setWidth(self.doc_width * .5)
        terms_frame_fmt.setPosition(qtg.QTextFrameFormat.FloatLeft)
        terms_frame = cursor.insertFrame(terms_frame_fmt)

        cursor.setPosition(root.lastPosition())
        line_items_frame_fmt = qtg.QTextFrameFormat()
        line_items_frame_fmt.setMargin(25)
        line_items_frame = cursor.insertFrame(line_items_frame_fmt)

        # Create the heading
        # create a format for the characters
        std_format = qtg.QTextCharFormat()

        logo_format = qtg.QTextCharFormat()
        logo_format.setFont(
            qtg.QFont('Ubuntu', 24, qtg.QFont.DemiBold))
        logo_format.setUnderlineStyle(
            qtg.QTextCharFormat.SingleUnderline)
        logo_format.setVerticalAlignment(
            qtg.QTextCharFormat.AlignMiddle)

        label_format = qtg.QTextCharFormat()
        label_format.setFont(qtg.QFont('Sans', 12, qtg.QFont.Bold))

        # create a format for the block
        cursor.setPosition(logo_frame.firstPosition())
        # The easy way:
        #cursor.insertImage('logo-tc.png')
        # The better way:
        logo_image_fmt = qtg.QTextImageFormat()
        logo_image_fmt.setName('logo-tc.png')
        logo_image_fmt.setHeight(48)
        cursor.insertImage(logo_image_fmt, qtg.QTextFrameFormat.FloatLeft)
        cursor.insertText('   ')
        cursor.insertText('TC computing, LMT', logo_format)
        cursor.insertBlock()
        cursor.insertText('Chacabuco 13, Arica, 1000000', std_format)

        ## Customer address
        cursor.setPosition(cust_addr_frame.lastPosition())

        address_format = qtg.QTextBlockFormat()
        address_format.setLineHeight(
            150, qtg.QTextBlockFormat.ProportionalHeight)
        address_format.setAlignment(qtc.Qt.AlignRight)
        address_format.setRightMargin(25)

        cursor.insertBlock(address_format)
        cursor.insertText('Batch:', label_format)
        cursor.insertBlock(address_format)
        cursor.insertText(data['b_name'], std_format)
        cursor.insertBlock(address_format)
        cursor.insertText(data['b_num'])

        ## Terms
        cursor.setPosition(terms_frame.lastPosition())
        cursor.insertText('Terms:', label_format)
        cursor.insertList(qtg.QTextListFormat.ListDisc)
        # cursor is now in the first list item

        term_items = (
            f'<b>Production date:</b> {data["p_date"]}',
            f'<b>Production terms:</b> {data["p_terms"]}',
            f'<b>Production due:</b> {data["p_due"]}',
        )

        for i, item in enumerate(term_items):
            if i > 0:
                cursor.insertBlock()
            # We can insert HTML too, but not with a textformat
            cursor.insertHtml(item)

        ## Line items
        table_format = qtg.QTextTableFormat()
        table_format.setHeaderRowCount(1)
        table_format.setWidth(
            qtg.QTextLength(qtg.QTextLength.PercentageLength, 100))

        # headings = ('Time', 'Description', 'User', 'Cost')
        headings = ('Time', 'Description')#, 'Cost')
        num_rows = len(data['line_items']) + 1
        num_cols = len(headings)

        cursor.setPosition(line_items_frame.lastPosition())
        table = cursor.insertTable(num_rows, num_cols, table_format)

        # now we're in the first cell of the table
        # write headers
        for heading in headings:
            cursor.insertText(heading, label_format)
            cursor.movePosition(qtg.QTextCursor.NextCell)

        # write data
        for row in data['line_items']:
            for col, value in enumerate(row):
                text = f'{value}' if col in (0, 1) else f'{value}'
                cursor.insertText(text, std_format)
                cursor.movePosition(qtg.QTextCursor.NextCell)

        # Append a row
        table.appendRows(1)
        cursor = table.cellAt(num_rows, 0).lastCursorPosition()
        cursor.insertText('Total', label_format)
        cursor = table.cellAt(num_rows, 1).lastCursorPosition()
        # cursor.insertText(f"${data['total_due']}", label_format)
        cursor.insertText(f"{data['total_due']}", label_format)



class MainWindow(qtw.QMainWindow):

    def __init__(self):
        """MainWindow constructor.

        This widget will be our main window.
        We'll define all the UI components in here.
        """
        super().__init__()
        # Main UI code goes here
        main = qtw.QWidget()
        main.setLayout(qtw.QHBoxLayout())
        self.setCentralWidget(main)

        
        
        form = ReportForm()
        main.layout().addWidget(form)
        # main.layout().setSizePolicy(qtw.Expanding)

        self.preview = ReportView()
        main.layout().addWidget(self.preview)

        form.submitted.connect(self.preview.build_report)

        # Printing
        print_tb = self.addToolBar('Printing')
        print_tb.addAction('Configure Printer', self.printer_config)
        print_tb.addAction('Print Preview', self.print_preview)
        print_tb.addAction('Print dialog', self.print_dialog)
        print_tb.addAction('Export PDF', self.export_pdf)

        self.printer = qtps.QPrinter()
        # Configure defaults:
        self.printer.setOrientation(qtps.QPrinter.Portrait)
        self.printer.setPageSize(qtg.QPageSize(qtg.QPageSize.Letter))
        self._update_preview_size()
        
        
        

        # End main UI code
        self.show()

    def _update_preview_size(self):
        self.preview.set_page_size(
            self.printer.pageRect(qtps.QPrinter.Point))

    def printer_config(self):
        dialog = qtps.QPageSetupDialog(self.printer, self)
        dialog.exec()
        self._update_preview_size()

    def _print_document(self):
        # doesn't actually kick off printer,
        # just paints document to the printer object
        self.preview.document().print(self.printer)

    def print_dialog(self):
        # bug fix for
        # self._print_document()
        # this can cause the document to start printing,
        dialog = qtps.QPrintDialog(self.printer, self)

        # Instead we'll add this line, so _print_document is triggered when the dialog is
        # accepted:
        dialog.accepted.connect(self._print_document)
        dialog.exec()
        self._update_preview_size()

    def print_preview(self):
        dialog = qtps.QPrintPreviewDialog(self.printer, self)
        dialog.paintRequested.connect(self._print_document)
        dialog.exec()
        self._update_preview_size()

    def export_pdf(self):
        filename, _ = qtw.QFileDialog.getSaveFileName(
            self, "Save to PDF", qtc.QDir.homePath(), "PDF Files (*.pdf)")
        if filename:
            self.printer.setOutputFileName(filename)
            self.printer.setOutputFormat(qtps.QPrinter.PdfFormat)
            self._print_document()

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    # it's required to save a reference to MainWindow.
    # if it goes out of scope, it will be destroyed.
    mw = MainWindow()
    sys.exit(app.exec())
