# 打包：把各页内嵌进播放器外壳，得到一个可以单独发给别人的 课件.html
# 用法：python3 pack.py [文件夹]     文件夹里要有 index.html（播放器）和它引用的各页
import json, pathlib, re, sys
root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '.')
shell = (root / 'index.html').read_text(encoding='utf-8')
count = 0
def embed(m):
    global count
    page = root / m.group(3)
    if not page.exists():
        raise SystemExit('找不到页面文件：' + m.group(3))
    count += 1
    # 把 < 转成 <：页面代码里有 </script>，不转义会把播放器自己的脚本截断
    return m.group(1) + json.dumps(page.read_text(encoding='utf-8'), ensure_ascii=False).replace('<', '\\u003c')
out = re.sub(r'''(\bsrc\s*:\s*)(["'])([^"'<>]+\.html)\2''', embed, shell)
if not count:
    raise SystemExit('没有在 index.html 的 DECK.pages 里找到 src: "xxx.html"')
(root / '课件.html').write_text(out, encoding='utf-8')
print(f'已打包 {count} 页 → {root / "课件.html"}')
