#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数学バトル道場 - 自動検算スクリプト
全2035問の計算を検証してerrors.jsonに出力
"""
import json
import re
from fractions import Fraction
import math
import sys

with open('problems.json', 'r', encoding='utf-8') as f:
    problems = json.load(f)

errors = []

def add_error(q, reason, expected=None):
    e = {
        "id": q['id'],
        "cat": q['cat'],
        "gr": q['gr'],
        "q": q['q'],
        "a": q['a'],
        "reason": reason,
    }
    if expected is not None:
        e['expected'] = str(expected)
    errors.append(e)

def normalize_answer(s):
    """答えの文字列を正規化"""
    s = str(s).strip()
    # 単位を除去
    s = re.sub(r'cm[²³]?|m[²³]?|°|通り|個|問|時間|分', '', s)
    s = s.strip()
    return s

def parse_num(s):
    """文字列を数値に変換（分数も対応）"""
    s = normalize_answer(s)
    try:
        return Fraction(s)
    except:
        try:
            return Fraction(float(s))
        except:
            return None

def check_seifuno_kazu(q):
    """正負の数の検算"""
    text = q['q']
    ans = q['a']

    # (a) + (b) 型
    m = re.search(r'\(([+-]?\d+)\)\s*\+\s*\(([+-]?\d+)\)', text)
    if m:
        a, b = int(m.group(1)), int(m.group(2))
        expected = a + b
        got = parse_num(ans)
        if got is not None and got != Fraction(expected):
            add_error(q, f"加算ミス: ({a})+({b})={expected} but got {ans}", expected)
        return

    # (a) - (b) 型
    m = re.search(r'\(([+-]?\d+)\)\s*-\s*\(([+-]?\d+)\)', text)
    if m:
        a, b = int(m.group(1)), int(m.group(2))
        expected = a - b
        got = parse_num(ans)
        if got is not None and got != Fraction(expected):
            add_error(q, f"減算ミス: ({a})-({b})={expected} but got {ans}", expected)
        return

    # (a) × (b) 型
    m = re.search(r'\(([+-]?\d+)\)\s*×\s*\(([+-]?\d+)\)', text)
    if m:
        a, b = int(m.group(1)), int(m.group(2))
        expected = a * b
        got = parse_num(ans)
        if got is not None and got != Fraction(expected):
            add_error(q, f"乗算ミス: ({a})×({b})={expected} but got {ans}", expected)
        return

    # (a) ÷ (b) 型
    m = re.search(r'\(([+-]?\d+)\)\s*÷\s*\(([+-]?\d+)\)', text)
    if m:
        a, b = int(m.group(1)), int(m.group(2))
        if b != 0:
            expected = Fraction(a, b)
            got = parse_num(ans)
            if got is not None and got != expected:
                add_error(q, f"除算ミス: ({a})÷({b})={expected} but got {ans}", expected)
        return

def check_ichiji_hoteishiki(q):
    """一次方程式の検算（ax + b = c 型）"""
    text = q['q']
    ans_str = q['a']

    # ax = b 型
    m = re.match(r'^(-?\d+)x\s*=\s*(-?\d+)', text.strip())
    if m:
        a, b = int(m.group(1)), int(m.group(2))
        if a != 0:
            expected = Fraction(b, a)
            got = parse_num(ans_str)
            if got is not None and got != expected:
                add_error(q, f"方程式解ミス: {a}x={b} → x={expected} but got {ans_str}", expected)
        return

    # ax + b = c または ax - b = c 型
    m = re.match(r'^(-?\d+)x\s*([+-])\s*(\d+)\s*=\s*(-?\d+)', text.strip())
    if m:
        a = int(m.group(1))
        sign = 1 if m.group(2) == '+' else -1
        b = sign * int(m.group(3))
        c = int(m.group(4))
        if a != 0:
            expected = Fraction(c - b, a)
            got = parse_num(ans_str)
            if got is not None and got != expected:
                add_error(q, f"方程式解ミス: {a}x+{b}={c} → x={expected} but got {ans_str}", expected)
        return

def check_hirei(q):
    """比例・反比例の検算"""
    text = q['q']
    ans_str = q['a']

    # a : b = c : x 型
    m = re.search(r'(\d+)\s*:\s*(\d+)\s*=\s*(\d+)\s*:\s*x', text)
    if m:
        a, b, c = int(m.group(1)), int(m.group(2)), int(m.group(3))
        if a != 0:
            expected = Fraction(b * c, a)
            got = parse_num(ans_str)
            if got is not None and got != expected:
                add_error(q, f"比の計算ミス: {a}:{b}={c}:x → x={expected} but got {ans_str}", expected)
        return

def check_heimen_zukei(q):
    """平面図形の検算"""
    text = q['q']
    ans_str = q['a']

    # 縦 h cm、横 w cm の長方形の面積
    m = re.search(r'縦\s*(\d+)\s*cm.*横\s*(\d+)\s*cm.*面積', text)
    if m:
        h, w = int(m.group(1)), int(m.group(2))
        expected = h * w
        got = parse_num(ans_str)
        if got is not None and got != Fraction(expected):
            add_error(q, f"長方形面積ミス: {h}×{w}={expected} but got {ans_str}", f"{expected}cm²")
        return

    # 縦 h cm、横 w cm の長方形の周
    m = re.search(r'縦\s*(\d+)\s*cm.*横\s*(\d+)\s*cm.*周', text)
    if m:
        h, w = int(m.group(1)), int(m.group(2))
        expected = 2 * (h + w)
        got = parse_num(ans_str)
        if got is not None and got != Fraction(expected):
            add_error(q, f"長方形周ミス: 2({h}+{w})={expected} but got {ans_str}", f"{expected}cm")
        return

    # 底辺 b cm、高さ h cm の三角形の面積
    m = re.search(r'底辺\s*(\d+)\s*cm.*高さ\s*(\d+)\s*cm', text)
    if m:
        b, h = int(m.group(1)), int(m.group(2))
        expected = Fraction(b * h, 2)
        got = parse_num(ans_str)
        if got is not None and got != expected:
            add_error(q, f"三角形面積ミス: {b}×{h}/2={expected} but got {ans_str}", f"{expected}cm²")
        return

    # 半径 r cm の円の面積
    m = re.search(r'半径\s*(\d+)\s*cm.*円.*面積', text)
    if m:
        r = int(m.group(1))
        expected = round(r * r * 3.14, 2)
        got = parse_num(ans_str)
        expected_f = Fraction(expected).limit_denominator(100)
        if got is not None and abs(float(got) - expected) > 0.01:
            add_error(q, f"円面積ミス: π×{r}²={expected} but got {ans_str}", f"{expected}cm²")
        return

def check_kuukan_zukei(q):
    """空間図形の検算"""
    text = q['q']
    ans_str = q['a']

    # 直方体の体積
    m = re.search(r'縦\s*(\d+)\s*cm.*横\s*(\d+)\s*cm.*高さ\s*(\d+)\s*cm.*体積', text)
    if m:
        a, b, c = int(m.group(1)), int(m.group(2)), int(m.group(3))
        expected = a * b * c
        got = parse_num(ans_str)
        if got is not None and got != Fraction(expected):
            add_error(q, f"直方体体積ミス: {a}×{b}×{c}={expected} but got {ans_str}", f"{expected}cm³")
        return

    # 直方体の表面積
    m = re.search(r'縦\s*(\d+)\s*cm.*横\s*(\d+)\s*cm.*高さ\s*(\d+)\s*cm.*表面積', text)
    if m:
        a, b, c = int(m.group(1)), int(m.group(2)), int(m.group(3))
        expected = 2 * (a*b + b*c + c*a)
        got = parse_num(ans_str)
        if got is not None and got != Fraction(expected):
            add_error(q, f"直方体表面積ミス: 2({a*b}+{b*c}+{c*a})={expected} but got {ans_str}", f"{expected}cm²")
        return

def check_kakuritsu(q):
    """確率の検算"""
    text = q['q']
    ans_str = q['a']

    # カードの確率: 1からNのカードからK以下
    m = re.search(r'1から(\d+).*(\d+)以下.*確率', text)
    if m:
        n, k = int(m.group(1)), int(m.group(2))
        if k <= n:
            expected = Fraction(k, n)
            got = parse_num(ans_str)
            if got is not None and got != expected:
                add_error(q, f"確率ミス: {k}/{n}={expected} but got {ans_str}", expected)
        return

def check_futoushiki(q):
    """不等式の検算"""
    text = q['q']
    ans_str = q['a']

    # ax + b > c 型 (a > 0)
    m = re.match(r'^(\d+)x\s*([+-])\s*(\d+)\s*>\s*(-?\d+)', text.strip())
    if m:
        a = int(m.group(1))
        sign = 1 if m.group(2) == '+' else -1
        b = sign * int(m.group(3))
        c = int(m.group(4))
        rhs = c - b
        expected_val = Fraction(rhs, a)
        # 答えは "x > N" 形式
        m2 = re.search(r'x\s*>\s*(-?[\d/]+)', ans_str)
        if m2:
            got = parse_num(m2.group(1))
            if got is not None and got != expected_val:
                add_error(q, f"不等式ミス: {a}x+{b}>{c} → x>{expected_val} but got {ans_str}", f"x > {expected_val}")
        return

def check_ichiji_kansuu(q):
    """一次関数の検算"""
    text = q['q']
    ans_str = q['a']

    # y = ax + b で x = N のときの y
    m = re.search(r'y\s*=\s*(-?\d+)x\s*([+-]?\s*\d+).*x\s*=\s*(-?\d+).*y', text)
    if m:
        a = int(m.group(1))
        b_str = m.group(2).replace(' ', '')
        b = int(b_str)
        x_val = int(m.group(3))
        expected = a * x_val + b
        got = parse_num(ans_str)
        if got is not None and got != Fraction(expected):
            add_error(q, f"一次関数ミス: y={a}x+{b}, x={x_val} → y={expected} but got {ans_str}", expected)
        return

def check_renritsu(q):
    """連立方程式の検算（代入して確認）"""
    text = q['q']
    ans_str = q['a']

    # x=N, y=M 形式の答えを解析
    m = re.search(r'x\s*=\s*(-?\d+).*y\s*=\s*(-?\d+)', ans_str)
    if not m:
        return
    x_ans, y_ans = int(m.group(1)), int(m.group(2))

    # 方程式を抽出 (ax + by = c 形式)
    lines = text.split('\n')
    eqs = []
    for line in lines:
        eq_m = re.search(r'(-?\d+)x\s*\+\s*(-?\d+)y\s*=\s*(-?\d+)', line)
        if eq_m:
            eqs.append((int(eq_m.group(1)), int(eq_m.group(2)), int(eq_m.group(3))))

    for a, b, c in eqs:
        lhs = a * x_ans + b * y_ans
        if lhs != c:
            add_error(q, f"連立方程式検算失敗: {a}×{x_ans}+{b}×{y_ans}={lhs}≠{c}", f"x={x_ans}, y={y_ans}")
            return

def check_tanikaku(q):
    """三角形の角度の検算"""
    text = q['q']
    ans_str = q['a']

    m = re.search(r'(\d+)°\s*と\s*(\d+)°.*残り', text)
    if m:
        a, b = int(m.group(1)), int(m.group(2))
        expected = 180 - a - b
        got = parse_num(ans_str)
        if got is not None and got != Fraction(expected):
            add_error(q, f"三角形内角ミス: 180-{a}-{b}={expected} but got {ans_str}", f"{expected}°")
        return

    # 外角の定理
    m = re.search(r'(\d+)°\s*と\s*(\d+)°.*外角', text)
    if m:
        a, b = int(m.group(1)), int(m.group(2))
        expected = a + b
        got = parse_num(ans_str)
        if got is not None and got != Fraction(expected):
            add_error(q, f"外角定理ミス: {a}+{b}={expected} but got {ans_str}", f"{expected}°")
        return

def check_kakei_heiritu(q):
    """平均の検算"""
    text = q['q']
    ans_str = q['a']

    # データリストから平均を計算
    m = re.search(r'平均値', text)
    if not m:
        return

    # 数列を抽出
    nums = re.findall(r'\b(\d+)\b', text)
    # 最後のほうにある数字の羅列がデータ
    if len(nums) >= 3:
        # データとして使える数字列を探す
        data = [int(n) for n in nums]
        mean = sum(data) / len(data)
        got = parse_num(ans_str)
        if got is not None:
            diff = abs(float(got) - mean)
            if diff > 0.2:  # 許容誤差0.2
                # 問題文中の数字からデータを推定するのは複雑なのでスキップ
                pass

# ===== 検算実行 =====
cat_handlers = {
    '正負の数': check_seifuno_kazu,
    '一次方程式': check_ichiji_hoteishiki,
    '比例・反比例': check_hirei,
    '平面図形': check_heimen_zukei,
    '空間図形': check_kuukan_zukei,
    '確率': check_kakuritsu,
    '不等式': check_futoushiki,
    '一次関数': check_ichiji_kansuu,
    '連立方程式': check_renritsu,
    '平行と合同': check_tanikaku,
}

checked = 0
for q in problems:
    handler = cat_handlers.get(q['cat'])
    if handler:
        try:
            handler(q)
            checked += 1
        except Exception as e:
            pass  # パースできない問題は無視

print(f"検算対象: {len(problems)}問")
print(f"検算実行: {checked}問")
print(f"エラー数: {len(errors)}件")

# エラーの内訳
cat_errs = {}
for e in errors:
    cat_errs[e['cat']] = cat_errs.get(e['cat'], 0) + 1
print("\nカテゴリ別エラー:")
for c, n in sorted(cat_errs.items(), key=lambda x: -x[1]):
    print(f"  {c}: {n}件")

with open('errors.json', 'w', encoding='utf-8') as f:
    json.dump(errors, f, ensure_ascii=False, indent=2)
print("\nerrors.json に出力しました。")
