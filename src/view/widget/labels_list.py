from PyQt5.QtWidgets import QListWidget, QSizePolicy, QPushButton, QListWidgetItem

from src.controller.action.menu import import_label


class LabelsListWidget(QListWidget):

    def __init__(self):
        QListWidget.__init__(self)
        self.setMaximumWidth(150)
        self.setSpacing(15)
        self.itemClicked.connect(import_label)
        self.setStyleSheet("""
        QListWidget::item {
          cursor: pointer;
          display: inline-block;
          min-height: 1em;
          outline: none;
          border: none;
          vertical-align: baseline;
          background: #E0E1E2 none;
          color: rgba(0, 0, 0, 0.6);
          font-family: 'Lato', 'Helvetica Neue', Arial, Helvetica, sans-serif;
          margin: 0em 0.25em 0em 0em;
          padding: 0.78571429em 1.5em 0.78571429em;
          text-transform: none;
          text-shadow: none;
          font-weight: bold;
          line-height: 1em;
          font-style: normal;
          text-align: center;
          text-decoration: none;
          border-radius: 0.28571429rem;
          -webkit-box-shadow: 0px 0px 0px 1px transparent inset, 0px 0em 0px 0px rgba(34, 36, 38, 0.15) inset;
                  box-shadow: 0px 0px 0px 1px transparent inset, 0px 0em 0px 0px rgba(34, 36, 38, 0.15) inset;
          -webkit-user-select: none;
             -moz-user-select: none;
              -ms-user-select: none;
                  user-select: none;
          -webkit-transition: opacity 0.1s ease, background-color 0.1s ease, color 0.1s ease, background 0.1s ease, -webkit-box-shadow 0.1s ease;
          transition: opacity 0.1s ease, background-color 0.1s ease, color 0.1s ease, background 0.1s ease, -webkit-box-shadow 0.1s ease;
          transition: opacity 0.1s ease, background-color 0.1s ease, color 0.1s ease, box-shadow 0.1s ease, background 0.1s ease;
          transition: opacity 0.1s ease, background-color 0.1s ease, color 0.1s ease, box-shadow 0.1s ease, background 0.1s ease, -webkit-box-shadow 0.1s ease;
          will-change: '';
          -webkit-tap-highlight-color: transparent;
        }
        QListWidget::item:hover {
          background-color: #CACBCD;
          background-image: none;
          -webkit-box-shadow: 0px 0px 0px 1px transparent inset, 0px 0em 0px 0px rgba(34, 36, 38, 0.15) inset;
                  box-shadow: 0px 0px 0px 1px transparent inset, 0px 0em 0px 0px rgba(34, 36, 38, 0.15) inset;
          color: rgba(0, 0, 0, 0.8);
        }
        """)

        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(1)
        self.setSizePolicy(size_policy)

    def add_label(self, label_name):
        label_widget_item = LabelWidgetItem(label_name, self)
        self.addItem(label_widget_item)


class LabelWidgetItem(QListWidgetItem):
    parent: LabelsListWidget

    def __init__(self, name, parent):
        QListWidgetItem.__init__(self)
        self.parent = parent
        self.setText(name)
