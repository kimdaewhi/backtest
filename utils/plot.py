import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import matplotlib.font_manager as fm

# ✅ 기본 폰트를 'NanumGothic'으로 변경
plt.rcParams['font.family'] = 'NanumGothic'
plt.rcParams['axes.unicode_minus'] = False

plt.style.use('seaborn-v0_8-bright')

def plot_backtest_results(df, trades, short_sma, long_sma):
    """ Backtest Visualization - Clean & Modern """
    fig, ax = plt.subplots(3, 1, figsize=(16, 9), gridspec_kw={'height_ratios': [3, 1, 1]})

    # ✅ 1️⃣ Price & SMA (라인 두께 조정)
    ax[0].plot(df.index, df['close'], label="Price", color="#444", linewidth=1.2, alpha=0.9)  
    ax[0].plot(df.index, short_sma, label="SMA10", color="#FF6F61", linestyle="--", linewidth=1.5, alpha=0.8)
    ax[0].plot(df.index, long_sma, label="SMA50", color="#5B84B1", linestyle="--", linewidth=1.5, alpha=0.8)

    # ✅ Trade Signals (컬러 변경 & 투명도 조절)
    for trade in trades:
        color, marker = ('#6ABF69', '^') if trade['type'] == 'buy' else ('#E57373', 'v')
        ax[0].scatter(trade['date'], trade['price'], marker=marker, color=color, s=75, edgecolors='black', linewidth=0.6, alpha=0.8)

    ax[0].legend(loc="upper left", fontsize=10, frameon=False)
    ax[0].set_title("Price & Moving Averages", fontsize=12, fontweight="medium", pad=10)
    ax[0].set_ylabel("Price ($)", fontsize=10, fontweight="medium")
    ax[0].spines['top'].set_visible(False)
    ax[0].spines['right'].set_visible(False)
    ax[0].spines['left'].set_color("#999")  
    ax[0].spines['bottom'].set_color("#999")  

    # ✅ 2️⃣ Volume
    ax[1].bar(df.index, df['volume'], color="gray", alpha=0.4, width=0.8)
    ax[1].set_title("Volume", fontsize=12, fontweight="medium", pad=10)
    ax[1].set_ylabel("Volume", fontsize=10, fontweight="medium")
    ax[1].spines['top'].set_visible(False)
    ax[1].spines['right'].set_visible(False)
    ax[1].spines['left'].set_color("#999")
    ax[1].spines['bottom'].set_color("#999")

    # ✅ 3️⃣ Cumulative PnL (라인 두께 조정)
    pnl = df['close'].pct_change().cumsum()
    ax[2].plot(df.index, pnl, label="PnL", color="#9C27B0", linewidth=1.8, alpha=0.9)
    ax[2].axhline(0, linestyle="--", color="#666", alpha=0.5)  
    ax[2].set_title("Cumulative PnL", fontsize=12, fontweight="medium", pad=10)
    ax[2].set_ylabel("PnL (%)", fontsize=10, fontweight="medium")
    ax[2].spines['top'].set_visible(False)
    ax[2].spines['right'].set_visible(False)
    ax[2].spines['left'].set_color("#999")
    ax[2].spines['bottom'].set_color("#999")

    # ✅ X축 라벨 기울기 제거 & 폰트 크기 줄이기
    for axis in ax:
        axis.xaxis.set_major_locator(mdates.MonthLocator())
        axis.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        plt.setp(axis.xaxis.get_majorticklabels(), rotation=0, fontsize=9, fontweight="light")

    # ✅ 차트 간 간격 조정
    plt.subplots_adjust(hspace=0.4)

    plt.tight_layout()
    plt.show()
