// What the site adds with a script: search, previews of what a link leads to, and
// the arrow keys. Everything else works without it.
(() => {
  const root = new URL(".", document.currentScript.src).href;
  const load = (() => {
    const cache = {};
    return (name) => (cache[name] ??= fetch(root + name).then((r) => r.json()));
  })();
  const fold = (s) => s.normalize("NFD").replace(/\p{M}/gu, "").toLowerCase();
  const esc = (s) => s.replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
  const typing = (el) => el && (el.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(el.tagName));

  // ------------------------------------------------------------ search

  const open = document.querySelector(".search-open");
  const dialog = document.createElement("dialog");
  dialog.className = "search-dialog";
  dialog.setAttribute("aria-label", "Search the book");
  dialog.setAttribute("closedby", "any");
  dialog.innerHTML = `<input type="search" placeholder="Search the book" aria-label="Search the book" autocomplete="off" spellcheck="false"><p class="visually-hidden" role="status"></p><ul class="search-results"></ul>`;
  document.body.append(dialog);
  const input = dialog.querySelector("input");
  const list = dialog.querySelector("ul");
  const status = dialog.querySelector("[role=status]");
  let docs = null;
  let selected = -1;

  async function index() {
    if (!docs) {
      docs = (await load("search.json")).map((d) => ({ ...d, ft: fold(d.t), fa: fold(d.a || ""), fb: fold(d.b || "") }));
    }
    return docs;
  }

  function score(doc, words) {
    let total = 0;
    for (const w of words) {
      let s = 0;
      if (doc.ft === w) s += 60;
      else if (doc.ft.startsWith(w)) s += 30;
      else if (doc.ft.includes(w)) s += 18;
      if (doc.fa.includes(w)) s += 14;
      let at = doc.fb.indexOf(w);
      for (let n = 0; at >= 0 && n < 6; n++) {
        s += 1;
        at = doc.fb.indexOf(w, at + w.length);
      }
      if (!s) return 0;
      total += s;
    }
    // Entries are what people look for most often.
    return total + (doc.g ? 2 : 0);
  }

  function snippet(doc, words) {
    const at = Math.min(...words.map((w) => doc.fb.indexOf(w)).filter((i) => i >= 0));
    if (!isFinite(at)) return esc((doc.b || "").slice(0, 110));
    const start = Math.max(0, at - 50);
    let text = esc(doc.b.slice(start, start + 140));
    for (const w of words) {
      text = text.replace(new RegExp(`(${w.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")})`, "i"), "<mark>$1</mark>");
    }
    return (start ? "…" : "") + text + "…";
  }

  async function run() {
    const words = fold(input.value).split(/\s+/).filter(Boolean);
    selected = -1;
    if (!words.length) {
      list.innerHTML = status.textContent = "";
      return;
    }
    const all = await index();
    const hits = all.map((d) => [score(d, words), d]).filter(([s]) => s).sort((a, b) => b[0] - a[0]).slice(0, 25);
    list.innerHTML = hits.length
      ? hits.map(([, d]) => `<li><a href="${root}${esc(d.u)}"><span class="r-title">${esc(d.t)}</span> ${d.g ? `<span class="grade-tab ${esc(d.k || "")}">${esc(d.g)}</span>` : ""}<span class="r-where">${esc(d.c || "")}</span><span class="r-text">${snippet(d, words)}</span></a></li>`).join("")
      : `<li class="search-note">Nothing in the book matches that.</li>`;
    status.textContent = `${hits.length} results`;
  }

  function show() {
    dialog.showModal();
    input.select();
    index();
  }

  if (open) {
    open.hidden = false;
    open.addEventListener("click", show);
  }
  input.addEventListener("input", run);
  dialog.addEventListener("click", (e) => { if (e.target === dialog) dialog.close(); });
  dialog.addEventListener("keydown", (e) => {
    const links = [...list.querySelectorAll("a")];
    if (e.key === "ArrowDown" || e.key === "ArrowUp") {
      e.preventDefault();
      if (!links.length) return;
      selected = (selected + (e.key === "ArrowDown" ? 1 : -1) + links.length) % links.length;
      links.forEach((a, i) => a.setAttribute("aria-selected", i === selected));
      links[selected].scrollIntoView({ block: "nearest" });
    } else if (e.key === "Enter" && links.length) {
      e.preventDefault();
      location.href = links[Math.max(selected, 0)].href;
    }
  });

  // ------------------------------------------------------------ keys

  document.addEventListener("keydown", (e) => {
    if (e.defaultPrevented || e.metaKey || e.ctrlKey || e.altKey || typing(document.activeElement)) return;
    if (e.key === "/") {
      e.preventDefault();
      show();
    } else if (e.key === "ArrowLeft" || e.key === "ArrowRight") {
      const link = document.querySelector(`link[rel="${e.key === "ArrowLeft" ? "prev" : "next"}"]`);
      if (link) location.href = link.href;
    }
  });

  // ------------------------------------------------------------ previews

  // A glossary word, a technique or a citation shows what it leads to, so that you
  // needn't leave your place: on hover or focus, or on a first tap on a touch screen.
  const box = document.createElement("div");
  box.className = "preview";
  box.popover = "manual";
  box.setAttribute("role", "tooltip");
  document.body.append(box);
  // The stylesheet tethers the preview to its link where the browser can do that.
  const tethered = CSS.supports("anchor-name: --preview");
  const isOpen = () => box.matches(":popover-open");
  let current = null;
  let timer = 0;

  const targetOf = (a) => {
    if (!a.href.startsWith(root)) return null;
    return decodeURI(a.href.slice(root.length));
  };
  const previewable = (a) => a && a.closest("main") && !a.closest(".pager, .crumbs, .preview") && a.matches("a.tref, a.jt, a.tref-plain, .cite a");

  function place(a) {
    if (tethered) {
      document.querySelectorAll("[data-previewed]").forEach((link) => {
        link.style.anchorName = "";
        delete link.dataset.previewed;
      });
      a.style.anchorName = "--preview";
      a.dataset.previewed = "";
    } else {
      const r = a.getBoundingClientRect();
      const below = r.bottom + box.offsetHeight + 12 < innerHeight;
      box.style.left = `${Math.max(8, Math.min(r.left, document.documentElement.clientWidth - box.offsetWidth - 8))}px`;
      box.style.top = `${below ? r.bottom + 6 : r.top - box.offsetHeight - 6}px`;
    }
  }

  async function reveal(a, withLink) {
    const previews = await load("previews.json");
    const data = previews[targetOf(a)];
    if (!data || current !== a) return;
    box.innerHTML = `<div class="preview-title"><span>${esc(data.t)}</span>${data.g ? `<span class="grade-tab ${esc(data.c || "")}">${esc(data.g)}</span>` : ""}</div><div>${esc(data.h)}</div>${withLink ? `<a class="preview-go" href="${esc(a.href)}">Go there</a>` : ""}`;
    if (tethered) place(a);
    if (!isOpen()) box.showPopover();
    if (!tethered) place(a);
  }

  function hide() {
    clearTimeout(timer);
    current = null;
    if (isOpen()) box.hidePopover();
  }

  document.addEventListener("pointerover", (e) => {
    if (e.pointerType === "touch") return;
    const a = e.target.closest?.("a");
    if (previewable(a)) {
      clearTimeout(timer);
      current = a;
      timer = setTimeout(() => reveal(a, false), 180);
    } else if (!e.target.closest?.(".preview") && current) {
      clearTimeout(timer);
      timer = setTimeout(hide, 150);
    }
  });
  document.addEventListener("focusin", (e) => {
    const a = e.target.closest?.("a");
    if (a && a.matches(":focus-visible") && previewable(a)) {
      current = a;
      reveal(a, false);
    } else if (!e.target.closest?.(".preview")) hide();
  });
  // A first tap on touch shows the preview, with a link to go there.
  let touched = false;
  document.addEventListener("pointerdown", (e) => { touched = e.pointerType === "touch"; });
  document.addEventListener("click", (e) => {
    const a = e.target.closest?.("a");
    if (touched && previewable(a) && current !== a && !e.metaKey) {
      e.preventDefault();
      current = a;
      reveal(a, true);
    } else if (!e.target.closest?.(".preview")) hide();
  });
  document.addEventListener("keydown", (e) => { if (e.key === "Escape") hide(); });
  // A preview that isn't tethered can't follow its link.
  if (!tethered) addEventListener("scroll", hide, { passive: true });

  // ------------------------------------------------------------ the outline

  const here = document.querySelector('.outline [aria-current="page"]');
  if (here) {
    const nav = here.closest(".outline");
    nav.scrollTop = Math.max(0, here.offsetTop - nav.clientHeight / 3);
  }

  // ------------------------------------------------------------ closed answers

  // A backlink or a "Cited in" can lead into an answer that is still closed, and not
  // every browser opens it for you.
  const openAnswer = () => {
    const target = location.hash && document.getElementById(decodeURIComponent(location.hash.slice(1)));
    const closed = target && target.closest("details:not([open])");
    if (closed) {
      closed.open = true;
      target.scrollIntoView();
    }
  };
  addEventListener("hashchange", openAnswer);
  openAnswer();
})();
