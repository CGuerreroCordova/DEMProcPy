import numpy as np
from itertools import product
from exceptions import (WindowSizeHighError, WindowSizeEvenError,
                        CenterCloseBorderError, NumpyArrayExpectedError,
                        InnerSizeError)

class SlidingWindow:
    """
    Provide an interator of sliding window over a two dimensional ndarray.

    Attributes
    ----------
    grid : ndarray
        The grid on which the iterator will be created to get the sliding
        window
    window_size: int
        The size of the sliding window
    _indices_nan: list(tuple(int, int))
        List of pair of indices of sliding windows which will be set as nan
    iter_over_ones: bool
        Indicates if the iteration will be done only on the grid elements with
        value 1

    Methods
    -------
    customize
        Allow to customize the sliding window returned defining indices to set
        as np.nan. For this class no one element in the window will be set as
        nan.
    """

    def __init__(self, grid, window_size, iter_over_ones=False):
        """
        Parameters
        ----------
        grid : ndarray
            The grid on which the iterator will be created to get the sliding
            window
        window_size: int
            The size of the sliding window
        iter_over_ones: bool, optional
            Indicates if the iteration will be done only on the grid elements
            with value 1 (default is False)
        """
        self.grid = grid
        self.window_size = window_size
        self._indices_nan = []
        self.iter_over_ones = iter_over_ones

    @property
    def grid(self):
        """
        ndarray: Get or set the numpy array for which the iteration is done.

        Raises
        ------
        NumpyArrayExpectedError:
            If the parameters provided is not ndarray type.

        """
        return self._grid

    @grid.setter
    def grid(self, value):
        if not isinstance(value, np.ndarray):
            raise NumpyArrayExpectedError(value)
        self._grid = value.astype('float32')

    @property
    def window_size(self):
        """
        int: Sliding window size. Dimensions of sliding windows will be:
        window_size x window_size

        Raises
        ------
        WindowSizeHighError:
            If the value provided is greater than any of the dimensions of
            the window.
        WindowSizeEvenError:
            If the provided values is not odd.
        """
        return self._window_size

    @window_size.setter
    def window_size(self, value):
        if any(value > i for i in self.grid.shape):
            raise WindowSizeHighError(value, self.grid.shape)
        elif value % 2 != 1:
            raise WindowSizeEvenError(value)
        self._window_size = int(value)

    def __iter__(self):
        """
        Define the iterator for the SlidingWindow class. Use window size and
        grid dimensions to create elements to produce. Allow customize the
        window produces in terms of set some values of the window as nan, this
        way differents kind of windoes can be customized and created. For one
        instance only one type of customization is allowed.

        Yields
        -------
        ndarray, tuple(int, int)
            * The next sliding window, going through the grid by row and by
            column, that is, for each row it moves from the left to the right
            until the end of the row and then go to the next row, continuing
            to the last element of the last row.
            * A tuple with actual indices of iteration in relation with input
            grid

        Notes
        -----
        Are presented two examples. One of them using 'iter' and 'next', and
        the other one using 'for, in'

        Examples
        --------
        >>> import numpy as np
        >>> from sliding_window import SlidingWindow
        >>> grid = np.arange(25).reshape((5, 5))
        >>> grid
        array([[ 0,  1,  2,  3,  4],
               [ 5,  6,  7,  8,  9],
               [10, 11, 12, 13, 14],
               [15, 16, 17, 18, 19],
               [20, 21, 22, 23, 24]])
        >>> sliding = SlidingWindow(grid, window_size=3)
        >>> i = iter(sliding)
        >>> next(i)
        (array([[ 0.,  1.,  2.],
               [ 5.,  6.,  7.],
               [10., 11., 12.]], dtype=float32), (1, 1))
        >>> next(i)
        (array([[ 1.,  2.,  3.],
               [ 6.,  7.,  8.],
               [11., 12., 13.]], dtype=float32), (1, 2))
        >>> next(i)
        (array([[ 2.,  3.,  4.],
               [ 7.,  8.,  9.],
               [12., 13., 14.]], dtype=float32), (1, 3))
        >>> next(i)
        (array([[ 5.,  6.,  7.],
               [10., 11., 12.],
               [15., 16., 17.]], dtype=float32), (2, 1))
        >>> grid_2 = np.arange(16).reshape((4, 4))
        >>> grid_2
        array([[ 0,  1,  2,  3],
               [ 4,  5,  6,  7],
               [ 8,  9, 10, 11],
               [12, 13, 14, 15]])
        >>> sliding_2 = SlidingWindow(grid_2, window_size=3)
        >>> for window in sliding_2:
        ...     print(window)
        (array([[ 0.,  1.,  2.],
               [ 4.,  5.,  6.],
               [ 8.,  9., 10.]], dtype=float32), (1, 1))
        (array([[ 1.,  2.,  3.],
               [ 5.,  6.,  7.],
               [ 9., 10., 11.]], dtype=float32), (1, 2))
        (array([[ 4.,  5.,  6.],
               [ 8.,  9., 10.],
               [12., 13., 14.]], dtype=float32), (2, 1))
        (array([[ 5.,  6.,  7.],
               [ 9., 10., 11.],
               [13., 14., 15.]], dtype=float32), (2, 2))
        """
        ny, nx = self.grid.shape
        left_up = self.window_size // 2
        right_down = left_up + 1

        self.customize()

        def range_grid(bound_index):
            return range(left_up, (bound_index - right_down) + 1)

        for j in range_grid(ny):
            for i in range_grid(nx):
                if not self.iter_over_ones or int(self.grid[j, i]) == 1:
                    neighbour = self.grid[j - left_up: j + right_down,
                                i - left_up: i + right_down]
                    neighbour = self._set_nan(neighbour)
                    yield neighbour, (j, i)

    def __getitem__(self, coords):
        """
        Slice a window with dimensions of window_size * window_size attribute
        class from grid attribute class, centered in indices indicated by
        coords. If some class inherits from this class and customized method is
        override, some elements of the window can be nan, depending of the
        customization

        Parameters
        ----------
        coords: tuple(int, int)
            Coordinates to get the window from grid

        Returns
        -------
        ndarray
            The window sliced from grid

        Raises
        ------
        CenterCloseBorderError
            If coordinates of the center to slice is too close to the border

        Examples
        --------
        >>> import numpy as np
        >>> from sliding_window import SlidingWindow
        >>> grid = np.arange(25).reshape((5, 5))
        >>> grid
        array([[ 0,  1,  2,  3,  4],
               [ 5,  6,  7,  8,  9],
               [10, 11, 12, 13, 14],
               [15, 16, 17, 18, 19],
               [20, 21, 22, 23, 24]])
        >>> sliding = SlidingWindow(grid, window_size=3)
        >>> sliding[1, 1]
        array([[ 0.,  1.,  2.],
               [ 5.,  6.,  7.],
               [10., 11., 12.]], dtype=float32)
        >>> sliding[3,3]
        array([[12., 13., 14.],
               [17., 18., 19.],
               [22., 23., 24.]], dtype=float32)
        >>> sliding[1,3]
        array([[ 2.,  3.,  4.],
               [ 7.,  8.,  9.],
               [12., 13., 14.]], dtype=float32)
        """
        j, i = coords
        left_up = self.window_size // 2
        right_down = left_up + 1

        self.customize()

        def _get_slice(coord):
            """
            Return slice corresponding to coord minus the middle of the window
            size
            """
            return slice(coord - left_up, coord + right_down)

        if self._check_border(j, i, left_up, right_down):
            neighbours = self.grid[_get_slice(j), _get_slice(i)]
            neighbours = self._set_nan(neighbours)
            return neighbours
        else:
            raise CenterCloseBorderError(coords, window_size=self.window_size)

    def _check_border(self, j, i, left_up, right_down):
        """
        Check if indices j, i are too close to the border
        """
        ny, nx = self.grid.shape
        return all(index >= left_up for index in (j, i)) and \
               j <= (ny - right_down) + 1 and \
               i <= (nx - right_down) + 1

    def customize(self):
        """
        Allow to customize the sliding window returned defining indices to set
        as np.nan. For this class no one element in the window will be set as
        nan.

        Returns
        -------
        None
        """
        pass

    def _set_nan(self, neighbours):
        """
        Set as nan elements of the window. The elements defined
        in self._indices_nan will be set as nan, the rest of elements keep its
        value. The window modified and returned is copied in this method.

        Parameters
        ----------
        neighbours: ndarray
            window to set some element as nan.

        Returns
        -------
        ndarray:
            A copy of the input window with some or none elements set as nan

        """
        cp_window = neighbours.copy()
        for indices in self._indices_nan:
            cp_window[indices] = np.nan
        return cp_window


class SlidingIgnoreBorder(SlidingWindow):

    def __init__(self, grid, window_size, *args, **kwargs):
        super().__init__(grid, window_size, *args, **kwargs)
        self.grid = self._add_extra_margin()

    def _add_extra_margin(self):
        ny, nx = self.grid.shape
        ny = ny + self.window_size - 1
        nx = nx + self.window_size - 1
        middle = self.window_size // 2
        grid_expanded = np.empty((ny, nx))
        grid_expanded[:] = np.nan
        grid_expanded[middle:ny - middle, middle:nx - middle] = \
            self.grid.astype('float32')
        return grid_expanded

class CircularWindow(SlidingWindow):

    def __init__(self, grid, window_size, *args, **kwargs):
        super().__init__(grid, window_size, *args, **kwargs)

    def customize(self):
        self._indices_nan.extend(self.remove_corners(self.window_size))
        super().customize()

    def remove_corners(self, ny):
        return [(0, 0), (0, ny - 1), (ny - 1, 0), (ny - 1, ny - 1)]


class InnerWindow(SlidingWindow):

    def __init__(self, grid, window_size, inner_size, *args, **kwargs):
        self.inner_size = inner_size
        super().__init__(grid, window_size, *args, **kwargs)

    def customize(self):
        self._indices_nan.extend(self.inner_window(self.window_size,
                                                   self.inner_size))
        super().customize()

    def inner_window(self, ny, inner_size):

        if inner_size > self.window_size:
            raise InnerSizeError(inner_size, self.window_size)
        else:
            ratio_inner = inner_size // 2
            center = ny // 2
            indices = (center - ratio_inner, center + ratio_inner + 1)
            pairs = product(range(*indices), range(*indices))
            # Removing the center from the list to set nan
            inner_window = ((x, y) for x, y in pairs if not x == y == center)
            return inner_window


class NoCenterWindow(SlidingWindow):

    def __init__(self, grid, window_size, *args, **kwargs):
        super().__init__(grid, window_size, *args, **kwargs)

    def customize(self):
        self._indices_nan.extend(self.center_index(self.window_size))
        super().customize()

    def center_index(self, ny):
        center = ny // 2
        return [(center, center)]


class IgnoreBorderInnerSliding(SlidingIgnoreBorder, InnerWindow,
                               NoCenterWindow):
    def __init__(self, grid, *, window_size, inner_size):
        super().__init__(grid=grid, window_size=window_size,
                         inner_size=inner_size)
