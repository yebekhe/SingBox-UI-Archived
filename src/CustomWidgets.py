from PyQt6.QtGui import QColor, QBrush, QPaintEvent, QPainter, QRadialGradient
from PyQt6.QtWidgets import QCheckBox, QPushButton, QStyleOption, QStyle
from PyQt6.QtCore import (
    Qt, QSize, QPoint, QPointF, QRectF, QRect,
    QEasingCurve, QPropertyAnimation, QSequentialAnimationGroup,
    pyqtSlot, pyqtProperty, QTimer)

class SwitchButton(QCheckBox):
    def __init__(self,
                 parent=None,
                 bar_color='#808080aa',
                 checked_color="#00B0ff",
                 handle_color=Qt.GlobalColor.white,
                 pulse_unchecked_color="#44999999",
                 pulse_checked_color="#4400b0ee"):
        super().__init__(parent)

        self.bar_brush = QBrush(QColor(bar_color).lighter(130))
        self.bar_checked_brush = QBrush(QColor(checked_color).lighter(130))
        self.handle_brush = QBrush(handle_color)
        self.handle_checked_brush = QBrush(QColor(checked_color))
        self.pulse_unchecked_animation = QBrush(QColor(pulse_unchecked_color))
        self.pulse_checked_animation = QBrush(QColor(pulse_checked_color))

        self.setContentsMargins(8, 0, 8, 0)
        self._handle_position = 0
        self._pulse_radius = 0

        self.animation = QPropertyAnimation(self, b"handle_position", self)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.animation.setDuration(200)  # time in ms

        self.pulse_anim = QPropertyAnimation(self, b"pulse_radius", self)
        self.pulse_anim.setDuration(350)  # time in ms
        self.pulse_anim.setStartValue(10)
        self.pulse_anim.setEndValue(20)

        self.animations_group = QSequentialAnimationGroup()
        self.animations_group.addAnimation(self.animation)
        self.animations_group.addAnimation(self.pulse_anim)

        self.stateChanged.connect(self.setup_animation)

    def sizeHint(self):
        return QSize(60, 45)

    def hitButton(self, pos: QPoint):
        return self.contentsRect().contains(pos)

    @pyqtSlot(int)
    def setup_animation(self, value):
        self.animations_group.stop()
        if value:
            self.animation.setEndValue(1)
        else:
            self.animation.setEndValue(0)
        self.animations_group.start()

    def paintEvent(self, e: QPaintEvent):
        contRect = self.contentsRect()
        handleRadius = round(0.24 * contRect.height())

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.GlobalColor.transparent)
        barRect = QRectF(0, 0, contRect.width() - handleRadius, 0.40 * contRect.height())
        barRect.moveCenter(QPointF(contRect.center()))
        rounding = barRect.height() / 2

        trailLength = contRect.width() - 2 * handleRadius
        xPos = contRect.x() + handleRadius + trailLength * self._handle_position

        if self.pulse_anim.state() == QPropertyAnimation.State.Running:
            painter.setBrush(
                self.pulse_checked_animation if self.isChecked() else self.pulse_unchecked_animation)
            painter.drawEllipse(QPointF(xPos, barRect.center().y()),
                          self._pulse_radius, self._pulse_radius)

        if self.isChecked():
            painter.setBrush(self.bar_checked_brush)
            painter.drawRoundedRect(barRect, rounding, rounding)
            painter.setBrush(self.handle_checked_brush)
        else:
            painter.setBrush(self.bar_brush)
            painter.drawRoundedRect(barRect, rounding, rounding)
            painter.setPen(Qt.GlobalColor.lightGray)
            painter.setBrush(self.handle_brush)

        painter.drawEllipse(QPointF(xPos, barRect.center().y()),
                            handleRadius, handleRadius)
        painter.end()

    @pyqtProperty(float)
    def handle_position(self):
        return self._handle_position

    @handle_position.setter
    def handle_position(self, pos):
        self._handle_position = pos
        self.update()

    @pyqtProperty(float)
    def pulse_radius(self):
        return self._pulse_radius

    @pulse_radius.setter
    def pulse_radius(self, pos):
        self._pulse_radius = pos
        self.update()


class RoundToggleButton(QPushButton):
    def __init__(self,
                 parent=None, 
                 is_dark=False,
                 unchecked_color="#e53935", 
                 checked_color="#66bb6a",
                 curve_color="#1fa5f3",):
        super().__init__(parent)
        
        self.animation_duration = 600  # in ms
        self.animation_steps = 12
        self.radius = 65

        self.checked_color = QColor(checked_color)
        self.unchecked_color = QColor(unchecked_color)
        self.curve_color = QColor(curve_color)
        background_color = '#eee'
        if is_dark:
            self.curve_color = self.curve_color.lighter(130)
            background_color = '#212d40'
        self.background_color = QColor(background_color)
        self.current_color = self.unchecked_color
        self.target_color = self.unchecked_color
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.animate_color)
        self.setCheckable(True)
        self.clicked.connect(self.toggle_animation)
        
    def toggle_animation(self):
        self.target_color = self.checked_color if self.isChecked() else self.unchecked_color
        self.animation_timer.start(self.animation_duration // self.animation_steps)

    def animate_color(self):
        if self.current_color == self.target_color:
            self.animation_timer.stop()
            return

        step_size = 1.0 / self.animation_steps
        r = self.current_color.red() + int(step_size * (self.target_color.red() - self.current_color.red()))
        g = self.current_color.green() + int(step_size * (self.target_color.green() - self.current_color.green()))
        b = self.current_color.blue() + int(step_size * (self.target_color.blue() - self.current_color.blue()))
        self.current_color = QColor(r, g, b)
        self.update()

    def hitButton(self, pos: QPoint): # limit the position of clickable area
        return QRect(138, 70, 117, 115).contains(pos)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        opt = QStyleOption()
        opt.initFrom(self)     
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, opt, painter, self)
        painter.setPen(Qt.GlobalColor.transparent)

        radius = self.radius
        center = QPointF(self.rect().center())
        #draw background curves
        painter.setBrush(QBrush(self.curve_color))
        painter.drawEllipse(center, 500, 500)
        painter.setBrush(QBrush(self.background_color))
        center.setY(center.y()+90)
        painter.drawEllipse(center, 250, 100)
        center.setY(center.y()-90)
        # Draw main button
        gradient = QRadialGradient(center, radius, center)
        gradient.setColorAt(0, self.current_color)
        gradient.setColorAt(1, self.current_color.darker(150))
        painter.setBrush(QBrush(gradient))
        painter.drawEllipse(center, radius, radius)
        #Draw the connect/disconnect text
        painter.setPen(QColor(255, 255, 255))
        font = painter.font()
        font.setPointSize(12)
        font.setBold(True)
        painter.setFont(font)
        text = "Connect" if not self.isChecked() else "Disconnect"
        text_rect = QRect(0, 0, self.width(), self.height())
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, text)
        painter.end()