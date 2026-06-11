# Chrome Web Store listing — Subject Guard for Gmail

Copy/paste into the Web Store Developer Dashboard. Field names match the dashboard.

---

## Item name
```
Subject Guard for Gmail
```
> Note: the extension's own name/description are localized via `src/_locales/`
> (chrome.i18n), so `chrome://extensions` and the store show translated names
> automatically.
>
> This file is the **English master + dashboard field guide**. Fully localized
> per-language listing copy (summary + detailed description for all 13
> languages) is generated into **`store/listings/<lang>.md`** — paste each into
> the matching language under the dashboard's "Store listing" → language
> selector. Edit the copy in `tools/listings.json`, not in the generated files.

## Summary (short description — max 132 characters)
```
Stops you from sending Gmail messages without a subject. No pop-ups, no settings — it just won't send until you add one.
```
(118 characters)

## Category
```
Productivity
```

## Language
```
English (United States)
```

---

## Detailed description

```
Ever fired off an email and then realized — too late — that the subject line was blank? Subject Guard for Gmail makes that impossible.

When you try to send a message with an empty subject, it quietly stops the send. The subject field shakes, turns red, and gets focused, and a small hint appears and fades away on its own. No alert box to dismiss, no dialog to click through — just a gentle nudge to type a subject. Once you do, sending works exactly as normal.

WHAT IT CATCHES
• Clicking the Send button
• The Ctrl+Enter / ⌘+Enter keyboard shortcut
• Pressing Enter or Space while the Send button is focused

DESIGNED TO STAY OUT OF THE WAY
• No settings to configure — install it and it works.
• No pop-ups or alerts you have to close.
• No way to "send anyway" — that's the point. If you want a subject-less email, just remove the extension.
• Inline replies keep working normally (they already have a subject from the thread).

WORKS IN YOUR LANGUAGE
The hint appears in your Gmail's language, with support for English, Spanish, German, French, Portuguese, Italian, Dutch, Russian, Chinese, Japanese, Korean, Arabic, and Hindi (right-to-left languages included).

PRIVACY
Subject Guard for Gmail does not collect, store, or transmit any data. It runs entirely in your browser, only on mail.google.com, and only checks whether the subject field is empty. It makes no network requests and has no servers. Your emails never leave your computer.

Open source and free.
```

---

## Single purpose (required field)

```
Subject Guard for Gmail has one purpose: to prevent the user from sending a Gmail message that has an empty subject line. It detects send actions in Gmail and blocks them while the subject field is blank, prompting the user to add a subject.
```

---

## Permission justifications

The extension declares **no** entries in a `permissions` array. Its only access comes
from a content script matched to a single host. Paste the relevant text into each
justification box the dashboard shows.

### Host permission — `https://mail.google.com/*`
```
The extension's entire function is to guard the Gmail compose window. It injects a content script only on mail.google.com to detect when the user sends a message and to read whether the subject field is empty. This host access is the minimum required to do that and is not used for anything else. No other sites are accessed.
```

### Remote code
```
None. All code is bundled in the extension package. The extension loads no remote scripts and makes no network requests.
```

---

## Data usage disclosures (Privacy practices tab)

Answer the certification checkboxes as follows:

- **What user data do you collect?** — None. Do not check any data-type boxes
  (no personally identifiable info, no authentication info, no personal
  communications, no web history, no user activity, no website content).
- **I do not sell or transfer user data to third parties** — ✓ certify
- **I do not use or transfer user data for purposes unrelated to the item's single purpose** — ✓ certify
- **I do not use or transfer user data to determine creditworthiness or for lending** — ✓ certify

Because no data is collected, a privacy policy URL is not strictly required, but
providing one speeds review. A ready-to-host policy is below.

---

## Privacy policy (host at https://nann.in/gmail-subject-guard/privacy)

```
Privacy Policy — Subject Guard for Gmail

Last updated: 11 June 2026

Subject Guard for Gmail does not collect, store, transmit, sell, or share any
personal data or user data of any kind.

The extension runs entirely within your browser on mail.google.com. Its only
action is to check whether the subject field of a Gmail message you are
composing is empty, and to block the send if it is. It does not read the
content of your emails, your contacts, or any other information. It makes no
network requests and communicates with no external servers.

No data leaves your device. There is nothing to opt out of.

Contact: Johannes Nanninga — https://nann.in/
```

---

## Screenshots

Upload the localized images from `store/`:
`screenshot-en.png` for the default listing, plus the per-language files
(`screenshot-de.png`, `-es`, `-fr`, `-it`, `-ja`, `-ko`, `-nl`, `-pt`, `-ru`,
`-zh`) under each matching store locale. All are 1280×800.
```
```

## Reviewer notes (optional "Notes for reviewer" field)

```
The extension uses a single content script on mail.google.com. It blocks the
send action only when the subject field (input[name="subjectbox"]) is empty,
and shows a non-blocking visual hint. No data is collected and no network
requests are made. Source is available at https://nann.in/ .
```
