// Subject Guard for Gmail
// Blocks the send action (button click and Ctrl/Cmd+Enter) when the subject
// field of the compose window is empty. Instead of an alert, the subject
// field is focused, highlighted and a small auto-dismissing hint is shown.

(() => {
  const FLASH_MS = 2500;
  const RTL_LANGS = new Set(["ar", "he", "fa", "ur"]);

  let hideTimer = null;

  // Pick the hint language from Gmail's own UI language (the language the
  // user is actually reading), falling back to the browser locale and then
  // English. NSG_HINTS is supplied by i18n.js, loaded before this script.
  function currentLang() {
    const raw =
      document.documentElement.getAttribute("lang") ||
      navigator.language ||
      "en";
    return raw.toLowerCase().split("-")[0];
  }

  function hintText() {
    const lang = currentLang();
    return (
      (typeof NSG_HINTS !== "undefined" && (NSG_HINTS[lang] || NSG_HINTS.en)) ||
      "Add a subject before sending"
    );
  }

  // Gmail's send button keeps the locale-independent classes T-I-KE and L3.
  // As a fallback, match the (untranslated) keyboard shortcut in the tooltip.
  function findSendButton(el) {
    if (!(el instanceof Element)) return null;
    const btn = el.closest('[role="button"]');
    if (!btn) return null;
    if (btn.classList.contains("T-I-KE") && btn.classList.contains("L3")) {
      return btn;
    }
    const tip =
      (btn.getAttribute("data-tooltip") || "") +
      " " +
      (btn.getAttribute("aria-label") || "");
    if (/(ctrl|⌘|cmd)\s*[-+]?\s*enter/i.test(tip)) return btn;
    return null;
  }

  // Walk up from the send button / editor until we find the compose
  // container that holds the subject input.
  function findSubjectFor(el) {
    let node = el instanceof Element ? el : null;
    while (node && node !== document.body) {
      const subject = node.querySelector('input[name="subjectbox"]');
      if (subject) return subject;
      node = node.parentElement;
    }
    return null;
  }

  function isVisible(el) {
    return !!el && el.offsetParent !== null;
  }

  // Inline replies have no visible subject field — those must stay sendable.
  function subjectMissing(origin) {
    const subject = findSubjectFor(origin);
    if (!subject || !isVisible(subject)) return null;
    return subject.value.trim() === "" ? subject : null;
  }

  function showHint(subject) {
    let hint = document.querySelector(".nsg-hint");
    if (!hint) {
      hint = document.createElement("div");
      hint.className = "nsg-hint";
      document.body.appendChild(hint);
    }
    hint.textContent = hintText();
    const rtl = RTL_LANGS.has(currentLang());
    hint.dir = rtl ? "rtl" : "ltr";
    const rect = subject.getBoundingClientRect();
    hint.style.top = `${rect.bottom + 6}px`;
    // Anchor to the side the text reads from.
    if (rtl) {
      hint.style.left = "auto";
      hint.style.right = `${window.innerWidth - rect.right}px`;
    } else {
      hint.style.right = "auto";
      hint.style.left = `${rect.left}px`;
    }
    hint.classList.add("nsg-hint-visible");
  }

  function flash(subject) {
    subject.classList.remove("nsg-missing");
    // Restart the shake animation if it is already running.
    void subject.offsetWidth;
    subject.classList.add("nsg-missing");
    subject.focus();
    showHint(subject);

    clearTimeout(hideTimer);
    hideTimer = setTimeout(() => {
      subject.classList.remove("nsg-missing");
      const hint = document.querySelector(".nsg-hint");
      if (hint) hint.classList.remove("nsg-hint-visible");
    }, FLASH_MS);
  }

  function block(event, subject) {
    event.preventDefault();
    event.stopImmediatePropagation();
    flash(subject);
  }

  // Mouse path: Gmail reacts to mouseup/click, intercept both in the
  // capture phase so its own handlers never run.
  for (const type of ["mousedown", "mouseup", "click"]) {
    document.addEventListener(
      type,
      (event) => {
        const btn = findSendButton(event.target);
        if (!btn) return;
        const subject = subjectMissing(btn);
        if (subject) block(event, subject);
      },
      true
    );
  }

  // Keyboard path: Ctrl/Cmd+Enter anywhere in the compose window, or
  // Enter/Space while the send button itself is focused.
  document.addEventListener(
    "keydown",
    (event) => {
      const sendShortcut =
        (event.ctrlKey || event.metaKey) && event.key === "Enter";
      const btn = findSendButton(event.target);
      const buttonActivation =
        btn && (event.key === "Enter" || event.key === " ");
      if (!sendShortcut && !buttonActivation) return;

      const subject = subjectMissing(btn || event.target);
      if (subject) block(event, subject);
    },
    true
  );
})();
