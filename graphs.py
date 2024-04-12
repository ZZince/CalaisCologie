"""Graph module that contains all the graphing functions for the interface.

The functions here should be taking data as a python list and return a matplotlib figure in 
form of a png file (using TemporaryFile()).
"""

import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
import textwrap
import tempfile

from tempfile import TemporaryFile

FilePath = str


class Grapher():
    """Class that contains all the graphing functions for the interface.
    All functions return a filename to a png file containing the graph."""

    def __init__(self) -> None:
        pass

    def _figure_to_file(self, figure: plt.figure) -> str:
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as file:
            file_name = file.name
            figure.savefig(file_name, format='png')
        return file_name

    def clear_plt(fun):
        def wrapper(*args, **kwargs):
            plt.clf()
            return fun(*args, **kwargs)
        return wrapper

    @clear_plt
    def pie_chart_graph(self, data: list, labels: list, graph_title: str = None, x_axis_label: str = None, show_percent=False) -> FilePath:

        plt.figure(figsize=(5, 5))

        labels = [
            "\n".join(textwrap.wrap(label, 15)) for label in labels
        ]

        default_colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
        colors = default_colors[1:len(data)+1]  # Skip the first color (blue)

        p, tx, autotexts = plt.pie(data, labels=labels,
                                   autopct="",
                                   startangle=-135,
                                   colors=colors)

        for i, val in enumerate(autotexts):
            if show_percent:
                val.set_text(f"{data[i]} ({data[i]/sum(data)*100:.1f}%)")
            else:
                val.set_text(f"{data[i]}")

        if graph_title:
            plt.title(graph_title)
        if x_axis_label:
            plt.xlabel(x_axis_label)

        plt.axis('equal')
        plt.tight_layout()
        return self._figure_to_file(plt)

    def funnel_chart_graph(self, data: list, labels: list, graph_title: str = "Graphe pyramidal", reverse=True, data_is_percent=True) -> FilePath:
        data, labels = zip(*sorted(zip(data, labels), reverse=True))

        total = sum(data)
        percentages = [value / total * 100 for value in data]
        cumulative_percentages = [sum(percentages[:i + 1])
                                  for i in range(len(percentages))]

        # Generate a color shade for each label
        # start_color = red
        # end_color = dark blue
        colors = [
            (1 - i / len(labels), i/len(labels), 0) for i in range(len(labels))
        ]

        fig, ax = plt.subplots(figsize=(8, 6))

        points = [
            (
                (0, -1),
                (200, -1),
                (200-cumulative_percentages[0], 0),
                (cumulative_percentages[0], 0)
            )
        ]

        for idx, (percent, next_percent) in enumerate(zip(cumulative_percentages, cumulative_percentages[1:])):
            points.append(
                (
                    (percent, idx),
                    (200-percent, idx),
                    (200-next_percent, idx+1),
                    (next_percent, idx+1),

                )
            )

        # Notch all the y coordiantes up by 0.5 to center the labels on the slice
        for idx, ((x1, y1), (x2, y2), (x3, y3), (x4, y4)) in enumerate(points):
            points[idx] = (
                (x1, y1+0.5),
                (x2, y2+0.5),
                (x3, y3+0.5),
                (x4, y4+0.5)
            )

        for i in range(len(labels)):

            top_left, top_right, bottom_right, bottom_left = points[i]

            path = Path([top_left, top_right, bottom_right, bottom_left, top_left],
                        [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY])
            patch = patches.PathPatch(
                path, facecolor=colors[i]
            )
            ax.add_patch(patch)

            # Add the % text
            # ax.text(100, i, f'{labels[i]} - {percentages[i]:.1f}% ({data[i]})',
            #         ha='center', va='center', color='black', fontsize=12)

            ax.text(100, i, f'{data[i]}{"%" if data_is_percent else ""}',
                    ha='center', va='center', color='black', fontsize=12)

        # Customize plot appearance

        # x axis
        ax.set_xlim(0, 200)

        # y axis
        if reverse:
            ax.set_ylim(len(cumulative_percentages), -1)
        else:
            ax.set_ylim(-1, len(cumulative_percentages))

        # Remove the x and y axis ticks and labels
        ax.set_xticks([])
        # ax.set_yticks([])
        ax.set_yticks(range(len(cumulative_percentages)))
        ax.set_xticklabels([])
        # ax.set_yticklabels([])
        ax.set_yticklabels(labels)

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.grid(axis='x', linestyle='--')

        # plt.xlabel('Pourcentage') # It's obvious, so we don't need to label it
        plt.title(graph_title)
        plt.tight_layout()

        return self._figure_to_file(plt)


if __name__ == '__main__':
    from PyQt6.QtWidgets import QMainWindow, QLabel, QApplication
    from PyQt6.QtGui import QPixmap
    import sys

    g = Grapher()

    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()

            # Create a QLabel widget to display the image
            self.image_label = QLabel(self)
            self.setCentralWidget(self.image_label)

            # Set the image file name
            # Replace with the actual file name or path
            image_file = g.funnel_chart_graph(
                [42, 78, 56, 12, 34], ['A', 'B', 'C', 'D', 'E'], 'Pyramid Graph')

            # Load the image using QPixmap
            pixmap = QPixmap(image_file)

            # Set the pixmap as the image content of the QLabel
            self.image_label.setPixmap(pixmap)

            # Adjust the size of the main window to fit the image
            self.resize(pixmap.width(), pixmap.height())

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
