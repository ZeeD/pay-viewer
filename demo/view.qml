import QtQuick
import QtQuick.Controls

RangeSlider {
    signal first_moved(real first_value)
    signal second_moved(real second_value)

    first.onMoved: first_moved(first.value)
    second.onMoved: second_moved(second.value)
}
