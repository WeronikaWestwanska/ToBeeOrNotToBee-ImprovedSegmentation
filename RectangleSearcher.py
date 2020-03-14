import numpy
 
class RectangleSearcher(object):

    #---------------------------------------------------------------
    # searches for regions of interest
    # args:
    # image - input image as numpy [height, width]
    # window_size - window size on which the image is divided
    #---------------------------------------------------------------
    def search_for_roi(self, image, window_size):
        
        result = []
        
        width = numpy.shape(image)[1]
        height = numpy.shape(image)[0]
 
        rows_count = int(numpy.floor(height / window_size))
        cols_count = int(numpy.floor(width / window_size))
        
        if rows_count * window_size < height:
            rows_count += 1
        
        if cols_count * window_size < width:
            cols_count += 1
 
        windows = numpy.zeros((rows_count, cols_count))
        visited_windows = numpy.zeros((rows_count, cols_count))
 
        # Decide if window has an object.
        for i in range(0, rows_count):
            for j in range(0, cols_count):
 
                windows[i, j] = self.does_window_contain_object(
                    image, width, height, window_size, i, j)
        
        neighbours_list = []
 
        # Now look for 8-connected neighbours.
        for i in range(0, rows_count):
            for j in range(0, cols_count):
 
                neighbours = []
                self.find_neighbours(windows, visited_windows, i, j, rows_count, cols_count, neighbours)
 
                if len(neighbours) > 0:
                    neighbours_list.append(neighbours)
 
        # Based on that find big rectangles.
        for neighbours in neighbours_list:
 
            first_window = neighbours[0]
            minx = first_window[1] * window_size
            miny = first_window[0] * window_size
            maxx = numpy.min((minx + window_size, width))
            maxy = numpy.min((miny + window_size, height))
            for window_index in range(1, len(neighbours)):
 
                window = neighbours[window_index]
                lminx = window[1] * window_size
                lminy = window[0] * window_size
                lmaxx = numpy.min((lminx + window_size, width))
                lmaxy = numpy.min((lminy + window_size, height))
 
                # Update minx, miny, maxx, maxy.
                minx = numpy.min((minx, lminx))
                miny = numpy.min((miny, lminy))
                maxx = numpy.max((maxx, lmaxx))
                maxy = numpy.max((maxy, lmaxy))
 
            result.append((minx, miny, maxx, maxy))
 
        return result

    #---------------------------------------------------------------
    # cheks if specified window contains the object 
    # args:
    # image_as_array - image
    # width - width
    # height - height
    # window_size - size of window
    # window_row - row of the window in the image
    # window_column - column of the window in the image
    #--------------------------------------------------------------- 
    def does_window_contain_object(self, image_as_array, width, height, 
                                   window_size, window_row, window_column):
 
        window_offset_x = window_column * window_size
        window_offset_y = window_row * window_size
        maxx = numpy.min((width, window_offset_x + window_size))
        maxy = numpy.min((height, window_offset_y + window_size))
        for x in range(window_offset_x, maxx):
            for y in range(window_offset_y, maxy):
 
                if image_as_array[y, x] == 255.0:
                    return 1
 
        return 0

    #---------------------------------------------------------------
    # finds potential neighbouring windows with object 
    # args:
    # windows - array of windows
    # visited_windows - visited windows
    # row - row of the window
    # column - column of the window
    # rows_count - how many rows
    # cols_count - how many columns
    # result - resulting collection of windows
    #---------------------------------------------------------------
    def find_neighbours(self, windows, visited_windows, 
                           row, column, rows_count, cols_count, result):
 
        if row < 0 or row >= rows_count or column < 0 or column >= cols_count:
            return
 
        if visited_windows[row, column] == 1:
            return
 
        if windows[row, column] == 0:
            return
 
        result.append([row, column])
        visited_windows[row, column] = 1
 
        self.find_neighbours(windows, visited_windows, row - 1, column - 1, rows_count, cols_count, result)
        self.find_neighbours(windows, visited_windows, row - 1, column, rows_count, cols_count, result)
        self.find_neighbours(windows, visited_windows, row - 1, column + 1, rows_count, cols_count, result)
        self.find_neighbours(windows, visited_windows, row, column - 1, rows_count, cols_count, result)
        self.find_neighbours(windows, visited_windows, row, column + 1, rows_count, cols_count, result)
        self.find_neighbours(windows, visited_windows, row + 1, column - 1, rows_count, cols_count, result)
        self.find_neighbours(windows, visited_windows, row + 1, column, rows_count, cols_count, result)
        self.find_neighbours(windows, visited_windows, row + 1, column + 1, rows_count, cols_count, result)