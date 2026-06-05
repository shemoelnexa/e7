import base64, re, pathlib

root = pathlib.Path("/mnt/d/Code Files/e7")
cdn  = pathlib.Path("/tmp/cdn")
html = (root/"index.html").read_text(encoding="utf-8")

def b64(p): return base64.b64encode(pathlib.Path(p).read_bytes()).decode()

# ---------- Font Awesome CSS with woff2 inlined ----------
fa = (cdn/"fa.css").read_text(encoding="utf-8")
for name in ["fa-solid-900","fa-brands-400","fa-regular-400"]:
    fa = fa.replace(f"url(../webfonts/{name}.woff2)", f"url(data:font/woff2;base64,{b64(cdn/(name+'.woff2'))})")
fa = re.sub(r',?url\(\.\./webfonts/[^)]*\)\s*format\([^)]*\)', '', fa)
fa = re.sub(r'src:\s*;', '', fa)

boot_css=(cdn/"bootstrap.min.css").read_text(encoding="utf-8")
aos_css =(cdn/"aos.css").read_text(encoding="utf-8")
boot_js =(cdn/"bootstrap.bundle.min.js").read_text(encoding="utf-8")
aos_js  =(cdn/"aos.js").read_text(encoding="utf-8")

html = html.replace('<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" />','<style>/* bootstrap 5.3.0 */\n'+boot_css+'\n</style>')
html = html.replace('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" />','<style>/* font-awesome 6.4.0 */\n'+fa+'\n</style>')
html = html.replace('<link href="https://unpkg.com/aos@2.3.1/dist/aos.css" rel="stylesheet" />','<style>/* aos 2.3.1 */\n'+aos_css+'\n</style>')
html = html.replace('<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>','<script>/* bootstrap bundle */\n'+boot_js+'\n</script>')
html = html.replace('<script src="https://unpkg.com/aos@2.3.1/dist/aos.js"></script>','<script>/* aos */\n'+aos_js+'\n</script>')

# ---------- local fonts ----------
for fn,_ in [("HelveticaNowDisplay-THIN.ttf",0),("HelveticaNowDisplay-LIGHT.ttf",0),("HelveticaNowDisplay-REGULAR.ttf",0),("HelveticaNowDisplay-MEDIUM.ttf",0),("HelveticaNowDisplay-BOLD.ttf",0),("HelveticaNowDisplay-EXTRABOLD.ttf",0),("HelveticaNowDisplay-BLACK.ttf",0)]:
    html = html.replace(f"url('assets/fonts/{fn}')", f"url('data:font/ttf;base64,{b64(root/'assets/fonts'/fn)}')")

# ---------- video ----------
html = html.replace('<source src="assets/minhaji-hero.mp4" type="video/mp4" />', f'<source src="data:video/mp4;base64,{b64(root/"assets/minhaji-hero.mp4")}" type="video/mp4" />')

# ---------- ALL images under assets/img referenced anywhere (src="..." or url('...')) ----------
mime={"png":"image/png","jpg":"image/jpeg","jpeg":"image/jpeg","svg":"image/svg+xml","webp":"image/webp"}
refs=sorted(set(re.findall(r"assets/img/[\w.\-]+\.(?:png|jpe?g|svg|webp)", html)))
for ref in refs:
    ext=ref.rsplit('.',1)[1].lower()
    html = html.replace(ref, f"data:{mime[ext]};base64,{b64(root/ref)}")
print("inlined images:", len(refs), [r.split('/')[-1] for r in refs])

out=root/"e7-landing-page.html"; out.write_text(html,encoding="utf-8")
leftover=re.findall(r'(assets/|https://cdn\.jsdelivr|https://unpkg|https://cdnjs)', html)
print("output size MB:", round(out.stat().st_size/1024/1024,1))
print("remaining external/asset refs:", len(leftover), set(leftover))
