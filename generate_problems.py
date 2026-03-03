#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数学バトル道場 - 問題自動生成スクリプト
既存217問に追加して合計2000問以上を生成
"""
import json
import random
import math
import itertools
from fractions import Fraction

random.seed(42)

# 既存問題を読み込み
with open('problems.json', 'r', encoding='utf-8') as f:
    existing = json.load(f)

existing_ids = {q['id'] for q in existing}
next_id = max(q['id'] for q in existing) + 1
new_questions = []

def add_q(cat, gr, q, a, h1, h2, exp):
    global next_id
    new_questions.append({
        "id": next_id,
        "cat": cat,
        "gr": gr,
        "q": q,
        "a": str(a),
        "h1": h1,
        "h2": h2,
        "exp": exp
    })
    next_id += 1

def fmt(n):
    """整数または分数を文字列に変換"""
    if isinstance(n, float):
        if n == int(n):
            return str(int(n))
        return str(n)
    return str(n)

# ===== 正負の数 (中1) - 95問追加 =====
def gen_seifuno_kazu(count=95):
    done = 0
    ops_list = ['+', '-', '*', '//']

    # 加減算
    pairs = []
    for a in range(-20, 21):
        for b in range(-20, 21):
            if a != 0 and b != 0:
                pairs.append((a, b))
    random.shuffle(pairs)

    for a, b in pairs:
        if done >= count: break
        ans = a + b
        q_str = f"({'+' if a>0 else ''}{a}) + ({'+' if b>0 else ''}{b}) を計算しなさい。"
        add_q("正負の数","中1", q_str, ans,
              f"正負の和: 符号に注意して絶対値を計算する",
              f"|{a}|={abs(a)}, |{b}|={abs(b)}",
              f"({'+' if a>0 else ''}{a}) + ({'+' if b>0 else ''}{b}) = {ans}")
        done += 1

    # 減算
    for a, b in pairs:
        if done >= count: break
        ans = a - b
        q_str = f"({'+' if a>0 else ''}{a}) - ({'+' if b>0 else ''}{b}) を計算しなさい。"
        add_q("正負の数","中1", q_str, ans,
              f"引き算は符号を変えてたし算に",
              f"({'+' if a>0 else ''}{a}) - ({'+' if b>0 else ''}{b}) = ({'+' if a>0 else ''}{a}) + ({'-' if b>0 else '+'}{abs(b)})",
              f"= {ans}")
        done += 1

    # 乗算
    for a in range(-10, 11):
        for b in range(-10, 11):
            if done >= count: break
            if a == 0 or b == 0: continue
            ans = a * b
            q_str = f"({'+' if a>0 else ''}{a}) × ({'+' if b>0 else ''}{b}) を計算しなさい。"
            sign = "正×正=正" if a>0 and b>0 else ("負×負=正" if a<0 and b<0 else "正×負=負 または 負×正=負")
            add_q("正負の数","中1", q_str, ans,
                  sign,
                  f"|{a}| × |{b}| = {abs(a)*abs(b)}",
                  f"({'+' if a>0 else ''}{a}) × ({'+' if b>0 else ''}{b}) = {ans}")
            done += 1

gen_seifuno_kazu(95)

# ===== 文字と式 (中1) - 95問追加 =====
def gen_moji_shiki(count=95):
    done = 0

    # ax + b の式を値で評価
    for a in range(-5, 6):
        for b in range(-10, 11):
            for x_val in range(-5, 6):
                if done >= count: break
                if a == 0: continue
                ans = a * x_val + b
                b_str = f"+ {b}" if b >= 0 else f"- {abs(b)}"
                expr = f"{a}x {b_str}" if b != 0 else f"{a}x"
                q_str = f"x = {x_val} のとき、{expr} の値を求めなさい。"
                add_q("文字と式","中1", q_str, ans,
                      f"xに{x_val}を代入する",
                      f"{a} × ({x_val}) {b_str} = ?",
                      f"{a} × ({x_val}) {b_str if b!=0 else ''} = {a*x_val}{('+'+str(b)) if b>0 else (str(b) if b<0 else '')} = {ans}")
            if done >= count: break
        if done >= count: break

    # 同類項の整理
    coeffs = [(2,3),(4,-1),(3,2),(-1,5),(6,-3),(2,-2),(5,1),(-3,4)]
    for a1, a2 in coeffs:
        if done >= count: break
        total = a1 + a2
        add_q("文字と式","中1",
              f"{a1}x + {a2}x を計算しなさい。",
              f"{total}x",
              "同類項はxの係数どうしをたす",
              f"({a1} + {a2})x = ?",
              f"({a1} + {a2})x = {total}x")
        done += 1

    # 分配法則
    for a in range(2, 8):
        for b in range(-5, 6):
            for c in range(-5, 6):
                if done >= count: break
                if b == 0 or c == 0: continue
                # a(bx + c) = abx + ac
                ab = a * b
                ac = a * c
                ac_str = f"+ {ac}" if ac >= 0 else str(ac)
                add_q("文字と式","中1",
                      f"{a}({b}x + {c}) を展開しなさい。",
                      f"{ab}x{('+'+str(ac)) if ac>0 else str(ac)}",
                      "分配法則: a(b+c)=ab+ac",
                      f"{a}×{b}x = {ab}x, {a}×{c} = {ac}",
                      f"{a}({b}x + {c}) = {ab}x {ac_str}")
            if done >= count: break
        if done >= count: break

gen_moji_shiki(95)

# ===== 一次方程式 (中1) - 119問追加 =====
def gen_ichiji_hoteishiki(count=119):
    done = 0

    # ax = b 型
    for a in range(1, 15):
        for b in range(-30, 31, 3):
            if done >= count: break
            if b == 0: continue
            if b % a != 0:
                # 分数解
                f = Fraction(b, a)
                ans = str(f)
            else:
                ans = str(b // a)
            add_q("一次方程式","中1",
                  f"{a}x = {b} を解きなさい。",
                  ans,
                  f"両辺を{a}で割る",
                  f"x = {b} ÷ {a}",
                  f"x = {ans}")
            done += 1
        if done >= count: break

    # ax + b = c 型
    for a in range(1, 8):
        for b in range(-10, 11):
            for c in range(-10, 11):
                if done >= count: break
                if b == 0 or a == 0: continue
                # ax = c - b
                rhs = c - b
                if rhs % a == 0:
                    ans = str(rhs // a)
                else:
                    ans = str(Fraction(rhs, a))
                b_str = f"+ {b}" if b > 0 else str(b)
                add_q("一次方程式","中1",
                      f"{a}x {b_str} = {c} を解きなさい。",
                      ans,
                      f"移項して ax = {c} {('-'+str(b)) if b>0 else ('+'+str(abs(b)))} の形にする",
                      f"{a}x = {c} - ({b}) = {rhs}",
                      f"x = {rhs} ÷ {a} = {ans}")
                done += 1
            if done >= count: break
        if done >= count: break

gen_ichiji_hoteishiki(119)

# ===== 比例・反比例 (中1) - 95問追加 =====
def gen_hirei(count=95):
    done = 0

    # y = ax の問題
    for a in range(-8, 9):
        if done >= count: break
        if a == 0: continue
        for x_val in range(-10, 11):
            if done >= count: break
            if x_val == 0: continue
            ans = a * x_val
            add_q("比例・反比例","中1",
                  f"y は x に比例し、x=1のとき y={a} です。x={x_val} のときの y を求めなさい。",
                  ans,
                  "比例の式: y = ax",
                  f"比例定数 a = {a}、y = {a}x に x={x_val} を代入",
                  f"y = {a} × {x_val} = {ans}")
            done += 1

    # y = a/x の問題
    for a in range(-20, 21):
        if done >= count: break
        if a == 0: continue
        for x_val in [1, 2, 4, 5, 10, -1, -2, -4, -5, -10]:
            if done >= count: break
            if a % x_val != 0: continue
            ans = a // x_val
            add_q("比例・反比例","中1",
                  f"y は x に反比例し、x=1のとき y={a} です。x={x_val} のときの y を求めなさい。",
                  ans,
                  "反比例の式: y = a/x",
                  f"比例定数 a = {a}、y = {a} ÷ {x_val}",
                  f"y = {a} ÷ {x_val} = {ans}")
            done += 1

    # 比の問題
    for a in range(1, 10):
        for b in range(1, 10):
            if done >= count: break
            for c in range(1, 20):
                if done >= count: break
                # a:b = c:x => x = bc/a
                if (b * c) % a == 0:
                    x = (b * c) // a
                    add_q("比例・反比例","中1",
                          f"{a} : {b} = {c} : x のとき x を求めなさい。",
                          x,
                          "比の性質: 外項の積 = 内項の積",
                          f"{a} × x = {b} × {c} = {b*c}",
                          f"x = {b*c} ÷ {a} = {x}")
                    done += 1

gen_hirei(95)

# ===== 平面図形 (中1) - 121問追加 =====
def gen_heimen_zukei(count=121):
    done = 0
    pi_approx = "3.14"

    # 長方形の面積・周長
    for w in range(2, 20):
        for h in range(2, 20):
            if done >= count: break
            area = w * h
            peri = 2 * (w + h)
            add_q("平面図形","中1",
                  f"縦 {h} cm、横 {w} cm の長方形の面積を求めなさい。",
                  f"{area}cm²",
                  "長方形の面積 = 縦 × 横",
                  f"{h} × {w} = ?",
                  f"{h} × {w} = {area} (cm²)")
            done += 1
            if done < count:
                add_q("平面図形","中1",
                      f"縦 {h} cm、横 {w} cm の長方形の周の長さを求めなさい。",
                      f"{peri}cm",
                      "長方形の周 = (縦 + 横) × 2",
                      f"({h} + {w}) × 2 = ?",
                      f"({h} + {w}) × 2 = {h+w} × 2 = {peri} (cm)")
                done += 1
        if done >= count: break

    # 三角形の面積
    for b in range(2, 15):
        for h in range(2, 15):
            if done >= count: break
            if (b * h) % 2 == 0:
                area = b * h // 2
                add_q("平面図形","中1",
                      f"底辺 {b} cm、高さ {h} cm の三角形の面積を求めなさい。",
                      f"{area}cm²",
                      "三角形の面積 = 底辺 × 高さ ÷ 2",
                      f"{b} × {h} ÷ 2 = ?",
                      f"{b} × {h} ÷ 2 = {b*h} ÷ 2 = {area} (cm²)")
                done += 1

    # 円の面積・円周（π=3.14使用）
    for r in range(1, 16):
        if done >= count: break
        area = round(r * r * 3.14, 2)
        circ = round(2 * r * 3.14, 2)
        area_str = str(int(area)) if area == int(area) else str(area)
        circ_str = str(int(circ)) if circ == int(circ) else str(circ)
        add_q("平面図形","中1",
              f"半径 {r} cm の円の面積を求めなさい。（π=3.14）",
              f"{area_str}cm²",
              "円の面積 = π × r²",
              f"3.14 × {r}² = 3.14 × {r*r} = ?",
              f"3.14 × {r*r} = {area_str} (cm²)")
        done += 1

gen_heimen_zukei(121)

# ===== 空間図形 (中1) - 122問追加 =====
def gen_kuukan_zukei(count=122):
    done = 0

    # 直方体の体積・表面積
    for a in range(2, 10):
        for b in range(2, 10):
            for c in range(2, 10):
                if done >= count: break
                vol = a * b * c
                surf = 2 * (a*b + b*c + c*a)
                add_q("空間図形","中1",
                      f"縦 {a} cm、横 {b} cm、高さ {c} cm の直方体の体積を求めなさい。",
                      f"{vol}cm³",
                      "直方体の体積 = 縦 × 横 × 高さ",
                      f"{a} × {b} × {c} = ?",
                      f"{a} × {b} × {c} = {vol} (cm³)")
                done += 1
                if done < count:
                    add_q("空間図形","中1",
                          f"縦 {a} cm、横 {b} cm、高さ {c} cm の直方体の表面積を求めなさい。",
                          f"{surf}cm²",
                          "直方体の表面積 = 2(縦×横 + 横×高さ + 高さ×縦)",
                          f"2({a}×{b} + {b}×{c} + {c}×{a}) = 2({a*b} + {b*c} + {c*a}) = ?",
                          f"2 × {a*b + b*c + c*a} = {surf} (cm²)")
                    done += 1
            if done >= count: break
        if done >= count: break

    # 円柱の体積（π=3.14）
    for r in range(1, 8):
        for h in range(1, 8):
            if done >= count: break
            vol = round(r * r * 3.14 * h, 2)
            vol_str = str(int(vol)) if vol == int(vol) else str(vol)
            add_q("空間図形","中1",
                  f"底面の半径 {r} cm、高さ {h} cm の円柱の体積を求めなさい。（π=3.14）",
                  f"{vol_str}cm³",
                  "円柱の体積 = π × r² × h",
                  f"3.14 × {r}² × {h} = 3.14 × {r*r} × {h} = ?",
                  f"3.14 × {r*r*h} = {vol_str} (cm³)")
            done += 1

gen_kuukan_zukei(122)

# ===== 資料の活用 (中1) - 122問追加 =====
def gen_shiryo(count=122):
    done = 0

    # 平均
    datasets = [
        [3,5,7,9,11],
        [2,4,6,8,10],
        [10,20,30,40,50],
        [1,3,5,7,9,11,13],
        [15,18,22,25,30],
        [100,200,300,400,500],
        [4,8,12,16,20],
        [6,9,12,15,18,21],
    ]

    for data in datasets:
        if done >= count: break
        mean = sum(data) / len(data)
        mean_str = str(int(mean)) if mean == int(mean) else str(mean)
        data_str = ", ".join(map(str, data))
        add_q("資料の活用","中1",
              f"次のデータの平均値を求めなさい。\n{data_str}",
              mean_str,
              "平均 = 合計 ÷ 個数",
              f"合計 = {sum(data)}, 個数 = {len(data)}",
              f"{sum(data)} ÷ {len(data)} = {mean_str}")
        done += 1

    # 中央値
    for n in range(5, 15):
        if done >= count: break
        data = sorted(random.sample(range(1, 50), n))
        if n % 2 == 1:
            median = data[n // 2]
        else:
            m1, m2 = data[n//2 - 1], data[n//2]
            median = (m1 + m2) / 2
        median_str = str(int(median)) if median == int(median) else str(median)
        data_str = ", ".join(map(str, data))
        add_q("資料の活用","中1",
              f"次のデータの中央値を求めなさい。\n{data_str}",
              median_str,
              f"データを並べて{n}番目の真ん中" + ("の値" if n%2==1 else "2つの平均"),
              f"並べると: {data_str}",
              f"中央値 = {median_str}")
        done += 1

    # 最頻値（モード）
    for _ in range(40):
        if done >= count: break
        base = random.randint(1, 20)
        data = [base] * 3 + [base+1, base+2, base-1, base+3, base-2]
        random.shuffle(data)
        mode = base
        data_str = ", ".join(map(str, data))
        add_q("資料の活用","中1",
              f"次のデータの最頻値を求めなさい。\n{data_str}",
              str(mode),
              "最頻値 = 最も多く出てくる値",
              f"{base} が {data.count(base)} 回出現している",
              f"最頻値 = {mode}")
        done += 1

    # 範囲
    for _ in range(40):
        if done >= count: break
        data = sorted(random.sample(range(1, 100), random.randint(5, 10)))
        rang = max(data) - min(data)
        data_str = ", ".join(map(str, data))
        add_q("資料の活用","中1",
              f"次のデータの範囲を求めなさい。\n{data_str}",
              str(rang),
              "範囲 = 最大値 - 最小値",
              f"最大値 = {max(data)}, 最小値 = {min(data)}",
              f"{max(data)} - {min(data)} = {rang}")
        done += 1

gen_shiryo(122)

# ===== 式の計算 (中2) - 121問追加 =====
def gen_shiki_keisan(count=121):
    done = 0

    # 多項式の加減
    for a1, b1, a2, b2 in [(2,3,4,-1),(3,-2,1,5),(5,2,-3,4),(-1,3,2,-2),(4,-3,2,1),
                            (3,1,-2,-3),(6,2,1,-4),(2,-5,3,2),(-3,4,5,-1),(1,2,-1,-2)]:
        if done >= count: break
        # (a1x+b1) + (a2x+b2)
        sa = a1 + a2
        sb = b1 + b2
        ans = f"{sa}x{'+'+str(sb) if sb>0 else str(sb)}" if sb != 0 else f"{sa}x"
        add_q("式の計算","中2",
              f"({a1}x + {b1}) + ({a2}x + {b2}) を計算しなさい。",
              ans,
              "同類項（xの項どうし、定数項どうし）をまとめる",
              f"xの係数: {a1} + {a2} = {sa}, 定数: {b1} + {b2} = {sb}",
              f"= {ans}")
        done += 1

    # 単項式の乗除
    for a in range(-5, 6):
        for b in range(2, 8):
            if done >= count: break
            if a == 0: continue
            product = a * b
            add_q("式の計算","中2",
                  f"{a}x × {b} を計算しなさい。",
                  f"{product}x",
                  "単項式の乗算: 係数×係数",
                  f"{a} × {b} = {product}",
                  f"{a}x × {b} = {product}x")
            done += 1

    # 展開 (x+a)(x+b) = x² + (a+b)x + ab
    for a in range(-6, 7):
        for b in range(-6, 7):
            if done >= count: break
            if a == 0 or b == 0: continue
            s = a + b
            p = a * b
            s_str = f"+ {s}" if s > 0 else (str(s) if s < 0 else "")
            p_str = f"+ {p}" if p > 0 else (str(p) if p != 0 else "")
            ans_str = f"x²{s_str}x{p_str}".replace("+ -","- ")
            if s == 0:
                ans_str = f"x²{p_str}"
            add_q("式の計算","中2",
                  f"(x + {a})(x + {b}) を展開しなさい。",
                  ans_str,
                  f"(x+a)(x+b) = x² + (a+b)x + ab の公式を使う",
                  f"a+b = {a}+{b} = {s}, a×b = {a}×{b} = {p}",
                  f"= x² + {s}x + {p} = {ans_str}")
            done += 1
        if done >= count: break

gen_shiki_keisan(121)

# ===== 連立方程式 (中2) - 121問追加 =====
def gen_renritsu(count=121):
    done = 0

    # ax + by = c, dx + ey = f 型
    # x, y を先に決めてから係数を生成
    solutions = []
    for x in range(-5, 6):
        for y in range(-5, 6):
            if x == 0 and y == 0: continue
            solutions.append((x, y))
    random.shuffle(solutions)

    coeff_sets = [
        (1, 1, 1, -1),
        (2, 1, 1, 2),
        (3, 1, 1, 3),
        (2, 3, 3, 2),
        (1, 2, 2, 1),
        (3, 2, 2, 3),
        (4, 1, 1, 4),
        (2, -1, 1, 2),
        (1, -1, 1, 1),
        (3, -2, 2, 3),
    ]

    for (x, y), (a, b, d, e) in zip(solutions[:count], coeff_sets * 15):
        if done >= count: break
        c = a*x + b*y
        f = d*x + e*y
        add_q("連立方程式","中2",
              f"連立方程式を解きなさい。\n{a}x + {b}y = {c}\n{d}x + {e}y = {f}",
              f"x={x}, y={y}",
              "加減法または代入法を使う",
              f"①×{e} - ②×{b} でyを消去: ({a*e-d*b})x = {c*e-f*b}",
              f"x = {x}, y = {y}")
        done += 1

gen_renritsu(121)

# ===== 不等式 (中2) - 123問追加 =====
def gen_futoushiki(count=123):
    done = 0

    # ax + b > c 型（a > 0）
    for a in range(1, 8):
        for b in range(-10, 11):
            for c in range(-10, 11):
                if done >= count: break
                if b == 0: continue
                # ax > c - b
                rhs = c - b
                if rhs % a == 0:
                    threshold = rhs // a
                    ans = f"x > {threshold}"
                else:
                    f_val = Fraction(rhs, a)
                    ans = f"x > {f_val}"
                b_str = f"+ {b}" if b > 0 else str(b)
                add_q("不等式","中2",
                      f"{a}x {b_str} > {c} を解きなさい。",
                      ans,
                      "不等式の変形: 正の数で割るとき不等号の向きは変わらない",
                      f"{a}x > {c} - ({b}) = {rhs}",
                      f"x > {rhs} ÷ {a} = {ans[4:]}")
                done += 1
            if done >= count: break
        if done >= count: break

    # -ax + b < c 型（a > 0、割ると不等号反転）
    for a in range(1, 6):
        for b in range(-8, 9):
            for c in range(-8, 9):
                if done >= count: break
                if b == 0: continue
                # -ax < c - b => x > (b-c)/a
                rhs = b - c
                if rhs % a == 0:
                    threshold = rhs // a
                    ans = f"x > {threshold}"
                else:
                    f_val = Fraction(rhs, a)
                    ans = f"x > {f_val}"
                b_str = f"+ {b}" if b > 0 else str(b)
                add_q("不等式","中2",
                      f"-{a}x {b_str} < {c} を解きなさい。",
                      ans,
                      "負の数で割るとき不等号の向きが逆になる",
                      f"-{a}x < {c} - ({b}) = {c-b}, 両辺を -{a} で割ると向き反転",
                      f"x > {c-b} ÷ (-{a}) = {ans[4:]}")
                done += 1
            if done >= count: break
        if done >= count: break

gen_futoushiki(123)

# ===== 一次関数 (中2) - 120問追加 =====
def gen_ichiji_kansuu(count=120):
    done = 0

    # y = ax + b への代入
    for a in range(-5, 6):
        for b in range(-8, 9):
            for x_val in range(-5, 6):
                if done >= count: break
                if a == 0: continue
                y_val = a * x_val + b
                b_str = f"+ {b}" if b > 0 else (str(b) if b < 0 else "")
                expr = f"y = {a}x {b_str}".strip()
                add_q("一次関数","中2",
                      f"{expr} で x = {x_val} のときの y を求めなさい。",
                      str(y_val),
                      f"xに{x_val}を代入する",
                      f"y = {a} × ({x_val}) {b_str} = ?",
                      f"y = {a*x_val} {b_str} = {y_val}")
                done += 1
            if done >= count: break
        if done >= count: break

    # 傾きと切片を求める問題
    for a in range(-4, 5):
        for b in range(-6, 7):
            if done >= count: break
            if a == 0: continue
            b_str = f"+ {b}" if b > 0 else (str(b) if b < 0 else "")
            expr = f"y = {a}x {b_str}".strip()
            add_q("一次関数","中2",
                  f"{expr} の傾きと切片を答えなさい。（「傾き=N, 切片=M」形式）",
                  f"傾き={a}, 切片={b}",
                  "y = ax + b の a が傾き、b が切片",
                  f"y = ({a})x + ({b})",
                  f"傾き = {a}, 切片 = {b}")
            done += 1

    # 2点を通る直線の式
    pts = [(0,1,1,3),(0,2,2,6),(1,3,3,7),(0,-1,2,3),(1,0,3,4),
           (0,5,1,3),(2,1,4,5),(1,-2,3,2),(-1,0,1,4),(0,3,3,9)]
    for x1,y1,x2,y2 in pts:
        if done >= count: break
        if x2 == x1: continue
        a = Fraction(y2-y1, x2-x1)
        b = y1 - a * x1
        if a.denominator == 1 and b.denominator == 1:
            a_int, b_int = int(a), int(b)
            b_str = f"+ {b_int}" if b_int > 0 else (str(b_int) if b_int < 0 else "")
            ans = f"y = {a_int}x {b_str}".strip()
            add_q("一次関数","中2",
                  f"2点 ({x1}, {y1}) と ({x2}, {y2}) を通る一次関数の式を求めなさい。",
                  ans,
                  "傾き = (y₂ - y₁) ÷ (x₂ - x₁)",
                  f"傾き = ({y2} - {y1}) ÷ ({x2} - {x1}) = {a_int}",
                  f"y = {a_int}x {b_str}".strip())
            done += 1

gen_ichiji_kansuu(120)

# ===== 平行と合同 (中2) - 121問追加 =====
def gen_heikou_gougo(count=121):
    done = 0

    # 三角形の内角の和（xを求める）
    for a in range(30, 120, 5):
        for b in range(30, 120, 5):
            if done >= count: break
            if a + b >= 180: continue
            x = 180 - a - b
            if x <= 0: continue
            add_q("平行と合同","中2",
                  f"三角形の2つの角が {a}° と {b}° のとき、残りの角 x を求めなさい。",
                  f"{x}°",
                  "三角形の内角の和は180°",
                  f"x = 180 - {a} - {b}",
                  f"x = 180 - {a+b} = {x}°")
            done += 1

    # 平行線と角度（対頂角、同位角、錯角）
    for angle in range(30, 170, 5):
        if done >= count: break
        add_q("平行と合同","中2",
              f"2直線が交わるとき、一方の角が {angle}° ならば対頂角は何度ですか。",
              f"{angle}°",
              "対頂角は等しい",
              f"対頂角 = {angle}°",
              f"対頂角は等しいので {angle}°")
        done += 1

    # 多角形の内角の和
    for n in range(3, 13):
        if done >= count: break
        total = (n - 2) * 180
        add_q("平行と合同","中2",
              f"{n}角形の内角の和を求めなさい。",
              f"{total}°",
              f"多角形の内角の和 = (辺の数 - 2) × 180°",
              f"({n} - 2) × 180 = {n-2} × 180",
              f"{n-2} × 180 = {total}°")
        done += 1

    # 合同条件
    conds = [
        ("3組の辺がそれぞれ等しい", "SSS合同"),
        ("2組の辺とその間の角がそれぞれ等しい", "SAS合同"),
        ("1組の辺とその両端の角がそれぞれ等しい", "ASA合同"),
    ]
    for cond, name in conds:
        if done >= count: break
        add_q("平行と合同","中2",
              f"三角形の合同条件「{cond}」の略称（アルファベット3文字）を答えなさい。",
              name[:3],
              "三角形の合同条件は3種類ある",
              f"{cond}",
              f"略称は{name}")
        done += 1

    # 外角の定理
    for a in range(30, 100, 5):
        for b in range(30, 100, 5):
            if done >= count: break
            if a + b >= 180: continue
            ext = a + b
            add_q("平行と合同","中2",
                  f"三角形の2つの内角が {a}° と {b}° のとき、これらと隣り合わない外角を求めなさい。",
                  f"{ext}°",
                  "三角形の外角 = 隣り合わない2つの内角の和",
                  f"外角 = {a}° + {b}°",
                  f"= {ext}°")
            done += 1

gen_heikou_gougo(121)

# ===== 確率 (中2) - 95問追加 =====
def gen_kakuritsu(count=95):
    done = 0

    # さいころ1個
    faces = [1, 2, 3, 4, 5, 6]
    problems = [
        (lambda f: f == 3, "3が出る", Fraction(1,6)),
        (lambda f: f % 2 == 0, "偶数が出る", Fraction(1,2)),
        (lambda f: f % 2 == 1, "奇数が出る", Fraction(1,2)),
        (lambda f: f >= 4, "4以上が出る", Fraction(1,2)),
        (lambda f: f <= 2, "2以下が出る", Fraction(1,3)),
        (lambda f: f % 3 == 0, "3の倍数が出る", Fraction(1,3)),
        (lambda f: f == 1 or f == 6, "1または6が出る", Fraction(1,3)),
        (lambda f: f < 5, "5未満が出る", Fraction(2,3)),
    ]

    for pred, desc, prob in problems:
        if done >= count: break
        prob_str = str(prob) if prob.denominator != 1 else str(int(prob))
        add_q("確率","中2",
              f"1個のさいころを投げるとき、{desc}確率を求めなさい。",
              prob_str,
              f"全体の場合の数は6通り",
              f"条件を満たす場合: {[f for f in faces if pred(f)]}",
              f"P = {len([f for f in faces if pred(f)])} ÷ 6 = {prob_str}")
        done += 1

    # コインの問題
    coin_probs = [
        ("表が出る", Fraction(1,2)),
        ("裏が出る", Fraction(1,2)),
        ("2回投げて2回とも表", Fraction(1,4)),
        ("2回投げて少なくとも1回表", Fraction(3,4)),
    ]
    for desc, prob in coin_probs:
        if done >= count: break
        prob_str = str(prob)
        add_q("確率","中2",
              f"コインを投げるとき、{desc}確率を求めなさい。",
              prob_str,
              "コインの表・裏は等確率",
              "全体の場合数を数える",
              f"P = {prob_str}")
        done += 1

    # カード問題
    for n in range(2, 10):
        for k in range(1, n):
            if done >= count: break
            prob = Fraction(k, n)
            prob_str = str(prob) if prob.denominator != 1 else str(int(prob))
            add_q("確率","中2",
                  f"1から{n}までの数字が書かれたカードから1枚引くとき、{k}以下の数が出る確率を求めなさい。",
                  prob_str,
                  f"全体{n}通りのうち条件を満たすのは{k}通り",
                  f"P = {k} ÷ {n}",
                  f"P = {prob_str}")
            done += 1

    # 2個のさいころ
    all_pairs = [(i,j) for i in range(1,7) for j in range(1,7)]
    dice_problems = [
        (lambda p: p[0]+p[1]==7, "和が7になる", "6通り"),
        (lambda p: p[0]==p[1], "同じ目が出る", "6通り"),
        (lambda p: p[0]+p[1]==10, "和が10以上", "6通り"),
        (lambda p: p[0]*p[1]<=6, "積が6以下", "計算"),
    ]
    for pred, desc, hint in dice_problems:
        if done >= count: break
        favorable = [p for p in all_pairs if pred(p)]
        prob = Fraction(len(favorable), 36)
        prob_str = str(prob) if prob.denominator != 1 else str(int(prob))
        add_q("確率","中2",
              f"2個のさいころを同時に投げるとき、{desc}確率を求めなさい。",
              prob_str,
              "全体の場合の数は6×6=36通り",
              f"条件を満たすのは{len(favorable)}通り",
              f"P = {len(favorable)}/36 = {prob_str}")
        done += 1

gen_kakuritsu(95)

# ===== 場合の数 (中2) - 123問追加 =====
def gen_baaino_kazu(count=123):
    done = 0

    # 順列 P(n,r) = n!/(n-r)!
    from math import factorial, perm, comb

    for n in range(3, 9):
        for r in range(2, n+1):
            if done >= count: break
            p = perm(n, r)
            add_q("場合の数","中2",
                  f"{n}人の中から{r}人を選んで1列に並べる方法は何通りですか。",
                  f"{p}通り",
                  f"順列 P({n},{r}) = {n}×{n-1}×...×{n-r+1}",
                  f"{' × '.join(str(n-i) for i in range(r))} = ?",
                  f"= {p}通り")
            done += 1

    # 組合せ C(n,r) = n!/(r!(n-r)!)
    for n in range(3, 9):
        for r in range(2, n//2 + 2):
            if done >= count: break
            c = comb(n, r)
            add_q("場合の数","中2",
                  f"{n}人の中から{r}人を選ぶ組合せは何通りですか。",
                  f"{c}通り",
                  f"組合せ C({n},{r}) = P({n},{r}) ÷ {r}!",
                  f"C({n},{r}) = {perm(n,r)} ÷ {factorial(r)} = ?",
                  f"= {c}通り")
            done += 1

    # 積の法則・和の法則
    for a in range(2, 7):
        for b in range(2, 7):
            if done >= count: break
            product = a * b
            add_q("場合の数","中2",
                  f"コインを投げる（表・裏の{a}種類）操作とサイコロを投げる（{b}種類）操作を続けて行うとき、全体の場合の数を求めなさい。",
                  f"{product}通り",
                  "積の法則: 2つの操作の場合の数を掛け合わせる",
                  f"{a} × {b} = ?",
                  f"{a} × {b} = {product}通り")
            done += 1

    # 道順の数え方（格子点）
    for right in range(2, 6):
        for up in range(2, 5):
            if done >= count: break
            from math import comb
            ways = comb(right + up, right)
            add_q("場合の数","中2",
                  f"格子状の道で、右に{right}マス・上に{up}マス移動するとき、最短経路の数を求めなさい。",
                  f"{ways}通り",
                  f"右({right}回)と上({up}回)の合計{right+up}回の操作から右を選ぶ組合せ",
                  f"C({right+up},{right}) = {ways}",
                  f"{ways}通り")
            done += 1

gen_baaino_kazu(123)

# ===== 方程式 (既存カテゴリ) - 95問追加 =====
def gen_hoteishiki_extra(count=95):
    done = 0

    # 分数方程式
    for num, denom in [(1,2),(1,3),(2,3),(1,4),(3,4),(1,5),(2,5)]:
        for c in range(1, 15):
            if done >= count: break
            # (num/denom)x = c => x = c*denom/num
            from fractions import Fraction
            ans_f = Fraction(c * denom, num)
            ans = str(ans_f) if ans_f.denominator != 1 else str(int(ans_f))
            add_q("方程式","中1",
                  f"({num}/{denom})x = {c} を解きなさい。",
                  ans,
                  f"両辺に{denom}をかけて分母を払う",
                  f"{num}x = {c} × {denom} = {c*denom}, x = {c*denom} ÷ {num}",
                  f"x = {ans}")
            done += 1
        if done >= count: break

    # 文章題（速さ・距離・時間）
    speed_problems = [
        (60, 120, "時速60kmで走る車が120km進むのにかかる時間（時間）"),
        (80, 240, "時速80kmで走る車が240km進むのにかかる時間（時間）"),
        (50, 200, "時速50kmで走る車が200km進むのにかかる時間（時間）"),
        (4, 12, "分速4mで歩くとき12mを歩くのにかかる時間（分）"),
        (3, 15, "毎分3mで進むとき15mを進むのにかかる時間（分）"),
    ]
    for speed, dist, desc in speed_problems:
        if done >= count: break
        time = dist // speed
        add_q("方程式","中1",
              f"{desc}を求めなさい。\nxを時間として方程式を立てて解きなさい。",
              f"{time}",
              "時間 = 距離 ÷ 速さ",
              f"{speed}x = {dist} と立式",
              f"x = {dist} ÷ {speed} = {time}")
        done += 1

    # 文章題（個数・代金）
    for price1 in range(50, 200, 30):
        for price2 in range(80, 300, 40):
            for n1 in range(2, 8):
                if done >= count: break
                total = price1 * n1 + price2 * (10 - n1)
                add_q("方程式","中1",
                      f"{price1}円のりんごと{price2}円のみかんを合わせて10個買ったら合計{total}円でした。りんごは何個買いましたか。",
                      f"{n1}個",
                      f"りんごをx個とすると、みかんは(10-x)個",
                      f"{price1}x + {price2}(10-x) = {total} を解く",
                      f"{price1}x + {price2*10} - {price2}x = {total}, {price1-price2}x = {total-price2*10}, x = {n1}")
                done += 1
            if done >= count: break
        if done >= count: break

gen_hoteishiki_extra(95)

# ===== 図形 (既存カテゴリ) - 95問追加 =====
def gen_zukei_extra(count=95):
    done = 0

    # ピタゴラスの定理
    pythagorean = [
        (3,4,5), (5,12,13), (8,15,17), (7,24,25),
        (6,8,10), (9,12,15), (5,12,13), (10,24,26),
        (3,4,5), (12,16,20), (15,20,25), (8,15,17),
    ]
    for a, b, c in pythagorean:
        if done >= count: break
        add_q("図形","中2",
              f"直角三角形で2辺の長さが {a} cm と {b} cm のとき、斜辺の長さを求めなさい。",
              f"{c}cm",
              "ピタゴラスの定理: a² + b² = c²",
              f"{a}² + {b}² = {a**2} + {b**2} = {c**2}",
              f"√{c**2} = {c} cm")
        done += 1

    # 相似比と面積比
    for ratio in range(2, 6):
        if done >= count: break
        area_ratio = ratio * ratio
        add_q("図形","中2",
              f"相似な2つの図形の相似比が 1:{ratio} のとき、面積比を求めなさい。",
              f"1:{area_ratio}",
              "面積比 = 相似比の2乗",
              f"1² : {ratio}² = 1 : {area_ratio}",
              f"面積比 = 1 : {area_ratio}")
        done += 1

    # 三平方の定理の応用（正方形の対角線）
    for side in range(1, 12):
        if done >= count: break
        diag_sq = 2 * side * side
        # 整数になる場合のみ
        diag = math.sqrt(diag_sq)
        if diag == int(diag):
            add_q("図形","中2",
                  f"1辺が {side} cm の正方形の対角線の長さを求めなさい。",
                  f"{int(diag)}cm",
                  "対角線 = 1辺 × √2 (ピタゴラスの定理)",
                  f"{side}² + {side}² = {diag_sq} = {int(diag)}²",
                  f"対角線 = {int(diag)} cm")
            done += 1

    # 円の弧・弦・扇形（面積、弧の長さ）
    for r in range(3, 12):
        for angle in [30, 45, 60, 90, 120, 150]:
            if done >= count: break
            arc = round(2 * r * 3.14 * angle / 360, 2)
            sector_area = round(r * r * 3.14 * angle / 360, 2)
            arc_str = str(int(arc)) if arc == int(arc) else str(arc)
            sector_str = str(int(sector_area)) if sector_area == int(sector_area) else str(sector_area)
            add_q("図形","中2",
                  f"半径 {r} cm、中心角 {angle}° の扇形の弧の長さを求めなさい。（π=3.14）",
                  f"{arc_str}cm",
                  f"弧の長さ = 2πr × (中心角/360°)",
                  f"2 × 3.14 × {r} × ({angle}/360) = ?",
                  f"= {arc_str} cm")
            done += 1
            if done < count:
                add_q("図形","中2",
                      f"半径 {r} cm、中心角 {angle}° の扇形の面積を求めなさい。（π=3.14）",
                      f"{sector_str}cm²",
                      f"扇形の面積 = πr² × (中心角/360°)",
                      f"3.14 × {r}² × ({angle}/360) = 3.14 × {r*r} × {angle/360}",
                      f"= {sector_str} cm²")
                done += 1
        if done >= count: break

gen_zukei_extra(95)

# ===== 全問題をまとめて保存 =====
all_questions = existing + new_questions
print(f"既存問題: {len(existing)}問")
print(f"新規問題: {len(new_questions)}問")
print(f"合計: {len(all_questions)}問")

# 単元別集計
cats = {}
for q in all_questions:
    cats[q['cat']] = cats.get(q['cat'], 0) + 1
print("\n=== 単元別問題数 ===")
for cat, cnt in sorted(cats.items(), key=lambda x: -x[1]):
    print(f"  {cat}: {cnt}問")

with open('problems.json', 'w', encoding='utf-8') as f:
    json.dump(all_questions, f, ensure_ascii=False, indent=2)

print("\n✅ problems.json 書き出し完了")
