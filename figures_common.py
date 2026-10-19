# -*- coding: utf-8 -*-
"""绘图公共工具：统一舍入规则。

**为何需要它**：正文与 Table 1 按科学报告惯例对 .x5 一律进位（75.35 → 75.4），
而 Python 的 `format(x, ".1f")` 对二进制浮点采用银行家舍入，且 75.35 的二进制表示略小于
75.35，结果为 75.3 —— 造成图与正文出现 0.1 个百分点的冲突。
对一篇以「预注册 + 诚实报告」为核心卖点的稿件，这类冲突会直接动摇审稿人对数字的信任。

本模块提供 `r1()`，与正文/Table 1 的写法规则一致（ROUND_HALF_UP）。
所有 figures_*.py 中出现 `{x:.1f}` 之处应改用 `r1(x)`。
"""
from decimal import Decimal, ROUND_HALF_UP

__all__ = ["r1", "r2", "pct"]


def r1(x) -> str:
    """一位小数；.x5 一律进位（75.35→75.4，83.85→83.9）。"""
    return str(Decimal(repr(float(x))).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))


def r2(x) -> str:
    """两位小数。"""
    return str(Decimal(repr(float(x))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def pct(x) -> str:
    """百分数，一位小数 + % 号。"""
    return r1(x) + "%"


if __name__ == "__main__":
    # 自检：与正文/Table 1 的既定写法逐项比对
    EXPECT = [(75.35, "75.4"), (70.35, "70.4"), (83.85, "83.9"),
              (69.84, "69.8"), (56.7, "56.7"), (79.83, "79.8")]
    print("  舍入规则自检（须与 结果汇总_v1.md / Table 1 一致）")
    ok = True
    for v, exp in EXPECT:
        got = r1(v)
        py = format(v, ".1f")
        mark = "✔" if got == exp else "✘"
        ok &= got == exp
        print("    %-8s -> r1=%-6s 期望=%-6s %s   (Python :.1f = %s)"
              % (v, got, exp, mark, py))
    print("  %s" % ("全部一致 ✔" if ok else "✘ 有不一致"))