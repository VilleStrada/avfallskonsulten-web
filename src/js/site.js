/* avfallskonsulten.se: meny, cookie-samtycke och bokningsformulär. Ingen beroenden. */
(function () {
  "use strict";

  /* ---------- Meny ---------- */
  var topp = document.querySelector(".topp");
  var menyKnapp = document.querySelector(".topp__meny-knapp");
  if (menyKnapp) {
    menyKnapp.addEventListener("click", function () {
      var oppen = topp.classList.toggle("ar-oppen");
      menyKnapp.setAttribute("aria-expanded", oppen ? "true" : "false");
    });
  }
  document.querySelectorAll(".meny__grupp-knapp").forEach(function (knapp) {
    knapp.addEventListener("click", function () {
      var oppen = knapp.getAttribute("aria-expanded") === "true";
      document.querySelectorAll(".meny__grupp-knapp").forEach(function (k) { k.setAttribute("aria-expanded", "false"); });
      knapp.setAttribute("aria-expanded", oppen ? "false" : "true");
    });
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") {
      topp && topp.classList.remove("ar-oppen");
      menyKnapp && menyKnapp.setAttribute("aria-expanded", "false");
      document.querySelectorAll(".meny__grupp-knapp").forEach(function (k) { k.setAttribute("aria-expanded", "false"); });
    }
  });
  document.addEventListener("click", function (e) {
    if (topp && !topp.contains(e.target)) {
      topp.classList.remove("ar-oppen");
      menyKnapp && menyKnapp.setAttribute("aria-expanded", "false");
      document.querySelectorAll(".meny__grupp-knapp").forEach(function (k) { k.setAttribute("aria-expanded", "false"); });
    }
  });

  /* ---------- Cookie-samtycke ---------- */
  var NYCKEL = "ak_cookie_val";
  var banner = document.getElementById("cookie");
  var gtmId = document.body.getAttribute("data-gtm");
  var gtmLaddad = false;

  function laddaGtm() {
    if (gtmLaddad || !gtmId) return;
    gtmLaddad = true;
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({ "gtm.start": new Date().getTime(), event: "gtm.js" });
    var s = document.createElement("script");
    s.async = true;
    s.src = "https://www.googletagmanager.com/gtm.js?id=" + encodeURIComponent(gtmId);
    document.head.appendChild(s);
  }
  function lasVal() { try { return localStorage.getItem(NYCKEL); } catch (e) { return null; } }
  function sparaVal(v) { try { localStorage.setItem(NYCKEL, v); } catch (e) {} }
  function visaBanner() { if (banner) banner.hidden = false; }
  function doljBanner() { if (banner) banner.hidden = true; }

  var val = lasVal();
  if (val === "ja") laddaGtm();
  else if (val !== "nej") visaBanner();

  document.querySelectorAll("[data-cookie]").forEach(function (k) {
    k.addEventListener("click", function () {
      var v = k.getAttribute("data-cookie");
      sparaVal(v);
      doljBanner();
      if (v === "ja") laddaGtm();
    });
  });
  document.querySelectorAll("[data-cookie-installningar]").forEach(function (k) {
    k.addEventListener("click", function () { visaBanner(); window.scrollTo({ top: document.body.scrollHeight }); });
  });

  /* ---------- Bokningsformulär ----------
     Live (Loopia): formuläret postas till includes/skicka.php som mejlar info@ och skickar vidare till /tack.
     Staging (GitHub Pages, data-form="staging"): ingen PHP finns, så vi visar bara tack-rutan. */
  var formLage = document.body.getAttribute("data-form");
  document.querySelectorAll("form.form").forEach(function (form) {
    var t = form.querySelector('input[name="t"]');
    if (t) t.value = String(Date.now()); /* tidsstämpel, skicka.php avvisar svar snabbare än 3 s */
    form.addEventListener("submit", function (e) {
      form.classList.remove("ar-fel");
      if (!form.checkValidity()) {
        e.preventDefault();
        form.classList.add("ar-fel");
        var forsta = form.querySelector(":invalid");
        if (forsta) forsta.focus();
        return;
      }
      var honung = form.querySelector(".honung input");
      if (honung && honung.value) { e.preventDefault(); return; } /* spamrobot */
      if (formLage === "staging") {
        e.preventDefault();
        form.classList.add("ar-skickad");
        form.scrollIntoView({ block: "start" });
      }
    });
    /* skicka.php skickar tillbaka hit med ?fel=1 (fält saknas) eller ?fel=2 (mejlet gick inte) */
    if (/[?&]fel=\d/.test(location.search)) {
      form.classList.add("ar-fel", "ar-serverfel");
      form.scrollIntoView({ block: "start" });
    }
  });

  /* ---------- Hero-film: laddas först när sidan är klar, så att den inte påverkar LCP.
     Spelar alltid (även med "reducerad rörelse", som är vanligt på Windows-jobbdatorer).
     Om webbläsaren vägrar autoplay: nytt försök vid första klick/touch/scroll/tangent,
     och en spela-knapp visas om filmen inte kommit igång inom 2 s. ---------- */
  var film = document.querySelector(".hero2__video[data-src]");
  var spelaKnapp = document.querySelector(".hero2__spela");
  if (film) {
    film.muted = true; /* krävs för tyst autoplay, utöver attributet i HTML */
    film.addEventListener("playing", function () {
      film.classList.add("ar-igang");
      if (spelaKnapp) spelaKnapp.hidden = true;
    });
    var forsokSpela = function () {
      if (!film.src) film.src = film.getAttribute("data-src");
      var p = film.play();
      if (p && p.catch) p.catch(function () {});
    };
    var vidInteraktion = function () {
      if (film.paused) forsokSpela();
      ["click", "touchstart", "scroll", "keydown"].forEach(function (ev) { document.removeEventListener(ev, vidInteraktion); });
    };
    var startaFilm = function () {
      forsokSpela();
      ["click", "touchstart", "scroll", "keydown"].forEach(function (ev) { document.addEventListener(ev, vidInteraktion, { passive: true }); });
      setTimeout(function () {
        if (film.paused && spelaKnapp) spelaKnapp.hidden = false;
      }, 2000);
    };
    if (spelaKnapp) spelaKnapp.addEventListener("click", function (e) { e.stopPropagation(); forsokSpela(); });
    /* pausa filmen när hero inte syns, så att den inte drar kraft medan man läser längre ner */
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (poster) {
        poster.forEach(function (p) {
          if (!film.src) return;
          if (p.isIntersecting) { var pr = film.play(); if (pr && pr.catch) pr.catch(function () {}); }
          else film.pause();
        });
      }, { threshold: 0.05 }).observe(film);
    }
    if (document.readyState === "complete") setTimeout(startaFilm, 300);
    else window.addEventListener("load", function () { setTimeout(startaFilm, 300); });
  }

  /* ---------- Rörelse: intoning vid scroll och uppräkning av siffror ---------- */
  var mindreRorelse = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (!mindreRorelse && "IntersectionObserver" in window) {
    document.documentElement.classList.add("js");
    var hero = document.querySelector(".hero2");
    /* setTimeout i stället för requestAnimationFrame: rAF pausas i bakgrundsflikar och då skulle texten aldrig tonas in */
    if (hero) setTimeout(function () { hero.classList.add("ar-laddad"); }, 30);
    var mal = document.querySelectorAll(
      ".sektion > .wrap > *, .fni .wrap > *, .fortroende__punkt, .steg__punkt, .kort, .huvudkort, .reco, .faq, .omraden__rad > *, .boka__rad > *"
    );
    mal.forEach(function (el) { el.setAttribute("data-reveal", ""); });
    var io = new IntersectionObserver(function (poster) {
      poster.forEach(function (p) {
        if (p.isIntersecting) { p.target.classList.add("ar-synlig"); io.unobserve(p.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.05 });
    mal.forEach(function (el) { io.observe(el); });
    /* element som redan är i bild när sidan laddas ska inte vänta */
    setTimeout(function () {
      mal.forEach(function (el) {
        var r = el.getBoundingClientRect();
        if (r.top < window.innerHeight && r.bottom > 0) el.classList.add("ar-synlig");
      });
    }, 50);

    /* räkna upp tal, t.ex. "231 omdömen" */
    document.querySelectorAll("[data-rakna]").forEach(function (el) {
      var slut = parseInt(el.getAttribute("data-rakna"), 10);
      var startat = false;
      var r = new IntersectionObserver(function (poster) {
        if (!poster[0].isIntersecting || startat) return;
        startat = true;
        var t0 = null;
        function steg(t) {
          if (!t0) t0 = t;
          var andel = Math.min((t - t0) / 1200, 1);
          var lätt = 1 - Math.pow(1 - andel, 3);
          el.textContent = Math.round(slut * lätt);
          if (andel < 1) requestAnimationFrame(steg);
        }
        requestAnimationFrame(steg);
      }, { threshold: 0.5 });
      r.observe(el);
    });
  }

  /* ---------- Kärlväljare (schablon från våra avtal, inga priser) ---------- */
  var kvLgh = document.getElementById("kv-lgh");
  if (kvLgh) {
    var SCHABLON = [
      { max: 10, rader: [["Papper", 2, 370, "var 4:e vecka"], ["Plast", 1, 370, "var 4:e vecka"], ["Glas", 2, 240, "var 8:e vecka"], ["Metall", 1, 140, "var 8:e vecka"], ["Tidningar", 1, 240, "var 8:e vecka"]] },
      { max: 25, rader: [["Papper", 1, 660, "varje vecka"], ["Plast", 1, 370, "varje vecka"], ["Glas", 2, 190, "var 4:e vecka"], ["Metall", 1, 190, "var 4:e vecka"], ["Tidningar", 1, 240, "var 8:e vecka"]] },
      { max: 40, rader: [["Papper", 1, 660, "två gånger i veckan"], ["Plast", 1, 660, "varje vecka"], ["Glas", 2, 240, "varannan vecka"], ["Metall", 1, 190, "var 4:e vecka"], ["Tidningar", 1, 240, "var 4:e vecka"]] },
      { max: 70, rader: [["Papper", 3, 660, "varje vecka"], ["Plast", 3, 370, "varje vecka"], ["Glas", 3, 190, "varannan vecka"], ["Metall", 1, 190, "varannan vecka"], ["Tidningar", 1, 240, "var 4:e vecka"]] },
      { max: 99999, rader: [["Papper", 5, 660, "varje vecka"], ["Plast", 2, 660, "varje vecka"], ["Glas", 4, 190, "var 4:e vecka"], ["Metall", 2, 240, "var 4:e vecka"], ["Tidningar", 1, 370, "var 4:e vecka"]] }
    ];
    var FARG = { Papper: "#3b6fb6", Plast: "#e07b2a", Glas: "#2e8b57", Metall: "#7a8794", Tidningar: "#8c5aa6" };
    var FORKL = { Papper: "pappersförpackningar", Plast: "plastförpackningar", Glas: "färgat och ofärgat glas, ett kärl vardera", Metall: "metallförpackningar", Tidningar: "tidningar och returpapper, tillval" };
    var kvUt = document.getElementById("kv-lgh-ut"), kvLista = document.getElementById("kv-lista"), kvSumma = document.getElementById("kv-summa");
    var kvSenast = -1;
    function kvRita() {
      var lgh = parseInt(kvLgh.value, 10);
      kvUt.textContent = lgh;
      var grupp = 0;
      while (lgh > SCHABLON[grupp].max) grupp++;
      if (grupp === kvSenast) return;
      kvSenast = grupp;
      var html = "", tot = 0;
      SCHABLON[grupp].rader.forEach(function (r) {
        tot += r[1];
        html += '<li class="kv__rad ar-ny"><span class="kv__ikon" style="background:' + FARG[r[0]] + '">' + r[0].slice(0, 2) + '</span>' +
          '<span><strong>' + r[0] + '</strong><small>' + FORKL[r[0]] + ', töms ' + r[3] + '</small></span>' +
          '<span class="kv__antal">' + r[1] + ' × ' + r[2] + ' L</span></li>';
      });
      kvLista.innerHTML = html;
      var spann = lgh <= SCHABLON[0].max ? "upp till " + SCHABLON[0].max : (grupp === SCHABLON.length - 1 ? "fler än 70" : (SCHABLON[grupp - 1].max + 1) + " till " + SCHABLON[grupp].max);
      kvSumma.textContent = "Ungefär " + tot + " kärl för " + spann + " lägenheter. Vi anpassar storlekar och intervall efter hur snabbt kärlen fylls.";
    }
    kvLgh.addEventListener("input", kvRita);
    kvRita();
  }

  /* ---------- Före och efter-reglage ---------- */
  document.querySelectorAll("[data-foreefter]").forEach(function (box) {
    var inp = box.querySelector("input[type=range]"), bilder = box.querySelector(".foreefter__bilder");
    function satt(v) {
      v = Math.max(0, Math.min(100, v));
      box.style.setProperty("--pos", v + "%");
      box.style.setProperty("--andel", (v / 100) || 0.0001);
      inp.value = v;
    }
    inp.addEventListener("input", function () { satt(parseFloat(inp.value)); });
    var drar = false;
    function fran(e) {
      var r = bilder.getBoundingClientRect();
      satt((e.clientX - r.left) / r.width * 100);
    }
    bilder.addEventListener("pointerdown", function (e) { drar = true; bilder.setPointerCapture(e.pointerId); fran(e); });
    bilder.addEventListener("pointermove", function (e) { if (drar) fran(e); });
    bilder.addEventListener("pointerup", function () { drar = false; });
    bilder.addEventListener("pointercancel", function () { drar = false; });
    satt(50);
  });

  /* ---------- Rullande citat ---------- */
  document.querySelectorAll("[data-citat]").forEach(function (band) {
    var kort = band.querySelectorAll(".citat__kort"), prickar = band.querySelectorAll(".citat__prickar button");
    var i = 0, timer;
    function visa(n) {
      i = (n + kort.length) % kort.length;
      kort.forEach(function (k, j) { k.classList.toggle("ar-aktiv", j === i); });
      prickar.forEach(function (p, j) { p.classList.toggle("ar-aktiv", j === i); p.setAttribute("aria-selected", j === i ? "true" : "false"); });
    }
    function starta() { clearInterval(timer); if (!mindreRorelse) timer = setInterval(function () { visa(i + 1); }, 6000); }
    prickar.forEach(function (p, j) { p.addEventListener("click", function () { visa(j); starta(); }); });
    band.addEventListener("mouseenter", function () { clearInterval(timer); });
    band.addEventListener("mouseleave", starta);
    visa(0); starta();
  });

  /* ---------- Förvald tjänst via länk ?tjanst=... ---------- */
  var m = location.search.match(/[?&]tjanst=([^&]+)/);
  if (m) {
    var sel = document.getElementById("tjanst");
    if (sel) sel.value = decodeURIComponent(m[1]);
  }
})();
