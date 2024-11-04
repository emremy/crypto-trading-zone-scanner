# Crypto Trading Zone Scanner

"Crypto Trading Zone Scanner" is a Python project that scans spot-listed coins on Binance, using indicators such as RSI (Relative Strength Index) and Bollinger Bands to determine buy and sell signals across multiple timeframes. The tool can scan data for 1 minute, 5 minutes, 15 minutes, 1 hour, 4 hours, and 1 day intervals, giving users flexibility in monitoring market trends.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)

---

## Features

- Scans Binance spot-listed coins for RSI and Bollinger Band values
- Determines buy and sell signals based on market indicators
- Supports multiple timeframes: 1 minute, 5 minutes, 15 minutes, 1 hour, 4 hours, and 1 day
- Can be customized to add more indicators or adjust buy/sell thresholds

## Requirements

- Python 3.12.4
- Homebrew
- Git

> **Note**: Please ensure that your environment has `ta-lib` installed, as this library is essential for technical analysis.

## Installation

Clone this repository to your local machine:

```bash
git clone https://github.com/your-username/crypto-trading-zone-scanner.git
cd crypto-trading-zone-scanner
pip install -r requirements.txt
python main.py
```

Install nuxt project(optional):

```bash
sh install-nuxt-tradingview.sh
```

Start project:

```bash
sh start.sh
```

Special thanks to [@volkanakkus](https://github.com/volkanakkus)
