import gdb # pylint: disable=E0401
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import numpy as np

from . import data_extractor


class PlottingError(Exception):
    pass


class Legend:
    def __init__(self):
        self.legend = []

    def add(self, name: str):
        self.legend.append(name)

    def apply(self):
        plt.legend(self.legend)


def plot_1d(args, plot_function):
    legend = Legend()

    for arg in args.split():
        data = data_extractor.extract_var(arg)

        if data.ndim == 2 and not np.iscomplexobj(data):
            for i, row in enumerate(data):
                plot_function(row)
                legend.add(f"{arg}[{i}]")
        elif data.ndim == 1:
            if np.iscomplexobj(data):
                plot_function(np.real(data))
                plot_function(np.imag(data))
                plot_function(np.abs(data))
                legend.add(f"real({arg})")
                legend.add(f"imag({arg})")
                legend.add(f"abs({arg})")
            else:
                plot_function(data)
                legend.add(arg)
        else:
            raise PlottingError(f"Unsuitable for plotting: {arg}")
    
    legend.apply()
    plt.grid()
    plt.show()


class Plot(gdb.Command):
    def __init__(self):
        super(Plot, self).__init__("plot", gdb.COMMAND_OBSCURE)

    def invoke(self, args, from_tty):
        plot_1d(args, plt.plot)


class Scatter(gdb.Command):
    def __init__(self):
        super(Scatter, self).__init__("scatter", gdb.COMMAND_OBSCURE)

    def invoke(self, args, from_tty):
        legend = Legend()
        temp = []

        for arg in args.split():
            data = data_extractor.extract_var(arg)

            if data.ndim == 2 and not np.iscomplexobj(data) and 2 in data.shape:
                if data.shape[1] == 2:
                    plt.scatter(data[:,0], data[:,1])
                else:
                    plt.scatter(data[0], data[1])

                legend.add(arg)
            elif data.ndim == 1:
                if np.iscomplexobj(data):
                    plt.scatter(np.real(data), np.imag(data))
                    legend.add(arg)
                else:
                    temp.append(data)
            else:
                raise PlottingError(f"Unsuitable for plotting: {arg}")

        if len(temp):
            if len(temp) == 2:
                plt.scatter(temp[0], temp[1])
                legend.add("Data")
            else:
                raise PlottingError(f"Incorrect number of arguments")
        
        legend.apply()
        plt.grid()
        plt.show()


class Plot3D(gdb.Command):
    def __init__(self):
        super(Plot3D, self).__init__("plot3d", gdb.COMMAND_OBSCURE)

    def invoke(self, args, from_tty):
        z = data_extractor.extract_var(args)
        if z.ndim != 2:
            raise PlottingError(f"Unsuitable for plotting: {args}")

        x = np.arange(z.shape[1])
        y = np.arange(z.shape[0])
        xm, ym = np.meshgrid(x, y)

        fig = plt.figure()
        ax = p3.Axes3D(fig)
        ax.plot_surface(xm, ym, z)
        plt.show()


class Scatter3D(gdb.Command):
    def __init__(self):
        super(Scatter3D, self).__init__("scatter3d", gdb.COMMAND_OBSCURE)

    def invoke(self, args, from_tty):
        legend = Legend()
        temp = []

        fig = plt.figure()
        ax = p3.Axes3D(fig)

        for arg in args.split():
            data = data_extractor.extract_var(arg)

            if data.ndim == 2 and not np.iscomplexobj(data) and 3 in data.shape:
                if data.shape[1] == 3:
                    ax.scatter(data[:,0], data[:,1], data[:,2])
                else:
                    ax.scatter(data[0], data[1], data[2])

                legend.add(arg)
            elif data.ndim == 1:
                temp.append(data)  
            else:
                raise PlottingError(f"Unsuitable for plotting: {arg}")

        if len(temp):
            if len(temp) == 3:
                ax.scatter(temp[0], temp[1])
                legend.add("Data")
            else:
                raise PlottingError(f"Incorrect number of arguments")
        
        legend.apply()
        plt.grid()
        plt.show()


class Hist(gdb.Command):
    def __init__(self):
        super(Hist, self).__init__("hist", gdb.COMMAND_OBSCURE)

    def invoke(self, args, from_tty):
        hist = lambda x: plt.hist(x, bins="auto")
        plot_1d(args, hist)


class FFT(gdb.Command):
    def __init__(self):
        super(FFT, self).__init__("fft", gdb.COMMAND_OBSCURE)

    def invoke(self, args, from_tty):
        legend = Legend()
        fft_db = lambda x: 20*np.log10(np.abs(np.fft.fft(x)))

        for arg in args.split():
            data = data_extractor.extract_var(arg)

            if data.ndim == 2 and not np.iscomplexobj(data):
                for i, row in enumerate(data):
                    plt.plot(fft_db(row))
                    legend.add(f"{arg}[{i}]")
            elif data.ndim == 1:
                plt.plot(fft_db(data))
                legend.add(arg)
            else:
                raise PlottingError(f"Unsuitable for plotting: {arg}")

        legend.apply()
        plt.grid()
        plt.ylabel("PSD (dB)")
        plt.show()


Plot()
Scatter()
Plot3D()
Scatter3D()
Hist()
FFT()