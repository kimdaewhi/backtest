import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import matplotlib.font_manager as fm

plt.rcParams['font.family'] = 'NanumGothic'  # Windows: 맑은 고딕
plt.rcParams['axes.unicode_minus'] = False  # ✅ 음수(-) 기호 깨짐 방지

plt.style.use('seaborn-v0_8-darkgrid')  # ✅ 스타일 변경

def plot_backtest_results(df, trades, short_sma, long_sma):
    """ 백테스트 결과를 보기 좋은 차트로 시각화 """
    fig, ax = plt.subplots(3, 1, figsize=(16, 10), gridspec_kw={'height_ratios': [3, 1, 1]})
    
    # 1️⃣ 가격 차트 + 이동평균선
    ax[0].plot(df.index, df['close'], label="종가 (Closing Price)", color="#333333", linewidth=2)
    ax[0].plot(df.index, short_sma, label="단기 이동평균선 (SMA10)", color="#FF5733", linestyle="--", linewidth=2, alpha=0.8)
    ax[0].plot(df.index, long_sma, label="장기 이동평균선 (SMA50)", color="#338AFF", linestyle="--", linewidth=2, alpha=0.8)

    # 매매 신호 표시
    for trade in trades:
        if trade['type'] == 'buy':
            ax[0].scatter(trade['date'], trade['price'], marker='^', color='#28A745', s=150, edgecolors='black', zorder=3, label="매수 신호 (BUY)")
            ax[0].annotate("매수", (trade['date'], trade['price']), textcoords="offset points", xytext=(-10,10), ha='center', fontsize=10, color="green")
        elif trade['type'] == 'sell':
            ax[0].scatter(trade['date'], trade['price'], marker='v', color='#DC3545', s=150, edgecolors='black', zorder=3, label="매도 신호 (SELL)")
            ax[0].annotate("매도", (trade['date'], trade['price']), textcoords="offset points", xytext=(-10,-15), ha='center', fontsize=10, color="red")

    ax[0].legend(loc="upper left", fontsize=12)
    ax[0].set_title("📈 주가 및 이동평균선", fontsize=14, fontweight="bold")
    ax[0].set_ylabel("가격 (₩)", fontsize=12)
    ax[0].grid(True, linestyle="--", alpha=0.5)

    # 2️⃣ 거래량 차트
    ax[1].bar(df.index, df['volume'], color="#6C757D", alpha=0.7, width=0.8)
    ax[1].set_title("📊 거래량 (Trading Volume)", fontsize=14, fontweight="bold")
    ax[1].set_ylabel("거래량", fontsize=12)
    ax[1].grid(True, linestyle="--", alpha=0.5)

    # 3️⃣ 누적 수익률 차트
    pnl = df['close'].pct_change().cumsum()  # 누적 수익률 계산
    ax[2].plot(df.index, pnl, label="누적 수익률 (Cumulative PnL)", color="#9C27B0", linewidth=2)
    ax[2].axhline(0, linestyle="--", color="black", alpha=0.5)
    ax[2].set_title("💰 누적 수익률 (Cumulative PnL)", fontsize=14, fontweight="bold")
    ax[2].set_ylabel("수익률 (%)", fontsize=12)
    ax[2].grid(True, linestyle="--", alpha=0.5)

    # X축 포맷 조정
    for axis in ax:
        axis.xaxis.set_major_locator(mdates.MonthLocator())
        axis.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        plt.setp(axis.xaxis.get_majorticklabels(), rotation=45, fontsize=10)

    plt.tight_layout()
    plt.show()
