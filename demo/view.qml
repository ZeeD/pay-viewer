import QtQuick
import QtQuick.Controls

RangeSlider {
    signal first_moved(real first_value)
    signal second_moved(real second_value)

    from: 1
    to: 100
    first.value: 25
    second.value: 75

    first.onMoved: first_moved(first.value)
    second.onMoved: second_moved(second.value)
}
