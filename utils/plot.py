import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import matplotlib.font_manager as fm
from scipy.signal import savgol_filter

# ✅ 기본 폰트 설정
plt.rcParams["font.family"] = "NanumGothic"
plt.rcParams["axes.unicode_minus"] = False
plt.style.use("seaborn-v0_8-bright")

line_color = {
    "blue": "#1681A3",
    "yellow_gold": "#F4CC60",
    "deep_purple": "#66477D",
    "light_green": "#A7D84C",
    "vermilion": "#CD4633",
    "soft_orange": "#F99D5C",
    "sky_blue": "#94DBD3",
}

def smooth_series(series, window=7, polyorder=3):
    """데이터 부드럽게 만들기 (Savitzky-Golay 필터 적용)"""
    return savgol_filter(series, window_length=window, polyorder=polyorder)

def plot_backtest_results(df, trades, short_sma, long_sma):
    """백테스트 결과 시각화 (블로그 방식의 Minor Tick 적용)"""
    fig, ax = plt.subplots(3, 1, figsize=(16, 9), gridspec_kw={"height_ratios": [3, 1, 1]})

    # ✅ 1️⃣ 주가 & 이동평균선
    ax[0].plot(df.index, smooth_series(df["close"]), label="주가", color=line_color["blue"], linewidth=1.2, alpha=0.9)
    ax[0].plot(df.index, smooth_series(short_sma), label="SMA10", color=line_color["yellow_gold"], linestyle="--", linewidth=1.5, alpha=0.8)
    ax[0].plot(df.index, smooth_series(long_sma), label="SMA50", color=line_color["deep_purple"], linestyle="--", linewidth=1.5, alpha=0.8)

    # ✅ 매매 시그널 (매수/매도)
    for trade in trades:
        if trade["type"] == "buy":
            ax[0].scatter(trade["date"], trade["price"], marker="^", color="#4CAF50", s=100, edgecolors="#555", linewidth=1.2, alpha=0.9, zorder=3)
        elif trade["type"] == "sell":
            ax[0].scatter(trade["date"], trade["price"], marker="v", color="#E53935", s=100, edgecolors="#555", linewidth=1.2, alpha=0.9, zorder=3)

    ax[0].legend(loc="upper left", fontsize=10, frameon=False)
    ax[0].set_title("주가 & 이동평균선", fontsize=11, fontweight="medium", pad=10)
    ax[0].set_ylabel("주가 ($)", fontsize=10, fontweight="medium")

    # ✅ 2️⃣ 거래량
    ax[1].bar(df.index, df["volume"], color="gray", alpha=0.4, width=0.8)
    ax[1].set_title("거래량", fontsize=11, fontweight="medium", pad=10)
    ax[1].set_ylabel("거래량", fontsize=10, fontweight="medium")

    # ✅ 3️⃣ 수익률(PnL)
    pnl = df["close"].pct_change().cumsum()
    ax[2].plot(df.index, smooth_series(pnl), label="수익률", color="#9C27B0", linewidth=1.8, alpha=0.9)
    ax[2].axhline(0, linestyle="--", color="#666", alpha=0.5)
    ax[2].set_title("누적 수익률", fontsize=11, fontweight="medium", pad=10)
    ax[2].set_ylabel("수익률 (%)", fontsize=10, fontweight="medium")

    # ✅ X축 Major/Minor Tick 설정 (균등 분배)
    for axis in ax:
        # ✔ Major Tick: 매월 15일 (중간 날짜)
        axis.xaxis.set_major_locator(mdates.MonthLocator(bymonthday=15))
        axis.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))

        # ✔ Minor Tick: 7일 간격 (모든 월에서 균일한 분배)
        axis.xaxis.set_minor_locator(mdates.DayLocator(interval=7))
        axis.xaxis.set_minor_formatter(mdates.DateFormatter("%d"))

        # ✔ Minor Label을 X축 위쪽으로 이동 & 색상 변경
        axis.xaxis.set_tick_params(which="minor", pad=10, labeltop=False, labelbottom=True)
        plt.setp(axis.xaxis.get_minorticklabels(), fontsize=8, fontweight="light", color="gray")


    plt.subplots_adjust(hspace=0.4)
    plt.show()
