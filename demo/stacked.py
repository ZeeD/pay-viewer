from sys import argv
from typing import TYPE_CHECKING

from PySide6.QtCharts import QBarCategoryAxis
from PySide6.QtCharts import QBarSet
from PySide6.QtCharts import QChart
from PySide6.QtCharts import QChartView
from PySide6.QtCharts import QStackedBarSeries
from PySide6.QtCharts import QValueAxis
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QWidget

from payviewer.loader import load
from payviewer.model import Info
from payviewer.model import get_descrizione
from payviewer.settings import Settings

if TYPE_CHECKING:
    from datetime import date


def q_bar_category_axis(title: str, categories: list[str]) -> QBarCategoryAxis:
    ret = QBarCategoryAxis()
    ret.setTitleText(title)
    ret.append(categories)
    return ret


def q_value_axis(title: str, min_: float, max_: float) -> QValueAxis:
    ret = QValueAxis()
    ret.setTitleText(title)
    ret.setRange(min_, max_)
    # ensure 0 is shown
    ret.setTickCount(1 + (int(max_ - min_) // 1_000))

    return ret


def q_bar_set(label: str, values: list[float]) -> QBarSet:
    for _value in values:
        pass
    ret = QBarSet(label)
    ret.append(values)
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


def infos_to_data(
    infos: list[Info],
) -> list[tuple[str, list[tuple[str, float]]]]:
    all_descrizione = {
        get_descrizione(additional_detail): 0
        for info in infos
        for additional_detail in info.additional_details
    }.keys()

    tmp: dict[str, dict[str, float]] = {
        descrizione: {get_key(info.when): 0 for info in infos}
        for descrizione in all_descrizione
    }
    for info in infos:
        for additional_detail in info.additional_details:
            descrizione = get_descrizione(additional_detail)
            key = get_key(info.when)

            tmp[descrizione][key] = float(
                -additional_detail.trattenute
                if additional_detail.trattenute
                else additional_detail.competenze
            )
    ret: list[tuple[str, list[tuple[str, float]]]] = []
    for descrizione, when_values in tmp.items():
        if all(value == 0 for value in when_values.values()):
            continue

        whens: list[tuple[str, float]] = []
        for when in sorted(when_values):
            value = when_values[when]
            whens.append((when, value))
        ret.append((descrizione, whens))

    return ret


def stacked() -> QWidget:
    infos = load(Settings().data_path)
    data = infos_to_data(infos)

    axis_x = q_bar_category_axis('Month', [t[0] for t in data[0][1]])
    axis_y = q_value_axis('€', -5_000, 10_000)

    stacked_bar_series = q_stacked_bar_series(
        *[
            q_bar_set(descrizione, [t[1] for t in when_values])
            for descrizione, when_values in data
        ]
    )

    chart = QChart()
    chart.addSeries(stacked_bar_series)

    chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
    chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
    stacked_bar_series.attachAxis(axis_x)
    stacked_bar_series.attachAxis(axis_y)

    chart.legend().setVisible(True)
    chart.legend().setAlignment(Qt.AlignmentFlag.AlignLeft)

    return QChartView(chart)


def main() -> None:
    app = QApplication(argv)
    w = stacked()
    w.resize(1280, 720)
    w.show()
    raise SystemExit(app.exec())


if __name__ == '__main__':
    main()
