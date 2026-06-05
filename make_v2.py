import re, pathlib

root = pathlib.Path("/mnt/d/Code Files/e7")
html = (root / "index.html").read_text(encoding="utf-8")

def sub(pattern, repl, flags=0, expect=1, label=""):
    global html
    html, n = re.subn(pattern, lambda m: repl, html, flags=flags)
    assert n == expect, f"[{label}] expected {expect} replacement(s), got {n}"

# ---------------------------------------------------------------------------
# 1. HEADER — remove search box + Register Interest button
# ---------------------------------------------------------------------------
sub(r'            <div class="search-box"[^\n]*\n            <div class="header-button d-none d-lg-flex">\n.*?\n            </div>\n            <div class="mobile-menu-toggle">',
    '            <div class="mobile-menu-toggle">', flags=re.S, label="header")

# 2. MOBILE SIDEBAR — remove Register Interest button
sub(r'      <a href="#register" class="btn btn-light"[^\n]*</a>\n      <div class="langset"',
    '      <div class="langset"', label="sidebar-register")

# 3. SEARCH OVERLAY — remove the whole block
sub(r'  <!-- ={5,} SEARCH OVERLAY ={5,} -->\n  <div class="search-overlay".*?\n  </div>\n\n  <main',
    '  <main', flags=re.S, label="search-overlay")

# ---------------------------------------------------------------------------
# 4. HERO — drop the register form, add a badge, add Platforms section after
# ---------------------------------------------------------------------------
HERO = '''    <section class="hero-section inner-banner overlay-banner" id="home">
      <div class="hero-ph"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="3" y="4" width="18" height="14" rx="2"/><path d="M3 16l5-5 4 4 3-3 6 6"/><circle cx="8.5" cy="8.5" r="1.5"/></svg><span data-li="en">Hero Visual</span><span data-li="ar">الصورة الرئيسية</span></div>
      <div class="container-fluid">
        <div class="row align-items-end">
          <div class="col-xl-8 col-lg-10" data-aos="fade-up">
            <div class="banner-description">
              <span class="hero-badge"><span data-li="en">Powered by AI · Built for Education</span><span data-li="ar">مدعوم بالذكاء الاصطناعي · مصمم للتعليم</span></span>
              <h1 data-lang="en">Learning that moves as fast as your <span class="accent">students do.</span></h1>
              <h1 data-lang="ar">تعلّم يواكب <span class="accent">وتيرة طلابك.</span></h1>
              <p data-lang="en">Minhaji gives schools and universities a smarter way to deliver, manage and track digital learning — across every device, online and offline.</p>
              <p data-lang="ar">منهجي يمنح المدارس والجامعات طريقة أذكى لتوزيع المحتوى الرقمي وإدارته ومتابعة أداء المتعلمين — عبر جميع الأجهزة، باتصال أو بدونه.</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ============ PLATFORMS ============ -->
    <section class="platforms-section">
      <div class="container-fluid">
        <p class="platforms-label"><span data-li="en">Available on</span><span data-li="ar">متاح على</span></p>
        <div class="platform-tags">
          <span class="tag">Web</span>
          <span class="tag">Mac</span>
          <span class="tag">Windows</span>
          <span class="tag">iOS</span>
          <span class="tag">Android</span>
        </div>
      </div>
    </section>'''
sub(r'    <section class="hero-section inner-banner overlay-banner" id="home">.*?\n    </section>',
    HERO, flags=re.S, label="hero")

# ---------------------------------------------------------------------------
# 5. WHAT YOU GET — replace image/text with a 6-card benefits grid
# ---------------------------------------------------------------------------
def card(icon, en_h, ar_h, en_p, ar_p):
    return f'''          <div class="benefit-card">
            <div class="benefit-icon">{icon}</div>
            <h4 data-lang="en">{en_h}</h4>
            <h4 data-lang="ar">{ar_h}</h4>
            <p data-lang="en">{en_p}</p>
            <p data-lang="ar">{ar_p}</p>
          </div>'''

CARDS = "\n".join([
    card("AI", "AI that helps students learn, not just read", "ذكاء اصطناعي يساعد على الفهم، لا مجرد القراءة",
         "An interactive assistant answers questions directly from book content. Smart page summaries help students absorb material faster, and related articles and videos add context where textbooks fall short.",
         "مساعد تفاعلي يجيب على الأسئلة مباشرة من محتوى الكتاب. ملخصات ذكية تساعد الطلاب على استيعاب المادة بسرعة أكبر، ومقالات ومقاطع فيديو ذات صلة تعمق الفهم حيث يقف الكتاب المدرسي."),
    card("Data", "Full visibility into learner engagement", "رؤية كاملة لمشاركة المتعلمين",
         "Real-time dashboards show who's reading, for how long, and where understanding drops off. Decisions based on actual data, not guesswork.",
         "لوحات تحليل فورية تُظهر من يقرأ وكم من الوقت وأين تكمن صعوبات الفهم. قرارات مبنية على بيانات حقيقية، لا تخمينات."),
    card("Sync", "Works on every device, even offline", "يعمل على كل الأجهزة، حتى بدون إنترنت",
         "Web, Mac, Windows, iOS and Android. Progress, bookmarks and notes sync automatically across all of them. Students keep reading even without a connection.",
         "ويب، ماك، ويندوز، iOS وأندرويد. التقدم والإشارات المرجعية والملاحظات تتزامن تلقائياً عبر جميعها. الطالب يواصل القراءة حتى بدون إنترنت."),
    card("A11y", "Built for every type of learner", "مصمم لجميع أنواع المتعلمين",
         "Text-to-speech, instant translation, adjustable display settings and interactive annotations. Minhaji works for a wide range of learning preferences and accessibility needs.",
         "تحويل النص إلى صوت، ترجمة فورية، إعدادات عرض قابلة للتعديل، وتعليقات تفاعلية. منهجي يناسب طيفاً واسعاً من أساليب التعلم واحتياجات إمكانية الوصول."),
    card("DRM", "Secure content, simple management", "محتوى محمي، إدارة بسيطة",
         "DRM-protected distribution keeps your content secure. SSO with Google, Office 365 and OpenID Connect means one less password for everyone. Scales to thousands of users without the headache.",
         "توزيع محمي بتقنية DRM يحافظ على أمان محتواك. تسجيل الدخول الموحد مع Google وOffice 365 وOpenID Connect يعني كلمة مرور أقل للجميع. قابل للتوسع لآلاف المستخدمين بدون تعقيد."),
    card("UX", "A reading experience students actually want to use", "تجربة قراءة يريد الطلاب فعلاً استخدامها",
         "Personalised themes, text sizes and viewing preferences. Highlights, notes and multimedia embedding. Single-page, double-page, zoom and brightness controls. Reading that adapts to the person.",
         "سمات شخصية وأحجام نص وتفضيلات عرض. تظليل وملاحظات وتضمين وسائط متعددة. تحكم في العرض المفرد والمزدوج والتكبير والسطوع. قراءة تتكيف مع الشخص."),
])

WYG = f'''    <section class="what-we-deliver-section" id="features">
      <div class="container-fluid">
        <div class="wwd-head" data-aos="fade-up">
          <h2 data-lang="en">What You Get</h2>
          <h2 data-lang="ar">ما تحصل عليه</h2>
          <h3 class="wwd-sub" data-lang="en">Everything educators and institutions actually need.</h3>
          <h3 class="wwd-sub" data-lang="ar">كل ما تحتاجه المؤسسات التعليمية فعلاً.</h3>
        </div>
        <div class="benefits-grid" data-aos="fade-up" data-aos-delay="100">
{CARDS}
        </div>
      </div>
    </section>'''
sub(r'    <section class="what-we-deliver-section" id="features">.*?\n    </section>',
    WYG, flags=re.S, label="what-you-get")

# ---------------------------------------------------------------------------
# 6. Remove the 3 FEATURE sections, STANDARDS band, EMPOWERING CTA
# ---------------------------------------------------------------------------
sub(r'\n    <!-- ={5,} FEATURE[^\n]*-->\n    <section class="feature-section">.*?\n    </section>',
    '', flags=re.S, expect=3, label="feature-sections")
sub(r'\n    <!-- ={5,} STANDARDS[^\n]*-->\n    <section class="certifications-standards-section">.*?\n    </section>',
    '', flags=re.S, label="standards")
sub(r'\n    <!-- ={5,} EMPOWERING[^\n]*-->\n    <section class="empowering-section">.*?\n    </section>',
    '', flags=re.S, label="empowering")

# ---------------------------------------------------------------------------
# 7. WHO IT'S FOR — replace big-list with 3 detailed cards
# ---------------------------------------------------------------------------
def whocard(en_h, ar_h, items):
    lis = "\n".join(f'              <li data-lang="en">{en}</li>\n              <li data-lang="ar">{ar}</li>'
                    for en, ar in items)
    return f'''          <div class="who-card">
            <h4 data-lang="en">{en_h}</h4>
            <h4 data-lang="ar">{ar_h}</h4>
            <ul>
{lis}
            </ul>
          </div>'''

WHO_CARDS = "\n".join([
    whocard("For Learners", "للطلاب والمتعلمين", [
        ("More engaging reading experience", "تجربة قراءة أكثر تفاعلاً"),
        ("AI assistance for faster understanding", "مساعد ذكي لفهم أسرع"),
        ("Flexible access, online and offline", "وصول مرن، مع الإنترنت أو بدونه"),
        ("Works on any device they already use", "يعمل على أي جهاز يستخدمونه"),
    ]),
    whocard("For Educators &amp; Institutions", "للمعلمين والمؤسسات", [
        ("Clear data on learner engagement and progress", "بيانات واضحة عن مشاركة الطلاب وتقدمهم"),
        ("Simplified content distribution", "توزيع محتوى مبسط"),
        ("Scalable for schools, universities and large orgs", "قابل للتوسع للمدارس والجامعات والمؤسسات الكبيرة"),
        ("Secure infrastructure, enterprise-grade auth", "بنية تحتية آمنة وتوثيق على مستوى المؤسسات"),
    ]),
    whocard("For Content Providers", "لمزودي المحتوى", [
        ("DRM protection for digital publications", "حماية DRM للمنشورات الرقمية"),
        ("Reach users across all major platforms", "الوصول للمستخدمين عبر جميع المنصات الرئيسية"),
        ("Higher engagement through AI-powered tools", "تفاعل أعلى عبر أدوات الذكاء الاصطناعي"),
    ]),
])

WHO = f'''    <section class="whofor-section" id="who">
      <div class="container-fluid">
        <div class="whofor-head" data-aos="fade-up">
          <h2 data-lang="en">Built for everyone in the <span>learning chain.</span></h2>
          <h2 data-lang="ar">مصمم لكل طرف في <span>سلسلة التعلم.</span></h2>
        </div>
        <div class="who-grid" data-aos="fade-up" data-aos-delay="100">
{WHO_CARDS}
        </div>
      </div>
    </section>'''
sub(r'    <section class="industries-we-support-section" id="who"[^>]*>.*?\n    </section>',
    WHO, flags=re.S, label="who")

# ---------------------------------------------------------------------------
# 8. FOOTER — drop the Register link, point Contact at email
# ---------------------------------------------------------------------------
sub(r'                  <li><a href="#register"><span data-li="en">Register</span><span data-li="ar">سجّل</span></a></li>\n',
    '', label="footer-register")
sub(r'<li><a href="#register"><span data-li="en">Contact</span>',
    '<li><a href="mailto:webteam@digitalnexa.com"><span data-li="en">Contact</span>', label="footer-contact")

# ---------------------------------------------------------------------------
# 9. JS — remove search + form-submit handlers (no longer in the DOM)
# ---------------------------------------------------------------------------
sub(r'    /\* ---- Search overlay ---- \*/\n    function openSearch\(\)\{.*?\n    function closeSearch\(\)\{.*?\n    document\.addEventListener\(\'keydown\'[^\n]*\n',
    "    document.addEventListener('keydown',e=>{if(e.key==='Escape'){closeSidebar();}});\n",
    flags=re.S, label="js-search")
sub(r'    /\* ---- Form submit ---- \*/\n    function handleSubmit\(e\)\{.*?\n    \}\n\n',
    '', flags=re.S, label="js-submit")

# ---------------------------------------------------------------------------
# 10. CSS — add styles for badge / platforms / benefits / who cards
# ---------------------------------------------------------------------------
CSS = '''    /* ============ V2 ADDITIONS ============ */
    .hero-section .banner-description .hero-badge{display:inline-block;width:fit-content;background:rgba(107,203,218,.18);border:1px solid rgba(107,203,218,.5);color:#fff;font-size:12px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;padding:7px 16px;border-radius:30px;margin-bottom:.2rem;}
    body.ar .hero-section .banner-description .hero-badge{letter-spacing:0;}

    .platforms-section{padding:2.5rem 0;background:#f4f7f8;border-bottom:1px solid var(--line);text-align:center;}
    .platforms-section .platforms-label{color:var(--gray);font-size:13px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;margin:0 0 1rem;}
    body.ar .platforms-section .platforms-label{letter-spacing:0;}
    .platform-tags{display:flex;justify-content:center;flex-wrap:wrap;gap:.7rem;}
    .platform-tags .tag{background:#fff;border:1px solid var(--line);padding:7px 20px;border-radius:30px;font-size:14px;font-weight:600;color:var(--slate-2);}

    .section-label{color:var(--teal-deep);font-size:12px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;margin-bottom:.8rem;}
    body.ar .section-label{letter-spacing:0;}
    .what-we-deliver-section .wwd-head .wwd-sub{color:var(--teal-2);font-size:28px;font-weight:500;line-height:1.2;text-transform:none;max-width:100%;margin:.4rem 0 2.5rem;}
    .benefits-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:1.6rem;}
    .benefit-card{background:#f4f7f8;border:1px solid var(--line);border-radius:16px;padding:2rem;transition:transform .25s ease,box-shadow .25s ease;}
    .benefit-card:hover{transform:translateY(-4px);box-shadow:0 14px 34px rgba(3,20,28,.08);}
    .benefit-icon{width:52px;height:52px;background:var(--teal);border-radius:12px;display:flex;align-items:center;justify-content:center;color:#fff;font-size:13px;font-weight:800;margin-bottom:1.2rem;}
    .benefit-card h4{color:var(--ink);font-size:18px;font-weight:700;line-height:1.3;margin:0 0 .6rem;}
    .benefit-card p{color:var(--slate-2);font-size:15px;font-weight:400;line-height:1.7;margin:0;}

    .whofor-section{padding:0 0 6rem;}
    .whofor-section .whofor-head{margin-bottom:2.5rem;}
    .whofor-section h2{color:#000;font-size:54px;font-weight:900;line-height:.95;text-transform:uppercase;max-width:760px;margin:0;}
    body.ar .whofor-section h2{text-transform:none;line-height:1.1;}
    .whofor-section h2 span{color:var(--teal-2);}
    .who-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:1.6rem;}
    .who-grid .who-card{background:#fff;border:1px solid var(--line);border-radius:16px;padding:2rem;}
    .who-grid .who-card h4{color:var(--teal-deep);font-size:18px;font-weight:700;margin:0 0 1rem;}
    .who-grid .who-card ul{list-style:none;padding:0;margin:0;}
    .who-grid .who-card li{color:var(--slate-2);font-size:15px;line-height:1.5;padding:.7rem 0;border-bottom:1px solid var(--line);}
    .who-grid .who-card li:last-child{border-bottom:none;}
    .who-grid .who-card li::before{content:'\\2192 \\00a0';color:var(--teal-deep);font-weight:700;}
    body.ar .who-grid .who-card li::before{content:'\\2190 \\00a0';}

    @media (max-width:991px){.whofor-section h2{font-size:38px;}}
'''
sub(r'  </style>\n</head>', CSS + '  </style>\n</head>', label="css")

(root / "index-v2.html").write_text(html, encoding="utf-8")

# quick sanity report
leftover_register = html.count('#register')
print("WROTE index-v2.html  size:", len(html), "bytes")
print("remaining '#register' refs:", leftover_register)
for tok in ['feature-section', 'certifications-standards-section', 'empowering-section',
            'hero-form', 'handleSubmit', 'search-overlay', 'platforms-section',
            'benefits-grid', 'who-grid', 'hero-badge']:
    print(f"  {tok:34s}: {html.count(tok)}")
