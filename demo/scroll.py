from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QSlider
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget

from qwt import QwtPlotCurve
from qwt.plot import QwtPlot
from qwt.scale_div import QwtScaleDiv

app = QApplication([__file__])

root = QWidget()

layout = QVBoxLayout(root)

plot = QwtPlot(root)
QwtPlotCurve.make([0, 9], [0, 9], '', plot)
plot.setAxisScaleDiv(QwtPlot.xBottom, QwtScaleDiv(0, 9))

slider = QSlider(Qt.Orientation.Horizontal, root)
slider.setRange(0, 9)


def change_lower_bound(value: int) -> None:
    plot.axisScaleDiv(QwtPlot.xBottom).setLowerBound(value)
    plot.replot()


slider.valueChanged.connect(change_lower_bound)

root.setLayout(layout)
layout.addWidget(plot)
layout.addWidget(slider)
root.show()

raise SystemExit(app.exec())
