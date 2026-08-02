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

    # 6つの惑星と5日分の全データを定義
    st.session_state.planet_stories = {
        "惑星ゾルバ (荒涼とした砂漠)": {
            1: {
                "log": "着陸成功。辺り一面に広がる赤茶色の砂漠です。通信の感度は良好ですが、微量の電磁波を検知しています。",
                "demand": {"食料": 2, "医薬品": 1, "資源": 3, "戦闘部隊": 0, "特殊アイテム": 0},
                "media": "video/zoruba1.mp4",
            },
            2: {
                "log": "突発的な砂嵐により一時的に視界がゼロに。機体のフィルターが目詰まりを起こしかけています。資源と食料の補給が急務です。",
                "demand": {"食料": 3, "医薬品": 1, "資源": 4, "戦闘部隊": 0, "特殊アイテム": 0},
                "media": "video/zoruba2.mp4",
            },
            3: {
                "log": "砂嵐が去った後、地表が削れて人工物の一部が露出しました。巨大な石造りの門のような遺跡を発見しました。",
                "demand": {"食料": 2, "医薬品": 1, "資源": 3, "戦闘部隊": 0, "特殊アイテム": 0},
                "media": "video/zoruba3.mp4",
            },
            4: {
                "log": "遺跡内部の調査中、自動防衛メカニズムが突発的に起動しました！戦闘部隊の支援がないと突破できません。",
                "demand": {"食料": 2, "医薬品": 2, "資源": 2, "戦闘部隊": 2, "特殊アイテム": 0},
                "media": "video/zoruba4.mp4",
            },
            5: {
                "log": "防衛システムの小康状態を突き、サンプル回収に成功しました。まもなく離脱ポイントへ移動します。帰還を待ちます！",
                "demand": {"食料": 2, "医薬品": 1, "資源": 2, "戦闘部隊": 1, "特殊アイテム": 0},
                "media": "video/zoruba5.mp4",
            },
        },
        "惑星アイシリア (氷結の世界)": {
            1: {
                "log": "着陸地点は一面の氷原です。気温マイナス60度。防寒スーツのヒーターがフル稼働していますが、エネルギー消費が激しいです。",
                "demand": {"食料": 5, "医薬品": 1, "資源": 1, "戦闘部隊": 0, "特殊アイテム": 0},
                "media": "video/aisiria1.mp4",
            },
            2: {
                "log": "観測機器のオイルが凍結し始めました。医薬品と保温資源がないと、隊員の凍傷リスクが高まります。",
                "demand": {"食料": 4, "医薬品": 3, "資源": 2, "戦闘部隊": 0, "特殊アイテム": 0},
                "media": "video/aisiria2.png",
            },
            3: {
                "log": "氷の洞窟を発見。内部に奇妙な熱源反応があります。凍結を溶かすための特殊アイテムが有効そうです。",
                "demand": {"食料": 4, "医薬品": 1, "資源": 1, "戦闘部隊": 0, "特殊アイテム": 2},
                "media": "video/aisiria3.png",
            },
            4: {
                "log": "氷の亀裂（クレバス）に隊員1名が一時落下しましたが自力で脱出。ただし機材の一部が破損しました。",
                "demand": {"食料": 4, "医薬品": 2, "資源": 2, "戦闘部隊": 0, "特殊アイテム": 0},
                "media": "video/aisiria4.png",
            },
            5: {
                "log": "氷の深層から極めて純度の高いエネルギー結晶を採取しました。エンジン出力を最大にして離脱します！",
                "demand": {"食料": 3, "医薬品": 1, "資源": 1, "戦闘部隊": 0, "特殊アイテム": 0},
                "media": "video/aisiria5.png",
            },
        },
        "惑星ベルデ (巨大ジャングル)": {
            1: {
                "log": "着陸地点は酸性雨と巨大植物に覆われたジャングルです。未知の植物から甘い芳香が漂っていますが、毒性に注意が必要です。",
                "demand": {"食料": 2, "医薬品": 3, "資源": 1, "戦闘部隊": 0, "特殊アイテム": 0},
                "media": "video/berude1.png",
            },
            2: {
                "log": "未知の巨大昆虫型生物にキャンプが襲撃されました。幸い撃退しましたが、弾薬と食料が消耗しています。",
                "demand": {"食料": 2, "医薬品": 2, "資源": 1, "戦闘部隊": 3, "特殊アイテム": 0},
                "media": "video/berude2.png",
            },
            3: {
               "log": "ジャングルの奥地に、かつて他文明が建てたと思われる放棄された前線基地の残骸を発見しました。",
                "demand": {"食料": 2, "医薬品": 1, "資源": 3, "戦闘部隊": 1, "特殊アイテム": 0},
                "media": "video/berude3.png",
            },
            4: {
                "log": "毒性の強い霧が発生し、隊員の士気が急低下しています。医薬品の投与と精神ケアが不可欠です。",
                "demand": {"食料": 2, "医薬品": 4, "資源": 1, "戦闘部隊": 0, "特殊アイテム": 1},
                "media": "video/berude4.png",
            },
            5: {
                "log": "新種の医療用有効成分を持つ植物のサンプルを採取完了しました。これより帰還モードに移行します。",
                "demand": {"食料": 2, "医薬品": 2, "資源": 1, "戦闘部隊": 0, "特殊アイテム": 0},
                "media": "video/berude5.png",
            },
        },
        "惑星ネビュラ (ガス状浮遊大陸)": {
            1: {
                "log": "地表が存在せず、数千メートルの空中に岩塊が浮遊しています。重力アンカーを固定して拠点を作りました。",
                "demand": {"食料": 3, "医薬品": 1, "資源": 1, "戦闘部隊": 0, "特殊アイテム": 2},
                "media": "video/nebula1.png",
            },
            2: {
                "log": "突風により、主要な浮遊岩のひとつの軌道がズレました。特殊アイテムを使った軌道安定化が必要です。",
                "demand": {"食料": 3, "医薬品": 1, "資源": 1, "戦闘部隊": 0, "特殊アイテム": 3},
                "media": "video/nebula2.png",
            },
            3: {
                "log": "浮遊大陸のエネルギーコアを発見。重力を操る技術の痕跡を確認しました。資源の配分を増やせば解析が進みます。",
                "demand": {"食料": 3, "医薬品": 1, "資源": 3, "戦闘部隊": 0, "特殊アイテム": 1},
                "media": "video/nebula3.png",
            },
            4: {
                "log": "強烈な磁気嵐が発生し、浮遊アンカーが外れかけました。戦闘部隊の力で強引に固定を死守しています。",
                "demand": {"食料": 3, "医薬品": 1, "資源": 2, "戦闘部隊": 2, "特殊アイテム": 1},
                "media": "video/nebula4.png",
            },
            5: {
                "log": "重力制御装置の核心データを持ち帰ることに成功しました。無重力エリアを脱出し、回収地点へ向かいます。",
                "demand": {"食料": 2, "医薬品": 1, "資源": 2, "戦闘部隊": 0, "特殊アイテム": 1},
                "media": "video/nebula5.png",
            },
        },
        "惑星オメガ (機械文明の廃墟)": {
            1: {
                "log": "かつて高度な機械文明が存在した痕跡を発見しました。しかし、都市のインフラは完全に死んでおらず、不気味に稼働しています。",
                "demand": {"食料": 3, "医薬品": 1, "資源": 2, "戦闘部隊": 1, "特殊アイテム": 0},
                "media": "video/omega1.png",
            },
            2: {
                "log": "都市の防衛ドローンに察知されました。警告音とともに敵性反応が増加中。戦闘部隊の増援がなければ危険です。",
                "demand": {"食料": 3, "医薬品": 1, "資源": 1, "戦闘部隊": 4, "特殊アイテム": 0},
                "media": "video/omega2.png",
            },
            3: {
                "log": "ネットワークの中枢にハッキングを試みています。特殊アイテムを投入すれば、敵の目を欺くことが可能です。",
                "demand": {"食料": 3, "医薬品": 1, "資源": 2, "戦闘部隊": 2, "特殊アイテム": 2},
                "media": "video/omega3.png",
            },
            4: {
                "log": "全自動防衛タレットの猛攻により、前線基地のバリアが限界です。資源を回して早急に修理を！",
                "demand": {"食料": 3, "医薬品": 2, "資源": 3, "戦闘部隊": 3, "特殊アイテム": 0},
                "media": "video/omega4.png",
            },
            5: {
                "log": "敵の中枢を一時停止させることに成功し、機密データを回収しました。完全封鎖される前に脱出します！",
                "demand": {"食料": 2, "医薬品": 1, "資源": 2, "戦闘部隊": 2, "特殊アイテム": 0},
                "media": "video/omega5.png",
            },
        },
        "惑星ヘイロー (高放射線帯)": {
            1: {
                "log": "着陸直後からガイガーカウンターが激しく鳴り響いています。高放射線帯のため、シールド服の着用が必須です。",
                "demand": {"食料": 3, "医薬品": 3, "資源": 1, "戦闘部隊": 0, "特殊アイテム": 0},
                "media": "video/halo1.png",
            },
            2: {
                "log": "放射線酔いによる隊員の体調不良者が続出しています。医薬品の配分を増やさないと数名が行動不能になります。",
                "demand": {"食料": 3, "医薬品": 5, "資源": 1, "戦闘部隊": 0, "特殊アイテム": 0},
                "media": "video/halo2.png",
            },
            3: {
                "log": "放射線をエネルギーに変換して発光する未知の鉱床を発見しました。特殊アイテムがあれば安全に採掘できます。",
                "demand": {"食料": 3, "医薬品": 2, "資源": 2, "戦闘部隊": 0, "特殊アイテム": 2},
                "media": "video/halo3.png",
            },
            4: {
                "log": "放射線量がピークに達し、通信機器に深刻なノイズが入っています。物資の補給が生命線です。",
                "demand": {"食料": 4, "医薬品": 4, "資源": 2, "戦闘部隊": 0, "特殊アイテム": 0},
                "media": "video/halo4.png",
            },
            5: {
                "log": "放射線シールドの耐久限界ギリギリで、全サンプルを回収しました。すぐにこの星から離脱します！",
                "demand": {"食料": 2, "医薬品": 3, "資源": 2, "戦闘部隊": 0, "特殊アイテム": 0},
                "media": "video/halo5.png",
            },
        },
    }

    # 各惑星の初期状態（1日目のデータをセット）
    st.session_state.planets = {}
    for planet_name in st.session_state.planet_stories.keys():
        story = st.session_state.planet_stories[planet_name][1]
        st.session_state.planets[planet_name] = {
            "hp": 100,
            "morale": 80,
            "status": "探索中",
            "log": story["log"],
            "demand": story["demand"],
            "video_url": story["media"],
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

# 特性の説明文を定義
traits_desc = {
    "惑星ゾルバ (荒涼とした砂漠)": "【特性】食料消費少 / 資源消耗大",
    "惑星アイシリア (氷結の世界)": "【特性】資源効率良 / 食料要求大",
    "惑星ベルデ (巨大ジャングル)": "【特性】医薬品節約 / 戦闘部隊必須",
    "惑星ネビュラ (ガス状浮遊大陸)": "【特性】資源消費少 / 特殊アイテム多",
    "惑星オメガ (機械文明の廃墟)": "【特性】要・戦闘部隊 / 高難易度",
    "惑星ヘイロー (高放射線帯)": "【特性】要・医薬品 / 超高難易度",
}

for planet_name, data in st.session_state.planets.items():
    trait_text = traits_desc.get(planet_name, "")
    with st.expander(
        f"🌍 {planet_name} {trait_text} (状態: {data['status']}) - HP: {data['hp']} | 士気: {data['morale']}",
        expanded=True,
    ):
        if data["status"] == "全滅":
            st.error("この部隊はすでに全滅しました……。")
            continue

        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown(f"**💬 現地からのレポート:**")
            st.info(data["log"])

            # --- 追加: 要求物資の表示 ---
            st.markdown(f"**📋 本日の要求物資:**")
            demands = data["demand"]
            # 横並びで要求数を綺麗に表示
            d_cols = st.columns(len(demands))
            for i, (k, v) in enumerate(demands.items()):
                with d_cols[i]:
                    st.metric(k, f"{v}個")

            st.markdown(f"**🎥 現場からの映像・画像記録:**")
            media_path = data["video_url"]
            if media_path.lower().endswith(
                (".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp")
            ):
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

        # 日数を進める（次は何日目になるか）
        # 日数を進める（次は何日目になるか）
        next_day = st.session_state.day + 1

        for planet_name, data in st.session_state.planets.items():
            if data["status"] == "全滅":
                continue

            alloc = allocations[planet_name]
            demand = data["demand"]

            # --- 要求充足度によるシミュレーション計算 ---
            # 不足している分だけペナルティ、ぴったり以上ならボーナス
            hp_diff = 0
            morale_diff = 0

            for resource_key in ["食料", "医薬品", "資源", "戦闘部隊", "特殊アイテム"]:
                sent = alloc[resource_key]
                req = demand[resource_key]

                if sent >= req:
                    # 要求を満たしている場合（余分に送っても少しボーナス）
                    hp_diff += 5 + (sent - req) * 2
                    morale_diff += 5
                else:
                    # 要求を下回っている場合、大幅なペナルティ（特に食料と医薬品・戦闘部隊の不足は致命的）
                    shortage_amount = req - sent
                    if resource_key in ["食料", "医薬品"]:
                        hp_diff -= shortage_amount * 15
                        morale_diff -= shortage_amount * 10
                    else:
                        hp_diff -= shortage_amount * 10
                        morale_diff -= shortage_amount * 5

            # 最終的なHPと士気の増減（基本変動も含める）
            data["hp"] = max(0, min(100, data["hp"] + hp_diff))
            data["morale"] = max(0, min(100, data["morale"] + morale_diff))

            # HPが0になったら全滅、そうでなければ次の日のログ・要求・動画をセット
            if data["hp"] <= 0:
                data["status"] = "全滅"
                data["log"] = (
                    "🚨 通信が途絶えました。部隊からの応答がありません……。"
                )
            elif next_day <= 5:
                story = st.session_state.planet_stories[planet_name][next_day]
                data["log"] = story["log"]
                data["demand"] = story["demand"]
                data["video_url"] = story["media"]
        # 日数を進める
        st.session_state.day = next_day

        # 毎日少しだけ司令部リソースを自然回復・補給
        st.session_state.global_resources["食料"] += 15
        st.session_state.global_resources["医薬品"] += 8
        st.session_state.global_resources["資源"] += 10

        st.rerun()
