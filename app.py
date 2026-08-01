import random
import streamlit as st

# ページ設定
st.set_page_config(
    page_title="惑星探索司令室 - Stellar Command",
    page_icon="🚀",
    layout="wide",
)

# --- セッション状態の初期化 ---
if "game_started" not in st.session_state:
    st.session_state.game_started = False


def init_game():
    st.session_state.day = 1
    st.session_state.game_over = False
    st.session_state.game_cleared = False
    st.session_state.global_resources = {
        "食料": 50,
        "医薬品": 30,
        "資源": 40,
        "戦闘部隊": 10,
        "特殊アイテム": 5,
    }

    # 6つの惑星と部隊の初期データ
    st.session_state.planets = {
        "惑星ゾルバ (荒涼とした砂漠)": {
            "hp": 100,
            "morale": 80,
            "status": "探索中",
            "log": "着陸成功。辺り一面に広がる赤茶色の砂漠です。通信の感度は良好ですが、微量の電磁波を検知しています。",
            "video_url": "video/zoruba1.mp4",
        },
        "惑星アイシリア (氷結の世界)": {
            "hp": 100,
            "morale": 70,
            "status": "探索中",
            "log": "着陸地点は一面の氷原です。気温マイナス60度。防寒スーツのヒーターがフル稼働していますが、エネルギー消費が激しいです。",
            "video_url": "video/aisiria1.mp4",
        },
        "惑星ベルデ (巨大ジャングル)": {
            "hp": 100,
            "morale": 90,
            "status": "探索中",
            "log": "着陸地点は酸性雨と巨大植物に覆われたジャングルです。未知の植物から甘い芳香が漂っていますが、毒性に注意が必要です。",
            "video_url": "video/berude1.png",
        },
        "惑星ネビュラ (ガス状浮遊大陸)": {
            "hp": 100,
            "morale": 75,
            "status": "探索中",
            "log": "足場が不安定です。特殊アイテムが役立ちそうです。",
            "video_url": "video/aisiria1.mp4",
        },
        "惑星オメガ (機械文明の廃墟)": {
            "hp": 100,
            "morale": 60,
            "status": "探索中",
            "log": "防衛ドローンが作動しました。戦闘部隊の支援が必要です。",
            "video_url": "video/aisiria1.mp4",
        },
        "惑星ヘイロー (高放射線帯)": {
            "hp": 100,
            "morale": 65,
            "status": "探索中",
            "log": "放射線量が上昇中。医薬品の消費が激しいです。",
            "video_url": "video/aisiria1.mp4",
        },
    }
    st.session_state.game_started = True


if not st.session_state.game_started:
    init_game()

# --- タイトル ---
st.title("🚀 惑星探索司令室: Stellar Command")
st.markdown(
    "6つの異なる惑星に派遣された探索部隊を管理し、**5日間の生存と全員の帰還**を目指せ！"
)
st.markdown("---")

# --- ゲーム終了・クリア判定 ---
active_planets = [
    p for p, data in st.session_state.planets.items() if data["status"] == "探索中"
]
destroyed_planets = [
    p for p, data in st.session_state.planets.items() if data["status"] == "全滅"
]

if st.session_state.day > 5:
    st.session_state.game_cleared = True

if len(destroyed_planets) >= 3:
    st.session_state.game_over = True

# --- 画面表示制御 ---
if st.session_state.game_cleared:
    st.balloons()
    st.success("🎉 おめでとうございます！全部隊が5日間の任務を完了し、帰還しました！")
    if st.button("もう一度プレイする"):
        init_game()
        st.rerun()
    st.stop()

if st.session_state.game_over:
    st.error(
        "💀 ゲームオーバー: 3つ以上の部隊が全滅、または司令部の管理が崩壊しました。"
    )
    if st.button("リトライ"):
        init_game()
        st.rerun()
    st.stop()

# --- サイドバー: 司令部リソース管理 ---
st.sidebar.header(f"📅 経過日数: 5日中 {st.session_state.day}日目")
st.sidebar.subheader("📦 司令部保有物資")

# リソース表示と補充
col_s1, col_s2 = st.sidebar.columns(2)
with col_s1:
    st.metric("食料", st.session_state.global_resources["食料"])
    st.metric("医薬品", st.session_state.global_resources["医薬品"])
    st.metric("資源", st.session_state.global_resources["資源"])
with col_s2:
    st.metric("戦闘部隊", st.session_state.global_resources["戦闘部隊"])
    st.metric("特殊アイテム", st.session_state.global_resources["特殊アイテム"])

st.sidebar.markdown("---")
st.sidebar.info(
    "各惑星の状況（レポートと動画）を確認し、必要な物資を割り当てて「翌日へ進む」を押してください。"
)

if st.sidebar.button("🚨 ゲームをリセット"):
    init_game()
    st.rerun()

# --- メイン画面: 惑星ごとの状況と物資配分 ---
st.header("📡 惑星からの日報と物資配分")

# 配分入力を保存する辞書
allocations = {}

for planet_name, data in st.session_state.planets.items():
    with st.expander(
        f"🌍 {planet_name} (状態: {data['status']}) - HP: {data['hp']} | 士気: {data['morale']}",
        expanded=True,
    ):
        if data["status"] == "全滅":
            st.error("この部隊はすでに全滅しました……。")
            continue

        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown(f"**💬 現地からのレポート:**")
            st.info(data["log"])
            st.markdown(f"**🎥 現場からの映像・画像記録:**")
            media_path = data["video_url"]
            # 拡張子を小文字で取得して画像かどうかを判定
            if media_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')):
                st.image(media_path, use_column_width=True)
            else:
                st.video(media_path)
        with col2:
            st.markdown(f"**🛠️ 物資配分 (本日の補給)**")
            f_food = st.slider(
                "食料",
                0,
                10,
                2,
                key=f"food_{planet_name}",
                help="部隊のHPと士気を維持します",
            )
            f_med = st.slider(
                "医薬品",
                0,
                5,
                1,
                key=f"med_{planet_name}",
                help="負傷を治療します",
            )
            f_res = st.slider(
                "資源",
                0,
                5,
                1,
                key=f"res_{planet_name}",
                help="インフラを修復します",
            )
            f_com = st.slider(
                "戦闘部隊",
                0,
                3,
                0,
                key=f"com_{planet_name}",
                help="危険な敵や障害に対応します",
            )
            f_sp = st.slider(
                "特殊アイテム",
                0,
                2,
                0,
                key=f"sp_{planet_name}",
                help="環境に応じた特殊な危機を回避します",
            )

            allocations[planet_name] = {
                "食料": f_food,
                "医薬品": f_med,
                "資源": f_res,
                "戦闘部隊": f_com,
                "特殊アイテム": f_sp,
            }

st.markdown("---")

# --- ターン進行ボタン ---
if st.button("🚀 物資を送信して翌日へ進む", type="primary", use_container_width=True):
    # 総消費量の計算
    total_consumed = {
        "食料": sum(a["食料"] for a in allocations.values()),
        "医薬品": sum(a["医薬品"] for a in allocations.values()),
        "資源": sum(a["資源"] for a in allocations.values()),
        "戦闘部隊": sum(a["戦闘部隊"] for a in allocations.values()),
        "特殊アイテム": sum(a["特殊アイテム"] for a in allocations.values()),
    }

    # 保有量チェック
    shortage = False
    for k in st.session_state.global_resources:
        if st.session_state.global_resources[k] < total_consumed[k]:
            st.error(
                f"⚠️ 物資「{k}」が不足しています！配分量を見直してください。(保有: {st.session_state.global_resources[k]} / 要求: {total_consumed[k]})"
            )
            shortage = True

    if not shortage:
        # リソースの減算
        for k in st.session_state.global_resources:
            st.session_state.global_resources[k] -= total_consumed[k]

        # 各惑星の環境シミュレーションとイベント更新
        logs_pool = [
            "現地の環境が安定しています。順調にサンプルを回収中。",
            "突発的な天候悪化により、物資の消費が増加しました。",
            "未確認の遺跡からエネルギー反応を検知しました。",
            "通信障害が発生しましたが、自力で復旧しました。",
            "現地生物の接近がありましたが、無事にやり過ごしました。",
        ]

        for planet_name, data in st.session_state.planets.items():
            if data["status"] == "全滅":
                continue

            alloc = allocations[planet_name]

            # HPと士気の増減計算
            # 食料がないとHP・士気低下
            hp_change = (
                (alloc["食料"] * 3)
                + (alloc["医薬品"] * 5)
                + (alloc["資源"] * 2)
                - 10
            )
            data["hp"] = max(0, min(100, data["hp"] + hp_change))
            data["morale"] = max(
                0, min(100, data["morale"] + (alloc["食料"] * 2) - 5)
            )

            # HPが0になったら全滅
            if data["hp"] <= 0:
                data["status"] = "全滅"
                data["log"] = (
                    "🚨 通信が途絶えました。部隊からの応答がありません……。"
                )
            else:
                data["log"] = random.choice(logs_pool)

        # 日数を進める
        st.session_state.day += 1

        # 毎日少しだけ司令部リソースを自然回復・補給
        st.session_state.global_resources["食料"] += 15
        st.session_state.global_resources["医薬品"] += 8
        st.session_state.global_resources["資源"] += 10

        st.rerun()
