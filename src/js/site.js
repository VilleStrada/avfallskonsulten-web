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

  /* ---------- Förvald tjänst via länk ?tjanst=... ---------- */
  var m = location.search.match(/[?&]tjanst=([^&]+)/);
  if (m) {
    var sel = document.getElementById("tjanst");
    if (sel) sel.value = decodeURIComponent(m[1]);
  }
})();
