# TabBar

The phone navigation (≤760px): a floating glass bar of five destinations at the bottom, the current one on a solid teal pill that slides.

**Provide** `nav.tabbar.glass` > `<span class="tabbar__pill">` + five links (icon + 11px label), the current with `aria-current="page"`. Halvo's CSS fixes it 10px from the sides and bottom (plus the safe-area inset) below 761px and hides it above; put `tabbar-space` on the page container so the last content clears it. Call `Halvo.motion.pill(pill, current, {radius: 18})`, again without animation on resize. The fifth slot is "More" and opens the all-pages sheet.

- Bar: radius 26, padding 6, five equal columns. Items 54px (44 in landscape), radius 18, `fs-2xs` 600 `muted`; current `accent-ink` on `accent`.
- It replaces the sidebar below 761px (`.side` hides itself there); the top bar keeps search and the profile.
- Motion: on load it slides up 90px (0.7s `expo.out`); the pill moves like the tabs pill.
