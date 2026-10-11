(() => {
  const $ = (s) => document.querySelector(s);
  const nav = $("#nav"), menu = $("#menuToggle"), status = $("#assistantStatus");
  const statusText = $("#statusText"), hint = $("#assistantHint"), button = $("#assistantButton"), toast = $("#toast");
  $("#year").textContent = new Date().getFullYear();
  menu.addEventListener("click", () => { const open = nav.classList.toggle("open"); menu.setAttribute("aria-expanded", String(open)); menu.textContent = open ? "×" : "☰"; });
  nav.querySelectorAll("a").forEach(a => a.addEventListener("click", () => { nav.classList.remove("open"); menu.setAttribute("aria-expanded", "false"); menu.textContent = "☰"; }));
  let timer;
  const showToast = (msg) => { toast.textContent = msg; toast.classList.add("show"); clearTimeout(timer); timer = setTimeout(() => toast.classList.remove("show"), 4200); };
  // Voice-call integration is handled by voice.js so the customer name can be
  // passed as a Retell dynamic variable when a call is actually created.
  document.querySelectorAll('a[href^="#"]').forEach(a => a.addEventListener("click", e => {
    const targetId = a.getAttribute("href");
    if (targetId === "#") { e.preventDefault(); window.scrollTo({top:0, behavior:"smooth"}); return; }
    const target = document.querySelector(targetId); if (target) { e.preventDefault(); target.scrollIntoView({behavior:"smooth", block:"start"}); }
  }));
})();
