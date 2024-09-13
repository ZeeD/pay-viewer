from collections import defaultdict
from decimal import Decimal
from itertools import chain
from statistics import mean
from typing import NamedTuple

from PySide6.QtCharts import QBarCategoryAxis
from PySide6.QtCharts import QBarSeries
from PySide6.QtCharts import QBarSet
from PySide6.QtCharts import QChart
from PySide6.QtCharts import QChartView
from PySide6.QtCharts import QValueAxis
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
from urllib3 import request

from payviewer.loader import load
from payviewer.model import ColumnHeader
from payviewer.model import Info
from payviewer.settings import Settings


def istat_client(year: int, mean_: Decimal) -> Decimal:
    somma = f'{mean_:.2f}'.replace('.', '%2C')
    response = request(
        'POST',
        'https://rivaluta.istat.it/Rivaluta/Widget/CalcolatoreCoefficientiAction.action',
        body=f'PERIODO=1&meseDa=Media%20Annua&annoDa={year}&meseA=Giugno&annoA=2024&SOMMA={somma}&EUROLIRE=true&',
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
    )
    raw_html = response.data.decode('latin1')
    try:
        raw_line = raw_html.splitlines()[38]
    except IndexError:
        return mean_
    raw_value = raw_line.split('"')[5]
    return Decimal(raw_value.replace('.', '').replace(',', '.'))


def get_yearly_incomes(infos: list[Info]) -> dict[int, list[Decimal]]:
    yearly_incomes = defaultdict[int, list[Decimal]](list)
    for info in infos:
        year = info.when.year
        income = info.howmuch(ColumnHeader.netto_da_pagare)
        if income is None:
            raise ValueError

        yearly_incomes[year].append(income)
    return yearly_incomes


def get_yearly_means(
    yearly_incomes: dict[int, list[Decimal]],
) -> dict[int, Decimal]:
    return {year: mean(incomes) for year, incomes in yearly_incomes.items()}


class MeanIstat(NamedTuple):
    mean: Decimal
    istat: Decimal


def get_yearly_means_istat(
    yearly_means: dict[int, Decimal],
) -> dict[int, MeanIstat]:
    return {
        year: MeanIstat(mean_, istat_client(year, mean_))
        for year, mean_ in yearly_means.items()
    }


class MeanIstatDelta(NamedTuple):
    mean: Decimal
    istat: Decimal
    delta: Decimal
    delta_istat: Decimal


def get_yearly_means_istat_delta(
    yearly_means_istat: dict[int, MeanIstat],
) -> dict[int, MeanIstatDelta]:
    (year, (mean_, istat)), *tail = sorted(yearly_means_istat.items())

    ret = {}
    ret[year] = MeanIstatDelta(mean_, istat, Decimal(0), Decimal(0))
    prev_mean = mean_
    prev_istat = istat
    for year, (mean_, istat) in tail:
        delta = mean_ - prev_mean
        delta_istat = istat - prev_istat
        ret[year] = MeanIstatDelta(mean_, istat, delta, delta_istat)
        prev_mean = mean_
        prev_istat = istat
    return ret


class HMeanIstat(NamedTuple):
    h_year: str
    h_mean: str
    h_istat: str


class HMeanIstatDelta(NamedTuple):
    h_year: str
    h_mean: str
    h_istat: str
    h_delta: str
    h_delta_istat: str


def dump(
    yearly_infos: dict[int, MeanIstat] | dict[int, MeanIstatDelta],
    headers: HMeanIstat | HMeanIstatDelta,
) -> None:
    if isinstance(headers, HMeanIstat):
        h_year, h_mean, h_istat = headers
        print(f'{h_year},{h_mean},{h_istat}')  # noqa: T201
    else:
        h_year, h_mean, h_istat, h_delta, h_delta_istat = headers
        print(  # noqa: T201
            f'{h_year},{h_mean},{h_istat},{h_delta},{h_delta_istat}'
        )

    for year, infos in sorted(yearly_infos.items()):
        if isinstance(infos, MeanIstat):
            mean, istat = infos
            print(f'{year},{mean:.2f},{istat:.2f}')  # noqa: T201
        elif isinstance(infos, MeanIstatDelta):
            mean, istat, delta, delta_istat = infos
            print(  # noqa: T201
                f'{year},{mean:.2f},{istat:.2f},{delta:.2f},{delta_istat:.2f}'
            )
        else:
            raise TypeError(type(infos))


def main() -> None:
    infos = load(Settings().data_path)
    yearly_incomes = get_yearly_incomes(infos)
    yearly_means = get_yearly_means(yearly_incomes)
    yearly_means_istat = get_yearly_means_istat(yearly_means)

    app = QApplication([__file__])
    ms, is_ = zip(*yearly_means_istat.values(), strict=True)
    mean = QBarSet('mean')
    mean.append([float(m) for m in ms])
    istat = QBarSet('istat')
    istat.append(is_)

    categories = QBarCategoryAxis()
    categories.append([str(y) for y in yearly_means_istat])
    axis_y  = QValueAxis()
    axis_y.setRange(min(chain(ms, is_)), max(chain(ms, is_)))

    series = QBarSeries()
    series.append(mean)
    series.append(istat)
    series.attachAxis(categories)
    series.attachAxis(axis_y)

    chart = QChart()
    chart.addSeries(series)
    chart.addAxis(categories, Qt.AlignmentFlag.AlignBottom)
    chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)


    mainui = QChartView()
    mainui.setChart(chart)
    mainui.resize(1024, 600)
    mainui.show()

    raise SystemExit(app.exec())


if __name__ == '__main__':
    main()
