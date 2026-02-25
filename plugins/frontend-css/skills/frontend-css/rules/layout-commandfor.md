---
title: Modal Controls Without onclick Handlers
impact: MEDIUM
impactDescription: declarative dialog and popover control without inline JavaScript
tags: layout, commandfor, command, dialog, popover, onclick
browser: 72%
---

## Modal Controls Without onclick Handlers

Opening a `<dialog>` or toggling a `[popover]` traditionally requires inline `onclick` handlers or `addEventListener` calls. The `commandfor` and `command` attributes let you declaratively wire a button to a target element's built-in actions — no JavaScript, no query selectors, no event delegation.

**Avoid (onclick with querySelector):**

```html
<button onclick="document.querySelector('#dlg').showModal()">Open</button>
<dialog id="dlg">
  <p>Dialog content</p>
  <button onclick="this.closest('dialog').close()">Close</button>
</dialog>
```

Or with event listeners:

```js
openBtn.addEventListener('click', () => dialog.showModal());
closeBtn.addEventListener('click', () => dialog.close());
```

**Prefer (declarative `commandfor` + `command`):**

```html
<button commandfor="dlg" command="show-modal">Open</button>

<dialog id="dlg">
  <p>Dialog content</p>
  <button commandfor="dlg" command="close">Close</button>
</dialog>
```

Zero JavaScript. The browser connects the button to the target element and invokes the specified command on click.

### Available commands

| Target element | Command          | Equivalent JS        |
| -------------- | ---------------- | -------------------- |
| `<dialog>`     | `show-modal`     | `dialog.showModal()` |
| `<dialog>`     | `close`          | `dialog.close()`     |
| `<dialog>`     | `show`           | `dialog.show()`      |
| `[popover]`    | `toggle-popover` | `el.togglePopover()` |
| `[popover]`    | `show-popover`   | `el.showPopover()`   |
| `[popover]`    | `hide-popover`   | `el.hidePopover()`   |

### Multiple triggers for the same target

```html
<button commandfor="settings" command="show-modal">⚙️ Settings</button>
<button commandfor="settings" command="show-modal">Open Settings</button>

<dialog id="settings">
  <h2>Settings</h2>
  <!-- content -->
  <button commandfor="settings" command="close">Done</button>
</dialog>
```

### Combined with popover

```html
<button commandfor="confirm" command="show-modal">Delete Account</button>

<dialog id="confirm">
  <p>Are you sure?</p>
  <button commandfor="confirm" command="close">Cancel</button>
  <button type="submit" form="delete-form">Confirm</button>
</dialog>
```

`commandfor` is the successor to `popovertarget` for dialogs, and generalizes the pattern of declaratively connecting a trigger button to a target element's action. The `command` event also fires on the target, allowing custom logic without replacing the declarative wiring:

```js
dialog.addEventListener('command', (e) => {
  if (e.command === 'close') {
    // run cleanup before the browser closes the dialog
  }
});
```

🟡 Newly available (~72%). Supported in Chromium and Firefox. Use `onclick` as a fallback for Safari until support lands.

Reference: [modern-css.com](https://modern-css.com) · [MDN — commandfor attribute](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/button#commandfor)
