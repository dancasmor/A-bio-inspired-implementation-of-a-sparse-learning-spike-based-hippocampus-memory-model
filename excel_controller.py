import xlsxwriter


class ExcelSpikeTracer:
    """
    Class used to control the creation of an excel file
    """

    def __init__(self, filePath, filename, simTime, numHeaders, contentColor, headerColor, orientationFormat, boxTableSize):
        """
        Init an object of type ExcelSpikeTracer

        @param filepath: base path to the folder where the excel will be stored
        @param filename: name of the excel file
        @param simTime: duration in time (ms) of the simulation
        @param numHeaders: numbers of headers
        @param contentColor: default color used in the content boxes of the table (spikes values)
        @param headerColor: default color used in the headers boxes of the table (row and column names)
        @param orientationFormat: orientation of the time stamp: "vertical" or "horizontal"
        @param boxTableSize: size of box in table
        """
        self.fullPath = filePath + filename + ".xlsx"
        self.excel = xlsxwriter.Workbook(self.fullPath)
        self.worksheet = self.excel.add_worksheet()
        self.headerFormat = self.create_format(headerColor)
        self.contentFormat = self.create_format(contentColor)
        self.simTime = int(simTime)
        self.orientation = orientationFormat
        self.numHeaders = numHeaders
        self.boxTableSize = boxTableSize

        self.write_header()

    def create_format(self, color):
        """
        Define a format for the content of the table

        @param color: color used in the format created
        @return: the default format used in the table with custom colors
        """
        excelFormat = self.excel.add_format()
        excelFormat.set_border()
        excelFormat.set_bold()
        excelFormat.set_align('center')
        excelFormat.set_align('vcenter')
        excelFormat.set_bg_color(color)

        return excelFormat

    def write_header(self):
        """
        Create the first header of the table with a time mark for each time step of the simulation

        @return:
        """
        if self.orientation == "horizontal":
            self.worksheet.set_column(0, self.simTime, self.boxTableSize)
            for i in range(self.simTime):
                self.worksheet.write(0, i + 1, i, self.headerFormat)
        else:
            self.worksheet.set_column(0, self.numHeaders, self.boxTableSize)
            for i in range(self.simTime):
                self.worksheet.write(i + 1, 0, i, self.headerFormat)


    def print_spikes(self, index, name, spikes, color):
        """
        Insert a row or column in the table marking with 1 the time stamp when the neuron fired

        @param index: the row where to insert the data
        @param name: the header of the row or column (neuron name)
        @param spikes: array of time stamps that represents the spikes fired
        @param color: color used to the marked boxes (when spikes happen)
        @return:
        """
        self.worksheet.write(index, 0, name, self.headerFormat)

        valuesFormat = self.create_format(color)
        for i in range(self.simTime):
            if self.orientation == "horizontal":
                if i in spikes:
                    self.worksheet.write(index, i + 1, 1, valuesFormat)
                else:
                    self.worksheet.write(index, i + 1, "", self.contentFormat)
            else:
                if i in spikes:
                    self.worksheet.write(i + 1, index, 1, valuesFormat)
                else:
                    self.worksheet.write(i + 1, index, "", self.contentFormat)

    def print_row(self, index, isHeader, values, color):
        """
        Insert a row in the table using the values passed as a parameters

        @param index: the row where to insert the data
        @param isHeader: if it is a header row o False if it is a content row
        @param values: array of values to insert in the row
        @param color: color used to fill the boxes in the row or list of color (one for each column)
        @return:
        """

        valuesFormat = []
        if isinstance(color, list):
            [valuesFormat.append(self.create_format(columnColor)) for columnColor in color]
        else:
            [valuesFormat.append(self.create_format(color)) for i in range(len(values))]

        for i in range(0, len(values)):
            if isHeader:
                self.worksheet.write(index, i, values[i], valuesFormat[i])
            else:
                self.worksheet.write(index, i+1, values[i], valuesFormat[i])


    def print_column(self, index, isHeader, values, color):
        """
        Insert a column in the table using the values passed as a parameters

        @param index: the column where to insert the data
        @param isHeader: if it is a header row o False if it is a content row
        @param values: array of values to insert in the column
        @param color: color used to fill the boxes in the column or list of color (one for each row)
        @return:
        """

        valuesFormat = []
        if isinstance(color, list):
            [valuesFormat.append(self.create_format(rowColor)) for rowColor in color]
        else:
            [valuesFormat.append(self.create_format(color)) for i in range(len(values))]

        for i in range(0, len(values)):
            if isHeader:
                self.worksheet.write(i, index, values[i], valuesFormat[i])
            else:
                self.worksheet.write(i+1, index, values[i], valuesFormat[i])


    def closeExcel(self):
        self.excel.close()