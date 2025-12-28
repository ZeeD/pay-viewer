from sys import argv
from typing import TYPE_CHECKING

from PySide6.QtCharts import QBarCategoryAxis
from PySide6.QtCharts import QBarSet
from PySide6.QtCharts import QChart
from PySide6.QtCharts import QChartView
from PySide6.QtCharts import QStackedBarSeries
from PySide6.QtCharts import QValueAxis
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtGui import QColorConstants
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QWidget

from payviewer.loader import load
from payviewer.model import ZERO
from payviewer.model import Info
from payviewer.settings import Settings

if TYPE_CHECKING:
    from datetime import date


def q_bar_category_axis(title: str, categories: list[str]) -> QBarCategoryAxis:
    ret = QBarCategoryAxis()
    ret.setTitleText(title)
    ret.append(categories)
    return ret


def q_value_axis(title: str) -> QValueAxis:
    ret = QValueAxis()
    ret.setTitleText(title)
    ret.setTickCount(40)
    return ret


def q_bar_set(label: str, values: list[float], color: QColor) -> QBarSet:
    for _value in values:
        pass
    ret = QBarSet(label)
    ret.append(values)
    ret.setColor(color)
    ret.setBorderColor(QColorConstants.DarkGreen)
    return ret


def q_stacked_bar_series(*bar_sets: QBarSet) -> QStackedBarSeries:
    ret = QStackedBarSeries()
    for bar_set in bar_sets:
        ret.append(bar_set)
    return ret


def get_key(when: 'date') -> str:
    return (
        f'{when.year}/{when.month:02d}' if when.day == 1 else f'{when.year}/13'
    )


def infos_to_data(infos: list[Info]) -> list[tuple[str, float, float]]:
    ret = []
    for info in infos:
        key = get_key(info.when)

        trattenute = ZERO
        competenze = ZERO
        for additional_detail in info.additional_details:
            trattenute += additional_detail.trattenute
            competenze += additional_detail.competenze

        ret.append((key, float(trattenute), float(competenze)))

    return ret


def stacked() -> QWidget:
    infos = load(Settings().data_path)
    data = infos_to_data(infos)

    axis_x = q_bar_category_axis('Mensilità', [t[0] for t in data])
    axis_y = q_value_axis('€')

    stacked_bar_series = q_stacked_bar_series(
        q_bar_set('netto', [t[2] - t[1] for t in data], QColorConstants.Green),
        q_bar_set(
            'trattenute', [t[1] for t in data], QColorConstants.DarkMagenta
        ),
    )

    chart = QChart()
    chart.addSeries(stacked_bar_series)
    chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
    chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
    stacked_bar_series.attachAxis(axis_x)
    stacked_bar_series.attachAxis(axis_y)
    chart.legend().setVisible(True)
    chart.legend().setAlignment(Qt.AlignmentFlag.AlignBottom)

    axis_y.applyNiceNumbers()

    return QChartView(chart)


def main() -> None:
    app = QApplication(argv)
    w = stacked()
    w.resize(1280, 720)
    w.show()
    raise SystemExit(app.exec())


if __name__ == '__main__':
    main()
