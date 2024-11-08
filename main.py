import sys
import webbrowser
from scanner import ScannerThread
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel,QListWidget,QProgressBar,QHBoxLayout,QComboBox,QMenu
from PyQt5.QtCore import Qt
from helpers import replace_coin_info, check_trading_chart

class CryptoTradingApp(QWidget):
    def __init__(self, chart_is_enabled):
        super().__init__()
        self.chart_is_enabled = chart_is_enabled
        self.setWindowTitle("Crypto Trading App")
        self.setGeometry(100, 100, 1000, 500)


        self.layout = QVBoxLayout()


        self.timeframe_label = QLabel("Select Timeframe:")
        self.timeframe_combo = QComboBox()
        self.timeframe_combo.setFixedWidth(150)
        self.timeframe_combo.addItems(['1m', '5m', '15m', '1h', '4h', '1d'])
        self.timeframe_combo.setCurrentIndex(5)


        self.title_layout = QHBoxLayout()
        self.buy_label = QLabel("Buy Zone")
        self.sell_label = QLabel("Sell Zone")
        self.safe_zone = QLabel("Safe Zone")
        

        self.title_layout.addWidget(self.buy_label)
        self.title_layout.addWidget(self.sell_label)
        self.title_layout.addWidget(self.safe_zone)


        self.buy_list = QListWidget()
        self.sell_list = QListWidget()
        self.safe_zone = QListWidget()


        self.log_layout = QHBoxLayout()
        self.log_layout.addWidget(self.buy_list)
        self.log_layout.addWidget(self.sell_list)
        self.log_layout.addWidget(self.safe_zone)


        self.button = QPushButton("Run Analysis")
        self.button.clicked.connect(self.run_analysis)


        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)


        self.label = QLabel("Results:")
        
        self.layout.addWidget(self.timeframe_label)
        self.layout.addWidget(self.timeframe_combo)
        self.layout.addWidget(self.label)
        self.layout.addLayout(self.title_layout)
        self.layout.addLayout(self.log_layout)
        self.layout.addWidget(self.progress_bar)
        self.layout.addWidget(self.button)

        self.buy_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.sell_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.safe_zone.setContextMenuPolicy(Qt.CustomContextMenu)

        self.buy_list.customContextMenuRequested.connect(self.show_context_menu)
        self.sell_list.customContextMenuRequested.connect(self.show_context_menu)
        self.safe_zone.customContextMenuRequested.connect(self.show_context_menu)
        
        self.setLayout(self.layout)

    def show_context_menu(self, pos):
        menu = QMenu(self)
        if self.chart_is_enabled:
            open_url_action = menu.addAction("Open in Browser")

            action = menu.exec_(self.sender().mapToGlobal(pos))

            if action == open_url_action:
                item = self.sender().currentItem()

                replace_coin_info(item.text(), self.get_tradingview_timeframe())
                if item:
                    webbrowser.open("http://localhost:3000")

    def run_analysis(self):
        self.buy_list.clear()
        self.sell_list.clear()
        self.safe_zone.clear()
        self.progress_bar.setValue(0)
        self.button.setDisabled(True)
        self.timeframe_combo.setDisabled(True)
        selected_interval = self.timeframe_combo.currentText()
        self.thread = ScannerThread(interval=selected_interval)
        self.thread.update_progress.connect(self.update_progress)
        self.thread.finished.connect(self.update_results)
        self.thread.start()
    
    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def get_tradingview_timeframe(self):
        timeframe = self.timeframe_combo.currentText()
        if timeframe == '1m':
            return '1'
        elif timeframe == '5m':
            return '5'
        elif timeframe == '15m':
            return '15'
        elif timeframe == '1h':
            return '60'
        elif timeframe == '4h':
            return '240'
        elif timeframe == '1d':
            return '1440'

    def update_results(self, result):
        
        for item in result["buy_zone"]:
            symbol = item['symbol']

            self.buy_list.addItem(f"{symbol}")

        for item in result["sell_zone"]:
            symbol = item['symbol']
            self.sell_list.addItem(f"{symbol}")

        for item in result["safe_zone"]:
            symbol = item['symbol']
            self.safe_zone.addItem(f"{symbol} - Info: {item['info']}")

        self.button.setDisabled(False)
        self.timeframe_combo.setDisabled(False)


def main():
    chart_is_enabled = check_trading_chart()
    app = QApplication(sys.argv)
    window = CryptoTradingApp(chart_is_enabled)
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()