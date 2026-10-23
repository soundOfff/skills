# Visual design antipatterns

A catalog of universal interface antipatterns for the antipattern worker of
`/flow-design-check`. Each entry names an observable failure, how to detect it
in a capture or in the diff, the fix, a grade, and the skills that flag it. The
catalog says nothing about any one design system. Whether a change matches the
repository's own rules is the drift worker's axis.

## How to read an entry

```text
### TY-01 Body text below 16px on mobile
Symptom: what a user or reviewer sees
Detect: the concrete cues, values, and properties that prove it
Fix: the correction
Grade: BLOCKING | MAJOR | POLISH. Sources: the skills that flag it.
```

Ids are stable. Cite them in findings as `TY-01`. Never renumber an entry. A
new entry takes the next number in its category. `BLOCKING` means unusable,
inaccessible, or misleading for some users. `MAJOR` means clearly wrong to a
trained eye and worth fixing before merge. `POLISH` means a craft detail that
never changes a verdict on its own.

Categories overlap on purpose. Contrast appears under color and under
accessibility, and motion safety appears under motion and under accessibility.
Cite the entry whose consequence you observed, and cite one id per defect.

## Categories

| Prefix | Category | Entries |
| --- | --- | --- |
| `HI` | Hierarchy | 29 |
| `LA` | Layout and spacing | 31 |
| `TY` | Typography | 59 |
| `CO` | Color and contrast | 41 |
| `SU` | Surfaces and depth | 30 |
| `IC` | Icons and imagery | 34 |
| `MO` | Motion | 38 |
| `IN` | Interaction and feedback | 44 |
| `ST` | Component states | 26 |
| `FO` | Forms | 42 |
| `NA` | Navigation and information architecture | 51 |
| `CP` | Content and copy | 60 |
| `RE` | Responsive | 39 |
| `AC` | Accessibility | 66 |
| `PE` | Perceived performance | 28 |
| `DA` | Data display | 45 |
| `GE` | Generic AI tells | 37 |
| `CS` | Consistency | 35 |

735 entries in total.

## Sources

The entries were merged on 2026-10-23 from 3063 raw antipatterns extracted
from these skills. A source key in an entry names the skill that flags it.

| Key | Skill | Upstream |
| --- | --- | --- |
| `impeccable` | impeccable, with its 30 reference files | pbakaus/impeccable |
| `design-taste-frontend` | design-taste-frontend | Leonxlnx/taste-skill |
| `minimalist-ui` | minimalist-ui | Leonxlnx/taste-skill |
| `gpt-taste` | gpt-taste | Leonxlnx/taste-skill |
| `redesign-existing-projects` | redesign-existing-projects | Leonxlnx/taste-skill |
| `better-ui` | better-ui | jakubkrehel/skills |
| `better-interface` | better-interface | jakubkrehel/skills |
| `better-accessibility` | better-accessibility | jakubkrehel/skills |
| `better-colors` | better-colors | jakubkrehel/skills |
| `better-layout` | better-layout | jakubkrehel/skills |
| `better-typography` | better-typography | jakubkrehel/skills |
| `better-writing` | better-writing | jakubkrehel/skills |
| `make-interfaces-feel-better` | make-interfaces-feel-better | jakubkrehel/make-interfaces-feel-better |
| `apple-design` | apple-design | emilkowalski/skills |
| `design-review` | design-review, with its checklist | Superfuture/design-review |
| `design-an-interface` | design-an-interface | mattpocock/skills |
| `ui-ux-pro-max` | ui-ux-pro-max, its sibling skills, and its guideline data | nextlevelbuilder/ui-ux-pro-max-skill |
| `frontend-design` | frontend-design | anthropics/claude-plugins-official |
| `design-plugin/<skill>` | accessibility-review, design-critique, design-system, ux-copy, design-handoff | Anthropic design plugin |
| `claude-code-workflows` | the design review agent and principles | OneRedOak/claude-code-workflows |
| `unslop` | unslop, for copy only | cursor/plugins, pstack |
| `deslop` | deslop | cursor/plugins, cursor-team-kit |

## Maintaining the catalog

Add an entry at the end of its category with the next id and the five-line
format above. Merge a duplicate into the older id and add the new sources.
Keep every entry universal: an aesthetic preference belongs in the
repository's design authority, not here. Keep thresholds attributed when
sources disagree. Write straight quotes, no dashes as punctuation, and no
stack-specific tool names, because the kit's validator reads this file.


## Hierarchy (HI)

### HI-01 No single focal point
Symptom: Nothing wins the eye; elements share the same size, weight, and color, so the screen's purpose is not obvious.
Detect: Blur or squint at the capture and no element dominates; similar font-size and font-weight everywhere, weights clustered at 400 to 600 or all at 200 to 300; the key message takes over 2 seconds to find.
Fix: Pick one primary element and two or three secondary ones; mute the rest by size, weight, color, and space.
Grade: MAJOR. Sources: impeccable, apple-design, ui-ux-pro-max, design-review, claude-code-workflows, design-plugin/design-critique.

### HI-02 More than one primary action per view
Symptom: Two or more equally loud buttons compete, so the user cannot tell what the view wants them to do.
Detect: More than one filled or accent-colored button among peers in a view, banner, or header; nav links in the accent at CTA weight; over 1 primary plus 1 to 2 secondary buttons visible, the rest not in a menu.
Fix: Fill exactly one primary action per view; make the others outline, ghost, text, or a menu.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max, design-review, design-plugin/design-critique, better-colors, better-layout.

### HI-03 Everything shown at once with no progressive disclosure
Symptom: Advanced settings, optional fields, and rarely needed details are all visible on first load, overwhelming the user.
Detect: All sections, settings, and optional fields expanded on first render with no accordion, steps, tabs, or "Advanced" toggle; expert controls at the same prominence as primary actions; metadata and secondary stats always visible; dense first-run explanations.
Fix: Show the common path first and reveal advanced options one level deeper when needed.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max.

### HI-04 Too many options at one decision point
Symptom: Users face many simultaneous choices with no recommended one, so they hesitate, misclick, or abandon.
Detect: Count options at one decision point: over 4 is a flag, 5 to 7 strains, 8 or more overloads; undivided lists over 4 items; 10 or more plans or templates ungrouped; identical pricing tiers with no highlighted plan.
Fix: Group, chunk to 4 or fewer, highlight a recommended default, or disclose the rest progressively.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max.

### HI-05 Emphasis spent on too many elements
Symptom: Many headings, buttons, badges, or sections are all big, bold, or dramatic, so none stands out.
Detect: Several font-weight 700 or heavier elements per viewport; uniformly large font-size and padding with no secondary tier; more than one full-bleed, oversized, or animated set piece per page; saturated color on most elements.
Fix: Amplify one hero element and restrain everything else in size, weight, and color.
Grade: MAJOR. Sources: impeccable, frontend-design.

### HI-06 Decoration competing with content
Symptom: Ornaments, glows, badges, and structural lines that encode nothing pull the eye from the content and actions.
Detect: Blobs, glows, gradients, patterns, or illustrations near primary actions or data; borders around every block, dividers between equal items, labels that classify nothing; showpiece effects over an unresolved layout; removing the element loses nothing.
Fix: Cut decoration and structural devices that encode nothing about the content.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max, frontend-design.

### HI-07 Element count too high for the view
Symptom: The screen is dense with equally weighted elements and no breathing room, so the primary task gets lost.
Detect: High element count per view with minimal whitespace; many borders, colors, badges, and icons; several equally weighted sections above the fold; promos, upsells, or notification panels at the primary task's prominence; the same data repeated in header and body.
Fix: Remove or mute everything that is not primary, drop repeats, and add whitespace.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max.

### HI-08 Headings not distinguishable from body
Symptom: A heading, body, and caption cannot be told apart without reading, so the page cannot be scanned.
Detect: Heading font-size or font-weight equal or near body values; 500 against 400 as the only weight difference; headings under 600 (ui-ux-pro-max spec: headings 600 to 700, body 400, labels 500); heading and body colors nearly identical.
Fix: Separate roles with size, weight, color, and space; use bold against regular.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max, design-review, claude-code-workflows, design-plugin/design-critique, redesign-existing-projects, frontend-design.

### HI-09 Hierarchy carried by one dimension
Symptom: Levels differ only in size, or only in color, and still fail to read as distinct.
Detect: Only font-size changes between levels with identical weight, color, and spacing; an oversized H1 over otherwise uniform text; levels differing only in color so a grayscale capture shows no structure; bright color plus bold with no size or spacing difference.
Fix: Combine two or three dimensions per level: size, weight, color, and space above.
Grade: MAJOR. Sources: impeccable, apple-design, design-taste-frontend, ui-ux-pro-max.

### HI-10 Heading too close in size to body
Symptom: Headings are only slightly bigger than body text, so levels do not register and nothing feels dramatic.
Detect: Primary heading to body ratio under 2:1 (impeccable; 3:1 or more is strong, 3x to 5x for display); tier ratios around 1.2 to 1.5; poster-style hero H1 under 5:1 (ui-ux-pro-max); banner headline under 32px (ui-ux-pro-max).
Fix: Push the primary size jump to 3:1 or more and keep intermediate tiers distinct.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max.

### HI-11 Primary content trailing in reading order
Symptom: The identifying title, key number, or main action sits where the eye arrives last, behind metadata.
Detect: Key content or action at the bottom right (LTR) or a dialog's primary action away from its expected slot; timestamps, tags, or buttons leading a row with the title trailing; the primary fact in text-sm after metadata.
Fix: Put identifying content first and large along the reading flow; let metadata and actions trail.
Grade: MAJOR. Sources: impeccable, better-layout, ui-ux-pro-max.

### HI-12 Wrong element emphasized
Symptom: A secondary element is larger, bolder, or brighter than the primary one, so the structure reads inverted.
Detect: Metadata larger or bolder than the title; secondary buttons in the accent color; an h3 larger or heavier than the h2 above it; a heading smaller than its paragraph unless an overline; a decorative element winning the squint test.
Fix: Reassign size, weight, color, and position so emphasis descends with importance.
Grade: MAJOR. Sources: design-review, design-plugin/design-critique, better-typography.

### HI-13 Complex task presented as one undifferentiated screen
Symptom: The user must read, decide, and navigate several things at once instead of one step at a time.
Detect: One form or page with many unrelated sections and no steps; several independent choices (plan, add-ons, billing, seats) on one screen; instructions, choices, and navigation controls mixed in one view; an onboarding step teaching several features or over 3 concepts.
Fix: Break the task into discrete steps so the user makes one decision at a time.
Grade: MAJOR. Sources: impeccable.

### HI-14 Hero stacked with secondary elements
Symptom: The hero carries taglines, trust strips, pricing, features, or avatars and reads as a list, not one moment.
Detect: Over 4 hero text elements (eyebrow or brand strip, headline, subtext, CTAs); both eyebrow and tagline; small text under the CTAs; trust string, logo row, avatars, price string, or check-icon list inside the hero; hero below 60% of the fold.
Fix: Keep headline, subtext, CTAs, and one small element; move everything else below the hero.
Grade: MAJOR. Sources: design-taste-frontend, ui-ux-pro-max.

### HI-15 Hero pushing the primary action below the first viewport
Symptom: The headline and copy push the CTA, navigation, or data below the fold, so the user must scroll to act.
Detect: Hero taller than 100dvh at desktop; CTA not visible at first paint; headline over 2 lines or subtext over 20 words or 3 to 4 lines; a full-height hero on a data-heavy or multi-page app with navigation below the fold.
Fix: Reduce scale or copy until the CTA fits; use a compact header on data-heavy apps.
Grade: MAJOR. Sources: design-taste-frontend, ui-ux-pro-max.

### HI-16 Secondary content ahead of core content on mobile
Symptom: On a phone the user scrolls past promos, filters, sidebars, or metadata before reaching the main content or action.
Detect: At phone widths the desktop sidebar, promos, filters, or metadata stack above the main column; every desktop panel stacked vertically with no tabs or accordions; nothing collapsed or hidden.
Fix: Order core content first on mobile and fold secondary content into tabs or accordions.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max.

### HI-17 Chrome outweighing content
Symptom: Thick toolbars, sidebars, and panels take a large share of the viewport, so the content looks secondary.
Detect: Multiple persistent toolbars, sidebars, or panels around a conversation, gallery, or document; chrome occupying a large share of the viewport; thick borders framing the content area.
Fix: Minimize chrome so the content dominates the view.
Grade: MAJOR. Sources: ui-ux-pro-max.

### HI-18 Destructive action styled or placed like the primary
Symptom: Delete sits beside Save in the same style, so it reads as the main action and one slip destroys data.
Detect: A delete or remove button using the primary fill or a hue close to the accent with no outline or icon distinction; delete and submit buttons side by side with no spatial separation.
Fix: Style destructive actions in the danger color with a distinct treatment and separate them from the primary.
Grade: MAJOR. Sources: ui-ux-pro-max, better-colors.

### HI-19 Accent color spread across the interface
Symptom: The brand color saturates backgrounds, borders, icons, and text, so nothing marked by it stands out.
Detect: Accent exceeding roughly 10% of visual weight; accent on backgrounds, borders, icons, and non-interactive text; the 60-30-10 split broken (60% neutral surfaces, 30% secondary text and borders, 10% accent).
Fix: Reserve the accent for CTAs, highlights, and focus; return everything else to neutrals.
Grade: MAJOR. Sources: impeccable.

### HI-20 Density too low for data-heavy content
Symptom: Oversized type and extreme whitespace leave little room for the products, data rows, or fields the user came for.
Detect: Display-scale typography, single accent, and minimal element count on a catalog, dashboard, form, or complex app; few items visible per viewport; users scroll to see what a denser layout would show at once.
Fix: Use a denser, functional layout for data, commerce, and forms.
Grade: MAJOR. Sources: ui-ux-pro-max.

### HI-21 Hierarchy that collapses in one theme
Symptom: The CTA or heading that pops in light mode disappears in dark mode, or the reverse.
Detect: Compare the primary action and headings across light and dark captures; the element that leads in one theme has low contrast against its surface in the other.
Fix: Give both themes the same emphasis order so whatever pops in light pops in dark.
Grade: MAJOR. Sources: design-taste-frontend.

### HI-22 Primary emphasis on the label instead of the fill
Symptom: The primary action is a neutral button with accent text, so it reads as a link.
Detect: A primary action styled with the accent as color on a neutral or transparent background instead of as the background.
Fix: Put the accent on the button background and keep the label on-accent.
Grade: MAJOR. Sources: better-colors.

### HI-23 Key element crowded by its neighbors
Symptom: The primary element has no surrounding white space, so it does not stand out from what sits beside it.
Detect: The primary element packed tightly against neighbors with no more margin around it than any other element on the screen.
Fix: Surround the primary element with more white space than anything else gets.
Grade: MAJOR. Sources: impeccable.

### HI-24 Field or step order defying user expectations
Symptom: Fields, steps, or content appear in an order that does not match how users think about the task.
Detect: Address before name, payment before cart review, a summary placed after details that depend on it; steps ordered unlike the user's mental model of the task.
Fix: Order fields, steps, and content to match how users think about the task.
Grade: MAJOR. Sources: impeccable.

### HI-25 Headings that do not describe their sections
Symptom: Vague or styling-driven headings produce an outline a screen reader user cannot navigate by.
Detect: Headings reading "Overview" or "Info"; the heading list in the accessibility tree does not describe the page; levels chosen for looks.
Fix: Write headings that describe their sections and form a coherent outline.
Grade: MAJOR. Sources: better-accessibility.

### HI-26 Message roles indistinguishable in a conversation view
Symptom: System and user messages look identical and the composer scrolls out of view.
Detect: Assistant and user messages sharing alignment, background, and type; user messages not aligned to one side; the input not pinned to the viewport.
Fix: Differentiate responses from user messages by alignment and surface; keep the composer pinned.
Grade: MAJOR. Sources: ui-ux-pro-max.

### HI-27 Feature list longer than it can emphasize
Symptom: The features section lists eight or more items, or pads a grid with trivial ones, so nothing is emphasized.
Detect: More than 3 to 5 key features, more than 4 to 6 feature cards, or more than 3 benefit bullets on a minimal page; a 6-card grid padded with trivial features for a simple product.
Fix: Cut to 3 to 5 features with one key message each, or drop the grid.
Grade: POLISH. Sources: ui-ux-pro-max.

### HI-28 Too many hierarchy cues on a simple composition
Symptom: Color and size contrast are piled on where space and weight alone would separate the levels.
Detect: Several simultaneous cues per level, such as size, weight, color, and a background, on a composition with only two or three levels.
Fix: Use the fewest dimensions needed; add color or size only when space and weight fall short.
Grade: POLISH. Sources: impeccable.

### HI-29 Tour spotlight without dimming the rest
Symptom: The highlighted element in a guided tour does not stand out from the page around it.
Detect: A tour step with a tooltip but no backdrop dimming the rest of the page; the target shares the page's full brightness.
Fix: Spotlight the element and dim everything else behind a scrim.
Grade: POLISH. Sources: impeccable.


## Layout and spacing (LA)

### LA-01 Content or controls under system safe areas
Symptom: Headers, tab bars, buttons or content sit under the status bar, notch or home indicator, so taps misfire.
Detect: Fixed bars or controls at `top: 0` or `bottom: 0` with no `env(safe-area-inset-*)`, SafeAreaView or inset padding; overlap on a notched device capture; key banner content outside the central 70 to 80 percent of the canvas.
Fix: Inset every fixed bar, control and key element by the safe-area insets or the platform's safe zone.
Grade: BLOCKING. Sources: ui-ux-pro-max, impeccable, better-layout.

### LA-02 Focus or anchor target scrolling under sticky chrome
Symptom: Tabbing or jumping to an anchor scrolls the focused control or heading fully behind a sticky header or footer.
Detect: `position: sticky` or `fixed` header, footer or cookie banner with no `scroll-padding-top` or `scroll-padding-bottom` on the scroller; `id` anchor targets without `scroll-margin-top`; Tab through the page and watch focus vanish (WCAG 2.4.11).
Fix: Pad the scroller by each sticky bar's height with `scroll-padding-top` or `scroll-padding-bottom`, and give anchor targets `scroll-margin-top`.
Grade: BLOCKING. Sources: better-accessibility, ui-ux-pro-max, better-layout.

### LA-03 Primary action pushed out of reach
Symptom: The primary button sits below the viewport, under the on-screen keyboard or in a pane that clips it.
Detect: Dialog without `max-height: 100dvh` or with its action row inside the scrolling region; primary button absolutely positioned, in a fixed-height area, or at the bottom of scrolling content instead of stable chrome.
Fix: Keep primary actions in normal flow or sticky chrome; cap dialogs at `100dvh` with a scrolling body and fixed footer.
Grade: BLOCKING. Sources: better-layout, impeccable.

### LA-04 Spacing that does not encode grouping
Symptom: Related items sit as far apart as unrelated ones; one gap everywhere, so nothing reads as a group.
Detect: Label-to-field gap equal to field-to-field gap; between-group gap under twice the within-group gap, or under 24px between unrelated control groups; one spacing value on every section; a heading's explainer or a control placed far from what it belongs to.
Fix: Use 8 to 12px inside groups, at least twice that between groups, and place controls beside what they affect.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max, better-layout, design-review, apple-design, design-taste-frontend.

### LA-05 Spacing values off the scale
Symptom: Padding, margins and gaps use arbitrary values, so nothing lines up and the rhythm feels random.
Detect: Literals such as `13px`, `18px`, `22px`, `27px`, `35px`, `mt-[37px]` or `p-[13px]` that are not multiples of 4; vertical gaps that are not multiples of the body line-height unit (24px for `16px/1.5`, impeccable).
Fix: Snap every value to one 4pt scale (4, 8, 12, 16, 24, 32, 48, 64, 96px) or its tokens.
Grade: MAJOR. Sources: impeccable, design-taste-frontend, ui-ux-pro-max, design-review, claude-code-workflows, design-plugin/design-system.

### LA-06 Inconsistent spacing between equivalent elements
Symptom: Two sections or siblings at the same level are separated by different amounts, so the layout looks sloppy.
Detect: Section gaps of 24px here and 40px there; 12px, 14px and 16px margins around one component type; `padding-top` differing from `padding-bottom` without optical reason; conflicting padding rules on one element; per-child `margin-bottom` with last-child overrides instead of `gap`.
Fix: Define spacing tiers by hierarchy (16, 24, 32, 48px), apply each tier consistently, and space siblings with `gap`.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max, design-review, frontend-design, better-layout, design-plugin/design-critique.

### LA-07 Edges not on shared alignment lines
Symptom: Left edges of headings, text, icons and controls in one column start at several different x positions.
Detect: Edges off by 1 to 8px under a grid overlay on the capture; differing `padding-inline-start` across stacked siblings (20px, 14px, 24px); an icon 2px off the text edge; nesting indents that are not one spacing step (16px) per level.
Fix: Snap everything to a few shared edges with one indent step per level; make deliberate offsets large enough to read.
Grade: MAJOR. Sources: impeccable, design-review, claude-code-workflows, better-layout.

### LA-08 Tap targets packed too close
Symptom: Adjacent buttons or icon controls touch or nearly touch, so fingers hit the wrong one and glyphs merge.
Detect: `gap-0` or `gap-1` between sibling controls; under 8px between targets (ui-ux-pro-max); under 12px between bordered controls or 24px between borderless glyphs (better-layout); 20px targets closer than 4px (better-accessibility); touch rows under 44pt.
Fix: Space targets by at least 8px, 12px for bordered and 24px for borderless controls; keep touch rows 44pt tall.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max, better-accessibility, better-layout.

### LA-09 Structure changing between sections or screens
Symptom: Column grid, container width or alignment differs between sections or equivalent screens, so the layout seems to shift.
Detect: Different `max-w-*` or `maxWidth` per route; widths and gutters improvised per page with no column grid; `text-align: center` on some sections and left on others; slide content alignment varying slide to slide.
Fix: Use one responsive column grid, one container width per device class and one alignment rule throughout.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max, claude-code-workflows.

### LA-10 Cramped layout with no breathing room
Symptom: Sections and groups run into each other; elements crowd or touch and nothing breathes.
Detect: Gaps between distinct groups no larger than gaps inside them; tight card and section padding; marketing section padding under 96px (minimalist-ui), under 128px (gpt-taste) or in the 20 to 40px range (impeccable).
Fix: Widen separation between groups and sections; marketing sections get 96px or more, up to 200px on brand surfaces.
Grade: MAJOR. Sources: impeccable, minimalist-ui, gpt-taste, claude-code-workflows.

### LA-11 Density mismatched to content and input
Symptom: Touch screens or marketing pages are as dense as data tables, or dashboards are as airy as brochures.
Detect: Rows or tap targets under 44px on a touch-first screen; marketing section padding under 48px; huge padding on a data-dense admin table; a diff loosening one toolbar beyond the product's established density.
Fix: Make touch and marketing surfaces roomier and data views tighter, and preserve an established working density.
Grade: MAJOR. Sources: impeccable, design-taste-frontend, design-review, redesign-existing-projects, better-layout.

### LA-12 Whitespace that frames nothing
Symptom: Empty space appears where content ran out while the focal element is cramped; large gaps separate nothing.
Detect: Uneven margins around the hero or CTA; tight padding on the most important block with empty corners elsewhere; hero top padding above 96px (`pt-24`) leaving content floating mid-viewport; sparse screens where content is lost.
Fix: Allocate generous, deliberate space around focal elements and tighten space that guides nothing.
Grade: MAJOR. Sources: impeccable, design-taste-frontend, design-review, design-plugin/design-critique.

### LA-13 Identical tiles repeated in a grid
Symptom: Six or more equal cards with the same icon, heading and text structure fill a section with no emphasis.
Detect: `grid-cols-3` or similar of uniform icon-heading-paragraph cards; 6 or more equal tiles (impeccable) or more than 5 cards (gpt-taste); identical rows repeated with the same column order and tile size.
Fix: Cut to 3 to 5 tiles or vary their size, structure and content treatment; otherwise drop the grid.
Grade: MAJOR. Sources: impeccable, design-taste-frontend, gpt-taste.

### LA-14 No max-width on wide screens
Symptom: Content and text stretch edge to edge on wide monitors, producing very long lines and loose compositions.
Detect: No `max-width` wrapper with auto margins around page content; width still scaling past 1440px; paragraphs without `max-w-prose` or `max-width: 65ch` to `75ch`.
Fix: Contain the page at 1200 to 1440px (`max-w-7xl mx-auto`) and text at 65 to 75 characters.
Grade: MAJOR. Sources: impeccable, design-taste-frontend, ui-ux-pro-max, redesign-existing-projects.

### LA-15 Content hidden under a fixed bar
Symptom: The first heading or last list items sit under a fixed header, tab bar, cookie banner or chat widget.
Detect: `position: fixed` or `sticky` bars with no matching `padding-top` or `padding-bottom` on the body or scroll container (an `h-20` nav without `pt-20`); several fixed elements with uncoordinated offsets overlapping each other.
Fix: Reserve content insets equal to each fixed bar's height plus safe areas, and offset stacked fixed elements from each other.
Grade: MAJOR. Sources: ui-ux-pro-max.

### LA-16 Same section shape repeated down the page
Symptom: Every section uses the same template, so the page has one rhythm and no moment of emphasis.
Detect: Heading, paragraph and grid stacked repeatedly; a layout family (3-column cards, split text and image, full-width quote) used twice; a third consecutive image-text split; fewer than 4 families across 8 sections.
Fix: Alternate structures and spacing; cap zigzag splits at two in a row and use each family once.
Grade: MAJOR. Sources: impeccable, design-taste-frontend.

### LA-17 Shared elements misaligned across sibling cards
Symptom: Titles, prices, feature lists or buttons in adjacent cards sit at different heights, so the row looks broken.
Detect: Shared elements across columns at differing Y positions in the capture; variable-height title or price blocks above lists; card buttons without `margin-top: auto` in a flex column; no subgrid or fixed rows.
Fix: Align shared elements across the row with subgrid or fixed-height blocks and pin buttons to the card bottom.
Grade: MAJOR. Sources: redesign-existing-projects.

### LA-18 Controls or text flush to the viewport edge
Symptom: A full-width button or text runs to the screen edge, reads as system chrome and clips against curved corners.
Detect: Interactive elements or text at `0` from the viewport edge with no layout margin; full-width buttons with under 16px inline inset on mobile; `position: fixed; bottom: 0; width: 100vw` buttons with no safe-area bottom padding.
Fix: Let only backgrounds and media bleed; inset controls and text with `padding-inline: 16px` and `padding-bottom: calc(16px + env(safe-area-inset-bottom))`.
Grade: MAJOR. Sources: better-layout.

### LA-19 Wrong stacking order
Symptom: A dropdown, toast or modal renders under a sticky header or a sibling despite a huge z-index.
Detect: Scattered `z-index` literals (999, 9999, 100000) with no scale; a parent with `transform`, `opacity` below 1, `filter` or position plus `z-index` creating a stacking context that traps the child.
Fix: Assign layers from one z-index scale (10, 20, 30, 50) and manage stacking at the parent that creates the context.
Grade: MAJOR. Sources: ui-ux-pro-max.

### LA-20 Content clipped by its container
Symptom: Text, descenders, focus rings, shadows or dropdowns are cut off at a container edge, especially at larger text sizes.
Detect: `overflow: hidden` on containers holding dynamic text or popovers; `height` instead of `min-height` on text containers; truncated content without an ellipsis in the capture, or at 200 percent zoom.
Fix: Give text containers `min-height`, use `overflow: auto` where needed, and clip only after verifying content fits.
Grade: MAJOR. Sources: ui-ux-pro-max, better-accessibility, impeccable, design-plugin/design-handoff.

### LA-21 Empty cell in a grid
Symptom: A blank tile or dead void sits in the middle or at the end of a grid.
Detect: Grid cell count not equal to item count; a placeholder `div` with background only; `col-span` or `row-span` values that do not interlock; no `grid-auto-flow: dense`.
Fix: Reshape the grid so N items fill N cells (1+2, 2+3, hero+4) and never paste a blank tile.
Grade: MAJOR. Sources: design-taste-frontend, gpt-taste.

### LA-22 Flex or grid child overflowing its track
Symptom: A long word or wide child pushes a flex or grid item past its column.
Detect: Flex or grid children without `min-width: 0` (and `min-height: 0` for grid); content wider than its track in the capture.
Fix: Set `min-width: 0` on flex items and `min-width: 0; min-height: 0` on grid items.
Grade: MAJOR. Sources: impeccable.

### LA-23 Nested scroll region trapping the main scroll
Symptom: A scrollable panel inside the page captures the wheel or finger, and users get stuck mid-page.
Detect: `overflow: auto` containers inside the main scroll on the same axis; a scroll view nested in a scroll view; scroll-jacking.
Fix: Remove nested same-axis scroll regions and let the page scroll as one.
Grade: MAJOR. Sources: ui-ux-pro-max.

### LA-24 Lines and boxes where space would carry the grouping
Symptom: Dividers, borders or card boxes separate content that spacing already separates, adding clutter.
Detect: `hr` or `border-b` inside a gap already twice the within-group gap; wrapper borders, backgrounds or shadows around single headings, paragraphs, controls or accordion items; stacked dividers; separators heavier than a hairline or in a strong color.
Fix: Let space carry the grouping; delete redundant lines and keep any needed separator a low-contrast hairline.
Grade: POLISH. Sources: impeccable, better-interface, make-interfaces-feel-better, minimalist-ui, better-layout.

### LA-25 Centered symmetric default on every section
Symptom: Every heading, paragraph and block is centered and mirror-symmetric, so nothing is emphasized and the page reads as a template.
Detect: `text-align: center` and `mx-auto` on every section including body paragraphs and lists; centered hero stack over three equal columns; 50/50 splits by default; no section left-aligned, asymmetric or breaking the container.
Fix: Left-align text blocks, center only short deliberate headline stacks, and vary alignment or proportion for emphasis.
Grade: POLISH. Sources: impeccable, design-taste-frontend, redesign-existing-projects, frontend-design.

### LA-26 Optical misalignment despite exact math
Symptom: Icons, play triangles, headings and padding are mathematically centered or equal yet look off-center or lopsided.
Detect: Play icon left-heavy in its circle; icon baseline not matching text; a large heading at `margin-left: 0` looking inset by its side-bearing; equal `padding-inline` on a text-plus-icon button pushing the icon out; identical top and bottom section padding reading top-heavy.
Fix: Nudge 1 to 2px (or `-0.05em` on headings) and give the icon side 2px less padding than the text side.
Grade: POLISH. Sources: impeccable, better-ui, make-interfaces-feel-better, redesign-existing-projects.

### LA-27 Layout structure mismatched to content or viewport
Symptom: Content is forced into a grid or narrow columns it does not suit, or desktop width goes unused behind accordions.
Detect: Tables or long text inside rounded bento cards; editorial asymmetry on dashboards or catalogs; multi-cell grids for content that reads as one column; cramped narrow columns on wide viewports; accordions hiding content at 1024px and up.
Fix: Match the structure to the content: single column for reading, grids for scannable blocks, more visible columns on desktop.
Grade: POLISH. Sources: impeccable, ui-ux-pro-max.

### LA-28 Image hairline drawn with a border
Symptom: An image's hairline adds width and height or sits outside the corner radius.
Detect: `border: 1px` on `img`, or `outline` without `outline-offset: -1px`; the image's rendered size differing from its declared size.
Fix: Use `outline: 1px solid` with `outline-offset: -1px` so the ring hugs the radius without affecting layout.
Grade: POLISH. Sources: better-ui, make-interfaces-feel-better.

### LA-29 Columns built from percentage math
Symptom: Hand-computed column widths wrap unexpectedly or leave uneven gutters at some viewport sizes.
Detect: `flex-basis: 33.333%` or `w-[calc(33%-1rem)]` on flex children with `calc()` gap compensation instead of a grid.
Fix: Build multi-column structure with CSS Grid (`grid-cols-1 md:grid-cols-3 gap-6`).
Grade: POLISH. Sources: design-taste-frontend, redesign-existing-projects.

### LA-30 Short cards stretched to the tallest
Symptom: Cards with little content carry awkward empty space to match the tallest card in the row.
Detect: Default `align-items: stretch` on card rows whose content length varies widely; large empty bottoms in the capture.
Fix: Allow variable heights or use a masonry layout when content length varies.
Grade: POLISH. Sources: redesign-existing-projects.

### LA-31 Snapped scroller misaligned with the page edge
Symptom: Snapped carousel items land against the padding edge instead of the content edge, out of line with the page.
Detect: `scroll-snap-type` with `padding-inline` but no matching `scroll-padding-inline`.
Fix: Set `scroll-padding-inline` equal to the scroller's padding.
Grade: POLISH. Sources: better-layout.


## Typography (TY)

### TY-01 Text rendered as an image without its exact words
Symptom: A banner or label is a picture of text, and screen readers get a paraphrase or nothing.
Detect: An img whose pixels contain words carries an alt that omits or paraphrases them, or the words could have been real text.
Fix: Use real text, or put the exact words in the alt attribute.
Grade: BLOCKING. Sources: better-accessibility, impeccable, better-typography, ui-ux-pro-max.

### TY-02 Body text measure outside the readable band
Symptom: Paragraphs run edge to edge or sit in a choppy narrow column, so the eye loses the line.
Detect: Count characters per line in the capture: over 75 (impeccable, ui-ux-pro-max, design-review, better-typography), over 80 (frontend-design), under 45 (impeccable, design-review) or outside 35 to 60 on mobile (ui-ux-pro-max), often from a container without a ch max-width.
Fix: Cap prose containers at about 65ch and recheck the cap whenever the body font size changes.
Grade: MAJOR. Sources: impeccable, design-taste-frontend, minimalist-ui, ui-ux-pro-max, design-review, redesign-existing-projects, frontend-design, better-typography.

### TY-03 Font sizes off the type scale
Symptom: Sizes such as 13px, 15px and 17px coexist, and similar elements differ by a pixel or two.
Detect: Look for font-size literals or utilities such as text-[15px] off the scale, more than 5 to 7 distinct sizes in a view, adjacent sizes 1 to 2px apart, and hard-coded sizes or families instead of typography tokens or platform styles.
Fix: Define one scale of 5 to 7 steps on a committed ratio and use only its tokens.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max, design-review, claude-code-workflows, better-typography, design-plugin/design-system, frontend-design.

### TY-04 Body line height outside 1.5 to 1.7
Symptom: Paragraph lines collide or float apart, and wrapped descriptions become a dense block.
Detect: The body line-height is under 1.5 (impeccable, ui-ux-pro-max, claude-code-workflows, better-typography), under 1.6 (minimalist-ui), under 1.4 (design-review, design-plugin/design-critique), or above 1.7 (impeccable) or 1.75 (ui-ux-pro-max); leading-tight or leading-none sits on card text that wraps to three lines (better-typography, floor 1.4).
Fix: Set body copy between 1.5 and 1.7 and give anything that wraps at least 1.4.
Grade: MAJOR. Sources: impeccable, minimalist-ui, ui-ux-pro-max, design-review, claude-code-workflows, design-plugin/design-critique, better-typography.

### TY-05 Body text under 16px
Symptom: Long-form copy is smaller than the browser default and hard to read on phones; iOS zooms inputs on focus.
Detect: Body or input font-size is under 16px, including text-sm, at mobile widths or in long-form copy with no named reason such as a small-running face or a dense professional tool; under 18px on senior-care products (ui-ux-pro-max).
Fix: Start body copy and inputs at 16px, or 18px for senior audiences.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max, better-typography, design-plugin/design-critique.

### TY-06 Small UI text under the size floor
Symptom: Captions, labels and table cells are illegible, especially on phones.
Detect: The computed font-size is under 12px, such as text-[10px] (ui-ux-pro-max, better-typography), under 14px at mobile widths where text-xs fails (impeccable), or under 14px on inputs and menus and 13px on captions (better-typography).
Fix: Keep readable text at 12px or more, 14px on mobile, and inputs and menus at 14px.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max, better-typography, claude-code-workflows.

### TY-07 Too many font families
Symptom: Several typefaces compete on one page and no family carries a clear role.
Detect: Count distinct font-family values, excluding monospace for code: more than 2 (design-review, ui-ux-pro-max), more than 2 to 3 (impeccable), or more than 3 in an application (better-typography); a distilled UI wants one (impeccable).
Fix: Limit the product to two families, or one family in several weights.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max, design-review, better-typography.

### TY-08 Typeface chosen by default
Symptom: The whole UI is set in the framework default and looks like every other product.
Detect: The only face is Inter, Roboto, Arial, Helvetica, system-ui or a bare sans-serif, with no pairing and no stated rationale; or a custom web font replaces system-ui for no reason and loses its optical tuning (apple-design).
Fix: Choose the typeface deliberately for the product's register, whether that is a web font or the system stack.
Grade: MAJOR. Sources: impeccable, redesign-existing-projects, frontend-design, ui-ux-pro-max, apple-design.

### TY-09 Display, script or decorative face on reading or functional text
Symptom: Paragraphs, labels, buttons, prices or legal text are set in a face built for headlines, and reading tires.
Detect: A display, condensed, pixel, script or handwritten family (Bebas Neue, Abril Fatface, Press Start 2P, Caveat, Kalam) sits on p, label, button, table cells, figures or text under 16px; extreme tracking or busy imagery sits behind body copy.
Fix: Reserve decorative faces for large headlines and accents, and set body, labels and data in a text face.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max, better-typography.

### TY-10 Font pairing without clear contrast
Symptom: Two typefaces look almost alike, or a second face appears for one word, so the pairing reads as a mistake.
Detect: Two sans families of one classification (Inter with Manrope) share the stack; a second @font-face is used only where a primary weight would do; heading and body moods clash; a lone italic serif word sits in a sans h1.
Fix: Use one family in several weights, or pair faces that contrast in classification, and emphasize within the family.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max, frontend-design, better-typography, design-taste-frontend.

### TY-11 Heading line height not tightened
Symptom: Multi-line headings have loose, gappy lines and display text floats apart.
Detect: Headings over about 32px carry line-height above 1.2 (design-review, impeccable), above 1.3 on display sizes (redesign-existing-projects), or the body value of 1.5 on an h1; targets are 1.05 (apple-design), 1.1 (better-typography, minimalist-ui) or 1.2 to 1.3 for subheadings (better-typography).
Fix: Set display text near 1.1 and subheadings at 1.2 to 1.3, unitless.
Grade: MAJOR. Sources: impeccable, apple-design, minimalist-ui, design-review, better-typography, redesign-existing-projects.

### TY-12 Same text role at different sizes, weights or leading
Symptom: Card titles or captions appear at one size and weight here and another there.
Detect: The same role or component class carries a different font-size, font-weight (500 here, 600 or 700 there) or line-height across screens; a title at 1.5rem carries body leading, or body text carries weight 600.
Fix: Give each role one size, line-height and weight, and reuse that pairing everywhere.
Grade: MAJOR. Sources: impeccable, design-review, better-typography.

### TY-13 Typeface mismatched to the product register
Symptom: A playful product wears a corporate face, a data tool wears a serif, or a non-technical brand wears monospace.
Detect: A serif display or body face sits on dashboards or developer tools with no brand rationale; monospace sits on non-code body or headings; a bubbly rounded face is chosen because the audience is children; the personality contradicts the brand.
Fix: Pick a face whose personality fits the register; one tuned sans usually carries product UI, with monospace reserved for code.
Grade: MAJOR. Sources: impeccable, design-taste-frontend.

### TY-14 Fluid or oversized type in dense product UI and body copy
Symptom: Headings in an app shell resize with the viewport, an h1 shrinks inside a sidebar, and dense screens feel jumpy.
Detect: clamp() or vw font-size appears in app shells, dashboards or data-dense views, or on p and body on content pages; step ratios exceed 1.2 in product UI; a huge display heading sits beside tiny body on a tool surface.
Fix: Use a fixed rem scale with 1.125 to 1.2 steps in product UI and reserve clamp() for marketing headings.
Grade: MAJOR. Sources: impeccable.

### TY-15 Fluid size with no rem offset
Symptom: Fluid headings shrink toward nothing on small screens.
Detect: The preferred clamp() term is a bare viewport unit such as 5vw with no added rem term such as 5vw + 1rem.
Fix: Add a rem offset to the preferred value so the size never collapses.
Grade: MAJOR. Sources: impeccable.

### TY-16 Hero headline wrapping past three lines
Symptom: A large hero headline wraps to four or more lines and becomes a text wall beside its asset.
Detect: text-7xl or text-8xl sits on a headline longer than five words; an h1 sits inside max-w-2xl or max-w-3xl; the capture shows more than three rendered lines.
Fix: Size the hero at text-4xl to text-6xl, widen its container, and keep it to two or three lines.
Grade: MAJOR. Sources: design-taste-frontend, gpt-taste.

### TY-17 Text invisible or shifting while web fonts load
Symptom: Headings are blank for a moment on first load, then snap in and reflow the page.
Detect: @font-face lacks font-display: swap or optional; no size-adjust or metric-matched fallback is set; the capture shows reflow when the web font arrives; many weight files load with no unicode-range subsetting and delay the swap.
Fix: Add font-display: swap or optional, a metric-matched fallback with size-adjust, and preload and subset critical fonts.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max, design-taste-frontend.

### TY-18 Web font with no fallback stack
Symptom: When the web font fails, text falls to a browser default with mismatched metrics and the layout shifts.
Detect: A font-family stack names only the web font, such as "Helvetica Now" with no "Helvetica Neue", Arial, sans-serif after it; a fallback's x-height visibly differs from the primary at the same size.
Fix: Give every face a fallback stack, ideally metric-matched for x-height.
Grade: MAJOR. Sources: impeccable, better-typography.

### TY-19 Thin weight at small sizes
Symptom: Text under 18px set light breaks up, and light text on a soft low-contrast surface disappears.
Detect: font-weight under 400, font-thin, font-extralight or font-light sits on text smaller than 18px; weights under 300 or italic sit on neumorphic or low-contrast surfaces.
Fix: Use 400 or heavier below 18px and reserve 100 to 300 for 28px and up, checked against the background.
Grade: MAJOR. Sources: better-typography, ui-ux-pro-max, claude-code-workflows.

### TY-20 Synthesized bold or italic
Symptom: Bold or italic text looks smeared or distorted because the browser fakes it.
Detect: font-weight or font-style values have no matching weight or style among the loaded @font-face files.
Fix: Load every face the design uses, or use a weight the family ships.
Grade: MAJOR. Sources: better-typography.

### TY-21 Font synthesis disabled on interface text
Symptom: Bold and italic emphasis silently vanishes when a fallback font renders.
Detect: font-synthesis: none sits on body or interface text rather than on an isolated verified treatment such as a wordmark.
Fix: Scope it to the isolated treatment, or set only the unwanted longhand after checking fallbacks.
Grade: MAJOR. Sources: better-typography.

### TY-22 Raw axis or feature tag where a CSS property exists
Symptom: A heading drops to regular weight on a fallback font, or tabular figures stop working when another feature is set.
Detect: font-variation-settings carries "wght"; font-feature-settings carries "tnum" or "zero" where font-variant-numeric would do.
Fix: Use font-weight and font-variant-numeric; keep raw tags for custom axes such as "GRAD" and niche features such as "ss01".
Grade: MAJOR. Sources: better-typography.

### TY-23 Line height with a unit
Symptom: A fixed 24px line height stays put when the font size changes, so larger text overlaps and smaller text floats.
Detect: line-height is set in px or rem, or through Tailwind leading-[24px].
Fix: Use a unitless line-height.
Grade: MAJOR. Sources: better-typography.

### TY-24 Descenders clipped by tight leading
Symptom: Italic display words with y, g, j, p or q have their descenders cut off.
Detect: leading-none or leading-[1] sits on display text containing italic descenders; overflow-hidden sits on the heading; no bottom padding or margin reserve exists on the wrapper.
Fix: Use at least leading-[1.1] and add pb-1 or mb-1 on the wrapper.
Grade: MAJOR. Sources: design-taste-frontend.

### TY-25 Truncated text with no way back
Symptom: Titles are cut with an ellipsis or clipped silently, and the full text is never reachable.
Detect: truncate, text-overflow: ellipsis or numberOfLines={1} sits on content that could wrap; overflow: hidden clips with no ellipsis; the cut text has no tooltip or expand affordance.
Fix: Prefer wrapping; when truncating, show an ellipsis and expose the full text on hover, focus or expand.
Grade: MAJOR. Sources: ui-ux-pro-max, better-layout, better-typography, better-interface.

### TY-26 Line clamp that does nothing
Symptom: Text meant to stop at three lines runs on.
Detect: -webkit-line-clamp is set without display: -webkit-box and -webkit-box-orient: vertical.
Fix: Add both properties, or use the line-clamp-3 utility.
Grade: MAJOR. Sources: better-typography.

### TY-27 Justified text with rivers
Symptom: Vertical channels of white space run through a paragraph.
Detect: text-align: justify sits on body text in application UI or without hyphenation; white gaps line up across lines in the capture.
Fix: Use text-align: start; if an editorial layout must justify, enable hyphens: auto with the correct lang.
Grade: MAJOR. Sources: better-typography, design-review.

### TY-28 All caps on body copy or every subheading
Symptom: Paragraphs are uppercase, or every subheader shouts in caps like template chrome.
Detect: text-transform: uppercase sits on p or body text, or on every h3, eyebrow or subheader.
Fix: Reserve caps for short labels and a few headings; use sentence case or small caps elsewhere.
Grade: MAJOR. Sources: impeccable, redesign-existing-projects.

### TY-29 Em dashes and en dashes in rendered copy
Symptom: Dashes appear in headlines, pills, quotes, captions, button text or alt text and read as a template tell.
Detect: U+2014 or U+2013 appears in rendered strings or the markup, including date and number ranges and label separators.
Fix: Use a period, comma, colon, parentheses or line break, and a plain hyphen for ranges.
Grade: MAJOR. Sources: design-taste-frontend.

### TY-30 CJK and emoji rendering untested
Symptom: Chinese, Japanese, Korean or emoji text shows fallback glyphs, odd line heights or broken truncation.
Detect: The font stack has no CJK fallback; character-count truncation splits a multi-byte emoji; line-height is tuned only for Latin.
Fix: Add CJK fallbacks, truncate by grapheme, and check line height with those scripts.
Grade: MAJOR. Sources: impeccable.

### TY-31 Display cut used at text sizes
Symptom: A Display variant at body size looks thin and cramped, or a Text cut at headline size looks heavy.
Detect: A family name containing Display (SF Pro Display, Heldane Display) sits on body-size text, or one containing Text sits on large headlines.
Fix: Use the optical cut that matches the size being set.
Grade: MAJOR. Sources: better-typography.

### TY-32 Gradient-filled text
Symptom: A heading is filled with a gradient that carries no meaning and reads unevenly across the glyphs.
Detect: background-clip: text pairs with a gradient background-image and color: transparent; Tailwind bg-clip-text text-transparent bg-gradient-to-r.
Fix: Use one solid color and emphasize through weight or size.
Grade: MAJOR. Sources: impeccable.

### TY-33 Text stroke on a variable font
Symptom: Stroked text shows stray lines inside the letters.
Detect: -webkit-text-stroke sits on a variable font whose overlapping contours are unmerged, with interior lines visible in the capture.
Fix: Use the static cut of the font for stroked text.
Grade: MAJOR. Sources: better-typography.

### TY-34 Lone word on the last line
Symptom: A heading or paragraph ends with a single word on its own line.
Detect: The capture shows a one-word final line; h1 to h3 lack text-wrap: balance; p, li, figcaption or blockquote lack text-wrap: pretty; a manual br forces a headline break.
Fix: Replace manual breaks with text-wrap: balance on headings and text-wrap: pretty on short and medium text.
Grade: POLISH. Sources: impeccable, make-interfaces-feel-better, design-review, redesign-existing-projects, design-taste-frontend.

### TY-35 Large headings at default tracking
Symptom: Display type looks loose and gappy.
Detect: Headings at 24px and up (better-typography) or 32px and up (impeccable) keep letter-spacing normal or 0; targets are -0.01 to -0.02em (better-typography, apple-design) or -0.02 to -0.04em (minimalist-ui).
Fix: Tighten display tracking slightly, written in em.
Grade: POLISH. Sources: impeccable, apple-design, minimalist-ui, design-review, redesign-existing-projects, better-typography.

### TY-36 All-caps labels without positive tracking
Symptom: Capitals in eyebrows, labels and small headings sit too close together.
Detect: text-transform: uppercase or font-variant-caps at 14px or less, or on 11 to 13px labels, has letter-spacing unset or 0.
Fix: Add 0.05em (better-typography) to 0.12em (impeccable) letter-spacing, slightly less for real small caps.
Grade: POLISH. Sources: impeccable, design-review, redesign-existing-projects, better-typography.

### TY-37 Body copy tracked away from zero
Symptom: Paragraphs look cramped or uneven because tracking meant for display sizes reaches body text.
Detect: letter-spacing other than 0, tracking-tight or tracking-tighter sits on body or small text; one global letter-spacing is shared by headings and body; letter-spacing is written in px, which does not scale.
Fix: Keep body copy at 0, vary tracking by size, and write it in em.
Grade: POLISH. Sources: ui-ux-pro-max, better-typography, apple-design.

### TY-38 Weights with no role mapping
Symptom: Weights from 100 to 900 are scattered, or only 400 and 700 exist so subtle levels cannot be expressed.
Detect: More than four distinct font-weight values are in use; 900 on headings and 700 on body where 600 and 500 would do; only 400 and 700 are loaded with no 500 or 600.
Fix: Define three or four weights with roles, such as 400, 500, 600 and 700.
Grade: POLISH. Sources: impeccable, claude-code-workflows, redesign-existing-projects, design-review.

### TY-39 Line height not tuned to context
Symptom: Narrow and wide columns, serif body and light-on-dark text all share one leading, and some of them read wrong.
Detect: Identical line-height sits on a narrow sidebar paragraph and a wide article; serif body keeps the sans value; a dark theme keeps light-mode line-height, letter-spacing normal and the same font-weight.
Fix: Give wide columns, serif body and light-on-dark text more leading (0.05 to 0.1), plus 0.01 to 0.02em tracking on dark.
Grade: POLISH. Sources: impeccable, frontend-design.

### TY-40 Balanced wrapping on paragraphs or long text
Symptom: Paragraph lines are evened unnaturally, or nothing changes because the browser ignores it past six lines.
Detect: text-wrap: balance or text-balance sits on p or article text; pretty or balance sits on blocks of ten or more lines, pre or code; Chromium balances six lines at most, Firefox ten.
Fix: Use text-wrap: pretty on paragraphs and default wrapping on long or preformatted text.
Grade: POLISH. Sources: make-interfaces-feel-better, better-typography.

### TY-41 Font smoothing missing at the root or set per component
Symptom: Text renders heavier than intended on macOS, or some components look differently anti-aliased from the rest.
Detect: html lacks -webkit-font-smoothing: antialiased and -moz-osx-font-smoothing: grayscale, or those declarations sit inside a component.
Fix: Apply both once on the root.
Grade: POLISH. Sources: make-interfaces-feel-better, better-typography.

### TY-42 Tabular figures on prose or static numbers
Symptom: Numbers inside sentences, phone numbers, zip codes and version strings look oddly spaced.
Detect: tabular-nums sits on body paragraphs, the root, or static display numbers; in Inter the digit 1 widens and centers.
Fix: Keep figures in prose proportional and verify the numerals in the font used.
Grade: POLISH. Sources: make-interfaces-feel-better, better-typography.

### TY-43 Kerning or optical sizing disabled
Symptom: Letter pairs sit unevenly, or small text renders with display proportions.
Detect: font-kerning: none appears anywhere; font-optical-sizing is none; "opsz" is hard-coded in font-variation-settings; a variable font with an optical axis has no font-optical-sizing: auto.
Fix: Remove those declarations; kerning and font-optical-sizing: auto are the defaults.
Grade: POLISH. Sources: impeccable, better-typography.

### TY-44 Hyphenation wrong for the context
Symptom: Headings and labels break mid-word, long words overflow narrow columns, or words split by the wrong language's rules.
Detect: hyphens: auto sits on headings or UI labels, or on elements whose lang is missing or wrong; long words in narrow columns have no soft hyphen or hyphens: auto and overflow.
Fix: Hyphenate narrow body columns only, with the correct lang, and mark break points in long words with a soft hyphen.
Grade: POLISH. Sources: impeccable, better-typography.

### TY-45 Axis or stylistic set the font does not support
Symptom: A width or slant setting does nothing, or a stylistic set does something unrelated in another font.
Detect: font-variation-settings carries tags not in the font's axis list, such as "wdth" on Inter; "ss01" or "cv11" is copied from another family without checking its docs.
Fix: Use only the axes and feature slots the font documents.
Grade: POLISH. Sources: better-typography.

### TY-46 Ligatures left on in code
Symptom: Code snippets merge character pairs, misrepresenting the source.
Detect: code elements lack font-variant-ligatures: none.
Fix: Set font-variant-ligatures: none on code.
Grade: POLISH. Sources: impeccable.

### TY-47 Label or badge wrapping mid-phrase
Symptom: A badge or short label breaks onto two lines and looks broken.
Detect: Badges and labels lack white-space: nowrap or whitespace-nowrap.
Fix: Set white-space: nowrap on labels and badges.
Grade: POLISH. Sources: better-typography, design-taste-frontend.

### TY-48 Underline cutting through descenders
Symptom: Link underlines slice through the tails of g, p and y.
Detect: text-decoration-skip-ink: none appears anywhere.
Fix: Remove it and adjust text-underline-offset or use from-font instead.
Grade: POLISH. Sources: better-typography.

### TY-49 Label text sitting low in tight containers
Symptom: Button and badge labels look vertically off-center because the font reserves space above and below its letters.
Detect: Text sits visibly below center in buttons or badges with no text-box: trim-both cap alphabetic; or container heights are tuned only for the trimmed result, which Firefox does not apply.
Fix: Apply text-box: trim-both cap alphabetic as a progressive enhancement and size containers for the untrimmed fallback.
Grade: POLISH. Sources: better-typography.

### TY-50 Faux small caps or superscripts
Symptom: Small caps built from scaled uppercase, or a superscript built from vertical-align, look mismatched in weight.
Detect: Scaled-down uppercase or vertical-align: super with reduced font-size stands in for font-variant-caps or font-variant-position; or those properties sit on a font lacking the glyphs.
Fix: Enable real glyphs with font-variant-caps and font-variant-position on a font that includes them.
Grade: POLISH. Sources: better-typography.

### TY-51 Drop cap without the Safari prefix
Symptom: The drop cap renders in Chromium but not in Safari.
Detect: initial-letter is set without -webkit-initial-letter.
Fix: Add -webkit-initial-letter and accept the Firefox fallback.
Grade: POLISH. Sources: better-typography.

### TY-52 Paragraph gap and first-line indent together
Symptom: Paragraphs are both separated by a gap and indented on their first line, doubling the signal.
Detect: A margin between paragraphs is combined with text-indent on the same paragraphs.
Fix: Use either space between paragraphs or a first-line indent, never both.
Grade: POLISH. Sources: impeccable.

### TY-53 Text baselines off the grid
Symptom: Baselines in adjacent columns do not line up.
Detect: Line heights and vertical margins are not multiples of the baseline unit; side-by-side text is misaligned in an overlay.
Fix: Snap line heights and vertical spacing to the baseline grid.
Grade: POLISH. Sources: impeccable.

### TY-54 Centered multi-line body text
Symptom: Long centered paragraphs are hard to track from line to line.
Detect: text-align: center or textAlign: 'center' sits on body text that wraps past two lines.
Fix: Left-align body text and keep centering for short headings and captions.
Grade: POLISH. Sources: ui-ux-pro-max.

### TY-55 Straight quotes in typographic copy
Symptom: Testimonials are wrapped in ASCII quotation marks instead of typographic quotes.
Detect: The straight ASCII " character wraps rendered quote text.
Fix: Use typographic curly quotes or none at all.
Grade: POLISH. Sources: design-taste-frontend.

### TY-56 Middle dots chained as separators
Symptom: Metadata strips read "foo · bar · baz · qux" with dots everywhere.
Detect: More than one middle dot appears per line in a metadata strip.
Fix: Use at most one middle dot per line; prefer line breaks, hairlines or columns.
Grade: POLISH. Sources: design-taste-frontend.

### TY-57 Pull quote styled like body text
Symptom: A testimonial is visually indistinguishable from the copy around it.
Detect: Quote text has no italic, muted color, quote marks or section background to set it apart.
Fix: Give quotes a distinct treatment such as italic, muted color and a quiet background.
Grade: POLISH. Sources: ui-ux-pro-max.

### TY-58 Bold emphasis overused in body copy
Symptom: Every proper noun or acronym is bold, so emphasis means nothing.
Detect: Many strong or b spans appear per paragraph.
Fix: Bold only what needs emphasis.
Grade: POLISH. Sources: unslop.

### TY-59 Pure black body text
Symptom: #000000 text is harsh against a white background.
Detect: color: #000 or #000000 sits on body text.
Fix: Use an off-black such as #111111 or #2F3437, with a softer gray for secondary text.
Grade: POLISH. Sources: minimalist-ui.


## Color and contrast (CO)

### CO-01 Text under its WCAG contrast ratio
Symptom: Body, label, caption, placeholder, heading or status text reads faint against its background.
Detect: Rendered pair against the nearest painted ancestor under 4.5:1 for normal text (7:1 for AAA) or 3:1 for large text (24px, or 18.67px bold); APCA Lc under 75 body, 60 labels, 45 large; text-gray-400 on white, body lighter than slate-700.
Fix: Move the text's lightness, not its hue, away from the background until it passes, then remeasure.
Grade: BLOCKING. Sources: impeccable, better-interface, ui-ux-pro-max, design-review, claude-code-workflows, design-plugin/accessibility-review, better-accessibility, better-colors.

### CO-02 UI component, icon or graphic under 3:1
Symptom: Input borders, checkbox outlines, icons, chart marks or button fills blend into the adjacent background.
Detect: Border, state indicator, icon, chart mark or accent fill under 3:1 against adjacent colors (inactive controls and logos exempt); #ddd border on white; #F97316, #10B981, #F59E0B accents on light surfaces; small icons under 4.5:1 (ui-ux-pro-max) or APCA Lc 30 (better-colors).
Fix: Darken or lighten the component color until it reaches 3:1 on every adjacent color.
Grade: BLOCKING. Sources: impeccable, ui-ux-pro-max, design-review, design-plugin/accessibility-review, better-accessibility, better-colors.

### CO-03 Dark-mode text or borders failing contrast
Symptom: Text and borders that passed on white are muddy or invisible on dark surfaces.
Detect: Same gray token on both themes; text-gray-600 on bg-gray-900; #9CA3AF on #111827; pairs measured in light only, though APCA scores mirrored pairs differently; dark primary text under 4.5:1, secondary under 3:1 (ui-ux-pro-max; WCAG keeps 4.5:1), OLED text under 7:1.
Fix: Give dark mode its own text and border tokens (such as #F9FAFB) and remeasure every pair there.
Grade: BLOCKING. Sources: impeccable, ui-ux-pro-max, claude-code-workflows, better-colors.

### CO-04 Light label on a mid-lightness fill
Symptom: A white label on a mid-tone button, badge or chip fails contrast and can vanish.
Detect: text-white on a Tailwind 500 fill or pastel button; white on fills with OKLCH L above about 56% (white on oklch(65% 0 0) measures 3.23:1, black 6.49:1); light text on light or dark on dark CTAs.
Fix: Compare black and white on the fill with the required metric, or move the fill to step 600, hover 700.
Grade: BLOCKING. Sources: gpt-taste, ui-ux-pro-max, better-colors.

### CO-05 Text over an image, video or gradient without a scrim
Symptom: Headline or caption text becomes unreadable over the lightest or darkest region behind it.
Detect: Text over background-image, an img, video or linear-gradient with no overlay; one contrast number reported for a gradient; worst region under 4.5:1; video hero without a roughly 60% dark overlay; mesh or aurora gradients behind tables, charts or long text.
Fix: Add a scrim or overlay, measure the worst region, and keep gradients away from data and long text.
Grade: BLOCKING. Sources: ui-ux-pro-max, better-colors, impeccable, design-taste-frontend.

### CO-06 Status conveyed by color alone
Symptom: Red or green text, dots or borders carry a state with no icon, text or underline.
Detect: Status variants differing only in color or background-color; an invalid field showing border-red-500 with no icon or error text; links told from body text by color only (WCAG 1.4.1).
Fix: Add a redundant cue beside the color: an icon, inline text or an underline.
Grade: BLOCKING. Sources: better-accessibility, ui-ux-pro-max.

### CO-07 Focus ring without 3:1 on every side
Symptom: The focus indicator is faint or vanishes where it crosses a fill, image or hover state.
Detect: outline: 2px solid with no color value, or ring utilities without an explicit color, so the ring renders in currentColor; ring measured under 3:1 against any adjacent color: component fill, page surface, image, gradient, hover or selected state.
Fix: Use an explicit focus token, such as outline: 2px solid var(--focus-ring), that reaches 3:1 around the whole perimeter.
Grade: BLOCKING. Sources: better-accessibility.

### CO-08 Status color used against its meaning
Symptom: The danger hue sits on a safe action, or success green marks a warning or a destructive action.
Detect: bg-red-* or text-destructive on primary or neutral actions; a danger, success or warning token on an element whose state does not match it; green on a delete button.
Fix: Use the status token that matches the state, or a neutral token when there is no state.
Grade: BLOCKING. Sources: better-interface, better-colors.

### CO-09 Pure black or pure white surfaces
Symptom: Large #000 or #fff regions look flat and harsh and leave no room for elevation steps.
Detect: #000, #000000, bg-black, #fff, #ffffff, bg-white, oklch(0% 0 0) or oklch(100% 0 0) as page, section, hero or dark-mode background; a ramp whose endpoints are pure black or white.
Fix: Use tinted near-black (OKLCH 12 to 18%, #0a0a0a, #121212) and off-white; keep surface steps above any deliberate OLED black.
Grade: MAJOR. Sources: impeccable, design-taste-frontend, redesign-existing-projects, better-colors, ui-ux-pro-max.

### CO-10 Dark theme as a straight inversion of light
Symptom: Dark mode looks harsh: pure black surfaces with no depth, neon accents, and pairs that passed in light fail.
Detect: filter: invert() or dark tokens mapping step n to max minus n with no value changes; #000 background; accent chroma identical to light; no tonal surface steps; dark: overrides bolted on piecemeal.
Fix: Swap semantic roles first, then lighten surfaces for depth, lower accent chroma, widen the dark end and remeasure.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max, claude-code-workflows, better-colors.

### CO-11 Elements that ignore the theme switch
Symptom: After switching themes some colors, shadows, logos, images or whole components stay in the other theme.
Detect: Literal colors in inline styles or JS; static box-shadow; SVG fills without currentColor; bg-gray-50 or text-gray-900 in components with no dark: variant or semantic token; a #FFFFFF panel inside a dark theme; light borders persisting on dark surfaces.
Fix: Route every theme-dependent value through a semantic token that swaps once; toggle every theme variant in a capture.
Grade: MAJOR. Sources: impeccable, design-taste-frontend, ui-ux-pro-max, better-colors.

### CO-12 More than one accent or too many hues
Symptom: Several saturated hues compete on buttons, links, badges and sections, so nothing reads as the primary action.
Detect: Two or more non-semantic saturated hues on CTAs, links or highlights; more than 2 to 4 hues beyond neutrals; --secondary and --tertiary tokens with no distinct role; every section or icon in a different hue.
Fix: Keep one accent on neutral bases and at most 2 to 4 hues beyond neutrals, status colors included.
Grade: MAJOR. Sources: impeccable, design-taste-frontend, redesign-existing-projects, design-review, better-colors.

### CO-13 Color dosage with no dominant base
Symptom: The accent floods large surfaces, or several hues share the stage equally, so color no longer directs attention.
Detect: Accent over roughly 10% of visible area with no stated strategy; saturated background-color on section or hero containers; four or more hues at similar area; no hue near 60%; density differing across sibling screens; saturated hero padded by gray chrome.
Fix: Let one base own about 60%, a secondary 30% and the accent 10%, applied consistently across sibling surfaces.
Grade: MAJOR. Sources: impeccable, minimalist-ui, frontend-design.

### CO-14 Oversaturated color
Symptom: Fully saturated hues shout from fills and text; the palette feels loud, cheap or alarming.
Detect: HSL saturation at or near 100% (#ff0000, #00ff00, #FF00FF) or above 80% on accents (design-taste-frontend, redesign-existing-projects); 100% saturation plus high lightness; Tailwind 500 neons as primary; neon accents on calm or health products.
Fix: Bring saturation to 70 to 85% (impeccable) or under 80% (design-taste-frontend) and let accents sit with the neutrals.
Grade: MAJOR. Sources: impeccable, design-taste-frontend, redesign-existing-projects, ui-ux-pro-max.

### CO-15 Gray text on a colored background
Symptom: Neutral gray labels on a brand, accent or status surface look muddy, washed out and low-contrast.
Detect: text-gray-*, #999 or a neutral text token over a tinted or saturated background such as a primary button, banner, hero or status badge.
Fix: Use a darker or lighter shade of the background hue, or transparency of the on-color text, instead of gray.
Grade: MAJOR. Sources: impeccable.

### CO-16 Accent spent on non-interactive decoration
Symptom: Headings, dividers, icons and badges wear the accent, so headings look clickable and the primary action no longer stands out.
Detect: The accent, or a hue within 15 degrees of it, on .section-title, dividers, backgrounds, body links, icons, badges and buttons at once; bold weight on most lines; several competing highlights.
Fix: Reserve the accent for the primary action, current selection and state; keep headings on the neutral text token.
Grade: MAJOR. Sources: impeccable, design-review, better-colors.

### CO-17 Ramp built in HSL or by eye
Symptom: Steps bunch at one end, the hue drifts and mid-steps look muddy, so the ramp reads as two colors.
Detect: hsl() ramps varying only lightness; uneven OKLCH L deltas or drifting hue; sRGB interpolation; 50 to 200 spaced 0.07 to 0.10 L like mid-ramp instead of 0.04 to 0.05; one step out of line around a pinned brand value.
Fix: Regenerate in OKLCH with a color library: constant hue, mid steps 0.07 to 0.10 L, light end 0.04 to 0.05.
Grade: MAJOR. Sources: impeccable, better-colors.

### CO-18 Theme polarity unfit for the use context
Symptom: A deep black UI is unreadable in sunlight or print, or a white screen glares in a dim media context.
Detect: #000000 or #121212 base on print-oriented, outdoor or color-accuracy products; bg-white base on video, photo or audio editors, sleep or night tools with no theme toggle; theme chosen with no stated scene (who, where, ambient light).
Fix: Derive the default theme from the physical use scene and offer the other theme as a toggle.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max.

### CO-19 Text on a translucent or blurred surface
Symptom: Text on a frosted header or glass panel loses contrast or shifts hue with whatever scrolls behind it.
Detect: Text inside backdrop-filter: blur() or a semi-transparent background measured against one static color; gray or saturated foreground on the blur; dark text on dark glass; blur outside 10 to 20px, white outside 15 to 30%; glass under long documents.
Fix: Test against the lightest and darkest content behind it; raise opacity, weight the text, and keep color on solid layers.
Grade: MAJOR. Sources: apple-design, ui-ux-pro-max, better-colors.

### CO-20 Dark-mode accent left untuned
Symptom: The accent glows neon on near-black, or has been dulled into an unrecognizable muddy gray-blue.
Detect: Dark-mode accent token with the same chroma as the light-mode accent (impeccable, better-colors), or so desaturated that the brand hue is no longer recognizable beside the light version (design-taste-frontend).
Fix: Lower the dark accent's chroma a step or two while holding its hue; compare both themes side by side.
Grade: MAJOR. Sources: impeccable, design-taste-frontend, better-colors.

### CO-21 Theme switch crossfading every element
Symptom: Flipping light and dark animates every surface at once and the page reads as a slow smear.
Detect: Transitions on color, background-color, border-color or box-shadow across many elements with no suppression during the flip; suppression wired only to matchMedia prefers-color-scheme and not to the in-app toggle (no disableTransitionOnChange).
Fix: Inject *,*::before,*::after{transition:none !important}, force a reflow, and remove it on the next frame for both triggers.
Grade: MAJOR. Sources: better-ui.

### CO-22 Out-of-gamut color clipped on sRGB screens
Symptom: A vivid color renders as a value nobody chose, and neighboring ramp steps flatten into one.
Detect: oklch() chroma beyond sRGB at that hue and lightness (cyans top out far lower than reds) declared with no sRGB value first and no @media (color-gamut: p3); a contrast fix pushed out of gamut.
Fix: Reduce chroma while holding hue and lightness; declare the sRGB value first and the vivid one inside @media (color-gamut: p3).
Grade: MAJOR. Sources: better-colors.

### CO-23 Text on an alpha or opacity-modified background
Symptom: Text sits on a semi-transparent fill whose rendered color depends on what is behind it, so contrast cannot be guaranteed.
Detect: Text inside an element whose background uses a Tailwind opacity modifier such as bg-accent/50, rgba(), hsla(), or color-mix() with transparent; widespread alpha on text, surfaces and borders; contrast quoted from the declaration rather than the rendered result.
Fix: Use solid tokens under text; define explicit overlay colors per context and reserve alpha for focus rings and see-through states.
Grade: MAJOR. Sources: impeccable, better-colors.

### CO-24 Chroma held into the ramp extremes
Symptom: Very light tints glow and very dark shades look like ink spilled on the brand instead of near-neutral surfaces.
Detect: OKLCH L near 0 or 100 with chroma close to the mid-ramp value, such as oklch(15% 0.25 h) or oklch(97% 0.2 h); the 50 and 950 steps as vivid as 500.
Fix: Peak chroma mid-ramp and reduce it toward both ends while holding the hue.
Grade: MAJOR. Sources: impeccable, better-colors.

### CO-25 Hue ramps unmatched at the same step
Symptom: red-500 looks heavier than blue-500, and the warning yellow looks weak beside the danger red.
Detect: OKLCH L differing between ramps at the same step number; one absolute chroma or saturation value copied across every hue ramp in the token file.
Fix: Match OKLCH L exactly per step, and set each ramp's chroma to the same proportion of its hue's maximum.
Grade: MAJOR. Sources: better-colors.

### CO-26 Neutrals improvised with no scale
Symptom: Grays differ in tint and step per component; warm and cool grays side by side look dirty.
Detect: Many more than 7 ad hoc gray values and no neutral token scale; neutral tokens whose OKLCH hue differs, some toward orange and some toward blue, such as #f5f5f0 beside #eef0f5; a tinted gray mixed with a pure gray.
Fix: Define one 5 to 7 step neutral ramp holding a single temperature, and route every gray through it.
Grade: MAJOR. Sources: claude-code-workflows, redesign-existing-projects, better-colors.

### CO-27 One hue carrying two meanings
Symptom: The same color signals different things, or two colors signal the same status, so users misread state.
Detect: A success, warning, danger or info hue reused for brand or decoration; two hues for one status; two roles whose tokens sit within 15 degrees of OKLCH hue of each other.
Fix: Give each color one meaning across the whole interface and treat anything within 15 degrees as that same color.
Grade: MAJOR. Sources: impeccable, better-colors.

### CO-28 Status and actions without a distinguishing color
Symptom: Success, error, warning, links and the primary action all use one neutral or brand color, hiding state at a glance.
Detect: Error messages in the brand accent; no success, error, warning or info tokens; no chroma anywhere on status, links or primary actions in a "quiet" grayscale pass.
Fix: Define semantic status tokens and use them consistently; a restrained palette still keeps color on state and actions.
Grade: MAJOR. Sources: impeccable, claude-code-workflows.

### CO-29 Framework default palette left in place
Symptom: Blue-500 primary, gray text and white background: the product looks like an unstyled framework template.
Detect: Unmodified Tailwind or Bootstrap palette tokens as the entire color system; default primary color left in place; the same generic palette reused across unrelated products.
Fix: Build a committed palette from the product's own hue with one dominant color and tinted neutrals.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max.

### CO-30 Generic gradient with no purpose
Symptom: A flat two-color gradient, usually purple to blue, sits on a background or heading for no reason.
Detect: linear-gradient(a, b) with exactly two stops in the purple and blue family; a gradient not built from the palette's own hues; gradient text or buttons added as decoration.
Fix: Remove it, or build an intentional multi-stop gradient from the chosen palette.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max.

### CO-31 Status hue within 15 degrees of the accent
Symptom: The destructive or warning button is indistinguishable from the primary action because the brand is nearly the same hue.
Detect: OKLCH hue of a status solid within 15 degrees of the accent solid, such as a red brand with a red danger token.
Fix: Move the status hue at least 15 degrees away, or give the destructive action an outlined treatment with an icon.
Grade: MAJOR. Sources: better-colors.

### CO-32 Primary call to action blending into its section
Symptom: The main button or search field does not stand out from the hero or section around it.
Detect: CTA text and background pair under 7:1 (ui-ux-pro-max); CTA fill in the same hue family as its surroundings; a search input with a faint border or fill on a hero.
Fix: Give the primary action a contrasting accent that clears 7:1 against its section.
Grade: MAJOR. Sources: ui-ux-pro-max.

### CO-33 Soft shadow as a control's only boundary
Symptom: Extruded tone-on-tone controls and cards are hard to tell from the base on dense screens or in dark themes.
Detect: Dual light and dark box-shadows on a single pastel base (#E0E5EC style) with no border or fill difference, used on dashboards, forms, multi-color apps or dark-only products.
Fix: Add a boundary or fill that reaches 3:1, or use flat surfaces where density or contrast matters.
Grade: MAJOR. Sources: ui-ux-pro-max.

### CO-34 Vibrating saturated color pair
Symptom: Saturated text on a saturated complementary background, such as blue on red, shimmers and is painful to read.
Detect: Two high-chroma hues roughly opposite on the wheel placed as foreground and background with no neutral between them.
Fix: Separate the two with a neutral, or change one hue or its lightness.
Grade: MAJOR. Sources: impeccable.

### CO-35 Body text on a mid-lightness surface
Symptom: Body text cannot pass on a mid-tone background no matter how dark or light the text is.
Detect: Body text on a background near OKLCH L 0.75, where even pure black reaches only about APCA Lc 60 and fails Lc 75.
Fix: Move the background toward one extreme; the background, not the text, has to change.
Grade: MAJOR. Sources: better-colors.

### CO-36 Illegible selection highlight
Symptom: Selected text disappears because the brand selection color and the text color have no contrast.
Detect: A ::selection rule whose background and color pair fails 4.5:1 or leaves text the same lightness as the highlight.
Fix: Pick a selection background and text color pair that stays legible.
Grade: MAJOR. Sources: better-typography.

### CO-37 Neutral chroma outside its narrow band
Symptom: Grays look lifeless beside the brand, or the gray ramp is visibly blue or orange and competes with the accent.
Detect: Zero-chroma neutrals (#888, #ccc, #f5f5f5, oklch(50% 0 0), unoverridden gray-500) next to saturated brand hues (impeccable); neutral ramp OKLCH chroma above 0.02 (better-colors).
Fix: Hold neutral chroma between 0.005 and 0.02 at the brand hue, or keep one consistent pure gray throughout.
Grade: POLISH. Sources: impeccable, better-colors.

### CO-38 No contrast hierarchy among text levels
Symptom: Every text level sits at maximum contrast, so nothing recedes and secondary text competes with primary.
Detect: #000 on #fff for all text; captions, metadata and tertiary labels at the same contrast as body and headings.
Fix: Reserve the strongest contrast for primary content and let secondary text sit at a gentler, still passing ratio.
Grade: POLISH. Sources: impeccable.

### CO-39 Palette energy contradicting the product's register
Symptom: Neon accents on a calm or health product feel alarming; flat grays on a playful product feel unmotivating.
Detect: Highly saturated accents (#00FF00, #FF00FF) on healthcare, mental health or spa interfaces; HSL saturation under 40% everywhere on streak, reward or game CTAs.
Fix: Match accent saturation and warmth to the product's register before tuning individual colors.
Grade: POLISH. Sources: ui-ux-pro-max.

### CO-40 Adjacent ramp steps indistinguishable
Symptom: Two neighboring ramp steps cannot be told apart, so the ramp has more steps than decisions.
Detect: Adjacent steps less than 0.03 apart in OKLCH L.
Fix: Drop one of the two steps.
Grade: POLISH. Sources: better-colors.

### CO-41 Invisible dividers
Symptom: Separator lines cannot be seen, so the grouping they were meant to carry is lost.
Detect: Divider or hairline color against its surface under APCA Lc 15 or visually indistinguishable in a capture.
Fix: Raise the divider to at least Lc 15 against its surface.
Grade: POLISH. Sources: better-colors.


## Surfaces and depth (SU)

### SU-01 Nested cards
Symptom: A card sits inside another card, stacking borders, shadows, and radii into a double outline.
Detect: A bordered or shadowed container directly inside another in the DOM; .card .card nesting; several box-shadow levels within one component; a double outline visible in the capture.
Fix: Flatten the structure; separate content within a card with spacing, typography, and subtle dividers.
Grade: MAJOR. Sources: impeccable.

### SU-02 Cards wrapping content that needs no containment
Symptom: Every block is boxed in a card, so elevation means nothing and the page reads as a grid of boxes.
Detect: Repeated rounded border shadow wrappers on lists, text blocks, and single stats; .card on most children of a section; uniform rounded rectangles everywhere; cards on content that is neither distinct, actionable, nor compared in a grid.
Fix: Group with spacing, border-t, or divide-y; keep cards for distinct, actionable, or compared items.
Grade: MAJOR. Sources: impeccable, design-taste-frontend, better-layout.

### SU-03 Shadows, borders, and tints that encode nothing
Symptom: Decorative shadows, gradients, borders, and tinted backgrounds add noise without marking hierarchy, grouping, or function.
Detect: Borders on every container; box-shadow on static, non-layered elements; linear-gradient backgrounds, pattern images, or noise textures with no role; tinted backgrounds that group nothing; multi-layer card shadows and color on non-semantic chips in routine product screens.
Fix: Remove every depth cue that does not reinforce hierarchy, grouping, or an interaction boundary.
Grade: MAJOR. Sources: impeccable.

### SU-04 Blur on surfaces with nothing behind them
Symptom: Frosted-glass panels appear on cards, headers, and dashboards as the house style, so blur signals no layer.
Detect: backdrop-filter: blur() or backdrop-blur-* with bg-white/10 or similar on most containers and static surfaces rather than only overlays; glass on dashboards, enterprise, or public-sector screens that need legibility.
Fix: Reserve blur for a few overlay surfaces such as modal and sheet backdrops; group the rest with borders or space.
Grade: MAJOR. Sources: impeccable, design-taste-frontend, ui-ux-pro-max.

### SU-05 Heavy shadows
Symptom: Shadows are dark and clearly visible, so surfaces look pasted on or floating.
Detect: Large blur or offset box-shadow with high-alpha black; default shadow-md, shadow-lg, or shadow-xl; shadow opacity at or above 0.05 (minimalist-ui); the shadow reads as a visible dark edge in the capture.
Fix: Use a subtle sm to xl scale, for example 0 2px 8px rgba(0,0,0,0.04).
Grade: MAJOR. Sources: impeccable, minimalist-ui.

### SU-06 Depth vocabulary inconsistent across the interface
Symptom: Cards, sheets, and modals each carry a different ad hoc shadow or style, so depth relationships are unreadable.
Detect: Arbitrary box-shadow literals or shadow-[...] values with no shared tokens; modals with lighter shadows than cards; equal shadow on sheet and chip; offsets with mixed signs implying several light sources; heavy shadows and blur inside an otherwise flat system.
Fix: Define one elevation scale with one light direction and assign levels by component role.
Grade: MAJOR. Sources: ui-ux-pro-max, design-plugin/design-system, redesign-existing-projects, apple-design, impeccable.

### SU-07 Shadows vanishing in dark mode
Symptom: Cards, menus, and page merge in dark mode because black shadows disappear on dark backgrounds.
Detect: The light-mode black box-shadow reused under the dark theme as the only elevation cue; no visible card edge in the dark capture; dark-end lightness steps as small as light-end steps.
Fix: Use surface lightness steps (15, 20, 25%) or a ring 0 0 0 1px rgba(255,255,255,0.08), hover 0.13.
Grade: MAJOR. Sources: impeccable, better-ui, make-interfaces-feel-better, better-colors.

### SU-08 Non-concentric nested radius
Symptom: A rounded child and its rounded parent share or mismatch radii, so the corners do not track each other.
Detect: Outer border-radius not equal to inner radius plus padding; rounded-xl p-2 wrapping rounded-xl; .card { border-radius: 12px; padding: 8px } with a 12px child; inner and outer curves not parallel in the capture.
Fix: Set outer radius equal to inner radius plus padding, for example 20px outer for 12px inner with 8px padding.
Grade: MAJOR. Sources: better-ui, make-interfaces-feel-better.

### SU-09 Side-stripe accent border
Symptom: Cards, list items, callouts, or alerts carry a thick colored left or right border as an accent.
Detect: border-left or border-right wider than 1px in a non-neutral color; border-l-4 border-blue-500 and similar; a colored stripe used as an "active" or "warning" marker.
Fix: Use a full 1px hairline, a 4 to 8% accent tint, a leading glyph, or a numbered prefix.
Grade: MAJOR. Sources: impeccable.

### SU-10 Colored glows and blurred blobs behind content
Symptom: Colored halos, glowing orbs, and radial blobs sit behind content, creating a hazy, overworked look.
Detect: Large-blur colored box-shadow such as 0 0 40px rgba(99,102,241,.5); filter: blur() on absolutely positioned colored circles; radial-gradient aurora backgrounds behind heroes; glowing buttons; multiple comma-separated shadows on one element.
Fix: Remove decorative glows and stacked shadows; earn depth with layout, type, and restrained surfaces.
Grade: MAJOR. Sources: impeccable.

### SU-11 Translucent surfaces merging with what is behind them
Symptom: Cards are so translucent they blend into the page, or two blurred layers overlap and legibility collapses.
Detect: Surface backgrounds with low alpha such as bg-white/30 and no border or elevation; card and page indistinguishable in a light-mode capture; nested elements both using light backdrop-filter materials.
Fix: Give surfaces enough opacity or elevation to separate; never stack two light translucent layers.
Grade: MAJOR. Sources: ui-ux-pro-max, apple-design.

### SU-12 Weak or misapplied modal scrim
Symptom: The page behind a modal stays almost as bright as the dialog, or a side panel dims everything.
Detect: Backdrop under roughly 40% black such as bg-black/20 (ui-ux-pro-max spec 40 to 60%); a blocking modal with no scrim or pushed-back background; a non-blocking parallel panel with a full scrim; stacked sheets not progressively dimmed.
Fix: Dim modal tasks with a 40 to 60% black scrim; use offset and translucency, no scrim, for parallel panels.
Grade: MAJOR. Sources: ui-ux-pro-max, apple-design.

### SU-13 Shadow used as a divider
Symptom: List separators, table cell boundaries, and hairlines rendered as shadows look blurry and float.
Detect: box-shadow standing in for border-b, border-t, or side separators between rows, cells, or sections; separator edges soft and offset in the capture.
Fix: Keep layout separators as 1px borders; use shadow rings only for elevation.
Grade: MAJOR. Sources: better-ui, make-interfaces-feel-better.

### SU-14 Heavy textures and stacked shadows on task-focused screens
Symptom: Bevels, textures, 3D tilts, or multi-layer shadows on lists, tables, and forms slow reading and feel dated.
Detect: Texture images, 8 to 12 stop gradients, neumorphic dual shadows, box-shadow stacks, transform: perspective() or rotateX, or overlapping layered depth on list, table, form, feed, or article screens.
Fix: Use flat surfaces separated by color blocking, 1px borders, or a single subtle shadow level.
Grade: MAJOR. Sources: ui-ux-pro-max.

### SU-15 Random dark section in a light page
Symptom: A single near-black band interrupts an otherwise light page and looks like a paste accident.
Detect: One section with a #111 or near-black background between light sections; a sudden jump in background luminance down the page with no theme change elsewhere.
Fix: Keep a consistent tone, using a slightly darker shade of the same palette, or commit to full dark mode.
Grade: MAJOR. Sources: redesign-existing-projects.

### SU-16 Opaque border breaking over mixed backgrounds
Symptom: A solid border designed for one background looks heavy or clashes when the element sits over images or mixed colors.
Detect: border: 1px solid with an opaque color on cards, dropdowns, or modals whose only job is elevation; opaque border-color on elements placed over photos or gradients; no transparent box-shadow ring.
Fix: Use 0 0 0 1px rgba(0,0,0,0.06), 0 1px 2px -1px rgba(0,0,0,0.06), 0 2px 4px 0 rgba(0,0,0,0.04); keep structural borders.
Grade: POLISH. Sources: better-ui, make-interfaces-feel-better.

### SU-17 Untinted black shadow on a tinted background
Symptom: Pure black shadows look muddy and detached on colored or warm surfaces.
Detect: box-shadow using rgba(0,0,0,x) or shadow-black on a tinted, colored, or cream background; no hue in the shadow color.
Fix: Tint shadows toward the background hue, such as dark blue on a blue surface.
Grade: POLISH. Sources: design-taste-frontend, redesign-existing-projects.

### SU-18 Large flat surfaces reading as unfinished
Symptom: A grid of identical plain cells or a hero on a flat fill reads as a default, unfinished composition.
Detect: A multi-cell grid where every cell shares one background with no image, tint, or pattern; hero, feature, or CTA sections as text on a plain fill; a flat two-stop 45deg linear-gradient with no variation.
Fix: Give two or three cells or sections purposeful variation: an image, a tint, a subtle pattern, or grain.
Grade: POLISH. Sources: design-taste-frontend, minimalist-ui, gpt-taste, redesign-existing-projects, frontend-design.

### SU-19 Pill radius on large containers or primary buttons
Symptom: Fully rounded cards, containers, or main buttons look toy-like and distract from content.
Detect: border-radius: 9999px or rounded-full on cards, containers, or primary CTAs; card radius above 12px (minimalist-ui); complex clip-path shapes on content containers.
Fix: Reserve pills for small tags; keep cards at 8 to 12px and primary buttons at 4 to 6px.
Grade: POLISH. Sources: impeccable, minimalist-ui.

### SU-20 Radius not scaled to element size and nesting
Symptom: Buttons, inputs, cards, and modals share one radius or each invent their own, so nesting reads flat or messy.
Detect: A single border-radius value such as 8px on every element regardless of size; or more values than a small set (4 to 6px inputs and buttons, 8 to 12px cards and modals).
Fix: Use a small set of radii, tighter on inner elements and softer on containers.
Grade: POLISH. Sources: redesign-existing-projects, claude-code-workflows.

### SU-21 Gradient interpolation producing a dull or unintended midpoint
Symptom: A two-hue gradient goes gray or dark in the middle, or routes through a hue nobody asked for.
Detect: linear-gradient between two vivid or opposite hues with no in oklab or in oklch and no third stop, midpoint visibly desaturated; in oklch sweeping through unintended hues; a conversion diff that altered the in space keyword.
Fix: Interpolate in oklab for a straight blend, in oklch shorter hue for a hue arc, or add a third stop.
Grade: POLISH. Sources: better-colors.

### SU-22 Banding on a large low-contrast gradient
Symptom: A hero gradient with little contrast between its stops steps visibly on 8-bit displays.
Detect: A gradient spanning a large area whose stops are close in lightness; visible bands in the capture.
Fix: Widen the contrast between stops, shrink the area, or overlay a subtle noise texture.
Grade: POLISH. Sources: better-colors.

### SU-23 Arbitrary z-index values
Symptom: Stacking order is unpredictable, so tooltips end up behind modals or dropdowns under sticky bars.
Detect: z-index: 999, 9999, or other magic numbers scattered through components; no shared layer scale.
Fix: Build a semantic scale: dropdown, sticky, modal backdrop, modal, toast, tooltip.
Grade: POLISH. Sources: impeccable, design-taste-frontend, redesign-existing-projects.

### SU-24 Chrome surface identical to content surface
Symptom: Sidebars, toolbars, and panels sit on the same surface as content, so structure reads flat.
Detect: Identical background on navigation chrome and the content area; identical blur or opacity on structural regions and interactive elements.
Fix: Give chrome a second neutral slightly cooler or warmer, or a heavier material than content.
Grade: POLISH. Sources: impeccable, apple-design.

### SU-25 Thick or opaque borders carving the page
Symptom: Heavy dark borders cut the page into boxes and add weight.
Detect: border: 2px solid #000 style dividers; fully opaque border colors on cards and inputs where a hairline would do.
Fix: Reduce border thickness, lower the opacity, or remove the border entirely.
Grade: POLISH. Sources: impeccable.

### SU-26 Glass panel with no edge definition
Symptom: A blurred translucent rectangle has no edge, so it looks like a flat smudge.
Detect: backdrop-filter: blur() or backdrop-blur-* with no 1px inner border such as border-white/10 and no inset highlight such as shadow-[inset_0_1px_0_rgba(255,255,255,0.1)].
Fix: Add a 1px low-opacity inner border and a subtle inset highlight for edge refraction.
Grade: POLISH. Sources: design-taste-frontend, redesign-existing-projects.

### SU-27 Concentric math forced past 24px padding
Symptom: Huge outer radii computed to satisfy the concentric formula on widely separated layers.
Detect: Padding greater than 24px with the outer radius still derived from inner radius plus padding; an oversized outer curve in the capture.
Fix: Past 24px of padding, treat the layers as separate surfaces and choose each radius independently.
Grade: POLISH. Sources: better-ui, make-interfaces-feel-better.

### SU-28 Images without an outline in a bordered system
Symptom: Photos float edge-less while neighboring cards carry rings, so depth is inconsistent.
Detect: img elements with no outline beside elements that use borders or shadow rings; light image edges disappearing into the background.
Fix: Add a 1px low-opacity outline to images.
Grade: POLISH. Sources: better-ui.

### SU-29 Interactive cards with no separation from the page
Symptom: Clickable product or item cards do not separate from the background, so nothing invites a click.
Detect: No elevation, border, or background difference between card and page; no hover lift (ui-ux-pro-max spec: 200ms lift plus scale) on cards that open something.
Fix: Add subtle elevation or a border and a short hover lift to clickable cards.
Grade: POLISH. Sources: ui-ux-pro-max.

### SU-30 Permanent divider under floating chrome
Symptom: A hard line sits under a sticky header even when nothing scrolls beneath it.
Detect: border-bottom: 1px on sticky or fixed headers regardless of scroll position; the line visible at the top of the page before any scroll.
Fix: Show a scroll edge effect only where floating UI overlaps content.
Grade: POLISH. Sources: apple-design.


## Icons and imagery (IC)

### IC-01 Broken image URL
Symptom: An image slot renders empty or shows the broken-image icon.
Detect: Guessed `images.unsplash.com/photo-...` or other invented URLs that return 404; missing images in the rendered capture.
Fix: Use verified assets or a seeded placeholder service; never invent image URLs.
Grade: BLOCKING. Sources: design-taste-frontend.

### IC-02 Mixed icon sets or styles side by side
Symptom: Icons in one screen differ in visual language: outline next to filled, different corner styles, different optical weight.
Detect: Imports from more than one icon library in a view; sibling icons mixing `solid` and `outline` or `weight="fill"` and `"regular"` in the same state; differing corner radius or stroke among neighbours.
Fix: Source all icons from one family; use one style per hierarchy level and reserve filled for state changes.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max, claude-code-workflows, design-taste-frontend, better-ui, minimalist-ui, design-review.

### IC-03 Raster icons and simple shapes shipped as bitmaps
Symptom: Icons, badges and marks blur or pixelate on high-DPI screens and cannot adapt to dark mode.
Detect: `.png` or `.jpg` icon assets, `<img src="icon.png">`, `require('./icon.png')` for UI glyphs; raster files for shapes CSS or SVG could draw.
Fix: Use SVG or platform vector icons; draw simple shapes with CSS or SVG.
Grade: MAJOR. Sources: better-ui, ui-ux-pro-max, claude-code-workflows, impeccable.

### IC-04 Icon stroke widths varying within one layer
Symptom: Some icons look bold and others hairline within the same bar, list or view.
Detect: `stroke-width` or `strokeWidth` values varying (1, 1.5, 2) across sibling icons at the same level.
Fix: Standardize one stroke width per visual layer, such as 1.5px or 2px.
Grade: MAJOR. Sources: ui-ux-pro-max, redesign-existing-projects, impeccable.

### IC-05 Icon stroke mismatched to text weight
Symptom: A hairline icon beside bold text reads as broken; a heavy icon beside regular text shouts.
Detect: `stroke-width="1.5"` next to `font-semibold` or `font-bold`; `stroke-width` 2 or 2.5 next to 400-weight 14 to 16px text.
Fix: Use 1.5px beside regular (400), 2px beside 500 to 600, 2.5px beside 700.
Grade: MAJOR. Sources: better-ui.

### IC-06 Inconsistent icon sizes in one context
Symptom: Icons in the same toolbar, nav or list render at 16, 20, 24 and 28px with no system.
Detect: Mixed literal `size`, `width` or `height` values on icons in one context; no `icon-sm`, `icon-md` (24px) or `icon-lg` tokens.
Fix: Define icon sizes as tokens and apply them consistently per context.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max.

### IC-07 Separate icon asset per state or hardcoded fills
Symptom: Hover, selected and disabled icons swap as separate files, or ignore the parent text color and never recolor.
Detect: `icon-hover.svg`, `icon-active.png`, state swaps by `src`; `fill="#666"`, `stroke="#000"` or any literal color inside imported SVGs; no `currentColor`.
Fix: One SVG drawn with `currentColor`; let CSS color and opacity drive every state.
Grade: MAJOR. Sources: better-ui.

### IC-08 Image slot left as a colored block or page with no imagery
Symptom: A solid-color rectangle stands in for the hero, or a restaurant, hotel, travel, fashion or product page has no photos.
Detect: Empty colored `<div>` boxes in hero or image slots; no `<img>`, framework image component or background image on an imagery-implying brief; fewer than 2 to 3 real images.
Fix: Ship real imagery (hero, product or lifestyle, supporting); if unsure use fewer photos, never a colored placeholder.
Grade: MAJOR. Sources: impeccable, design-taste-frontend.

### IC-09 Functional image named by its picture
Symptom: A search button is announced as "magnifying glass".
Detect: `alt` or `aria-label` on an image that is a link or button naming the glyph rather than the action or destination.
Fix: Describe the action or destination: search icon gets `alt="Search"`.
Grade: MAJOR. Sources: better-accessibility.

### IC-10 Hand-drawn SVG glyphs or illustrations
Symptom: Icons or illustrations drawn from scratch look crude and differ in weight, optical size and alignment from the set.
Detect: Inline `<svg><path d="M...">` glyphs authored in the component instead of library imports; large inline `<svg>` with many `<path>` elements as decoration.
Fix: Import icons from an established set; use generated or real imagery for illustration; draw only a single simple mark.
Grade: MAJOR. Sources: design-taste-frontend.

### IC-11 Distorted, recolored or guessed brand logos
Symptom: Third-party logos are stretched, tinted to match the theme or drawn from memory.
Detect: Logo images with non-uniform scaling, CSS `filter` or tint applied, hand-drawn approximations, insufficient clear space.
Fix: Use official brand assets at correct proportions, colors and clear space.
Grade: MAJOR. Sources: ui-ux-pro-max.

### IC-12 Non-directional or composite icons mirrored in RTL
Symptom: Logos, checkmarks, clocks, playback controls or badge overlays are flipped the wrong way under RTL.
Detect: Blanket `[dir="rtl"] svg { scale: -1 1 }` or `rtl:-scale-x-100` on brand marks, checkmarks, physical objects, play or rewind, or icons with overlays.
Fix: Flip only direction-dependent icons; analyze composite icons part by part and keep overlay positions.
Grade: MAJOR. Sources: better-ui.

### IC-13 Directional icons not mirrored in RTL
Symptom: Arrows, chevrons and progress indicators point the wrong way in RTL.
Detect: No `[dir="rtl"]` rules flipping directional icons with `transform: scaleX(-1)`.
Fix: Mirror directional icons under `[dir="rtl"]`.
Grade: MAJOR. Sources: impeccable, better-ui.

### IC-14 Unrecognizable icon metaphor
Symptom: Users cannot guess what an unlabeled icon does.
Detect: Abstract or invented glyphs for common actions; icons without labels that fail a "what does this do" test.
Fix: Use recognizable metaphors and add a label where the icon is ambiguous.
Grade: MAJOR. Sources: impeccable, apple-design.

### IC-15 Detailed icon collapsing at small size
Symptom: An icon that reads at 48px becomes mush at 16px; thin interior lines and tight counters blur.
Detect: Complex artwork rendered at 16px; glyph not recognizable at its smallest render size.
Fix: Test every icon at its smallest size and use simplified glyphs for small contexts.
Grade: MAJOR. Sources: better-ui.

### IC-16 Plain-text wordmarks in a logo wall
Symptom: A "trusted by" row shows styled text spans instead of logos; invented brands get no mark at all.
Detect: Logo wall built from `<span>` text; no SVG logos; invented brands without a generated monogram SVG.
Fix: Use real SVG logos; for made-up brands generate a simple inline SVG monogram matching the page style.
Grade: MAJOR. Sources: design-taste-frontend.

### IC-17 Meaningless labels overlaid on images
Symptom: Pills reading "Brand 02" or "Field notes" float over photos and add no information.
Detect: Absolutely positioned `<span>` labels inside image containers carrying decorative or version-stamp text.
Fix: Let the image stand alone or add a caption below it, outside the image.
Grade: MAJOR. Sources: design-taste-frontend.

### IC-18 Thin icon below contrast threshold
Symptom: Thin-stroke or fine-detail icons disappear against their background.
Detect: Outline icon stroke color against its background with absolute APCA Lc under 45.
Fix: Darken or lighten the icon color to at least Lc 45.
Grade: MAJOR. Sources: better-colors.

### IC-19 Blurry or upscaled imagery
Symptom: Photos look soft, pixelated or stretched from a thumbnail.
Detect: Low-resolution images, upscaled thumbnails, mismatched aspect ratios on content sites such as luxury, restaurant, real estate or photography.
Fix: Use high-resolution, brand-specific imagery sized for its slot.
Grade: MAJOR. Sources: ui-ux-pro-max.

### IC-20 Asymmetric icon geometrically centered
Symptom: Play triangles, arrows, stars and carets look shifted inside their button despite exact centering.
Detect: Directional or asymmetric glyphs centered with `justify-content: center` and no offset; symmetric `padding-inline` on a button with a trailing icon; or arbitrary `translate` on icons that already looked centered.
Fix: Nudge only when it looks wrong: play right about 2px, arrows toward their direction; prefer fixing the viewBox over margins.
Grade: POLISH. Sources: impeccable, better-ui, make-interfaces-feel-better.

### IC-21 Tinted or accent-colored image outline
Symptom: The hairline around images reads as dirt, a colored halo or a branded edge.
Detect: `outline` or `border` on `img` using slate, zinc, neutral, `#0a0a0a`, `#111827`, `#f5f5f7`, or the accent or ink color.
Fix: `outline: 1px solid oklch(0 0 0 / 0.1)` in light mode, `oklch(1 0 0 / 0.1)` in dark mode.
Grade: POLISH. Sources: better-ui, make-interfaces-feel-better.

### IC-22 Icon state swapped without transition
Symptom: Contextual icons pop in and out instantly on hover or state change (play to pause).
Detect: `display: none`, `hidden` or a bare conditional render on the icon with no `opacity`, `scale` or `filter` transition.
Fix: Animate `opacity` 0 to 1, `scale` 0.25 to 1, `blur` 4px to 0px.
Grade: POLISH. Sources: better-ui, make-interfaces-feel-better.

### IC-23 Inline icon misaligned or mis-sized against its text
Symptom: Icons sit a pixel above or below their label, have uneven side padding, or look oversized beside it.
Detect: Icon center not matching the text x-height center; missing `align-items: center` or baseline tweak; inconsistent `gap` around icons; fixed px icon size inline with text instead of `1em` to `1.25em`.
Fix: Center or baseline-align icons, keep one consistent gap, size inline icons `1em` to `1.25em`.
Grade: POLISH. Sources: impeccable, ui-ux-pro-max, better-ui.

### IC-24 Generic stock imagery
Symptom: Interchangeable stock photos (handshakes, smiling teams, "Italian food") that could belong to any competitor keep the site anonymous.
Detect: Category-level stock photography; people pointing at laptops or whiteboards; several mediocre hero or gallery photos with no committed mood.
Fix: Use specific, brand-owned or candid imagery, or one consistent illustration style; one decisive photo beats five.
Grade: POLISH. Sources: impeccable, design-taste-frontend, redesign-existing-projects, ui-ux-pro-max.

### IC-25 Image crop losing its subject
Symptom: A wide hero becomes an unreadable sliver on mobile, or the subject falls outside the slot's crop.
Detect: One image file for every breakpoint where composition should change; asset ratio differing from the slot (3:2 asset in a 3:1 header); `object-fit: cover` with no `object-position`.
Fix: Art-direct with `<picture>` and `<source media>`, set `object-position`, and match the asset ratio to its slot.
Grade: POLISH. Sources: impeccable, ui-ux-pro-max.

### IC-26 Placeholder or duplicated avatars
Symptom: Generic silhouettes stand in for people, or several distinct users share one avatar.
Detect: Default user-icon glyphs or grey circle placeholders in testimonial or team components; same `src` or seed across avatars in a list.
Fix: Use believable, unique avatar assets for every distinct person.
Grade: POLISH. Sources: design-taste-frontend, redesign-existing-projects.

### IC-27 Empty state with no visual or a generic library glyph
Symptom: A lone sentence floats in a large blank area, or a scaled-up folder icon sits above the empty-state text.
Detect: Empty state with no illustration or icon; icon-library glyphs scaled up as the empty-state visual.
Fix: Add a brand-matched illustration or purposeful icon to the empty state.
Grade: POLISH. Sources: impeccable.

### IC-28 Photo tone clashing with the palette
Symptom: Bright, saturated stock photography sits against a restrained palette and reads as pasted in.
Detect: Saturated or untreated photos next to a muted or monochrome interface; no desaturation, blend or tone overlay.
Fix: Treat photos to match the palette, for example `grayscale`, `mix-blend-luminosity`, a warm overlay, or reshoot.
Grade: POLISH. Sources: minimalist-ui, gpt-taste.

### IC-29 Raster image with no high-DPI variant
Symptom: Photos and raster graphics look blurry on retina screens.
Detect: Single 1x raster images without `srcset` or 2x variants.
Fix: Provide 2x assets or `srcset` for high-DPI screens.
Grade: POLISH. Sources: impeccable.

### IC-30 Icon off its native pixel grid
Symptom: Icons render soft and aliased.
Detect: A 24px-grid icon scaled to 16px or another fractional scale rather than the set's native 16, 20 or 24 sizes.
Fix: Render icons at the set's native grid sizes.
Grade: POLISH. Sources: better-ui.

### IC-31 Cliche feature icon metaphors
Symptom: Feature icons are the obvious template choices: rocket for launch, shield for security, bolt for speed, globe for global.
Detect: Rocket, shield, lightning bolt or globe icons next to feature titles.
Fix: Pick less obvious but still recognizable icons (fingerprint, spark, vault).
Grade: POLISH. Sources: redesign-existing-projects.

### IC-32 Icon style mismatched to its context
Symptom: Duotone or gradient marketing icons sit inside a dense tool UI, or thin outline icons look weak in a hero.
Detect: Decorative duotone or gradient glyphs in toolbars and tables; hairline outline glyphs as hero feature icons.
Fix: Use outlined icons for product UI, filled for nav bars, duotone or illustrative for marketing.
Grade: POLISH. Sources: ui-ux-pro-max.

### IC-33 Mockups presented as product screenshots
Symptom: Idealized renders in device frames misrepresent the app; screenshots and ratings do not match the store.
Detect: Illustrated or fake screens inside device frames; no real screenshots or real star ratings.
Fix: Show real screenshots in device frames with real ratings.
Grade: POLISH. Sources: ui-ux-pro-max.

### IC-34 Missing favicon
Symptom: The browser tab shows a blank or default icon.
Detect: No `<link rel="icon">` in the head.
Fix: Include a branded favicon.
Grade: POLISH. Sources: redesign-existing-projects.


## Motion (MO)

### MO-01 Motion with no reduced-motion handling
Symptom: Users who asked the OS for reduced motion still get every transition, entrance, and parallax effect.
Detect: `transition`, `animation`, `@keyframes`, Tailwind `animate-*` or `transition-*`, motion-library variants, or chart animation with no `@media (prefers-reduced-motion)` branch, `motion-safe:` prefix, or `useReducedMotion` check; exit animations and chart entrances with no guard.
Fix: Wrap motion in `@media (prefers-reduced-motion: no-preference)` so the static version is the default.
Grade: BLOCKING. Sources: better-accessibility, ui-ux-pro-max, better-ui.

### MO-02 Vestibular triggers kept under reduced motion
Symptom: Parallax, autoplaying loops, spinning, marquees, and auto-rotating carousels keep moving for reduced-motion users.
Detect: Under `prefers-reduced-motion: reduce`, scroll-linked `transform` or `background-attachment` parallax, `autoplay loop` video, animated GIFs, looping Lottie or CSS decoration, `rotate` keyframes, translations across large distances, marquees, or carousel autoplay that are only shortened rather than removed.
Fix: Disable these entirely under reduced motion and start carousels paused; reducing their duration is not enough.
Grade: BLOCKING. Sources: better-accessibility, ui-ux-pro-max.

### MO-03 Animation that blocks input
Symptom: The UI ignores taps and clicks while a transition plays; the user waits for it to finish.
Detect: `pointer-events: none` or an overlay applied for the animation duration; handlers disabled while animating; non-cancellable timing sequences; a tap during a sheet's slide-in does nothing until it completes; static content not interactive until its entrance ends.
Fix: Keep the UI interactive throughout any animation; a tap or gesture cancels it immediately.
Grade: BLOCKING. Sources: ui-ux-pro-max, design-review, impeccable, apple-design.

### MO-04 Media autoplaying with sound
Symptom: Audio starts on page load, startling users and drowning out screen-reader speech.
Detect: `<video autoplay>` or `<audio autoplay>` without `muted` (and `playsinline`); browsers may block it, leaving a frozen hero (WCAG 1.4.2).
Fix: Never autoplay with sound; autoplay only muted.
Grade: BLOCKING. Sources: better-accessibility, ui-ux-pro-max.

### MO-05 Content left invisible by a reveal that never fires
Symptom: Sections stay hidden or stuck mid-animation because the reveal depends on an animation that never runs.
Detect: `animation-timeline: scroll()` with initial `opacity: 0` outside an `@supports (animation-timeline: scroll())` block, so Firefox never reveals it; `whileInView` or scroll-trigger reveals that never fire; elements frozen at partial opacity or offset after navigation.
Fix: Make the static, visible state the default and gate the reveal behind `@supports` or a fired trigger.
Grade: BLOCKING. Sources: impeccable, design-taste-frontend.

### MO-06 Transition duration outside its band
Symptom: A button press reacts late, a modal lingers, or a celebration keeps playing while the user waits.
Detect: Compare `transition-duration` and `animation-duration` with use: feedback 100-150ms, state 200-300ms, layout 300-500ms, entrances 500-800ms (impeccable); most product transitions 150-250ms (impeccable, design-review); micro-interactions 150-300ms, never over 500ms (ui-ux-pro-max, claude-code-workflows); celebrations over 1s (impeccable); premium reveals may run 400-600ms (ui-ux-pro-max).
Fix: Assign each animation to its band and keep feedback under 500ms and celebrations under one second.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max, design-review, claude-code-workflows.

### MO-07 Motion with no purpose
Symptom: Things move because they can; the motion communicates no state, feedback, loading, or reveal.
Detect: Animations whose removal changes nothing a user needs; `transition: all` on static elements; ambient floating decoration; static navigation icons or text labels animating on state change; motion that no user action or state change explains.
Fix: Remove any animation that cannot name its job: feedback, state change, loading, or reveal.
Grade: MAJOR. Sources: impeccable, design-taste-frontend, ui-ux-pro-max, design-review, claude-code-workflows, frontend-design, better-ui, make-interfaces-feel-better.

### MO-08 Layout properties animated
Symptom: Movement stutters and drops frames because every frame recalculates layout and paint.
Detect: `transition` or `@keyframes` on `width`, `height`, `top`, `left`, `margin`, `padding`, `border-width`, `font-size`, large-area `box-shadow`, or `text-decoration-thickness`; `transition: all` on layout-affecting elements; native timing driving layout values.
Fix: Animate only `transform` and `opacity` (and `text-decoration-color` for underlines); use transforms for position changes.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max, redesign-existing-projects, design-review, better-typography, design-taste-frontend, apple-design, minimalist-ui.

### MO-09 Bounce, elastic, or overshooting easing
Symptom: Elements overshoot and wobble before settling; the motion reads as toy-like and dated.
Detect: `cubic-bezier()` with control points outside 0 to 1, such as `(0.34,1.56,0.64,1)`; `bounce`, `elastic`, `back` presets; spring `bounce` above 0 or damping below 1 on fades, menus, icon swaps, and toggles with no preceding flick; keyframes passing `scale(1.1)` before `scale(1)`.
Fix: Decelerate into the final value with ease-out quart, quint, or expo; allow bounce only after a momentum gesture (apple-design).
Grade: MAJOR. Sources: impeccable, apple-design, better-ui, make-interfaces-feel-better, ui-ux-pro-max.

### MO-10 Too many elements animating at once
Symptom: Every card, heading, and icon fades, slides, or bounces; attention has nowhere to land.
Detect: Entrance or hover animations on nearly every element; more than 1 to 2 animated focal elements per view (ui-ux-pro-max); concurrent `@keyframes` on unrelated elements; parallax, reveals, and hover effects stacked; many small effects with no single orchestrated moment.
Fix: Animate 1 to 2 key elements per view and spend the rest of the budget on one orchestrated moment.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max, frontend-design.

### MO-11 Release animation that ignores the gesture
Symptom: On release, a dragged element stops dead and then animates, or a flick snaps back instead of throwing.
Detect: Drag or swipe release driven by `transition`, `@keyframes`, or fixed-duration tweens; the release starts with zero velocity or from the model value instead of the on-screen one; snap target picked by position without projecting velocity; one spring for both axes.
Fix: Spring from the live value with the gesture's velocity, per axis, toward the projected destination (`(v/1000)*d/(1-d)`, d about 0.998).
Grade: MAJOR. Sources: apple-design, ui-ux-pro-max.

### MO-12 Animation on a high-frequency interaction
Symptom: Every keystroke, row hover, or tab switch plays an animation, charging its attention cost on each trigger.
Detect: Transitions longer than 150ms, or on properties other than `opacity` and `background-color`, bound to row `:hover`, `keydown`, or tab state; `staggerChildren` or `animation-delay` re-firing on repeated interaction; hover rules replaying an entrance keyframe; exit animations on frequent lists or toasts.
Fix: Give routine interactions instant feedback or a 150ms or shorter opacity or color transition; never stagger them.
Grade: MAJOR. Sources: better-ui, better-interface.

### MO-13 Interactive state animation that cannot be reversed
Symptom: Closing a drawer or toggling mid-animation snaps or restarts; the user waits for the old motion to finish.
Detect: `animation:` or `@keyframes` with `forwards` fill on `.open`, `:hover`, or toggled classes instead of `transition:`; fixed-timeline tweens on interactive states; the Animations panel cannot reverse it smoothly; `.drawer.open { animation: slideIn 200ms ease-out forwards }`.
Fix: Use CSS transitions that interpolate toward the latest state; reserve keyframes for one-shot staged sequences.
Grade: MAJOR. Sources: better-ui, make-interfaces-feel-better, ui-ux-pro-max, apple-design.

### MO-14 Theatrical effects on a task or calm surface
Symptom: A settings page, dashboard, form, or health app carries parallax, particles, shaders, marquees, or squishy press physics.
Detect: WebGL canvases, particle layers, 3 to 5 layer parallax, cinematic scroll, infinite marquees, spring deformation on press, or dramatic entrances on forms, tables, settings, admin, or data screens, and on SaaS, healthcare, finance, government, meditation, or children's products.
Fix: Keep sensory effects for marketing surfaces; on tools use subtle 200-250ms feedback, stronger hierarchy, and reduced-motion support.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max.

### MO-15 Page-load choreography on a product surface
Symptom: A dashboard, form, or chart plays a staged entrance on every load while the user is mid-task.
Detect: Staggered `animation-delay` reveals or orchestrated sequences on app shells, tables, forms, settings, or charts; bars growing from zero before values are readable; `AnimatePresence` without `initial={false}` so default-state icons, tabs, and toggles animate in on refresh.
Fix: Load product views into their settled state; add `initial={false}` so default-state controls skip mount animation.
Grade: MAJOR. Sources: impeccable, design-review, ui-ux-pro-max, better-ui, make-interfaces-feel-better.

### MO-16 Frame drops during animation or scroll
Symptom: Motion visibly stutters, especially on phones, tablets, or mid-range hardware.
Detect: Performance panel frames over 16ms (60fps) or rate below 50fps on target devices; long JavaScript tasks during motion; paint-heavy effects (large blur, shadow) animating; `transform` or `animation` applied directly to `<svg>` instead of a wrapper.
Fix: Restrict to compositor properties, move work off the main thread, animate an SVG's wrapper, and simplify until 60fps holds.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max.

### MO-17 Looping animation on a non-status element
Symptom: Icons, cards, or decorations pulse, bounce, shimmer, or float forever, pulling attention from content.
Detect: `animate-pulse`, `animate-bounce`, `animation-iteration-count: infinite`, `repeat: Infinity`, `Animated.loop`, or typewriter loops on informational cards or decoration rather than loaders or live feeds; ambient blobs faster than 20s or above opacity 0.04, or not `position: fixed; pointer-events: none` (minimalist-ui).
Fix: Reserve continuous animation for loading indicators and live status; leave informational sections still.
Grade: MAJOR. Sources: design-taste-frontend, ui-ux-pro-max, minimalist-ui, impeccable.

### MO-18 Motion that shifts surrounding content
Symptom: Neighbors jump as an element animates in, expands, or hovers; the layout feels unstable.
Detect: Entrance keyframes on `margin`, `height`, or `padding`; elements inserted without reserved space so siblings reflow; CLS during or after an animation in the capture; `transition-all` on layout-affecting elements.
Fix: Animate with `transform` and `opacity` inside reserved space so neighbors never move.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max, design-review.

### MO-19 Scroll-driven sequence misfiring
Symptom: Reveals lag the scroll or replay on every pass; pinned sections start before reaching the top.
Detect: `addEventListener('scroll')` with `getBoundingClientRect()` driving reveals instead of `IntersectionObserver`; observer never calls `unobserve`; ScrollTrigger `start: "top center"` or `"top 80%"` on pinned cards; horizontal track without `pin: true`, `scrub`, or `end: "+=distance"`.
Fix: Observe once and unobserve; pin at `"top top"`, scrub the track, and set the end distance explicitly.
Grade: MAJOR. Sources: impeccable, design-taste-frontend.

### MO-20 Declared entrance that never plays
Symptom: A hero, loading state, or whole page declares motion, yet nothing moves on a full refresh.
Detect: `<AnimatePresence initial={false}>` wrapping `initial="hidden" animate="visible"` variants; transitions and `whileInView` declared but no hero entry, scroll reveal, or CTA hover visible; verify on a full page refresh.
Fix: Remove the suppressor where the component relies on its `initial` prop, or ship a deliberately static page.
Grade: MAJOR. Sources: better-ui, make-interfaces-feel-better, design-taste-frontend.

### MO-21 Animations stacking or fighting after navigation
Symptom: Animations double up, keep running after leaving the page, or stutter because two engines drive one element.
Detect: Effects creating timelines, scroll triggers, or listeners without a cleanup (`ctx.revert()`); triggers accumulate and jump on re-mount; the same element animated by two libraries in one tree.
Fix: Give every animation effect a strict cleanup and each element a single animation source.
Grade: MAJOR. Sources: design-taste-frontend.

### MO-22 Stagger that makes the page slow to settle
Symptom: The last items of a list appear long after the first; the user waits for the trickle to end.
Detect: `animation-delay: calc(var(--i) * 50ms)` or per-item delays where count times delay exceeds about 500ms (10 items at 50ms is the ceiling); per-item delays well above 50ms on lists (ui-ux-pro-max); group increments far above 100-150ms.
Fix: Cap total stagger near 500ms by shrinking per-item delay or limiting staggered items.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max, better-ui.

### MO-23 Movement transitions not downgraded under reduced motion
Symptom: Reduced-motion users still get sliding panels, zooming cards, and gliding anchor scrolls.
Detect: `translate` or `scale` transitions, `scroll-behavior: smooth`, or `scrollTo({ behavior: "smooth" })` with no `prefers-reduced-motion: reduce` variant.
Fix: Under reduced motion, swap slides and scales for opacity crossfades and smooth scrolling for an instant jump.
Grade: MAJOR. Sources: better-accessibility.

### MO-24 Functional feedback stripped under reduced motion
Symptom: Reduced-motion users lose spinners, progress, hover color, focus rings, and press feedback.
Detect: A blanket `* { animation: none; transition: none }` under `prefers-reduced-motion: reduce` that also kills loading spinners, progress bars, and instant state changes.
Fix: Keep spinners, progress, and brief functional feedback; reduced motion targets vestibular triggers, not feedback.
Grade: MAJOR. Sources: better-accessibility, impeccable, apple-design.

### MO-25 State change that snaps
Symptom: Modals, drawers, toggles, hover highlights, and anchor jumps change instantly; the UI feels abrupt and cheap.
Detect: No `transition` on open, close, hover, or expanded states; `transition: none`, `duration-0`, or durations under about 100ms (impeccable); `display: none` toggled to `block`; toggle thumbs with no transform transition; elements unmounted with no exit; no `scroll-behavior: smooth` on anchor navigation.
Fix: Transition state changes over 150-300ms (200-300ms for show and hide) with a subtle exit, gated by reduced motion.
Grade: POLISH. Sources: impeccable, ui-ux-pro-max, redesign-existing-projects, claude-code-workflows, make-interfaces-feel-better, better-ui.

### MO-26 Linear or stock easing on UI transitions
Symptom: Motion feels mechanical, mushy, or weightless; elements stop abruptly or arrive sluggishly.
Detect: `transition-timing-function` or `animation-timing-function` of `linear`, `ease`, `ease-in-out`, or `Easing.linear` on hover, press, enter, or spatial transitions; default library easing values left untuned; `linear` is acceptable only for continuous motion (design-review).
Fix: Use exponential ease-out curves: `cubic-bezier(0.25,1,0.5,1)` quart, `cubic-bezier(0.22,1,0.36,1)` quint, `cubic-bezier(0.16,1,0.3,1)` expo, or a spring.
Grade: POLISH. Sources: impeccable, design-taste-frontend, ui-ux-pro-max, design-review, redesign-existing-projects, claude-code-workflows.

### MO-27 Exit louder or longer than the entrance
Symptom: Leaving elements slide their full height, shrink, or linger, stealing attention from where the user is going.
Detect: Exit duration equal to or above the enter (specs: 75% of enter, impeccable; 60-70%, ui-ux-pro-max; 150ms exit against 300ms enter, better-ui); `translateY(-100%)` or container-height travel outside drawer-close cases; `scale(0.5)` or 400ms on exits.
Fix: Exit with a small fixed `translateY` (about 12px) plus opacity over about 150ms, shorter than the enter.
Grade: POLISH. Sources: impeccable, better-ui, make-interfaces-feel-better, ui-ux-pro-max.

### MO-28 Entrance arriving as one undifferentiated block
Symptom: A marketing hero or first-load grid fades in as a single block, showing no hierarchy for the same cost.
Detect: One animated wrapper around title, description, and buttons with no `staggerChildren` or per-child `animation-delay`; list or grid children with no cascade; a declared stagger collapsing to simultaneous because parent variants and children sit in different component trees.
Fix: Split into semantic groups; stagger 30-50ms per list item (ui-ux-pro-max), 80ms (minimalist-ui), 100ms per group (better-ui), 100-150ms (impeccable).
Grade: POLISH. Sources: better-ui, make-interfaces-feel-better, minimalist-ui, redesign-existing-projects, ui-ux-pro-max, impeccable, design-taste-frontend.

### MO-29 Motion paths that break the spatial model
Symptom: A panel arrives from the right and leaves downward; forward and back look alike; exits fade in place.
Detect: Enter and exit transforms on different axes or directions; identical transition for push and pop, or direction varying by screen; sheets entering from random edges; exits animating `opacity` only; in-between frames giving no hint of the destination.
Fix: Dismiss along the arrival path, mirror forward and back consistently, and keep a directional hint on exits.
Grade: POLISH. Sources: apple-design, ui-ux-pro-max, better-ui, make-interfaces-feel-better.

### MO-30 Icon or material swap that reads as a flat fade
Symptom: An icon swap or blurred surface arrives as a plain opacity fade instead of a tangible change.
Detect: Icon enter at `scale: 0.5` or `0.6` (`scale-50`) instead of 0.25; no blur on the cross-fade; `ease`, `ease-in-out`, or `cubic-bezier(0.4, 0, 0.2, 1)` instead of `cubic-bezier(0.2, 0, 0, 1)` at 300ms; `backdrop-filter` surfaces animating `opacity` only.
Fix: Animate scale 0.25 to 1, opacity, and `blur(4px)` to 0 over 300ms, bounce 0; animate glass blur too.
Grade: POLISH. Sources: better-ui, make-interfaces-feel-better, apple-design.

### MO-31 Easing direction reversed or unmirrored
Symptom: Entering elements accelerate away, leaving elements decelerate into nothing, or open and close feel asymmetric.
Detect: `ease-in` such as `cubic-bezier(0.7,0,0.84,0)` on entrances; `ease-out` on exits (impeccable, ui-ux-pro-max, design-review; better-ui accepts ease-out both ways); there-and-back toggles without `ease-in-out`; the same curve on both directions of a reversible transition (apple-design).
Fix: Ease out entering, ease in leaving, ease in and out on toggles; mirror the curve on the return path.
Grade: POLISH. Sources: impeccable, ui-ux-pro-max, design-review, apple-design, better-ui.

### MO-32 Screen or content swap with a hard cut
Symptom: Routes, tab content, or swapped icons replace each other with a flash and no link between old and new.
Detect: Route changes with no crossfade, directional slide, or shared element; list-to-detail navigation where the same image appears on both screens but does not travel; conditional rendering swapping children of one container; a conditionally rendered icon unmounting instantly.
Fix: Crossfade content replaced in place, keep both icons in the DOM and cross-fade, and use shared-element transitions between related screens.
Grade: POLISH. Sources: impeccable, ui-ux-pro-max, better-ui.

### MO-33 Durations and easings that differ per component
Symptom: Similar transitions decelerate and time differently across the product, so motion feels incoherent.
Detect: Many distinct `transition-duration` and `timing-function` values across components with no motion tokens; mixed `ease`, `linear`, and custom curves; specs that say only "fades in" with no ms or curve; uniform untuned stagger offsets.
Fix: Define duration and easing tokens from one ease-out family and use them everywhere.
Grade: POLISH. Sources: impeccable, design-plugin/design-system, design-plugin/design-handoff, ui-ux-pro-max.

### MO-34 Collapsible panel that jumps, spills, or snaps
Symptom: An accordion jumps open, shows content spilling past its edge mid-animation, or its chevron never turns.
Detect: `transition: height` or a `max-height` hack on panels (`height: auto` cannot transition); no `overflow: hidden` during the transition; disclosure chevron without `transform: rotate()` on open; `display: none` toggled with no transition.
Fix: Transition `grid-template-rows` from 0fr to 1fr on a grid wrapper, clip overflow, and rotate the chevron.
Grade: POLISH. Sources: impeccable, ui-ux-pro-max.

### MO-35 Overlay that does not originate from its trigger
Symptom: A menu, popover, or dialog materializes from the center or from nowhere, unrelated to the button that opened it.
Detect: `transform-origin: center` (the default) on popovers and menus; modal entrance as a plain fade from the viewport center regardless of trigger location; drawers and detail views with no directional origin.
Fix: Set `transform-origin` to the trigger and animate from it with scale plus fade, or slide from the trigger side.
Grade: POLISH. Sources: apple-design, impeccable, ui-ux-pro-max.

### MO-36 Travel or scale larger than the change needs
Symptom: Buttons balloon on hover and elements fly in from far away; the motion is noticed more than the state change.
Detect: `:hover { transform: scale(1.1) }` or larger on buttons and cards (keep 1.02 to 1.05); entrance keyframes with `translateY(40px)` or more (keep 10 to 20px); durations and displacements a smaller version would read identically.
Fix: Cut travel and scale, not clarity: 10-20px travel, hover scale 1.02-1.05 with a color or shadow shift.
Grade: POLISH. Sources: impeccable, better-ui.

### MO-37 Large surface travelling at full opacity or strobing
Symptom: A big panel crossing the screen dominates attention, and very fast motion appears to strobe.
Detect: Large panels repositioning at full opacity; per-frame positional jumps large enough to read as discrete steps on fast transitions.
Fix: Fade large surfaces while they travel; keep per-frame movement small or add subtle motion blur.
Grade: POLISH. Sources: apple-design.

### MO-38 Elements resting below opacity 0.2
Symptom: Ghostly half-faded elements hang around and look like rendering bugs.
Detect: Animated `opacity` resting at values around 0.1 to 0.2; long tails on fade-outs that never reach 0.
Fix: Fade fully to 0 or keep elements clearly visible; never rest below 0.2.
Grade: POLISH. Sources: ui-ux-pro-max.


## Interaction and feedback (IN)

### IN-01 Destructive action with neither confirmation nor undo
Symptom: Delete, reset, bulk or account-level actions fire on a single click and the data cannot be brought back.
Detect: Delete, remove, reset or batch handlers run with no confirm step and no undo toast, especially for irreversible, multi-item or multi-user actions; the destructive button uses default styling.
Fix: Confirm irreversible, bulk or shared-impact actions, offer undo for reversible ones, and style destructive buttons distinctly.
Grade: BLOCKING. Sources: impeccable, better-interface, better-writing, ui-ux-pro-max, claude-code-workflows.

### IN-02 Action, error or critical content only in a timed element
Symptom: An undo link, error, recovery code or session continuation vanishes on a timer the user cannot extend.
Detect: Toasts that carry a button, an error or details to act on are dismissed by `duration` or `setTimeout`; undo links or one-time codes exist only in an auto-dismissing toast; session timeouts give no warning or extend option.
Fix: Keep actionable or critical content until dismissed, and let users extend or turn off time limits.
Grade: BLOCKING. Sources: better-accessibility, design-plugin/accessibility-review, design-taste-frontend.

### IN-03 Success shown before the server confirms
Symptom: The UI shows "Paid", "Deleted" or "Sent" before the request succeeds, so a failure leaves the user misled.
Detect: Handlers for payment, deletion or irreversible mutations update state optimistically; a success indicator renders before the response arrives and has no rollback on failure.
Fix: Wait for confirmation on payments and destructive actions; keep optimistic updates for low-stakes actions and mark them provisional.
Grade: BLOCKING. Sources: impeccable, design-review.

### IN-04 State change carried by motion alone
Symptom: What changed is visible only while the animation runs; with reduced motion or a blink nothing shows.
Detect: Compare before and after captures with transitions disabled: the two states show no persistent color, icon swap or label difference.
Fix: Pair every animated state change with a static cue, a color, icon or label that stays afterwards.
Grade: BLOCKING. Sources: better-ui, better-interface.

### IN-05 System gesture swallowed by an app handler
Symptom: Edge swipe-back, predictive back, Control Center, pinch-zoom or long-press stop working or do something unexpected inside the app.
Detect: Gesture recognizers cover the full screen or its edges; `gestureEnabled: false` has a custom replacement; predictive back is disabled; `preferredScreenEdgesDeferringSystemGestures` is set; custom pinch or long-press handlers map to non-standard actions.
Fix: Leave screen edges free, support swipe-back and predictive back, and keep platform gestures at their standard meanings.
Grade: BLOCKING. Sources: ui-ux-pro-max.

### IN-06 Decorative layer swallowing clicks
Symptom: A glow, gradient scrim, sheen or blur sits over a control that looks live and does nothing when clicked.
Detect: A `position: absolute; inset: 0` decorative element or an `::after` pseudo-element covers interactive content without `pointer-events: none`.
Fix: Give every decorative layer `pointer-events: none`.
Grade: BLOCKING. Sources: better-accessibility.

### IN-07 Audio or device sensor started without user opt-in
Symptom: Sound plays on load or first scroll, or the page requests orientation, light or location for a decorative effect.
Detect: Web Audio or `<audio>` playback is not gated on a user gesture and an explicit opt-in control; device APIs are called on page load without a user gesture or explanation.
Fix: Require an explicit user gesture and opt-in before any sound or sensor access.
Grade: BLOCKING. Sources: impeccable.

### IN-08 Core action reachable only by a hidden gesture
Symptom: Undo, delete or another core action works only via shake, swipe or long-press, with no visible control.
Detect: Swipe, shake or long-press handlers have no corresponding visible button that performs the same action.
Fix: Provide a visible button for every action a gesture performs.
Grade: BLOCKING. Sources: ui-ux-pro-max.

### IN-09 Whole-page touch-action none
Symptom: The whole page stops scrolling on touch.
Detect: `touch-action: none` is set on `html`, `body` or a full-page wrapper.
Fix: Scope `touch-action: none` to the surface that implements its own gestures.
Grade: BLOCKING. Sources: better-accessibility.

### IN-10 No pressed state on tap or click
Symptom: Pressing a button or card shows no highlight, ripple, opacity or scale change, so clicks feel dead.
Detect: There is no `:active` rule; `<Pressable>` has `activeOpacity={1}` or no pressed style; Android has no ripple; `-webkit-tap-highlight-color: transparent` has no replacement; highlight is bound to `click` or `touchend` only; nothing changes within 80 to 150ms (ui-ux-pro-max).
Fix: Highlight on pointer-down with a subtle scale (0.96 to 0.98), `translateY(1px)`, ripple, opacity or elevation, and commit on release.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max, apple-design, claude-code-workflows, design-taste-frontend, redesign-existing-projects.

### IN-11 No success confirmation after an action
Symptom: A save, submit, send or setting change completes silently; users repeat the action or doubt it worked.
Detect: The success path only updates state, with no toast, checkmark, banner, inline message or color flash after the mutation; a form submit has no success state; a tutorial step has no success check.
Fix: Confirm every completed save, submit, send and delete with brief visible feedback.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max, apple-design, claude-code-workflows.

### IN-12 Control styled like static text
Symptom: Users cannot tell what is clickable; links read as body text and the primary action is a missed inline link.
Detect: An `<a>` or `<button>` shares the color, weight and decoration of the copy beside it; a control has no underline, border, fill or accent in a system where the accent marks interactivity; the primary CTA is an inline text link.
Fix: Give every control a background shape, border, underline, accent or consistent placement zone, and make primary CTAs obvious buttons.
Grade: MAJOR. Sources: impeccable, design-review, design-plugin/design-critique, better-colors, better-layout.

### IN-13 Celebration-grade feedback on routine actions
Symptom: Confetti, sound or a playful flourish fires on saving a draft or toggling a setting; special moments stop feeling special.
Detect: Confetti libraries, sound or playful animation run on routine saves, toggles, clicks or hovers; several delight layers (sound, confetti, copy, animation) fire on one action; the effect covers the confirmation text; long effects repeat on frequent actions.
Fix: Reserve celebration for milestones, keep it to one short skippable moment, and use a gentle scale and fade elsewhere.
Grade: MAJOR. Sources: impeccable.

### IN-14 Clickable element with no hover change or pointer cursor
Symptom: Nothing changes when the pointer is over a card, row or custom button, so it does not read as clickable.
Detect: A `<div>`, `<span>` or `<li>` with `onClick` has no `:hover` style and no `cursor: pointer`; custom buttons use `cursor: default`; clickable images have no hover transform; spatial controls have no gaze hover effect.
Fix: Add `cursor: pointer` and a subtle hover change (background, shadow or slight scale) to every clickable element.
Grade: MAJOR. Sources: ui-ux-pro-max, gpt-taste, impeccable.

### IN-15 Sound or haptics on every interaction, or too loud
Symptom: Every click, scroll tick or keystroke chirps or buzzes, errors blare, and users mute the whole app.
Detect: Audio, `navigator.vibrate` or `Haptics.impactAsync` calls sit in generic click, hover, scroll, `onChange` or tab-switch handlers; audio plays at default or full volume; error tones are sharp and alarm-like.
Fix: Reserve sound and haptics for success, error, commit and snap moments, and keep them quiet and soft.
Grade: MAJOR. Sources: impeccable, apple-design, ui-ux-pro-max.

### IN-16 Confirmation dialog on a reversible or routine action
Symptom: "Are you sure?" interrupts every archive, move, trash or save, and users click through without reading.
Detect: `confirm()` or a modal guards navigation, save, archive, move, delete-to-trash or another action that could be undone, and no undo affordance follows the action.
Fix: Act at once and show an undo toast ("Project archived. Undo"); reserve confirmation for irreversible actions.
Grade: MAJOR. Sources: impeccable, apple-design, better-writing.

### IN-17 No undo for reversible or bulk actions
Symptom: An accidental archive, edit or bulk change cannot be reverted; users must redo work or avoid risky actions.
Detect: Archive, move, trash, edit or bulk handlers have no undo affordance or history, and the result toast carries no "Undo" action.
Fix: Offer undo, typically an "Undo" action in the result toast, for reversible and bulk actions.
Grade: MAJOR. Sources: impeccable, apple-design, ui-ux-pro-max, better-writing.

### IN-18 Toast timing too short, infinite or not paused
Symptom: Notifications pile up permanently, vanish before they can be read, or disappear while the user reaches for them.
Detect: Toast `duration` is 0 or Infinity with no close control; `duration` or `setTimeout` is under 5000ms (better-accessibility) or under about 2s (ui-ux-pro-max); the timer does not pause on `mouseenter` or `focusin`.
Fix: Auto-dismiss low-stakes toasts after 3 to 5s (ui-ux-pro-max) or at least 5s (better-accessibility), add a close, pause on hover.
Grade: MAJOR. Sources: ui-ux-pro-max, better-accessibility.

### IN-19 Onboarding hint not dismissable, not anchored or reappearing
Symptom: A floating tip or "What's new" banner has no close, points at nothing, or returns on every visit and device.
Detect: A tooltip is positioned generically with no dismiss control or "Don't show again"; an announcement has no close; no seen or completed flag is persisted, or it is stored only locally so returning users see the welcome again.
Fix: Anchor hints to their target, keep them brief and dismissable, and persist completion server-side.
Grade: MAJOR. Sources: impeccable.

### IN-20 Hover styles applied on touch devices
Symptom: Cards stick in their lifted hover state after a tap, and touch laptops get mouse-sized targets.
Detect: `.card:hover { transform: translateY(-2px) }` is not wrapped in `@media (hover: hover)`; there are no `(pointer: fine)`, `(pointer: coarse)` or `(hover: none)` queries; input method is inferred from viewport width.
Fix: Scope hover effects to `@media (hover: hover)`, use `:active` under `(hover: none)`, and size targets by pointer type.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max.

### IN-21 Gesture that updates only on release
Symptom: Dragging a sheet or swiping a card shows nothing until the finger lifts, then the element jumps.
Detect: The UI updates on `pointerup` only, with no per-`pointermove` update; discrete `swipeleft`-style events replace continuous tracking; no animated value is bound to the gesture translation.
Fix: Track the pointer 1:1 from the first move, recognizing all plausible gestures in parallel.
Grade: MAJOR. Sources: apple-design, ui-ux-pro-max.

### IN-22 Tap or drag with no movement threshold
Symptom: Slight finger wobble starts a drag, scroll fights swipe, and dragging off a button cannot cancel the tap.
Detect: A drag starts or a direction locks on the first `pointerdown` or `pointermove` with no distance (about 10px, apple-design) or delay threshold; dragging off a pressed control does not cancel it.
Fix: Require about 10px of movement or a long-press before dragging, then track 1:1, and allow cancel-by-drag on taps.
Grade: MAJOR. Sources: apple-design, ui-ux-pro-max.

### IN-23 Element that looks clickable but is not
Symptom: Part of a card, chip, row or badge that looks clickable collects dead clicks.
Detect: A non-interactive element shares the button's radius, fill, border and padding; a card has hover effects that do nothing; a container shows hover styling or `cursor: pointer` while its click handler sits on a smaller inner element.
Fix: Make anything that looks clickable clickable across its whole extent, and give static badges a visibly different treatment.
Grade: MAJOR. Sources: better-layout, better-accessibility, design-plugin/design-critique.

### IN-24 Focus ring on bare :focus instead of :focus-visible
Symptom: Mouse users see a ring after every click, or the author removes the ring for everyone to avoid that.
Detect: `:focus {` rules or `focus:` variants style the outline or ring with no `:focus-visible` counterpart; `outline: none` has no replacement.
Fix: Style `:focus-visible` only, preferring the browser's unmodified indicator.
Grade: MAJOR. Sources: impeccable, better-accessibility.

### IN-25 High-stakes step with no reassurance or closure
Symptom: Payment, delete or commit steps feel risky, and the flow ends on a blank page or a bare "Success".
Detect: A high-stakes action has no progress indicator, reassurance copy or undo; the flow's most intense moment is an error or a scary confirmation; completion lands on nothing or a bare "Success".
Fix: Add progress, reassuring copy and undo at high-stakes steps, and end with a clear satisfying confirmation.
Grade: MAJOR. Sources: impeccable.

### IN-26 Actions in a group with no visual rank or distinction
Symptom: Primary and secondary actions look identical, and Approve, Reject and Flag cannot be told apart at a glance.
Detect: Two buttons in one group have identical fill with no rank between primary and secondary; opposing actions share one styling with no color coding and no icons.
Fix: Rank primary over secondary, and give differing actions distinct styling and icons.
Grade: MAJOR. Sources: design-review, claude-code-workflows.

### IN-27 Feedback out of sync with its cause
Symptom: A sound, haptic or animation fires at a moment unrelated to the toggle flip or snap it confirms.
Detect: Feedback is triggered on a timer or at gesture start rather than on the causal event; the CSS transition lags the vibration or audio call; channels do not fire on the same frame.
Fix: Fire visual, audio and haptic feedback on the same frame as the causal event, matched to the action's physicality.
Grade: MAJOR. Sources: apple-design.

### IN-28 Drag that jumps on grab or drops when the pointer leaves
Symptom: Dragging jumps the element so the pointer sits at its center, and a fast drag drops it at the edge.
Detect: Drag code sets position to `clientX` or `clientY` without subtracting the grab offset; `pointermove` listeners sit on the element without `setPointerCapture`.
Fix: Keep the grab offset (`grabOffset = e.clientY - rect.top`) and capture the pointer for the whole drag.
Grade: MAJOR. Sources: apple-design.

### IN-29 Drag boundary and release that ignore physics
Symptom: Dragging past the edge freezes the element, and a quick flick back is ignored once past the halfway point.
Detect: `Math.min` or `Math.max` clamps position with no resistance beyond the bound; release logic compares position to a threshold with no check of velocity sign.
Fix: Rubber-band with increasing resistance past the bound, and decide reverse or commit by velocity sign at release.
Grade: MAJOR. Sources: apple-design.

### IN-30 Nested gesture handlers without arbitration
Symptom: A tap inside a draggable inside a horizontal scroller inside a swipe-back stack triggers the wrong action.
Detect: Nested tap, drag, horizontal scroll and back-swipe handlers share one region without `simultaneousHandlers` or `waitFor` arbitration.
Fix: Keep one primary gesture per region and arbitrate any nested gestures explicitly.
Grade: MAJOR. Sources: ui-ux-pro-max.

### IN-31 Horizontal swipe on main content fighting vertical scroll
Symptom: Vertical scrolling fights horizontal swipes on the primary content, so users accidentally page, dismiss or go back.
Detect: A horizontal `PanResponder` or `Swipeable` covers full-screen content; a carousel is the primary layout and is driven only by swipe; `overflow-x: scroll` sections span the viewport.
Fix: Keep vertical scroll primary and limit horizontal swipe to bounded carousels nested inside the vertical scroller.
Grade: MAJOR. Sources: ui-ux-pro-max.

### IN-32 Swipe action with no visible hint
Symptom: Rows can be swiped to reveal actions, but nothing hints at it and users never discover the feature.
Detect: `Swipeable` or gesture-driven rows show no chevron, label, peeking action or first-use coach mark.
Fix: Partially reveal the hidden action, add a chevron or label, or show a first-use hint.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max.

### IN-33 Press state that shifts layout
Symptom: Pressing a button nudges neighboring content or makes the row jitter.
Detect: Pressed styles change `padding`, `margin`, `border-width`, `width` or `height`; neighbors move between captures taken before and during a press.
Fix: Express press states with color, opacity, elevation or `transform` only, keeping layout bounds unchanged.
Grade: MAJOR. Sources: ui-ux-pro-max.

### IN-34 Live data with no connection or freshness indicator
Symptom: Users cannot tell whether data is live, stale or disconnected, and critical alerts do not stand out.
Detect: A real-time view has no connection status indicator, no visible auto-refresh state and no offline fallback; critical alerts are styled like routine rows.
Fix: Show connection status, a refresh indicator, an offline fallback and prominent critical alerts.
Grade: MAJOR. Sources: ui-ux-pro-max.

### IN-35 Custom gesture surface without touch-action none
Symptom: Dragging on a custom pan or zoom surface scrolls or pinch-zooms the page instead.
Detect: Pointer-event drag, pan or zoom handlers sit on a surface with no `touch-action: none`.
Fix: Set `touch-action: none` on the surface that implements its own gestures, and nowhere wider.
Grade: MAJOR. Sources: better-accessibility.

### IN-36 Default 300ms tap delay
Symptom: Taps feel laggy on mobile.
Detect: Interactive elements lack `touch-action: manipulation`, leaving double-tap-to-zoom enabled on controls.
Fix: Apply `touch-action: manipulation` to interactive elements.
Grade: MAJOR. Sources: ui-ux-pro-max, apple-design.

### IN-37 Destructive confirmation focusing the destructive button
Symptom: Pressing Enter as soon as a "Delete?" dialog opens deletes.
Detect: `autofocus` or an initial `.focus()` targets the Delete or Remove button in a destructive confirmation.
Fix: Focus the least destructive action, usually Cancel, when a destructive confirmation opens.
Grade: MAJOR. Sources: better-accessibility.

### IN-38 Focus moved to a toast
Symptom: A notification yanks focus away from the form the user was filling.
Detect: `.focus()` is called on toast elements, or `autofocus` sits inside a toast.
Fix: Announce the toast with a live region and leave focus where the user is working.
Grade: MAJOR. Sources: better-accessibility.

### IN-39 Pointer-events none on a layer the user must hit
Symptom: Clicking the modal backdrop no longer dismisses the dialog.
Detect: `pointer-events: none` is set on a scrim or layer that carries an `onClick` dismiss handler.
Fix: Keep pointer events on any layer the user is meant to hit; a click-to-dismiss scrim is a control.
Grade: MAJOR. Sources: better-accessibility.

### IN-40 Custom cursor effects without touch fallback or in task interfaces
Symptom: Cursor morphs, magnetic pull or trails distract in forms and dashboards and do nothing on touch.
Detect: Custom cursor JS or CSS runs on mobile-first products, forms or dashboards, and the effect has no touch fallback.
Fix: Drop custom cursors in touch and data contexts, and always provide a touch fallback.
Grade: MAJOR. Sources: ui-ux-pro-max, design-taste-frontend.

### IN-41 Exaggerated or misplaced press effect
Symptom: Buttons shrink or glow dramatically on hover or click, feel cartoonish, and bounce where motion distracts.
Detect: `:active` scale, `active:scale-[...]` or `whileTap` is under 0.95 (better-ui, make-interfaces-feel-better); hover transforms exceed a few pixels or percent; hover adds glow shadows; the tap scale applies to every button with no static variant.
Fix: Use `scale(0.96)` exactly (better-ui, make-interfaces-feel-better), gentle hover feedback, and a static variant where motion distracts.
Grade: POLISH. Sources: impeccable, better-ui, make-interfaces-feel-better.

### IN-42 Long operation with no cancel control
Symptom: Users cannot cancel a long operation.
Detect: A long-running loading state has no Cancel control.
Fix: Offer a Cancel control on long operations where cancellation is possible.
Grade: POLISH. Sources: impeccable.

### IN-43 Pull-to-refresh on every scroll container
Symptom: Scrolling up at the top accidentally reloads pages where refresh is meaningless.
Detect: Scroll containers keep default overscroll with no `overscroll-behavior: contain`.
Fix: Set `overscroll-behavior: contain` where pull-to-refresh is not wanted.
Grade: POLISH. Sources: ui-ux-pro-max.

### IN-44 Composite input wrapper not lit with its inner input
Symptom: A search box with an icon inside the border shows focus only on the bare input, breaking the border.
Detect: The wrapper carries the visible border but has no `:focus-within` style; the inner input ring is clipped or misaligned with the wrapper.
Fix: Group focus styles with `:focus-within` on the wrapper.
Grade: POLISH. Sources: better-accessibility.


## Component states (ST)

### ST-01 One component failure taking down the whole page
Symptom: A single failed widget or fetch replaces the entire interface with an error.
Detect: No error boundary around independent regions; one failed request renders a full-page error while unrelated content would still work.
Fix: Isolate failures per region so the rest of the interface keeps working.
Grade: BLOCKING. Sources: impeccable.

### ST-02 Media without playback controls
Symptom: Users cannot pause, seek or mute a video or audio element.
Detect: `<video>` or `<audio>` without the `controls` attribute and no custom control bar in the capture.
Fix: Always render playback controls.
Grade: BLOCKING. Sources: better-accessibility.

### ST-03 Interactive control without hover, focus, active or disabled treatment
Symptom: Controls look identical whether idle, hovered, pressed, focused or disabled, or each component styles these states differently.
Detect: No `:hover`, `:focus-visible`, `:active` or `:disabled` rule on buttons, links, rows or cards; identical captures with and without hover; no `hover:` or `active:` classes; no shared state tokens.
Fix: Define default, hover, focus, active and disabled for every control from shared state tokens.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max, design-review, redesign-existing-projects, claude-code-workflows, design-plugin/design-system, design-plugin/design-handoff.

### ST-04 Empty state that is blank or a dead end
Symptom: An empty list shows white space, an illustration, or a bare "No items" with nothing to do next.
Detect: Empty branch renders null or a single line of text; no explanation of what belongs here, why it is empty, or a primary action such as "Create your first project".
Fix: Explain briefly, state the value, and offer a clear action to create the first item.
Grade: MAJOR. Sources: impeccable, design-taste-frontend, ui-ux-pro-max, redesign-existing-projects, frontend-design, design-plugin/ux-copy, better-writing.

### ST-05 Loading, empty and error states missing
Symptom: Only the happy path is designed; the view is blank while loading, empty, or when a request fails.
Detect: Data-driven components with no loading, empty or error branch; bare "No data" text, unstyled error strings or a raw spinner; throttle the network, empty the data and force an error.
Fix: Design loading, empty, error and success states alongside the default.
Grade: MAJOR. Sources: impeccable, design-taste-frontend, design-review, claude-code-workflows, design-plugin/design-system, design-plugin/design-handoff.

### ST-06 Disabled control that looks enabled
Symptom: A disabled control keeps full emphasis and a pointer cursor, so clicks and taps silently do nothing.
Detect: `disabled` or `[aria-disabled]` elements styled like enabled ones; no opacity reduction (0.38 to 0.5 per ui-ux-pro-max), no `cursor: not-allowed`; a handler gated by a flag while the style and `disabled` attribute are unchanged.
Fix: Apply the disabled attribute, reduced emphasis and a non-pointer cursor together, and remove the handler.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max, design-review.

### ST-07 Failed request with no explanation or retry
Symptom: A failed or stalled request leaves a blank area, an endless spinner, or a cryptic message with no way forward.
Detect: Error branch renders nothing, only `error.message`, or "Failed to load" without a retry button; no request timeout or escape after a long wait; one catch-all message for 401, 403, 404, 429 and 500.
Fix: Say what happened per status, offer "Try again" or the right next step, and time out stalled requests.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max, apple-design.

### ST-08 Unavailable control or gated view with no stated reason
Symptom: A greyed-out button, read-only field or "access denied" screen gives no reason and no way to unlock it.
Detect: `disabled` or `aria-disabled` controls, hidden features or permission-gated views with no adjacent text naming why and what unlocks them; blank or generic access denied screens.
Fix: Say why and what unlocks it beside the control: "Add a payment method to publish".
Grade: MAJOR. Sources: impeccable, better-writing, better-accessibility, ui-ux-pro-max.

### ST-09 Native disabled on a control that must stay focusable
Symptom: Keyboard and touch users cannot reach the control or its explanation, and focus drops to body on submit.
Detect: `disabled` attribute on a control wrapped in a tooltip or carrying a reason; `disabled={isSubmitting}` on the focused submit button; both `disabled` and `aria-disabled="true"` on one element.
Fix: Use `aria-disabled="true"` with a handler guard so it stays focusable; never set both attributes.
Grade: MAJOR. Sources: better-accessibility.

### ST-10 Selected or active item indistinguishable from its neutral siblings
Symptom: The active tab, toggled bookmark or hovered row looks the same as inactive ones.
Detect: Icons with `variant="solid"` regardless of state; inactive tabs or rows carrying the full-chroma accent; hover and active, or hover fill and border, mapped to the same palette step.
Fix: Outline icons and muted color by default; reserve fill and saturated accent for selected, one palette step per role.
Grade: MAJOR. Sources: better-ui, impeccable, better-colors.

### ST-11 Async action with no pending or completion feedback
Symptom: After a click nothing changes while the request runs, repeat clicks fire again, and nothing confirms completion.
Detect: Async handler with no pending branch; submit button still clickable during the request; pending state that replaces the label with a spinner alone; no success toast, message or state change afterwards.
Fix: Show a spinner beside the original label, ignore repeat clicks while pending, and confirm success visibly.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max, better-accessibility, claude-code-workflows, design-plugin/design-handoff, apple-design.

### ST-12 aria-disabled control that still activates or looks enabled
Symptom: A control announces as disabled but still fires on click or Enter, submits the form, or looks live.
Detect: `aria-disabled="true"` with no early return in the handler, no form submission guard, no `[aria-disabled="true"]` style rule and no forced-colors treatment.
Fix: Block pointer, keyboard and submit behavior in code and style the state explicitly, including forced colors.
Grade: MAJOR. Sources: better-accessibility.

### ST-13 Interaction states visible in one theme only
Symptom: Hover, pressed, focused and disabled are visible in light mode but vanish in dark mode, or the reverse.
Detect: State styles without dark variants; a pressed overlay color that is invisible on dark surfaces; compare captures of each state in both themes.
Fix: Keep pressed, focused and disabled states equally distinguishable in light and dark.
Grade: MAJOR. Sources: ui-ux-pro-max.

### ST-14 Connection loss with no feedback
Symptom: Going offline mid-flow produces silent failures, confusing errors or lost work.
Detect: No offline detection, banner or queued-action message; actions fail without saying the connection is the cause.
Fix: Detect offline, say so, and queue or preserve the work until reconnection.
Grade: MAJOR. Sources: impeccable.

### ST-15 View state lost when hidden and shown again
Symptom: Returning to a tab or reopening a collapsed panel resets scroll position, inputs and selections.
Detect: `unmountOnBlur: true` on tab screens; a panel conditionally unmounted on visibility toggle instead of preserved; state not persisted.
Fix: Keep the subtree mounted or persist its state across hide and show.
Grade: MAJOR. Sources: ui-ux-pro-max.

### ST-16 Placeholder or disabled text too faint or indistinguishable from a value
Symptom: Placeholder hints look like entered text, or disabled labels and placeholders cannot be read.
Detect: `::placeholder` color equal to the input text color; `:disabled` or `::placeholder` text with APCA Lc under 30 (better-colors) or opacity so low it is illegible.
Fix: Give placeholder and disabled text at least Lc 30 while keeping it clearly lighter than entered text.
Grade: MAJOR. Sources: design-review, better-colors.

### ST-17 Missing data rendered as raw placeholders
Symptom: Absent fields show "undefined", "null", "NaN" or collapse into an empty gap.
Detect: Render with optional fields missing; literal "undefined", "null" or "NaN" in the capture; rows or cards whose layout collapses around the gap.
Fix: Provide a fallback for every missing value.
Grade: MAJOR. Sources: impeccable.

### ST-18 No-results state with no way out
Symptom: A search or filter returns nothing and the user is stuck.
Detect: Empty search or filter result showing only "No results"; no "clear filters" action or alternative query suggestion.
Fix: Suggest a different query and offer to clear filters.
Grade: MAJOR. Sources: impeccable, better-writing, ui-ux-pro-max.

### ST-19 Long operation with no progress or duration hint
Symptom: An operation running longer than a few seconds shows only a bare spinner or "Loading...".
Detect: Operations over a few seconds (30 seconds or more per impeccable) with a generic indicator; no progress bar, step count or time estimate.
Fix: Set expectations with a step or estimate ("Analyzing your data, usually 30 to 60 seconds") and show progress.
Grade: MAJOR. Sources: impeccable, design-plugin/ux-copy.

### ST-20 Guided tour pointing at empty screens
Symptom: A tour tells users to click real controls on an empty list or table, so the action fails.
Detect: Tour or tutorial steps targeting lists, tables or actions with no seeded data.
Fix: Provide sample data so every tour step works.
Grade: MAJOR. Sources: impeccable.

### ST-21 Button decoration with no purpose
Symptom: A standard button stacks gradient, glow and heavy shadow that carry no meaning and bury its state changes.
Detect: Button styles with several decorative layers at once (gradient plus glow plus heavy `box-shadow`) that stay the same on hover and press.
Fix: Use one plain, consistent button treatment and let state changes carry the signal.
Grade: MAJOR. Sources: impeccable.

### ST-22 Dialog that departs from the standard modal pattern
Symptom: A dialog appears in an unexpected place, cannot be dismissed the usual way, or does not hold focus.
Detect: Modal without an overlay, without an Escape or close control, with focus left behind it, or placed away from the expected position.
Fix: Use the standard modal pattern: overlay, close control, Escape, and contained focus.
Grade: MAJOR. Sources: impeccable.

### ST-23 Loading placeholder that does not match the final layout
Symptom: A spinner replaces the content, or skeleton blocks differ from the loaded shape, so the layout jumps when data arrives.
Detect: `animate-spin` ring or spinner component as the loading state for a layout; skeleton rows whose size or position differ from the rendered component; layout shift on data arrival.
Fix: Use skeleton placeholders shaped to the final layout.
Grade: POLISH. Sources: design-taste-frontend, ui-ux-pro-max.

### ST-24 Generic loading copy
Symptom: Loading text does not say what is loading.
Detect: "Loading..." or a bare spinner as the only loading copy for initial load, pagination and refresh alike.
Fix: Name what is loading: "Loading your projects..." or "Saving your draft...".
Grade: POLISH. Sources: impeccable.

### ST-25 Read-only field styled like a disabled one
Symptom: Intentionally non-editable values look broken or unavailable.
Detect: `readonly` inputs sharing the dimmed disabled style; `readOnly` and `disabled` mapped to the same visual.
Fix: Give read-only a distinct visual and semantic treatment from disabled.
Grade: POLISH. Sources: ui-ux-pro-max.

### ST-26 User-cleared state treated like first use
Symptom: After deliberately deleting everything, the user is re-onboarded with heavy value-proposition messaging.
Detect: The same first-use empty state, with its full value pitch, shown after an intentional clear.
Fix: Use a light touch with an easy path to recreate.
Grade: POLISH. Sources: impeccable.


## Forms (FO)

### FO-01 Input without a visible, associated label
Symptom: The field has no name for screen readers, or its only name is a placeholder that vanishes on typing.
Detect: `<input>`, `<select>` or `<textarea>` with no `<label for>` matching its `id`, no wrapping `<label>`, `aria-label` or `aria-labelledby`; label rendered as a `<span>`; `placeholder="Email"` or floating text as the only name; clicking the label does not focus the field.
Fix: Give every control a persistent visible label associated with `<label for>` or a wrapping `<label>`.
Grade: BLOCKING. Sources: impeccable, design-taste-frontend, ui-ux-pro-max, design-review, claude-code-workflows, design-plugin/accessibility-review, better-accessibility.

### FO-02 Typed input lost on error, re-render or hydration
Symptom: After a failed submit, a re-render or hydration, typed values vanish or the cursor leaves the field.
Detect: Form state reset or page reload on failed submission; controlled inputs re-keyed on render, changing `key` props, hydration overwriting `value`; type during load and watch the field.
Fix: Preserve typed values and focus through errors, re-renders and hydration.
Grade: BLOCKING. Sources: impeccable, better-accessibility.

### FO-03 Double submission possible
Symptom: Rapid or repeated clicks on submit send the request several times and create duplicates.
Detect: Submit button still active while the request is pending; `aria-disabled="true"` set on pending with no early return in the handler; click submit ten times and count the requests.
Fix: Ignore repeat clicks in the handler while pending and show the pending state.
Grade: BLOCKING. Sources: impeccable, better-accessibility.

### FO-04 Input text under 16px on mobile
Symptom: iOS Safari zooms the whole page when the input is focused.
Detect: `<input>` with `text-sm`, `14px` or any `font-size` under `16px` at mobile widths and no mobile override.
Fix: Size inputs to `16px` on mobile (`text-base sm:text-sm`), or keep `16px` and render smaller with `transform: scale()`.
Grade: BLOCKING. Sources: better-typography.

### FO-05 High-stakes deletion without a working typed confirmation
Symptom: Deleting an account, workspace or repository is one click away, or the confirm button is live before the name matches.
Detect: Delete flow for an account, workspace or repository with no type-the-name step; a "Type 'acme-web' to confirm" field whose button is enabled while the input does not match.
Fix: Require typing the object's name and keep the button disabled until it matches.
Grade: BLOCKING. Sources: better-writing.

### FO-06 Paste blocked on an input
Symptom: Users cannot paste a password, one-time code or other value.
Detect: `onPaste` handler calling `preventDefault()` or any other paste suppression on an input.
Fix: Never block paste.
Grade: BLOCKING. Sources: better-accessibility.

### FO-07 Error shown away from the field that failed
Symptom: Errors pile up in a banner, summary, toast or browser alert while the failing field itself looks normal.
Detect: Single error container above or below the form; `window.alert(` in form handlers; errors in a toast; error text rendered above the input or outside its container with no inline message.
Fix: Render each error directly below its field.
Grade: MAJOR. Sources: impeccable, design-taste-frontend, ui-ux-pro-max, redesign-existing-projects, better-accessibility, better-writing.

### FO-08 Validation timed too early, too late, or inconsistently
Symptom: A field turns red on the first keystroke, or users fill the whole form before learning about errors.
Detect: Validation in `onChange` or `onInput` rendering errors before blur (`mode: "onChange"`); validation only in the submit handler with no blur validation; mixed blur, change and submit timing across fields.
Fix: Validate on blur and again on submit, consistently; password strength meters are the exception.
Grade: MAJOR. Sources: impeccable, apple-design, ui-ux-pro-max.

### FO-09 Wrong input type or inputmode for the field
Symptom: Phone, email and amount fields open the full alphabetic keyboard, or a code field shows a number spinner.
Detect: `type="text"` without `inputmode` on email, phone, URL, numeric or decimal fields; native `keyboardType` left default with no `returnKeyType`; `type="number"` on one-time codes, PINs or card numbers.
Fix: Use `type="email"`, `tel`, `url`, `inputmode="decimal"` as fitting, and `type="text" inputmode="numeric"` for codes.
Grade: MAJOR. Sources: ui-ux-pro-max, better-accessibility.

### FO-10 Field the browser cannot autofill
Symptom: The browser, password manager or OS never offers saved emails, addresses, cards or one-time codes.
Detect: Name, email, phone, address, card, password or OTP inputs without a valid `autocomplete` token (`email`, `tel`, `cc-number`, `current-password`, `one-time-code`); `autocomplete="off"` on login; inputs outside a `<form>`; missing or generic `name`; div-based inputs; field names renamed in a redesign.
Fix: Use a real form, descriptive stable `name` attributes and the matching `autocomplete` token, sectioned where relevant.
Grade: MAJOR. Sources: impeccable, design-taste-frontend, ui-ux-pro-max, better-accessibility.

### FO-11 Inline error not announced with its field
Symptom: The error text is visible but screen readers never report the field as invalid or read the message.
Detect: Failing input without `aria-invalid="true"`, or a static `aria-invalid` never removed after the fix; error element with no `id` referenced by the input's `aria-describedby`; error or counter placed in `role="alert"` or `role="status"` instead.
Fix: Set `aria-invalid="true"` while failing and point `aria-describedby` at the inline error.
Grade: MAJOR. Sources: impeccable, design-review, better-accessibility, ui-ux-pro-max.

### FO-12 Required fields unmarked or inconsistently marked
Symptom: Users learn which fields are mandatory only after a failed submit, or the marker is never explained.
Detect: `required` inputs with no asterisk or "(required)" in the label; required logic only in JS with no `required` attribute; asterisks on one form and text on another; no "* required" legend once per form.
Fix: Use native `required` plus one visible indicator, explained once per form, or mark optional fields when most are required.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max, better-accessibility.

### FO-13 Submit disabled until the form is valid
Symptom: The submit button is greyed out while the form is being filled, with no way to learn what is missing.
Detect: `disabled={!isValid}` or `disabled` bound to validity or dirtiness rather than to a pending request; submit rejected for optional or minor issues.
Fix: Keep submit enabled until the request starts and validate on submit.
Grade: MAJOR. Sources: impeccable, better-accessibility.

### FO-14 Known constraint not shown before input
Symptom: Users discover length, format or password rules only after failing them.
Detect: Fields with format or length rules and no persistent hint before the user types; rule only in the placeholder, only in the error, or rendered after the submit button; no `maxlength` or `pattern`; hint not linked via `aria-describedby`.
Fix: State the rule as persistent helper text tied to the field with `aria-describedby`.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max, better-writing, claude-code-workflows, design-plugin/accessibility-review.

### FO-15 Form asking for more than the task needs
Symptom: Signup or lead forms demand phone, company size or role with no reason given.
Detect: Many required fields at signup; lead form over 3 fields (ui-ux-pro-max), newsletter form beyond email, conversion form over 5 fields (ui-ux-pro-max); sensitive or unexpected fields with no helper text saying why.
Fix: Collect the minimum now, explain each non-obvious ask, and defer the rest.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max.

### FO-16 Error message that does not say how to fix it
Symptom: The error says a value is wrong but not what a right one looks like, and wording varies between fields.
Detect: Messages like "Invalid" or "Incorrect format" with no example or rule; different phrasing patterns for similar validation errors in one form.
Fix: Name the problem and the correction ("Enter a date as DD/MM/YYYY") in one consistent pattern.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max.

### FO-17 Password field with no show toggle
Symptom: Users cannot verify what they typed and mistype passwords repeatedly.
Detect: `type="password"` or `secureTextEntry` with no show or hide control.
Fix: Add a show or hide toggle to every password field.
Grade: MAJOR. Sources: ui-ux-pro-max.

### FO-18 Submit with no visible response
Symptom: After pressing submit nothing visibly happens, then the page silently changes or silently fails.
Detect: Submit handler with no pending state and no success or error state rendered afterwards.
Fix: Show a pending state, then an explicit success or error state.
Grade: MAJOR. Sources: ui-ux-pro-max.

### FO-19 Long form or dirty modal that loses work
Symptom: A refresh, back swipe, crash or tap outside a modal wipes minutes of input.
Detect: Multi-section forms or editors with state only in memory; no draft persistence or unsaved-changes warning; modal or sheet with dirty state dismissed on outside tap or swipe without confirmation.
Fix: Autosave drafts and confirm before discarding unsaved changes.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max, better-accessibility.

### FO-20 Combobox that breaks the keyboard flow
Symptom: Arrowing through suggestions pulls focus out of the text field, or the list cannot be navigated, accepted or dismissed.
Detect: Options receive `.focus()` while the user types; no `aria-activedescendant` on the input; no ArrowDown to open, Enter to accept or Escape to close; typing does not filter.
Fix: Keep DOM focus in the input, update `aria-activedescendant`, and implement the APG combobox key map.
Grade: MAJOR. Sources: better-accessibility.

### FO-21 Label that does not name the data
Symptom: Users misread what a field is for, or the label crams in abbreviations and format codes.
Detect: Generic labels or placeholders ("Enter value", "Type here"); ambiguous labels ("Name" for company or person, "Date" without which); abbreviations and format strings inside `<label>` ("DOB (MM/DD/YYYY)").
Fix: Name the data in plain words ("Date of birth", "Company name") and put the format in a hint.
Grade: MAJOR. Sources: impeccable.

### FO-22 Invalid input accepted silently
Symptom: Bad emails, blank required fields and malformed values submit, or fail with no feedback.
Detect: Inputs without `required`, `type="email"`, `pattern` or script validation; enter a bad email or leave a required field blank and no inline error appears.
Fix: Validate on the client and show a clear inline error.
Grade: MAJOR. Sources: redesign-existing-projects, claude-code-workflows.

### FO-23 First invalid field not focused after a failed submit
Symptom: After submit, errors appear but focus stays on the button, so keyboard and screen reader users notice nothing.
Detect: Submit handler sets error state but calls no `.focus()` on the first invalid input.
Fix: Focus the first invalid field on a failed submit.
Grade: MAJOR. Sources: better-accessibility.

### FO-24 Checkbox and its text with a dead zone between them
Symptom: Clicking the text, or the gap between box and text, does not toggle the checkbox.
Detect: `<input type="checkbox">` followed by a sibling `<span>` with no wrapping `<label>` or `for` association; click the gap between them.
Fix: Wrap the input and its text in one `<label>` so they share one hit target.
Grade: MAJOR. Sources: better-accessibility.

### FO-25 Toggle labeled for its off state
Symptom: "Don't send read receipts" turns the switch into a double negative when it is off.
Detect: Switch or checkbox labels starting with "Don't", "Disable" or "Hide".
Fix: Label the toggle for what happens when it is on: "Send read receipts".
Grade: MAJOR. Sources: better-writing.

### FO-26 Free text where a constrained control fits
Symptom: Users type dates, countries, booleans or bounded numbers freehand and make format errors.
Detect: Text inputs for dates, times, enumerations, booleans or bounded ranges where a date picker, select, toggle, checkbox or slider fits.
Fix: Use the control that prevents invalid input.
Grade: MAJOR. Sources: impeccable, claude-code-workflows.

### FO-27 Input rejected or filtered before the user finishes
Symptom: Keystrokes vanish, partial values are refused, or an autofilled value with a trailing space fails for no visible reason.
Detect: `onKeyDown` or `onChange` handlers that `preventDefault()` or strip characters live; masked inputs rejecting partial values; validation regex applied to the raw value with no `.trim()`.
Fix: Accept free text, trim it, and validate after.
Grade: MAJOR. Sources: better-accessibility.

### FO-28 Form controls that look like different systems
Symptom: Inputs, selects and checkboxes on one surface differ in height, radius, border, focus style or spacing.
Detect: Differing heights, radii, borders and focus rings across controls; irregular gaps between field blocks instead of one standard gap.
Fix: Use one form-control vocabulary and one block gap across the surface.
Grade: MAJOR. Sources: impeccable, design-taste-frontend.

### FO-29 Input with no visible boundary
Symptom: Fields are invisible until focused; users do not know where to type.
Detect: Inputs with `border-0` or `border-none` and no background difference from the page (ui-ux-pro-max spec: light `#CCCCCC` border on white).
Fix: Give inputs a distinct border or background.
Grade: MAJOR. Sources: ui-ux-pro-max.

### FO-30 Fields run together with no grouping
Symptom: Address, payment and contact fields run on in one undifferentiated column.
Detect: More than 4 fields before a heading, divider or spacing break (impeccable); no `fieldset` and `legend` or section headings between logical groups.
Fix: Group related fields with `fieldset` and `legend` or clear sections, at most 4 fields per group.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max.

### FO-31 Scaled-input workaround applied incompletely
Symptom: A scaled input leaves an end gap, loses its leading, shifts off the start edge, or shrinks its ring.
Detect: `scale-[0.8125]` on an input without `w-[calc(100%/0.8125)]` and `shrink-0`; `line-height` not divided by the factor; no `origin-left rtl:origin-right`; `bg-*`, `border`, `ring` or `outline` on the scaled element.
Fix: Widen by the inverse scale, divide line-height, pin origin to the start edge, draw surface and ring on a wrapper.
Grade: MAJOR. Sources: better-typography.

### FO-32 Mobile input height below 44px
Symptom: Inputs are thin strips that are hard to tap on a phone.
Detect: Input `height` or `min-height` under 44px at mobile widths (`h-8`, `h-9`, `py-1`).
Fix: Make mobile inputs at least 44px tall.
Grade: MAJOR. Sources: ui-ux-pro-max.

### FO-33 Multi-step flow without progress indication
Symptom: Booking, registration or signup spans many steps with no sense of how many remain.
Detect: Multi-step forms with no step count, progress bar or named stages; steps that could be merged.
Fix: Shorten the flow and show a step indicator.
Grade: MAJOR. Sources: ui-ux-pro-max, impeccable.

### FO-34 Enter behavior hijacked in text inputs
Symptom: Enter in a single-line input does not submit, or Enter in a textarea submits instead of inserting a newline.
Detect: `onKeyDown` handlers that `preventDefault()` Enter on single-line inputs, or submit on bare Enter in `<textarea>`.
Fix: Let Enter submit single-line inputs; in a textarea Enter inserts a newline and only Cmd or Ctrl plus Enter submits.
Grade: MAJOR. Sources: better-accessibility.

### FO-35 Custom control that drops native behavior for no gain
Symptom: A hand-built select, checkbox or date picker confuses fluent users and loses keyboard or mobile picker behavior.
Detect: Custom replacement for a native control with no functional gain; native keyboard, mobile picker or autofill behavior missing from it.
Fix: Use the standard control and its affordances.
Grade: MAJOR. Sources: impeccable.

### FO-36 Hit-area pseudo-element placed on the input itself
Symptom: The extended tap target never renders on a checkbox or radio.
Detect: `input::before` or `input::after` used to extend the target.
Fix: Put the pseudo-element on a wrapping element or the button; form controls do not render it reliably.
Grade: MAJOR. Sources: better-accessibility.

### FO-37 Field left empty when a default, template or example exists
Symptom: Country, currency, date or quantity start blank, settings have no reset, and editors open on a blank slate.
Detect: Empty fields where context could prefill; required choices for values with obvious defaults; no "Reset to defaults"; no starter templates or example values.
Fix: Prefill sensible defaults, offer templates or examples, and provide a reset.
Grade: POLISH. Sources: impeccable, claude-code-workflows.

### FO-38 Placeholder that instructs instead of showing an example
Symptom: The placeholder reads "Enter your email", or a sentence of helper text spells out a format an example would show.
Detect: `placeholder` text that is an imperative sentence; a hint such as "Enter the date in month, day, year format" with no example.
Fix: Show a realistic example in the accepted format: `name@example.com`, `DD/MM/YYYY`.
Grade: POLISH. Sources: impeccable, better-writing.

### FO-39 Auto-focus where it disorients
Symptom: Focus jumps into a field on load, scrolling the page or disorienting screen reader users.
Detect: `autofocus` or programmatic focus on fields in modals, long pages or non-primary contexts.
Fix: Auto-focus only the single primary field of a focused task.
Grade: POLISH. Sources: impeccable.

### FO-40 Return key not advancing to the next field on mobile
Symptom: Users must tap each field manually to continue through a native form.
Detect: No `onSubmitEditing` focusing the next field's ref; no `returnKeyType`; `blurOnSubmit` unhandled.
Fix: Move focus to the next field from the return key and set a matching return key label.
Grade: POLISH. Sources: ui-ux-pro-max.

### FO-41 Spellcheck left on for emails, codes and usernames
Symptom: Red squiggles under email addresses and codes, with autocorrect mangling them.
Detect: Email, code or username inputs without `spellcheck="false"`.
Fix: Disable spellcheck on emails, codes and usernames.
Grade: POLISH. Sources: better-accessibility.

### FO-42 Fully custom caret
Symptom: A hand-built insertion bar lags, misaligns or disappears.
Detect: A custom-rendered caret element instead of `caret-color`.
Fix: Tint the native caret with `caret-color`.
Grade: POLISH. Sources: better-typography.


## Navigation and information architecture (NA)

### NA-01 Onboarding that blocks the product with no visible skip
Symptom: A tour or modal sequence stands between the user and the product, and no skip control is obvious.
Detect: Product routes gated behind onboarding completion; overlay with no "Skip" or "Back" button, or "Skip" as small muted text off the natural path; no replay entry afterwards.
Fix: Make onboarding optional with a visible skip and back, allow free click-through, and offer a replay.
Grade: BLOCKING. Sources: impeccable, ui-ux-pro-max.

### NA-02 Modal or wizard with no cancel, close, or back
Symptom: Once inside a dialog or multi-step flow the user cannot leave except by completing it or refreshing.
Detect: Dialog markup with no close button, no Escape handler, no backdrop dismiss, and no swipe-down on mobile; wizard steps or forms with only "Next" or "Submit".
Fix: Give every modal a close control and every step a cancel, back, or save-and-leave option.
Grade: BLOCKING. Sources: impeccable, ui-ux-pro-max.

### NA-03 Back that exits, resets, or skips history
Symptom: Pressing back leaves the app, jumps to home, loops, or loses several screens of history.
Detect: Custom back handlers calling navigate to home, reset, or exitApp on first press; replace used where push is expected; replaceState wiping the stack; modals and tabs outside history.
Fix: Push history on in-app navigation, go back one step, and never reset the stack silently.
Grade: BLOCKING. Sources: ui-ux-pro-max.

### NA-04 Hidden content with no visible cue
Symptom: A horizontal row ends flush at the edge or a collapsed section shows nothing, so the rest is never found.
Detect: `overflow-x: auto` scroller whose last visible item ends at the container edge with no 16 to 32px peek, fade, or arrow; collapsed section with no chevron or label.
Fix: Let the next item peek 16 to 32px, add an edge fade or arrow, or show a disclosure control.
Grade: BLOCKING. Sources: better-interface, better-layout.

### NA-05 Primary task blocked or needed function removed
Symptom: The main task cannot be completed; a control users need is missing, unreachable, or was cut for simplicity.
Detect: Walk the primary flow in the capture; a required control is absent or unreachable; the diff deletes a feature a task depends on.
Fix: Make the primary task completable and obvious; never remove necessary functionality to simplify.
Grade: BLOCKING. Sources: design-plugin/design-critique, impeccable.

### NA-06 Dropdown clipped or buried by its container
Symptom: A menu is cut off at the edge of its card or renders beneath sibling elements.
Detect: `position: absolute` dropdown inside a parent with `overflow: hidden` or `overflow: auto`, a transform, or a lower stacking context; no `popover` attribute, portal, or `position: fixed`.
Fix: Render the menu in the top layer with `popover`, a portal, or `position: fixed`.
Grade: BLOCKING. Sources: impeccable.

### NA-07 Anchor positioning with no fallback
Symptom: Dropdowns sit at the viewport origin or are mispositioned in Firefox and Safari.
Detect: `position-anchor`, `position-area`, or `@position-try` with no JavaScript or fixed-position fallback; support is limited to Chrome 125 and Edge 125 and later.
Fix: Add a `position: fixed` fallback computed from `getBoundingClientRect()` for browsers without anchor positioning.
Grade: BLOCKING. Sources: impeccable.

### NA-08 Page or step with no route back or to core navigation
Symptom: A deep page, sub-flow, or drill-down offers no way back, home, or to top-level sections.
Detect: Nested routes with no logo-home link, back link, breadcrumb, or close; sub-flow screens with no tab bar or sidebar; drill-down state with no back control; mobile sub-screens relying on browser chrome.
Fix: Give every screen a back route and keep core navigation reachable from deep pages.
Grade: MAJOR. Sources: impeccable, redesign-existing-projects, apple-design, ui-ux-pro-max.

### NA-09 Unfamiliar navigation pattern replacing a convention
Symptom: A custom nav metaphor or desktop convention replaces the pattern users expect on the platform.
Detect: Custom scroll, gesture, or nav behavior where a top bar, side nav, tabs, or breadcrumbs would do; hover menus, right-click, or desktop popovers at mobile widths; drawer as iOS top-level nav; no Android top app bar.
Fix: Use the platform's familiar pattern, including bottom sheets on mobile, unless testing proves the novelty better.
Grade: MAJOR. Sources: impeccable, apple-design, ui-ux-pro-max.

### NA-10 No current-location indicator
Symptom: Every nav link looks identical, so users cannot tell which page or section they are on.
Detect: Nav items with no `aria-current="page"` and no active color, weight, underline, or indicator; no breadcrumbs or progress cue on deep pages.
Fix: Style the active item differently, set `aria-current`, and add breadcrumbs on deep pages.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max, redesign-existing-projects, apple-design.

### NA-11 Unnecessary steps between intent and result
Symptom: A simple task takes extra screens, confirmations, or clicks that add nothing.
Detect: Count clicks from entry to completion of the primary action; interstitial screens with one option; confirmations on safe actions; signup or checkout steps that collect nothing essential; promotional interruptions in task flows.
Fix: Remove steps that add no value and surface the primary action directly.
Grade: MAJOR. Sources: impeccable, claude-code-workflows, design-plugin/design-critique.

### NA-12 Illogical or unpredictable information architecture
Symptom: Users cannot predict where features live and must memorize the structure to get around.
Detect: Related features in different nav sections; nav labels that differ from page titles; inconsistent placement across screens; multi-level nested menus with no breadcrumbs; no clear section order on the page.
Fix: Group related items together, name sections consistently, flatten deep nesting, and keep placement stable.
Grade: MAJOR. Sources: impeccable, claude-code-workflows, design-plugin/design-critique, ui-ux-pro-max.

### NA-13 Onboarding that teaches everything upfront
Symptom: A long tour or dense first screen explains every feature before the user has done anything real.
Detect: Tour with more than 7 steps; upfront feature carousel or multi-paragraph tour step; dedicated tutorial screens or mock components not shared with the product; no point-of-use hints or empty-state guidance.
Fix: Teach the few features that deliver value, in context, with real functionality, in 3 to 7 steps.
Grade: MAJOR. Sources: impeccable, design-plugin/ux-copy.

### NA-14 Modal used for routine edits or primary flows
Symptom: Single-field edits, settings, and detail views open dialogs; core flows run through stacked modals that break back and URL.
Detect: `<dialog>`, `role="dialog"`, or modal components triggered by edit buttons for one field, small confirmations, or detail views; primary destinations rendered as dialogs rather than routes; modals stacked on modals.
Fix: Edit inline or in a panel, give primary flows real routes, and keep modals for interruptions.
Grade: MAJOR. Sources: impeccable, redesign-existing-projects, ui-ux-pro-max.

### NA-15 Link text that does not name its destination
Symptom: Links read "Click here", "here", or several identical "Learn more", and make no sense out of context.
Detect: Link text "Click here" or "here"; two or more links with identical generic text on one page; link labels that do not predict the destination.
Fix: Write the destination into the link: "Read the billing docs", "Learn more about exports".
Grade: MAJOR. Sources: better-writing, impeccable.

### NA-16 Too many top-level navigation items
Symptom: The main nav or tab bar is too long to scan, crowds its icons, truncates labels, or wraps.
Detect: More than 5 top-level items without grouping (impeccable, ui-ux-pro-max); 6 or more bottom tabs where 3 to 5 is the range (ui-ux-pro-max); nav wrapping or overflowing at 1024px (design-taste-frontend).
Fix: Keep at most five top-level items on one line and group the rest under "More" or clear categories.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max, design-taste-frontend.

### NA-17 Search missing, buried, or blank until Enter
Symptom: Content-heavy views lack search or filters, or search hides in a menu and shows nothing until Enter.
Detect: Long tables, docs, or dashboards with no search field or filter controls; filters hidden behind icons; no search entry in the top bar or tab bar; no debounced suggestions, recent queries, or recent items.
Fix: Put search in the top bar, expose filters, and show suggestions and recents as the user types.
Grade: MAJOR. Sources: ui-ux-pro-max, impeccable.

### NA-18 Icon-only navigation
Symptom: Nav items show an icon with no visible text, so first-time users must guess each destination.
Detect: Sidebar, tab bar, or bottom nav items with only an icon and no visible label; `showLabel: false`; tooltips do not count as labels.
Fix: Pair every navigation icon with a visible text label.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max.

### NA-19 Vague or jargon navigation labels
Symptom: Nav items say "Items", "Things", or internal module names that users do not recognize.
Detect: Generic nouns such as "Items" or "Stuff" in navigation; codenames, module names, or database terms as labels; labels that do not predict where the link leads.
Fix: Use specific, user-facing labels such as "Your projects", "Team members", "Settings".
Grade: MAJOR. Sources: impeccable, design-plugin/design-critique.

### NA-20 Navigation levels mixed or nested
Symptom: Sub-sections appear in the bottom bar, utility links sit among core sections, or several nav patterns cover one level.
Detect: Bottom nav items that are not top-level screens or that change per section; tab bar, sidebar, and bottom nav rendering the same destinations at once; settings, help, and account links in the primary bar.
Fix: Use one pattern per hierarchy level, reserve the bottom bar for top-level screens, and move utility links to secondary navigation.
Grade: MAJOR. Sources: ui-ux-pro-max.

### NA-21 Route change that leaves title and focus stale
Symptom: Client-side navigation swaps the view silently; the tab title stays the same and focus stays on the old link.
Detect: Router with no `document.title` update or focus move on route change; a static `<title>` across routes; title ordered site first and page last (WCAG 2.4.2).
Fix: Set a page-specific title, most specific first, and move focus to the new `<h1>` or `<main>` on route change.
Grade: MAJOR. Sources: better-accessibility, ui-ux-pro-max.

### NA-22 Conversational, voice, or zero interface hiding needed controls
Symptom: Forms, data grids, or explicit controls are replaced by chat, voice, or predicted actions users cannot see.
Detect: Chat layout on data-heavy dashboards, traditional forms, or print-first content; voice-primary interaction with no visual fallback or unclear listening state; minimal UI with hidden predictions on data-entry products.
Fix: Provide a full visual UI with explicit controls and keep chat or voice optional.
Grade: MAJOR. Sources: ui-ux-pro-max.

### NA-23 Navigation not adapted to the viewport
Symptom: The full desktop nav tree is crammed into a phone header, or a hamburger appears on desktop.
Detect: One nav presentation across all sizes; multi-level menus rendered at mobile widths; hamburger as the only nav at 1024px and above.
Fix: Stage navigation: drawer or bottom nav on mobile, compact horizontal on tablet, full labeled nav on desktop.
Grade: MAJOR. Sources: impeccable.

### NA-24 Primary actions buried in menus or drawers
Symptom: Users must remember where features live because primary actions sit in overflow, context, or hamburger menus.
Detect: Main actions such as "Create" or "Checkout" inside a drawer, overflow menu, or reachable only by right-click.
Fix: Keep primary actions visible on screen and use drawers and menus for secondary items.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max, apple-design.

### NA-25 Actions crammed with no overflow menu
Symptom: A toolbar wraps to a second line, shrinks its icons, or shows a row of four or more secondary buttons.
Detect: More action buttons than fit the width; icons scaled down or tightly packed; more than 3 secondary actions visible at the top level with no "More" menu.
Fix: Put secondary actions behind an overflow menu once there are more than three.
Grade: MAJOR. Sources: ui-ux-pro-max, better-layout.

### NA-26 Button used for navigation
Symptom: A control that goes somewhere cannot be opened in a new tab, middle-clicked, or copied as a link.
Detect: `<button>` whose handler calls `router.push`, `navigate(...)`, or sets `location.href`; `<a>` without `href`; test Cmd or Ctrl click and middle-click on the control.
Fix: Render anything that navigates as a real `<a href>`, styled as a button if needed.
Grade: MAJOR. Sources: better-accessibility.

### NA-27 Navigation structure that differs between contexts or revisions
Symptom: Mobile and desktop organize features differently, or a redesign renames nav labels, slugs, and anchors.
Detect: Different nav labels, groupings, or hierarchies across breakpoints; the diff renames primary nav labels, page slugs, or anchor IDs without being asked.
Fix: Keep one information architecture across contexts and keep labels, slugs, and anchors stable unless asked.
Grade: MAJOR. Sources: impeccable, design-taste-frontend.

### NA-28 Scroll and state lost on back
Symptom: Returning to a list lands at the top with filters cleared, or a new page keeps the old scroll offset.
Detect: List screens remounting on back; filter state not persisted in the URL or store; scroll restoration disabled on history traversal; new routes not scrolled to top.
Fix: Restore scroll, filters, and input on back and forward, and scroll to top on a new navigation.
Grade: MAJOR. Sources: ui-ux-pro-max, better-accessibility.

### NA-29 Key screens not reachable by URL
Symptom: Switching tabs, filters, or views never changes the URL, so refresh or a shared link loses the state.
Detect: One URL for all states; no query params or hash updated on state change; detail screens reached only through in-memory navigation; notifications landing on home.
Fix: Reflect view and state in the URL and give every key screen a route or deep link.
Grade: MAJOR. Sources: ui-ux-pro-max.

### NA-30 Dropdown that drifts or overflows the viewport
Symptom: A menu near the screen edge extends off-screen, or it separates from its trigger on scroll or resize.
Detect: Fixed or absolute dropdown with no viewport boundary check or flip logic; position computed once from `getBoundingClientRect()` with no scroll or resize listeners.
Fix: Flip above when it would overflow the bottom, right-align at the right edge, and recalculate on scroll and resize.
Grade: MAJOR. Sources: impeccable.

### NA-31 No visible help entry point
Symptom: Users who get stuck cannot find help or documentation.
Detect: No help link, search, or docs entry visible in the interface; help buried in a footer.
Fix: Make help easy to find and searchable from the main interface.
Grade: MAJOR. Sources: impeccable.

### NA-32 Scroll-driven narrative that hides navigation
Symptom: A scroll-jacked or chapter-based story takes over the wheel; navigation disappears and there is no skip.
Detect: Horizontal track or chapter reveals driven by scroll hijacking; nav not visible during the track; no progress indicator; no skip to content or specs.
Fix: Keep navigation visible, show progress, and offer a skip past the narrative.
Grade: MAJOR. Sources: ui-ux-pro-max.

### NA-33 Overlay without light dismiss or top-layer stacking
Symptom: Clicking outside a dropdown does not close it, and overlays fight each other with z-index.
Detect: Tooltips or dropdowns built from positioned divs with manual outside-click handlers and escalating `z-index` values; no `popover` attribute.
Fix: Use the Popover API (`popover` with `popovertarget`) for light dismiss and top-layer stacking.
Grade: MAJOR. Sources: impeccable.

### NA-34 Destructive items styled like normal navigation
Symptom: "Delete account" and "Log out" sit in the same list and style as "Profile" and "Notifications".
Detect: Destructive entries not separated by spacing or a divider and not styled in the danger color.
Fix: Separate dangerous actions visually and spatially from normal navigation items.
Grade: MAJOR. Sources: ui-ux-pro-max.

### NA-35 Links that lead nowhere
Symptom: Buttons and links look live but go nowhere.
Detect: `href="#"` or `href=""` on visible links and buttons.
Fix: Link to real destinations or visibly disable the control.
Grade: MAJOR. Sources: redesign-existing-projects.

### NA-36 No way to clear filters, search, or selections
Symptom: Users get stuck in a filtered or selected state.
Detect: Filter chips with no remove control; search input with no clear; multi-select with no "Clear all".
Fix: Add an easy clear or reset for filters, search, and selections.
Grade: MAJOR. Sources: impeccable.

### NA-37 Menu role on site navigation
Symptom: Screen readers announce app-style menu behavior that the nav list does not implement.
Detect: `role="menu"` or `role="menuitem"` on a `<nav>` list of links.
Fix: Mark site navigation as `<nav>` with a list; reserve `menu` for app menus with arrow-key behavior.
Grade: MAJOR. Sources: better-accessibility.

### NA-38 Oversized navigation bar
Symptom: A huge header eats around 15 percent of the viewport.
Detect: Nav height above 80px at desktop where 64 to 72px is the default; `h-24`, `py-8`, or larger on the header.
Fix: Cap desktop nav height at 80px.
Grade: MAJOR. Sources: design-taste-frontend.

### NA-39 Settings not grouped
Symptom: A long flat list of unrelated settings.
Detect: No sections or tabs in the configuration panel.
Fix: Group related settings into sections or tabs.
Grade: MAJOR. Sources: claude-code-workflows.

### NA-40 No next steps after the first success
Symptom: After the first real action the user lands on a blank dashboard.
Detect: Post-completion state with no suggested actions.
Fix: Offer clear next steps after the first success.
Grade: MAJOR. Sources: impeccable.

### NA-41 Slides without navigation controls
Symptom: An HTML deck cannot be advanced by keyboard or click and shows no progress.
Detect: No arrow-key handler, click-to-advance, or progress bar in the slide markup.
Fix: Add keyboard arrows, click navigation, and a progress bar.
Grade: MAJOR. Sources: ui-ux-pro-max.

### NA-42 No legal links in the footer
Symptom: The footer lacks privacy policy and terms of service links.
Detect: No "Privacy" or "Terms" link in the footer.
Fix: Add privacy policy and terms links.
Grade: MAJOR. Sources: redesign-existing-projects.

### NA-43 No shortcuts, bulk actions, or saved views for repetitive work
Symptom: Frequent actions need the mouse every time, one item at a time, in a fixed layout.
Detect: No keydown handlers or shortcut hints for common actions; no multi-select in a tool used repeatedly; fixed columns or dashboard layout with no saved views.
Fix: Add keyboard shortcuts, bulk selection, and relevant customization for power users.
Grade: POLISH. Sources: impeccable, claude-code-workflows.

### NA-44 Breadcrumbs missing on deep pages or present on flat ones
Symptom: Three or more levels deep there is no trail back up, or a single-level site shows a breadcrumb.
Detect: Nested routes 3 or more levels deep, or drill-down analytics, with no breadcrumb component; breadcrumb on pages with fewer than 3 levels; drill-down with no deep links.
Fix: Add breadcrumbs consistently for hierarchies 3 or more levels deep and drop them elsewhere.
Grade: POLISH. Sources: ui-ux-pro-max.

### NA-45 No contextual help at the point of confusion
Symptom: Confusing fields and controls offer no hint, and getting help means leaving the task.
Detect: Non-obvious inputs with no helper text, tooltip, or info icon; help links that open a separate site with no inline panel.
Fix: Add inline hints, tooltips, or panels so help is available without leaving the context.
Grade: POLISH. Sources: impeccable.

### NA-46 Secondary content expanded at the top level
Symptom: Rarely used options and every detail section are visible at once in one long view.
Detect: No "Advanced" toggle or accordion; long scrolling views with every secondary section expanded inline.
Fix: Hide advanced and secondary content behind progressive disclosure and link deeper.
Grade: POLISH. Sources: claude-code-workflows, better-layout.

### NA-47 Badges overused or never cleared
Symptom: Several tabs carry red badges permanently, so they stop meaning anything.
Detect: Badge counts on multiple nav items; a badge not reset after the user visits the destination.
Fix: Use badges sparingly and clear them once the destination is visited.
Grade: POLISH. Sources: ui-ux-pro-max.

### NA-48 In-page anchor that jumps instead of scrolling
Symptom: Clicking an in-page link snaps instantly, and the user loses the sense of where they moved.
Detect: `<a href="#section">` links with no `scroll-behavior: smooth` on `html`.
Fix: Set `html { scroll-behavior: smooth }` and disable it under `prefers-reduced-motion`.
Grade: POLISH. Sources: ui-ux-pro-max.

### NA-49 Settings path described instead of linked
Symptom: Copy says "Go to Settings > Notifications > Email" with no link.
Detect: Breadcrumb-style navigation instructions in strings with no link to the destination.
Fix: Link straight to the referenced setting, such as a "Notification settings" link.
Grade: POLISH. Sources: better-writing.

### NA-50 Footer link farm
Symptom: The footer is four columns of links most users never need.
Detect: Footer grid with 4 link columns of 5 or more links each.
Fix: Reduce the footer to the main navigational paths and legally required links.
Grade: POLISH. Sources: redesign-existing-projects.

### NA-51 Default not-found page
Symptom: Broken URLs show the framework or browser default error page.
Detect: Default 404 rendered; no designed not-found route.
Fix: Design a helpful "page not found" page with a route back.
Grade: POLISH. Sources: redesign-existing-projects.


## Content and copy (CP)

### CP-01 Error with no next step
Symptom: An error says something failed and leaves the user with nothing to do.
Detect: Error, warning, or failure strings with no retry, correction, or instruction: "Something went wrong", "Save failed.", "Invalid date", "That password is too short"; error UI showing a message with no retry control, link, or next step.
Fix: Say what did not happen, then the next step: "Changes not saved. Check your connection and try again."
Grade: BLOCKING. Sources: better-writing, better-interface, impeccable, ui-ux-pro-max, design-plugin/ux-copy.

### CP-02 Button label that misstates the outcome
Symptom: The button promises one thing and does another, such as "Continue" that charges the card.
Detect: Compare the label with what happens after the click: "Continue" or "Next" that charges, sends, or commits; "Remove" on an action that permanently destroys data.
Fix: Name the real outcome, such as "Pay $49" or "Delete project"; keep "Remove" for recoverable actions.
Grade: BLOCKING. Sources: design-plugin/ux-copy, impeccable.

### CP-03 Manipulative wording in a choice
Symptom: The decline option shames the user, or urgency copy pressures a decision with no real deadline behind it.
Detect: Confirm-shaming decline links such as "No thanks, I like paying more", guilt text, countdown or scarcity copy with no data behind it, disguised choice labels.
Fix: Give the decline option a neutral label and remove urgency copy that is not true.
Grade: BLOCKING. Sources: ui-ux-pro-max.

### CP-04 Error that names neither the field nor the rule
Symptom: "Invalid input", "Error occurred", or "Something went wrong" with no indication of what is wrong.
Detect: Catch-all or one-word error strings not tied to a field and naming no rule or example: "Invalid input", "Invalid value", "Payment failed", "Error", "Invalid".
Fix: Name the field, the rule, and an example: "Email needs an @ symbol. Try name@example.com".
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max, design-plugin/ux-copy.

### CP-05 Raw codes or system log phrasing shown to users
Symptom: Users see "Error 500", "404 Not Found", an exception, or "Operation completed successfully".
Detect: HTTP codes, "ERR_CONN", exception names, stack traces, raw API messages, "Error 422", "Invalid input detected", "System error encountered", or nominalized machine phrasing in visible strings.
Fix: Translate into plain language with a next step: "You don't have permission to view this page. Contact your admin."
Grade: MAJOR. Sources: impeccable, design-review, design-plugin/ux-copy, ui-ux-pro-max.

### CP-06 Blame, apology, or exclamation in an error
Symptom: "You entered an invalid email!" or "Oops! Sorry, something went wrong" instead of the facts.
Detect: Error strings containing "Oops", "Whoops", "Uh oh", "Sorry", "We're sorry", "You entered", "You made", or an exclamation mark.
Fix: State the requirement calmly without blame: "Enter a date as DD/MM/YYYY".
Grade: MAJOR. Sources: impeccable, better-writing, frontend-design, redesign-existing-projects, design-plugin/ux-copy.

### CP-07 Button label that does not name the action
Symptom: Buttons read "Submit", "OK", "Go", "Click here", "Next", or a bare noun.
Detect: Button text with no leading verb and object: "Submit", "OK", "Go", "Click here", "Learn", "Info", "Free trial", "Let's go!"; "Continue" on an action with a specific result.
Fix: Verb plus object naming the outcome: "Create account", "Save changes", "Download PDF".
Grade: MAJOR. Sources: impeccable, better-writing, design-review, frontend-design, design-plugin/ux-copy, ui-ux-pro-max.

### CP-08 Confirmation that does not say what will happen
Symptom: The dialog asks "Are you sure?" and never names the item, the count, what is lost, or who is affected.
Detect: Titles "Are you sure?", "Confirm", or "Delete selected?"; destructive or shared-resource dialog bodies without "can't be undone", item counts, or the people who lose access.
Fix: Title names action, object, and count; body names the permanent loss and who is affected.
Grade: MAJOR. Sources: impeccable, better-writing, design-plugin/ux-copy.

### CP-09 Yes, No, OK, or an ambiguous Cancel on dialog buttons
Symptom: Dialog buttons cannot be answered without re-reading the question, so users misclick.
Detect: "OK", "Yes", or "No" as dialog button text; "Cancel" beside a cancel-like primary action such as "Cancel subscription".
Fix: Verb plus object: "Delete project" and "Cancel", or "Keep subscription" where cancel is ambiguous.
Grade: MAJOR. Sources: impeccable, better-writing, design-plugin/ux-copy.

### CP-10 Jargon or system-internal names in labels
Symptom: Labels, hints, and messages use acronyms, internal terms, or technical nouns users do not know.
Detect: Undefined acronyms, system names, "webhook config" in nav or settings, developer terms in a consumer product, formats or prior steps the user was never shown, no helper text.
Fix: Name things by what the user does, in plain language; define unavoidable terms inline.
Grade: MAJOR. Sources: impeccable, apple-design, frontend-design, claude-code-workflows, design-plugin/ux-copy, ui-ux-pro-max.

### CP-11 Label that forces the user to guess
Symptom: A control, field, nav item, or disclosure cannot be understood without trying it.
Detect: Vague or clever labels: "Go", "Items", "Home", "Stuff", "More", "Show more", a bare chevron with no noun or count; puns in nav or CTAs; strings readable two ways.
Fix: Name the contents or the action with one meaning: "Library", "Show 12 more results".
Grade: MAJOR. Sources: impeccable, apple-design, frontend-design, claude-code-workflows, design-plugin/ux-copy, better-layout.

### CP-12 One concept with several names
Symptom: The same object or action is called different things across screens or within one flow.
Detect: "project", "workspace", and "board" for one entity; "Remove" and "Delete" for one action; button "Publish" with toast "Posted"; "Get in touch", "Contact us", and "Let's talk" for one destination.
Fix: One term per concept, reused in every label, button, confirmation, and toast.
Grade: MAJOR. Sources: impeccable, unslop, design-plugin/ux-copy, frontend-design, design-taste-frontend, better-writing.

### CP-13 Tone mismatched to the stakes or the brand
Symptom: Jokes, confetti, or a chirpy voice on an error, destructive confirm, or payment; cold copy on success.
Detect: Humor, puns, mascots, emoji, exclamation marks, or wording like "Send to void" in errors, destructive confirmations, data-loss, security, payment, medical, or legal copy; flat tone in success or onboarding; voice outside the brand's register.
Fix: Calm and plain for errors and destructive flows, serious for data loss, warm for success and onboarding.
Grade: MAJOR. Sources: impeccable, better-writing.

### CP-14 Placeholder text and stock names in rendered UI
Symptom: Lorem ipsum, "John Doe", "Acme", "TODO", or "Item 1" show in the interface or its fixtures.
Detect: "Lorem ipsum", "Title here", "John Doe", "Jane Doe", "Acme", "Nexus", "SmartFlow", "TODO", "No data", "Error", numeric placeholders, or labels that mirror field names in rendered screens.
Fix: Use realistic, locale-appropriate content and written microcopy for every state.
Grade: MAJOR. Sources: impeccable, minimalist-ui, redesign-existing-projects, ui-ux-pro-max, design-taste-frontend.

### CP-15 Persistent information parked in an empty state
Symptom: Instructions or policy text that live only in the empty state vanish once content exists.
Detect: Help, rules, or limits rendered exclusively inside the empty-state branch.
Fix: Move persistent information to a place that stays visible once content exists.
Grade: MAJOR. Sources: better-writing.

### CP-16 Typos and broken grammar in visible copy
Symptom: Misspellings or sentences that do not parse appear in headlines, labels, captions, or messages.
Detect: Read every visible string in the diff and the capture, including alt text, captions, footers, and errors; spelling mistakes; fragments like "free on its past".
Fix: Rewrite as a correct, plain sentence.
Grade: MAJOR. Sources: impeccable, design-taste-frontend, claude-code-workflows.

### CP-17 Message that does not stand on its own
Symptom: A toast, headline, or screen only makes sense if the reader remembers something not on screen.
Detect: "it", "this", or "that way" with no antecedent on screen; toasts assuming the triggering action is remembered; screens stating no purpose or next step.
Fix: Rewrite each message so it names its subject and purpose by itself.
Grade: MAJOR. Sources: impeccable, design-taste-frontend.

### CP-18 Copy that could sit under any product
Symptom: Headlines and blurbs pitch a feeling instead of saying what the thing is or does.
Detect: Adjective-heavy blurbs with no concrete noun, verb, or number ("a delightful, seamless experience"); a hero that does not say what the product does; text that would read unchanged on another product.
Fix: Describe what it is or does with a mechanism, noun, or number.
Grade: MAJOR. Sources: frontend-design, unslop, design-review.

### CP-19 Marketing buzzwords in copy
Symptom: Copy leans on "Elevate", "Seamless", "Unleash", "Next-Gen", "Revolutionize", or "Game-changer".
Detect: Those words, "Delve", or superlatives in headlines, subheads, CTAs, or body copy.
Fix: Use concrete verbs and specific claims.
Grade: MAJOR. Sources: design-taste-frontend, minimalist-ui, impeccable.

### CP-20 Performative or poetic register in copy
Symptom: Copy performs restraint or craft, or sounds clever while saying nothing verifiable about the product.
Detect: "Quietly in use at", "honest", "on purpose"; labels like "From the field" or "Field notes"; a meta-sentence about the copy under a heading; self-aware asides about competitors; wordplay that does not track; "flywheel", "north star", "substrate".
Fix: Replace with a plain functional sentence or label: "Trusted by", "Testimonials".
Grade: MAJOR. Sources: design-taste-frontend, unslop.

### CP-21 Fabricated or unverifiable figures and claims
Symptom: Stats, counters, testimonials, or dates look invented or cite no source.
Detect: "92%", "4.1x", "99.99%", or "1234567" with no source or sample label; hard-coded "412 of 800" counters; "Trusted by industry leaders" with no name; testimonial grids with no real customers; identical dates on every post.
Fix: Use real data, label it as sample data, or remove the claim.
Grade: MAJOR. Sources: design-taste-frontend, unslop, redesign-existing-projects, ui-ux-pro-max.

### CP-22 Decorative label text that carries no information
Symptom: Captions and step labels fill space without telling the reader anything.
Detect: "hosting" or "payments" under logos in a logo wall; pseudo-archival credits like "Plate 03, House archive" under stock images; "Step 1", "Stage 2", or "Phase 01" with no verb-noun.
Fix: Delete the text or replace it with a functional label: "Install", "Configure", "Ship".
Grade: MAJOR. Sources: design-taste-frontend.

### CP-23 Sentence assembled from fragments around a variable
Symptom: Translated strings come out in the wrong word order or with broken grammar.
Detect: `"You have " + n + " new messages"`, template literals holding sentence fragments, one sentence split across several keys, or a variable appended outside the sentence.
Fix: One whole message with an ICU placeholder inside it (better-writing), or the count kept outside the sentence (impeccable).
Grade: MAJOR. Sources: better-writing, impeccable.

### CP-24 Hand-rolled plural
Symptom: "1 messages", "0 new messages" instead of "No new messages", or wrong forms in languages with more categories.
Detect: `n === 1 ? "" : "s"`, `${count !== 1 ? 's' : ''}`, or plural handling without `=0`, `one`, and `other` categories.
Fix: Use ICU plural categories or `Intl.PluralRules`, letting translators add `few` and `many`.
Grade: MAJOR. Sources: better-writing, impeccable.

### CP-25 Idioms, puns, or culture-bound humor in strings
Symptom: Copy a tired reader cannot parse on the first pass, or that breaks in another language or region.
Detect: Idioms, colloquialisms, puns, region-specific jokes or holiday themes applied globally; voice-driven wording in errors, destructive, or security copy; buttons sized to the English string with no room for expansion.
Fix: Choose plain words that translate, and revert to plain language wherever voice creates ambiguity.
Grade: MAJOR. Sources: better-writing, design-plugin/ux-copy, impeccable.

### CP-26 Abbreviations, arrows, and dropped articles in strings
Symptom: Messages read like shorthand: "5 mins ago", "Parser rejects bad date -> exit 2, no write".
Detect: "mins", "secs", "hrs", "msgs", arrow symbols, or strings missing articles or verbs in user-facing text.
Fix: Write whole sentences with articles and verbs; spell out units and arrows.
Grade: MAJOR. Sources: unslop, impeccable.

### CP-27 Wall of text in onboarding or help
Symptom: Paragraphs of explanation with no headings, steps, or lists, often before the user can act.
Detect: Dense prose blocks in the interface; long modal copy or document-like intro screens on first run; help text without headings, numbered steps, or lists.
Fix: Short paragraphs, headings, and steps; onboard through action instead of text.
Grade: MAJOR. Sources: impeccable.

### CP-28 Help or tour that labels features instead of guiding a task
Symptom: "This is the project button" rather than "Create a project"; help topics named after panels.
Detect: Tour steps that describe UI parts; help topics named after settings and panels rather than user goals.
Fix: Write each step and topic as a task: "Create a project", "Invite a teammate".
Grade: MAJOR. Sources: impeccable.

### CP-29 Patronizing or over-explaining copy
Symptom: Tooltips explain what a search box is; expert users get oversimplified instructions.
Detect: Explanations of standard patterns; verbose instructions for obvious controls; oversimplified language in a tool for experts.
Fix: Cut explanations of standard patterns and pitch copy at the audience's expertise.
Grade: MAJOR. Sources: impeccable.

### CP-30 Welcome screen with no value statement or time estimate
Symptom: The first screen says "Welcome!" and nothing about what the product is or how long setup takes.
Detect: A welcome step lacking a value statement, what the user will accomplish, an honest time estimate, and a skip.
Fix: State what the product is, what setup achieves, how long it takes, and offer a skip.
Grade: MAJOR. Sources: impeccable.

### CP-31 Marketing block copy over its length budget
Symptom: Hero, section, and testimonial text runs long and demands a full read instead of a glance.
Detect: Hero paragraph over 20 words or 4 lines; section heading over 8 words; section paragraph over 25 words; testimonial over 3 rendered lines; one headline doing the explainer, CTA, and disclaimer jobs.
Fix: Cut to the budget and give each written element one job.
Grade: MAJOR. Sources: design-taste-frontend, frontend-design.

### CP-32 Stray 0, NaN, or undefined rendered as text
Symptom: A literal "0", "NaN", "undefined", or "null" appears where nothing should show.
Detect: `{count && <Component/>}` where count can be 0 or NaN; "undefined", "NaN", or "null" visible in a capture.
Fix: Use an explicit condition: `count > 0 ? ... : null`.
Grade: MAJOR. Sources: ui-ux-pro-max.

### CP-33 AI agent presented as a human
Symptom: A chat agent has a human name and avatar with no AI label.
Detect: A human persona on an automated agent; generated content with no "AI" label.
Fix: Label AI agents and generated content clearly.
Grade: MAJOR. Sources: ui-ux-pro-max.

### CP-34 No fallback message when data is unavailable
Symptom: On network loss the screen hangs on a spinner or a raw error; personalized blocks render empty for new users.
Detect: No `navigator.onLine` or offline handling, offline banner, or retry; dynamic hero or testimonial blocks with no default content when user data is absent.
Fix: Show a plain offline message with retry, and default content when data is absent.
Grade: MAJOR. Sources: ui-ux-pro-max.

### CP-35 Visual asset crowded with text
Symptom: A poster, banner, or ad is mostly text and reads as cluttered.
Detect: Text covering most of a poster or canvas; text over 20% of an ad-sized banner; multiple paragraphs in a visual asset.
Fix: Keep text minimal and let the visual carry the message.
Grade: MAJOR. Sources: ui-ux-pro-max.

### CP-36 Copy that repeats itself
Symptom: Intros restate headings, tooltips paraphrase labels, captions explain clear buttons, or facts appear twice.
Detect: Heading text nearly verbatim in the first sentence beneath it; tooltip "Saves the item" on "Save"; help "This is the username field"; the same stat or label repeated in one view.
Fix: Say it once; help text answers the implicit question or is removed.
Grade: POLISH. Sources: impeccable, design-plugin/ux-copy, design-review.

### CP-37 Filler words and phrases in strings
Symptom: Strings are padded with words that add nothing.
Detect: "In order to", "Please note that", "Due to the fact that", "It is important to note that", "Please" on routine fields; taglines or "Did you notice?" toasts inside task flows.
Fix: Delete every word that does no work: "To", "Because", "Enter your email".
Grade: POLISH. Sources: better-writing, unslop, frontend-design, design-plugin/ux-copy, impeccable.

### CP-38 Overlong or dense strings
Symptom: Users must re-read tooltips, hints, and errors to parse them.
Detect: Multi-sentence helper text for simple fields; five-word button labels; multi-clause sentences in microcopy; long paragraphs in UI text.
Fix: One idea per sentence, in the fewest words that keep the full meaning.
Grade: POLISH. Sources: impeccable, unslop, design-plugin/ux-copy.

### CP-39 Inflated or figurative wording where a plain word exists
Symptom: Copy says "utilize", "leverage", "serves as", "boasts", or trails into "ensuring seamless" clauses.
Detect: "utilize", "leverage", "facilitate", "numerous", "in the event that"; "serves as", "stands as", "boasts", "features"; trailing "-ing" clauses with no fact; adverb plus weak verb with no figure; "from X to Y" with unrelated endpoints; "The future looks bright".
Fix: Use "use", "help", "is", "has", the measured number, or list the things directly.
Grade: POLISH. Sources: unslop.

### CP-40 Hedged or boilerplate warning text
Symptom: Warnings read "could potentially possibly", so users cannot tell how serious it is; copy carries legal boilerplate.
Detect: Stacked hedges in alerts and tooltips; disclaimers and qualifiers inside product copy.
Fix: Reduce to "may" and keep only essential information.
Grade: POLISH. Sources: unslop, impeccable.

### CP-41 Passive voice in buttons and messages
Symptom: "Your file has been uploaded" or "Changes could not be saved" hides who does what.
Detect: "has been", "will be", or "is", "are", "was", "were" plus a past participle in buttons, toasts, and errors.
Fix: Active voice naming the actor, or object plus past tense for status: "Changes saved".
Grade: POLISH. Sources: impeccable, redesign-existing-projects, frontend-design, unslop.

### CP-42 Mixed or template capitalization
Symptom: Labels mix title case and sentence case, or every heading capitalizes every word.
Detect: Mixed casing across buttons, headings, nav, and menus; `text-transform: capitalize`; headings with every word capitalized.
Fix: One convention everywhere; sentence case (unslop, redesign-existing-projects, frontend-design).
Grade: POLISH. Sources: impeccable, redesign-existing-projects, unslop, frontend-design, claude-code-workflows, better-writing.

### CP-43 Inconsistent terminal punctuation
Symptom: Some labels end with periods and others do not, or full sentences lack terminal punctuation.
Detect: Periods on some labels, tooltips, or list items but not others; complete sentences with no period.
Fix: Periods on sentences, none on labels, applied the same way everywhere.
Grade: POLISH. Sources: impeccable.

### CP-44 Em dash or colon stitching fragments
Symptom: Labels and blurbs are glued together with em dashes or a framing colon instead of ending the sentence.
Detect: The em dash character or `&mdash;` in visible strings; colons not followed by a list or example.
Fix: End the sentence; use periods, commas, or parentheses.
Grade: POLISH. Sources: impeccable, unslop.

### CP-45 Keyboard stand-ins for typographic punctuation
Symptom: Rendered text shows "...", "--", or a hyphen in a range like "2010-2020".
Detect: "...", "--", or a hyphen joining a numeric or date range in rendered strings outside code.
Fix: The ellipsis character and an en dash for ranges; rewrite "--" as the real character (better-typography) or a period (impeccable).
Grade: POLISH. Sources: better-typography, impeccable.

### CP-46 Mixed quote styles or curly quotes in code
Symptom: Straight and curly quotes mix across strings, or code samples show typographic quotes that break when copied.
Detect: Curly and straight quote characters side by side in UI strings; smart quotes inside `<code>` or `<pre>`.
Fix: One convention in prose, curly (better-typography) or straight (unslop); straight quotes always in code.
Grade: POLISH. Sources: better-typography, unslop.

### CP-47 Value and unit separated by a breakable space
Symptom: "10 km" breaks across lines with the number on one line and the unit on the next.
Detect: A regular space between a number and its unit or currency symbol in rendered text.
Fix: A non-breaking space (`&nbsp;`) between the value and its unit.
Grade: POLISH. Sources: better-typography.

### CP-48 Copy stored in uppercase
Symptom: Strings are typed in caps, so a restyle means rewriting copy and screen readers may spell letters.
Detect: Uppercase string literals in source or CMS content instead of `text-transform: uppercase`.
Fix: Store text in natural case and set case with `text-transform`.
Grade: POLISH. Sources: better-typography.

### CP-49 Status copy without its object
Symptom: Toasts and loaders say only "Success", "Done", "Processing", or "Please wait".
Detect: One-word success toasts or banners; loading or saving strings with no "-ing" verb and object.
Fix: Verb plus object: "Saving changes", "Changes saved", "Invite sent to sam@example.com".
Grade: POLISH. Sources: impeccable, better-writing.

### CP-50 Status copy padded or shouted
Symptom: "Saved successfully!" or "Woohoo! You did it!!!" for a routine action.
Detect: "successfully", an exclamation mark, several exclamation marks, emoji, or celebratory language in success and toast strings for minor actions.
Fix: Object plus past-tense verb with no exclamation: "Changes saved".
Grade: POLISH. Sources: better-writing, redesign-existing-projects, design-plugin/ux-copy.

### CP-51 Reader addressed in the third person
Symptom: "The user must enter a password" or "each subscriber can post his or her recipes".
Detect: "the user", "his or her", "he or she", or gendered pronouns for a generic reader in instructional strings.
Fix: Write "you" or the plural: "Enter your password", "Subscribers can post recipes".
Grade: POLISH. Sources: better-writing.

### CP-52 Possessive on every label
Symptom: "Your favorites", "Your projects", and "Your settings" appear everywhere.
Detect: Nav and heading labels starting with "Your" or "My" where the bare noun would do.
Fix: Use the bare noun: "Favorites".
Grade: POLISH. Sources: better-writing.

### CP-53 Negatively phrased hint
Symptom: A hint reads "Don't use fewer than 8 characters."
Detect: Helper or error text starting with "Don't" or "Do not".
Fix: Phrase the rule positively: "Use at least 8 characters".
Grade: POLISH. Sources: better-writing.

### CP-54 Input verb that does not match the device
Symptom: Copy says "Click the button" on a touch screen, or "tap" on desktop.
Detect: "click" in copy shown on touch, "tap" on pointer devices, or either where both apply.
Fix: "tap" on touch, "click" with a pointer, "select" when both are possible.
Grade: POLISH. Sources: better-writing.

### CP-55 Ambiguous date or time format
Symptom: A date like "01/02/03" can be read three ways, or an event time is shown in a fixed zone.
Detect: Numeric-only short dates without locale formatting; static time strings with no conversion to the viewer's timezone.
Fix: Relative or locale-aware dates, and times converted to the viewer's timezone.
Grade: POLISH. Sources: ui-ux-pro-max.

### CP-56 Quote attribution incomplete
Symptom: A testimonial is signed with a first name only and no role, company, or photo.
Detect: Attribution lines containing only a first name; testimonial cards missing avatar, name, or role.
Fix: Name plus role, with company or photo where available.
Grade: POLISH. Sources: design-taste-frontend, ui-ux-pro-max.

### CP-57 Mixed copy registers on one page
Symptom: Technical monospace metrics, editorial prose, and marketing punch lines collide in one composition.
Detect: Monospace metric strings such as "47 tasks, 0.6 context switches per day" next to long-form prose and exclamation-style marketing lines.
Fix: One copy register per page unless the brand voice calls for mixing.
Grade: POLISH. Sources: design-taste-frontend.

### CP-58 Long or context-dependent live region messages
Symptom: Screen readers re-read a long announcement on every change, so messages drone on.
Detect: Multi-sentence or context-dependent text in `role="status"` or `role="alert"` regions, especially with `aria-atomic="true"`.
Fix: Keep announcements short and self-contained.
Grade: POLISH. Sources: better-accessibility.

### CP-59 Print output hides link targets and collapsed content
Symptom: Printed pages show only anchor text and omit collapsed sections.
Detect: No `a[href]::after { content: attr(href) }` and no expansion of hidden sections in the print stylesheet.
Fix: Show full URLs and expand hidden sections in print styles.
Grade: POLISH. Sources: impeccable.

### CP-60 No shortcut hint at the point of use
Symptom: Power features exist but nothing in the interface reveals them.
Detect: A search box or command palette trigger with no keyboard shortcut hint; no shortcut reference anywhere.
Fix: Show the shortcut hint beside the control it triggers.
Grade: POLISH. Sources: impeccable.


## Responsive (RE)

### RE-01 Horizontal scroll at narrow widths
Symptom: The page scrolls sideways on phones or at 320px; content hangs off the edge or gets cut off.
Detect: `scrollWidth` greater than `innerWidth` at 320px, 375px or any width to 1440px; fixed-width tables, images without `max-width: 100%`, `w-screen` plus padding, negative margins, unbroken strings, animated elements extending past the viewport.
Fix: Constrain every element to the viewport width, wrap or inner-scroll wide content, and clip animated overflow with `overflow-x: hidden`.
Grade: BLOCKING. Sources: impeccable, ui-ux-pro-max, design-review, claude-code-workflows, better-accessibility, better-interface, better-layout, better-typography, gpt-taste.

### RE-02 Hover-only affordances on touch devices
Symptom: Actions, menus or tooltips revealed only on hover are unreachable on phones, tablets and touch-screen laptops.
Detect: Information or controls shown only under `:hover`; mega-menus or hover dropdowns at mobile widths; no `@media (hover: none)` fallback and no tap or always-visible alternative.
Fix: Treat hover as pointer-only; provide always-visible or tap-reachable equivalents at every width.
Grade: BLOCKING. Sources: impeccable, design-review, claude-code-workflows.

### RE-03 Core functionality removed on mobile
Symptom: Key features exist only on desktop; mobile users cannot complete the task.
Detect: Features or controls set to `display: none` or omitted at mobile widths rather than adapted.
Fix: Adapt the feature for small screens instead of hiding it.
Grade: BLOCKING. Sources: impeccable.

### RE-04 Core experience dependent on an unsupported enhancement
Symptom: In a browser or device without the enhancement the layout or content is broken rather than plainer.
Detect: Core content or layout depends on View Transitions, anchor positioning, WebGPU, scroll timelines or similar with no `@supports` or feature-detection branch.
Fix: Provide a functional fallback so the experience without the enhancement still works.
Grade: BLOCKING. Sources: impeccable.

### RE-05 Container collapsing to zero under size containment
Symptom: A component renders at zero width and its content vanishes.
Detect: `container-type: inline-size` on a flex item, inline-block or absolutely positioned element with no definite width.
Fix: Give the container a definite width before applying size containment.
Grade: BLOCKING. Sources: better-layout.

### RE-06 Multi-column layout that never collapses on phones
Symptom: Columns squeeze to unreadable widths, text wraps per word, or a sidebar crushes content on narrow screens.
Detect: Grid or flex rows, `2fr 1fr 1fr` tracks, bento grids, multi-column forms or a persistent sidebar with no collapse rule below 768px; a desktop base such as `grid-cols-3` with only `max-width` overrides; no `auto-fit, minmax()`.
Fix: Write the single-column mobile layout as the base and layer `md:` and `lg:` columns upward.
Grade: MAJOR. Sources: impeccable, design-taste-frontend, ui-ux-pro-max, claude-code-workflows.

### RE-07 Text container sized to the English string
Symptom: Translated or longer labels overflow, clip or truncate in buttons, tabs and nav items.
Detect: `width: 96px` or `w-24` on buttons and labels, `white-space: nowrap` on dynamic text, `overflow: hidden` on labels, rows without `flex-wrap`; no slack for German +30%, French +20%, Finnish +30 to 40%.
Fix: Size by padding and `max-width`, let rows wrap, budget 30 to 40% expansion, test a long locale.
Grade: MAJOR. Sources: impeccable, better-layout, design-plugin/design-handoff.

### RE-08 Fixed pixel width on a layout container
Symptom: A wrapper or component overflows small screens and leaves huge margins on large ones.
Detect: `width: 1200px`, `width: 960px`, `width: 600px`, `min-width` larger than the viewport, or `width="800"` on images and tables, without `max-width: 100%` or percentage widths.
Fix: Use fluid widths with `max-width`, percentages or `clamp()`; give images `max-width: 100%; height: auto`.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max, design-review, redesign-existing-projects.

### RE-09 Full-height section sized with 100vh
Symptom: The hero or bottom CTA hides under the mobile browser toolbar or jumps as the address bar shows and hides.
Detect: `height: 100vh`, `min-h-screen` or `h-screen` on heroes, full-bleed sections or full-height panes.
Fix: Use `min-height: 100dvh` (or `svh`) so browser chrome and the keyboard are accounted for.
Grade: MAJOR. Sources: design-taste-frontend, ui-ux-pro-max, redesign-existing-projects, better-layout.

### RE-10 Physical CSS properties on mirrored UI
Symptom: Under `dir="rtl"` margins, padding, borders, floats and alignment stay on the left and break the mirror.
Detect: `margin-left`, `padding-right`, `border-right`, `left:`, `text-align: left`, `float: left`, or Tailwind `ml-`, `pr-`, `left-`, `text-left`, `border-l`, `rounded-tl` on UI that mirrors.
Fix: Use logical properties: `margin-inline-start`, `padding-inline-end`, `inset-inline-start`, `text-align: start`, `float: inline-start`, `ms-`, `pe-`.
Grade: MAJOR. Sources: impeccable, better-layout.

### RE-11 Landscape orientation breaking the layout
Symptom: Rotating the phone or tablet clips content, hides CTAs or leaves a fixed header eating most of the height.
Detect: No `orientation` media queries or height-aware layouts; fixed heights assuming a tall viewport; fixed headers consuming most of the landscape height; no landscape captures in review.
Fix: Keep layouts readable and operable in both orientations; shrink or collapse fixed chrome in landscape.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max, apple-design.

### RE-12 Adaptation by shrinking instead of restructuring
Symptom: The mobile layout is the desktop layout squeezed narrower, with tiny text and cramped columns.
Detect: Same component tree and column structure at every width with only font and size reductions; `clamp()` type as the only responsive mechanism in app UI; no collapsed sidebar, responsive table or reordered content.
Fix: Make responsive behavior structural: collapse sidebars, reflow tables, reorder or remove content per context.
Grade: MAJOR. Sources: impeccable.

### RE-13 Phone patterns stretched across tablet and desktop
Symptom: Wide screens show a bottom tab bar, hamburger-only nav or one stretched column; tablets get the phone layout.
Detect: Bottom nav or hamburger-only nav rendered at 1024px and above; single column at 1024px and above; no distinct 768px to 1023px treatment; no sidebar, rail, two-column or master-detail variant.
Fix: Switch to a sidebar or rail at 1024px and above; use two-column or master-detail layouts on tablet.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max.

### RE-14 Viewport media query inside a reusable component
Symptom: A card keeps its wide layout inside a narrow sidebar and overflows, or stacks on a wide viewport with room.
Detect: `@media (min-width)` or `@media (max-width)` rules controlling the internals or `grid-template-columns` of a component that can live in narrow containers.
Fix: Put `container-type: inline-size` on the parent and use `@container (width < 400px)` on the component.
Grade: MAJOR. Sources: impeccable, better-layout.

### RE-15 Touch targets not enlarged on mobile
Symptom: The same tiny buttons and links appear at phone widths and are hard to tap.
Detect: Tap targets under 44px at 375px; no size increase for interactive elements under mobile breakpoints; desktop breakpoints assuming mouse only on touch-screen laptops.
Fix: Enlarge interactive elements to at least 44px on mobile and keep touch-sized targets on desktop too.
Grade: MAJOR. Sources: ui-ux-pro-max, claude-code-workflows, impeccable.

### RE-16 Dense chart unreadable at phone width
Symptom: A wide chart, scatter plot or map is squeezed into a phone with overlapping ticks and untappable points.
Detect: Fixed chart dimensions; same tick count and orientation at all widths; vertical bars with many categories, scatter, bubble or choropleth as the primary mobile view.
Fix: Simplify or re-orient charts on small screens (horizontal bars, fewer ticks) or offer a table view.
Grade: MAJOR. Sources: ui-ux-pro-max.

### RE-17 Breakpoint placed where the content does not break
Symptom: Some widths show a cramped expanded layout and others a needlessly stacked one; awkward states between breakpoints.
Detect: `@media (max-width: 768px)` or other round preset widths unrelated to where the sidebar or card grid actually stops fitting; only 768px and 1024px queries; layout broken at in-between widths.
Fix: Keep the expanded layout until it stops fitting, then collapse at that content-derived width.
Grade: MAJOR. Sources: impeccable, better-layout.

### RE-18 Grid or flex child refusing to shrink
Symptom: Long text or a wide table pushes the grid or flex layout past the viewport.
Detect: `grid-template-columns` with bare `1fr` tracks or flex children holding long text or wide tables without `minmax(0, 1fr)` or `min-width: 0`.
Fix: Use `minmax(0, 1fr)` on the track and `min-width: 0` on the flex child.
Grade: MAJOR. Sources: better-layout.

### RE-19 Unbroken long string overflowing its container
Symptom: A long URL, identifier, title or large number escapes its card, button or cell.
Detect: Containers holding user-generated or dynamic strings without `overflow-wrap: break-word` or `break-words`; stress with long strings and watch for text leaving boxes.
Fix: Apply `overflow-wrap: break-word` and define wrapping, truncation or scrolling rules for long content.
Grade: MAJOR. Sources: better-typography, claude-code-workflows.

### RE-20 Transforms and background positions unmirrored in RTL
Symptom: Under `dir="rtl"` flex rows mirror but translated or absolutely placed elements slide the wrong way.
Detect: `translateX(`, `background-position: left` or `right`, `left:` or `right:` positioning inside components used under RTL with no `[dir="rtl"]` override.
Fix: Add a `[dir="rtl"]` override for every physical value that has no logical form.
Grade: MAJOR. Sources: better-layout.

### RE-21 Safe-area inset paired with a logical offset
Symptom: In RTL a floating button flips sides but keeps the wrong inset and lands under a curved corner.
Detect: `inset-inline-end` or any `*-inline-*` property combined with `env(safe-area-inset-left)` or `-right`; no `[dir="rtl"]` block swapping sides and insets.
Fix: Pair each physical side with its own inset and override both in `[dir="rtl"]`.
Grade: MAJOR. Sources: better-layout.

### RE-22 Same narrow gutter at every width
Symptom: On tablets and in landscape, content hugs the edges with phone-sized margins.
Detect: Fixed horizontal padding such as 16px with no breakpoint or orientation variants.
Fix: Increase horizontal insets on larger widths and in landscape.
Grade: MAJOR. Sources: ui-ux-pro-max.

### RE-23 Heavy effects shipped unchanged to mobile
Symptom: Scroll animations, parallax and heavy scripts stutter on a mid-range phone while the desktop stays smooth.
Detect: Same desktop scroll-triggered animations and effects at mobile breakpoints; heavy scripts on mobile; no throttled or low-end device check.
Fix: Simplify or remove heavy effects on mobile and verify on a low-end device with throttled network.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max.

### RE-24 Spacing and alignment drifting between breakpoints
Symptom: Spacing and alignment are correct at one viewport and misaligned or cramped at others.
Detect: Capture at 320, 375, 414, 768, 1024 and 1440px; misaligned edges, inconsistent gaps, overlapping text or clipped buttons at tablet or mobile widths.
Fix: Make spacing and alignment hold at every breakpoint and verify each common width.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max.

### RE-25 Email template built like a web page
Symptom: The email overflows or collapses unpredictably in mail clients; styles are stripped and hover effects never fire.
Detect: Email templates over 600px wide, multi-column flex or grid, `<link rel="stylesheet">`, `:hover` rules, non-table layout.
Fix: Single column at 600px max, inline CSS, table-based layout, no hover dependence.
Grade: MAJOR. Sources: impeccable.

### RE-26 Illogical reflow order on small screens
Symptom: Content stacks in an order that breaks reading flow; the CTA ends up below long secondary content.
Detect: Sidebars stacking above primary content on mobile; primary actions pushed below secondary blocks after collapse.
Fix: Reflow so primary content and actions keep their logical order when stacked.
Grade: MAJOR. Sources: impeccable.

### RE-27 Width 100vw including the scrollbar
Symptom: The element is wider than the page and a horizontal scrollbar appears on desktop.
Detect: `width: 100vw` in CSS or `w-screen` in Tailwind.
Fix: Use `width: 100%`.
Grade: MAJOR. Sources: better-layout, ui-ux-pro-max.

### RE-28 Missing viewport meta
Symptom: Mobile renders the desktop layout zoomed out.
Detect: No `<meta name="viewport" content="width=device-width, initial-scale=1">` in the head.
Fix: Add the viewport meta tag.
Grade: MAJOR. Sources: ui-ux-pro-max.

### RE-29 Device detection instead of feature detection
Symptom: Hybrid or touch-screen devices get the wrong layout or interaction because of their user agent.
Detect: User-agent sniffing such as `isMobile` driving layout or interaction instead of `pointer`, `hover` or width queries.
Fix: Key behavior on feature and media queries (`pointer`, `hover`, width).
Grade: MAJOR. Sources: impeccable.

### RE-30 Progression indicator not mirrored in RTL
Symptom: Star ratings, steppers and progress bars fill from the left in an RTL interface.
Detect: Rating, stepper or progress components whose fill direction is hardcoded left to right.
Fix: Fill from the leading edge so the sequence mirrors in RTL.
Grade: MAJOR. Sources: better-layout.

### RE-31 Container query rule targeting the container itself
Symptom: The responsive rule never applies and the component stays in one layout.
Detect: An `@container` block whose selector is the element carrying `container-type`.
Fix: Put `container-type` on the parent and query the child.
Grade: MAJOR. Sources: better-layout.

### RE-32 Image served at one size for every viewport
Symptom: Phones download desktop-size imagery.
Detect: `<img>` without `srcset` and `sizes`, and no `<picture>` element.
Fix: Use `srcset` with multiple widths and `sizes`, or the `picture` element.
Grade: MAJOR. Sources: impeccable.

### RE-33 Image distorted when its container changes
Symptom: Images squash or stretch as the layout reflows.
Detect: `<img>` with fixed width and height but no `object-fit` or `aspect-ratio`.
Fix: Lock the image ratio with `aspect-ratio` and `object-fit: cover`.
Grade: MAJOR. Sources: design-review.

### RE-34 Display heading overflowing narrow viewports
Symptom: Oversized hero text runs off the edge of a phone screen.
Detect: Fixed display sizes of 60 to 120pt with no `clamp()` or width-based scaling; line-height outside 0.9 to 1.1.
Fix: Scale display sizes with `clamp()` or a width-based helper and keep line-height 0.9 to 1.1.
Grade: MAJOR. Sources: ui-ux-pro-max.

### RE-35 Navigation and controls in print output
Symptom: Printed pages include menus, buttons and footers.
Detect: No `@media print` rules hiding nav, footer and interactive elements; no page-break or margin rules.
Fix: Hide navigation, footer and controls in print; add page breaks, margins and page numbers.
Grade: MAJOR. Sources: impeccable.

### RE-36 Breakpoints inconsistent across components
Symptom: Sections reflow at unrelated widths, so parts of the page collapse at different moments.
Detect: One-off media query values such as `min-[900px]`, 913px or 1140px across files; breakpoints at specific phone widths; more than three breakpoints; no shared set such as 640, 768, 1024, 1280, 1536 (design-taste-frontend) or 375, 768, 1024, 1440 (ui-ux-pro-max).
Fix: Define one breakpoint set for the product (three usually suffice) and use it everywhere.
Grade: POLISH. Sources: design-taste-frontend, ui-ux-pro-max, impeccable.

### RE-37 Safe-area padding with no fallback
Symptom: On devices without insets the footer or bar loses its padding entirely.
Detect: `padding-bottom: env(safe-area-inset-bottom)` without `max()`.
Fix: Use `padding-bottom: max(1rem, env(safe-area-inset-bottom))`.
Grade: POLISH. Sources: impeccable.

### RE-38 Media queries written in px
Symptom: At a larger browser font size the layout stays wide while the text needs the narrow layout.
Detect: `@media (min-width: 768px)` in `px` where the codebase allows `rem` or `em`.
Fix: Write media queries in `rem` or `em`.
Grade: POLISH. Sources: better-accessibility.

### RE-39 Large content hidden with display none on mobile
Symptom: Mobile still downloads images and markup it never shows.
Detect: Large content blocks or images set to `display: none` at mobile widths.
Fix: Lazy-load or conditionally render instead of hiding heavy content with `display: none`.
Grade: POLISH. Sources: impeccable.


## Accessibility (AC)

### AC-01 Focus indicator removed without a replacement
Symptom: Tabbing through the page shows nothing moving; the focused control looks identical to the others.
Detect: outline: none, outline: 0, outline-none or focus:outline-none with no :focus-visible rule; :hover rules with no matching :focus-visible; a keyboard walkthrough capture where the focused element cannot be identified (WCAG 2.4.7).
Fix: Keep the browser ring or draw a visible 2px to 4px :focus-visible ring on every interactive element.
Grade: BLOCKING. Sources: impeccable, design-taste-frontend, better-interface, ui-ux-pro-max, design-review, redesign-existing-projects, frontend-design, claude-code-workflows, design-plugin/accessibility-review, better-accessibility.

### AC-02 Meaningful image without a text alternative
Symptom: Informative images, charts, icons, and star ratings are announced as "image", a filename, or nothing.
Detect: img with no alt, or alt="" on a content image; alt="image", "photo", "chart", or a filename; svg with no title or aria-label; star-rating icons with no text value; native Image with no accessibilityLabel (WCAG 1.1.1).
Fix: Describe the information the image carries, such as "Revenue rose 40% in Q4", and use alt="" only for decoration.
Grade: BLOCKING. Sources: impeccable, design-taste-frontend, ui-ux-pro-max, design-review, redesign-existing-projects, claude-code-workflows, design-plugin/accessibility-review, design-plugin/design-critique, better-accessibility.

### AC-03 Function or content reachable only by pointer
Symptom: Hover menus, tooltips, truncated values, chart marks, or drag-only steps cannot be reached with a keyboard or on touch.
Detect: Content revealed only by :hover, mousemove, or a title attribute with no focus equivalent; onMouseEnter with no onKeyDown; chart marks with no tabindex; a keyboard-only walk of the flow stalls at a step (WCAG 2.1.1).
Fix: Use native controls or add a keyboard path that opens, focuses, and activates the same content.
Grade: BLOCKING. Sources: impeccable, design-review, better-interface, claude-code-workflows, design-plugin/accessibility-review, better-accessibility, better-layout, ui-ux-pro-max.

### AC-04 Tab order diverging from visual order
Symptom: Tab and screen reader focus jump around the page in an order unrelated to the layout.
Detect: Any tabindex above 0; order, flex-direction: row-reverse, column-reverse, explicit grid placement, or absolute positioning that moves content out of source sequence; a Tab walk whose order differs from reading order (WCAG 2.4.3, 1.3.2).
Fix: Reorder the source so DOM order equals visual order and use only tabindex 0 and -1.
Grade: BLOCKING. Sources: impeccable, design-taste-frontend, ui-ux-pro-max, design-review, claude-code-workflows, design-plugin/accessibility-review, better-accessibility, better-layout.

### AC-05 Clickable div or span standing in for a button or link
Symptom: A control cannot be reached with Tab, ignores Enter and Space, and is announced as plain text.
Detect: div or span with onClick, View with onTouchEnd, or a card with a click handler and no role, tabindex, or key handlers; in a capture, a "button" Tab never reaches.
Fix: Use button for actions and a with href for navigation, or Pressable with accessibilityRole on native.
Grade: BLOCKING. Sources: impeccable, better-interface, ui-ux-pro-max, design-review, claude-code-workflows, design-plugin/accessibility-review, better-accessibility.

### AC-06 Interactive target too small
Symptom: Icon buttons, checkboxes, inline links, and chart marks are hard to hit and mis-taps land on neighbors.
Detect: Computed box under 24x24 CSS px with no WCAG 2.5.8 exception (better-accessibility); under 44x44px or 48x48dp Android (impeccable, ui-ux-pro-max, design-review, design-plugin/accessibility-review); under 40x40px desktop (make-interfaces-feel-better); h-6 w-6 buttons with no padding or hitSlop.
Fix: Enlarge the box, or extend the hit area with padding, hitSlop, or a pseudo-element to the platform minimum.
Grade: BLOCKING. Sources: impeccable, make-interfaces-feel-better, ui-ux-pro-max, design-review, design-plugin/accessibility-review, design-plugin/design-critique, better-accessibility.

### AC-07 Reduced-motion preference ignored
Symptom: Users who asked the OS for less motion still get entry animations, parallax, marquees, scroll hijack, and confetti.
Detect: Stylesheet defines animation or transition with no @media (prefers-reduced-motion: reduce) block; JS or native animation with no matchMedia, useReducedMotion, or reduceMotionEnabled check; ScrollTrigger, parallax, magnetic, or autoplay paths with no reduced branch (WCAG 2.3.3).
Fix: Under the query, replace spatial motion with short crossfades or set durations to 0.01ms and iteration count to 1.
Grade: BLOCKING. Sources: impeccable, design-taste-frontend, better-interface, apple-design, ui-ux-pro-max, design-review, frontend-design.

### AC-08 Meaning carried by color alone
Symptom: Error, selected, required, or status states vanish in grayscale or for color-blind users.
Detect: Only color or background-color differs between states; red border with no error text or icon; green and red dots with no label; links told apart from text by hue only; red text on green (WCAG 1.4.1).
Fix: Pair every color cue with an icon, text, underline, border, or shape, and write the error out.
Grade: BLOCKING. Sources: impeccable, better-interface, ui-ux-pro-max, design-review, better-colors, design-plugin/accessibility-review.

### AC-09 Text contrast below 4.5:1
Symptom: Body, label, placeholder, or button text is faint against its background in light or dark mode.
Detect: Measured text contrast under 4.5:1, or under 3:1 for large text (18px+, 14px bold); text-gray-400 on white, ::placeholder under 4.5:1, bg-white with text-white, yellow on white (WCAG 1.4.3; AAA 7:1 per impeccable).
Fix: Adjust the pair until it measures at least 4.5:1, or 3:1 for large text, in both themes.
Grade: BLOCKING. Sources: impeccable, design-taste-frontend, ui-ux-pro-max, design-review, frontend-design.

### AC-10 Icon-only control without an accessible name
Symptom: A screen reader announces "button" or "link" with no name for close, menu, search, or delete controls.
Detect: button or a containing only an svg or icon with no aria-label, aria-labelledby, title, or visually hidden text; native Pressable with no accessibilityLabel; empty computed name in the accessibility tree (WCAG 4.1.2).
Fix: Name the action with aria-label or hidden text and give the icon aria-hidden="true".
Grade: BLOCKING. Sources: impeccable, better-interface, ui-ux-pro-max, design-review, better-accessibility.

### AC-11 Layout breaks at 200% zoom or the largest text size
Symptom: Zoomed or enlarged text clips, overlaps, truncates, or forces horizontal scrolling.
Detect: Capture at 200% browser zoom or maximum Dynamic Type; fixed px heights or widths on text containers, overflow: hidden on text, px spacing around text, numberOfLines={1} on essential labels (WCAG 1.4.4, 1.4.10).
Fix: Size containers and spacing in rem or em and let them grow and wrap with the text.
Grade: BLOCKING. Sources: impeccable, ui-ux-pro-max, design-review, design-plugin/accessibility-review, apple-design, better-accessibility, better-interface, better-layout, better-typography.

### AC-12 Custom widget missing role, name, or state
Symptom: Custom toggles, tabs, accordions, and menus announce as plain text or "clickable" without selected, expanded, or checked state.
Detect: div-based widgets with no role or accessible name; no aria-expanded, aria-selected, aria-pressed, aria-checked, or aria-disabled on stateful controls; an accordion header that is not a button with aria-expanded; native components with no accessibilityRole or accessibilityState (WCAG 4.1.2).
Fix: Use the native element, or add the role, an accessible name, and the state attributes the role requires.
Grade: BLOCKING. Sources: impeccable, ui-ux-pro-max, design-plugin/accessibility-review, better-accessibility.

### AC-13 Modal that lets focus escape or cannot be closed with Escape
Symptom: Tab moves behind the open dialog, screen readers read the page beneath, or Escape does nothing.
Detect: Custom modal div with no inert on the background and no dialog with showModal(); Tab from the last control lands on page content; no wrap-around on Tab and Shift+Tab; no Escape keydown handler (WCAG 2.1.2).
Fix: Use dialog with showModal(), or set inert on the background, cycle Tab inside, and close on Escape.
Grade: BLOCKING. Sources: impeccable, ui-ux-pro-max, design-plugin/accessibility-review, better-accessibility.

### AC-14 Control boundary or icon under 3:1 contrast
Symptom: Input borders, icons, ghost buttons, and checkboxes fade into the surface and are hard to find.
Detect: Borders, icons, or control outlines under 3:1 against adjacent colors; input with border: none and only a low-alpha box-shadow ring; bg-transparent button with no border, ring, or fill; 1px hairlines and glow as the only edge (WCAG 1.4.11).
Fix: Give controls a border or fill that measures at least 3:1 against the surrounding surface.
Grade: BLOCKING. Sources: impeccable, better-ui, make-interfaces-feel-better, design-taste-frontend.

### AC-15 Zoom disabled in the viewport meta
Symptom: Pinch zoom does nothing on mobile, or the page renders at desktop width on phones.
Detect: meta name="viewport" containing user-scalable=no or maximum-scale=1, or the meta missing entirely (WCAG 1.4.4).
Fix: Use width=device-width, initial-scale=1 and fix iOS input zoom with a 16px input font size instead.
Grade: BLOCKING. Sources: impeccable, ui-ux-pro-max, better-accessibility.

### AC-16 Drag or gesture with no single-pointer alternative
Symptom: Reordering, deleting, zooming, or dismissing works only by drag, swipe, pinch, or long press.
Detect: onDragStart, drag libraries, sortable lists, or kanban columns with no move buttons or menu; swipe-to-delete, pull, or pinch handlers with no visible button equivalent (WCAG 2.5.1, 2.5.7).
Fix: Add visible buttons or a menu that performs the same move or action with a single pointer.
Grade: BLOCKING. Sources: impeccable, ui-ux-pro-max, better-accessibility.

### AC-17 Focus ring present but too faint
Symptom: A focus ring exists but is barely visible against the control or page surface.
Detect: Ring color under 3:1 against adjacent colors; ring hidden by overflow; focus-within outline color never measured against the wrapper background; invisible rings on light forms (WCAG 1.4.11).
Fix: Use a ring color that measures at least 3:1 against every surface it appears on.
Grade: BLOCKING. Sources: impeccable, design-taste-frontend, better-typography.

### AC-18 Keyboard trap in a widget or embed
Symptom: Focus enters a widget, editor, or iframe and cannot leave with Tab or Escape.
Detect: Custom widgets that preventDefault on Tab; iframes or embeds with no exit path; a Tab walk that cycles inside one component forever (WCAG 2.1.2).
Fix: Let Tab or Escape leave every focusable region and return focus to where it entered.
Grade: BLOCKING. Sources: impeccable, ui-ux-pro-max, design-plugin/accessibility-review.

### AC-19 Dialog opens without moving focus inside
Symptom: After a dialog opens, focus stays on the trigger behind it and the next Tab lands outside.
Detect: Open handler with no focus() call on autofocus or the first focusable element; the backdrop appears but a Tab after opening leaves the dialog.
Fix: On open, move focus to the first focusable element inside the dialog.
Grade: BLOCKING. Sources: impeccable, better-accessibility.

### AC-20 Interactive role without keyboard operation
Symptom: A control announces as a button, tab, or slider but Enter, Space, or arrow keys do nothing.
Detect: role="button", "tab", "menuitem", or "slider" on an element with no tabindex="0", no onKeyDown, or both Enter and Space missing; the role's aria-selected, aria-checked, or aria-valuenow absent (WCAG 2.1.1).
Fix: Use the native element, or implement the full ARIA APG key map and states the role promises.
Grade: BLOCKING. Sources: claude-code-workflows, better-accessibility.

### AC-21 Video without captions or audio without a transcript
Symptom: Deaf and hard-of-hearing users, and muted autoplay viewers, get none of the spoken content.
Detect: video with no track kind="captions" and no burned-in captions; audio or podcast embed with no transcript link or text nearby (WCAG 1.2.1, 1.2.2).
Fix: Add a captions track to every video and a transcript to every audio-only piece.
Grade: BLOCKING. Sources: ui-ux-pro-max, better-accessibility.

### AC-22 Moving or auto-updating content with no pause control
Symptom: A live chart, marquee, or autoplaying video keeps moving and the user cannot stop it.
Detect: Streaming chart, marquee, or autoplay media with no pause, stop, or hide control; motion not frozen under prefers-reduced-motion; current value not shown as static text (WCAG 2.2.2).
Fix: Add a pause control, freeze the motion under reduced motion, and show the current value as text.
Grade: BLOCKING. Sources: ui-ux-pro-max, better-interface, better-accessibility, design-plugin/accessibility-review.

### AC-23 Digits reversed by hand for RTL
Symptom: Numbers inside right-to-left text render backwards, so phone numbers and amounts read wrong.
Detect: String manipulation or CSS that reverses digit runs for dir="rtl".
Fix: Never reorder digits; wrap mixed-direction values in bdi and rely on the bidi algorithm.
Grade: BLOCKING. Sources: better-layout, better-typography.

### AC-24 Chart with no text or table alternative
Symptom: Screen reader users get "image" or nothing from a chart, map, or graph carrying the key insight.
Detect: canvas or svg chart with no aria-label, caption, summary, or data table; values visible only on hover; gauge, funnel, or waffle with no numeric text; network graph, word cloud, 3D plot, or sunburst with no list view (WCAG 1.1.1).
Fix: Provide a data table or list view, a text summary of the takeaway, and key values as visible text.
Grade: BLOCKING. Sources: ui-ux-pro-max, better-accessibility.

### AC-25 Overlay without dialog semantics or an accessible name
Symptom: Screen readers do not announce that a dialog opened or what it is called.
Detect: Custom overlay with no role="dialog", no aria-modal="true", and no aria-labelledby pointing at its heading; no native dialog element.
Fix: Use dialog with showModal(), or add role="dialog", aria-modal="true", and aria-labelledby on the heading.
Grade: BLOCKING. Sources: better-accessibility.

### AC-26 aria-hidden on or above a focusable element
Symptom: Tab lands on controls that do not exist for a screen reader, including off-screen carousel slides.
Detect: aria-hidden="true" on a button, a with href, input, or tabindex="0" element or on any ancestor of one; hidden interactive content without inert, tabindex="-1", or display: none.
Fix: Remove aria-hidden from focusable subtrees, or make the subtree inert so it leaves the tab order too.
Grade: BLOCKING. Sources: better-accessibility.

### AC-27 Screen-reader-only text hidden incorrectly
Symptom: Text meant for screen readers only is skipped or read as one run-together string.
Detect: sr-only or visually-hidden class using display: none or visibility: hidden; width: 0 and height: 0 instead of 1px; missing white-space: nowrap.
Fix: Use the 1px clip pattern with margin -1px, overflow hidden, clip-path inset(50%), and white-space nowrap.
Grade: BLOCKING. Sources: better-accessibility.

### AC-28 Unexpected context change on focus
Symptom: Merely focusing a control submits a form, opens a window, or navigates.
Detect: onfocus handlers that navigate or submit; select elements that change the page on focus or on change without a button (WCAG 3.2.1).
Fix: Change context only on explicit activation such as Enter, click, or a submit button.
Grade: BLOCKING. Sources: design-plugin/accessibility-review.

### AC-29 Audio that ignores system sound settings or has no mute
Symptom: Sound plays despite the device being on silent and there is no way to turn it off.
Detect: Audio playback with no in-app mute toggle and no respect for the system silent or volume setting (WCAG 1.4.2).
Fix: Honor the system sound setting and provide a visible mute control.
Grade: BLOCKING. Sources: impeccable.

### AC-30 Missing landmarks and structure built from divs
Symptom: Assistive technology cannot jump between header, navigation, main, and footer; the page reads as one stream.
Detect: No main, nav, header, footer, aside, or equivalent role attributes; lists, tables, and articles built from div; required fields marked only by styling (WCAG 1.3.1).
Fix: Wrap regions in landmark elements and use list, table, and article elements for their structure.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max, design-review, redesign-existing-projects, claude-code-workflows, design-plugin/accessibility-review, better-accessibility.

### AC-31 Heading levels skipped or chosen for size
Symptom: Screen reader users cannot build an outline; the document jumps from h1 to h3 or h4.
Detect: h1 followed by h3 or h4; more than one h1; headings picked for their look; styled div or span where a heading belongs (WCAG 1.3.1).
Fix: Use one h1, nest levels in order, and style headings with classes independent of level.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max, design-review, claude-code-workflows, design-plugin/accessibility-review, better-accessibility.

### AC-32 Dynamic status change not announced
Symptom: Toasts, "Saved", result counts, loading states, and live updates are silent for screen reader users.
Detect: Status text updated with no aria-live region, role="status", accessibilityLiveRegion, or announceForAccessibility; success shown only visually; a toast container that calls focus() instead (WCAG 4.1.3).
Fix: Announce through a polite live region without moving focus.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max, better-accessibility.

### AC-33 Missing skip link
Symptom: Keyboard users must Tab through the whole header and navigation on every page to reach content.
Detect: No a href="#main" as the first focusable element, or one that is hidden and never shown on focus; no main element with a matching id (WCAG 2.4.1).
Fix: Add a "Skip to main content" link first in the DOM, hidden until focused.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max, redesign-existing-projects, better-accessibility.

### AC-34 Font size in px or font scaling disabled
Symptom: The user's larger default font or system text size has no effect on the app.
Detect: font-size in px on html, body, or p; Text with allowFontScaling={false} applied broadly; a very low maxFontSizeMultiplier; fixed fontSize values that ignore the system scale.
Fix: Set font sizes in rem or em and keep system font scaling on.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max, better-typography.

### AC-35 ARIA role rebuilding a native element
Symptom: A div-based button, checkbox, select, or dialog loses the keyboard behavior and states the native element provides.
Detect: role="button", "link", "checkbox", or "textbox" on div or span; custom components replicating select, checkbox, dialog, or the focus ring from scratch with no brand reason.
Fix: Use the native element and delete the ARIA; customize only when the platform control cannot be styled.
Grade: MAJOR. Sources: better-accessibility, better-interface, ui-ux-pro-max.

### AC-36 Large-area or slow looping motion behind content
Symptom: Full-screen parallax, video, or gently swaying backgrounds induce vestibular discomfort even without a preference set.
Detect: Full-viewport parallax, autoplay video, or animated gradients behind content; infinite animations with a period near 5s; multi-layer parallax on commerce, dashboard, or mobile-first pages with no skip.
Fix: Avoid full-viewport moving backgrounds and slow infinite oscillation; keep motion small and finite.
Grade: MAJOR. Sources: apple-design, design-taste-frontend, ui-ux-pro-max.

### AC-37 Composite widget with a Tab stop per item and no arrow keys
Symptom: Tab visits every tab, menu item, option, or toolbar button, and arrow keys do nothing.
Detect: Every item in role="tablist", "menu", "toolbar", "listbox", or "radiogroup" has tabindex="0"; no ArrowLeft, ArrowRight, Home, or End handling; arrow keys move a highlight without moving focus; menu button not opened by Enter, Space, or ArrowDown.
Fix: Use a roving tabindex where the active item is 0, the rest are -1, and arrow keys move focus.
Grade: MAJOR. Sources: impeccable, better-accessibility.

### AC-38 Focus not returned to the trigger on close
Symptom: Closing a dialog or menu drops focus to body and the keyboard user restarts from the top.
Detect: Close handler with no triggerRef.current?.focus() or fallback container focus; after closing, the next Tab starts from the top of the page.
Fix: On close, return focus to the trigger, or to the nearest logical container if the trigger is gone.
Grade: MAJOR. Sources: impeccable, better-accessibility.

### AC-39 Overlapping hit areas
Symptom: Tapping near one compact control triggers its neighbor.
Detect: Extended padding or pseudo-element hit areas of adjacent controls that intersect; dense icon rows with no gap between targets.
Fix: Shrink the extension as little as needed or add spacing so no two hit areas overlap.
Grade: MAJOR. Sources: make-interfaces-feel-better, better-layout, better-accessibility.

### AC-40 Reduced-transparency preference ignored
Symptom: Users who asked for less transparency still get blurred, translucent surfaces with low-contrast text.
Detect: backdrop-filter or translucent backgrounds with no @media (prefers-reduced-transparency: reduce) block setting a solid fill and backdrop-filter: none.
Fix: Provide a solid-fill fallback under the query with contrast that holds without blur.
Grade: MAJOR. Sources: design-taste-frontend, apple-design.

### AC-41 Increased-contrast preference not honored
Symptom: Users who enable increased contrast see no difference, or dark mode gets worse.
Detect: No @media (prefers-contrast: more) rule; one override shared by light and dark so the darkened color lands on the dark background too; values widened by under 0.15 OKLCH L and never remeasured.
Fix: Give each appearance its own stronger value with a defined border, widening L by at least 0.15.
Grade: MAJOR. Sources: apple-design, better-colors.

### AC-42 Focus ring too thin or too thick
Symptom: A 1px ring disappears; a 5px ring overwhelms the control.
Detect: outline-width or ring box-shadow spread outside 2px to 3px (impeccable) or 2px to 4px (ui-ux-pro-max).
Fix: Use a 2px to 3px ring.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max, better-accessibility.

### AC-43 Link used for an action
Symptom: An anchor deletes, toggles, or submits; Space does not activate it and the URL may change.
Detect: a href="#" with onClick, or a with no href and a handler, performing an action rather than navigating.
Fix: A link that performs an action is a styled button; keep a for navigation.
Grade: MAJOR. Sources: better-accessibility, design-review.

### AC-44 Visual-only context with no screen reader equivalent
Symptom: Sighted users see an external-link icon or a table caption; screen reader users get nothing.
Detect: target="_blank" links with no "Opens in new tab" text; tables with no caption; non-obvious controls with no hint.
Fix: Add visually hidden text, a caption, or a hint where aria-label is not an option.
Grade: MAJOR. Sources: better-accessibility, ui-ux-pro-max.

### AC-45 Role that contradicts the element's behavior
Symptom: A screen reader trusts an incorrect role and misdescribes the control or hides its native semantics.
Detect: role="menu" on links, role="alert" on static text, role="button" on navigation; h2 role="button" or ul role="presentation" with no reason.
Fix: Remove the wrong role; no ARIA is better than bad ARIA, and native semantics stay unless necessary.
Grade: MAJOR. Sources: better-accessibility.

### AC-46 Accessible name that omits the visible label
Symptom: Voice-control users say the text on the button and nothing activates.
Detect: aria-label whose text does not contain, or does not start with, the visible label text, such as "Send" named "Submit message" (WCAG 2.5.3).
Fix: Start the accessible name with the visible text, or let the visible text name the control.
Grade: MAJOR. Sources: better-accessibility.

### AC-47 Icon button named after its glyph
Symptom: Screen readers hear "Trash", "Close icon", or "X" instead of the action.
Detect: aria-label or accessibilityLabel values naming the icon shape rather than the action.
Fix: Name the action, such as "Delete project" or "Close dialog".
Grade: MAJOR. Sources: better-writing.

### AC-48 Announcement politeness mismatched to urgency
Symptom: A success toast or result count interrupts mid-sentence, or a form-level failure is never heard.
Detect: aria-live="assertive" or role="alert" on success toasts, result counts, loading messages, or as a notification default; form-level errors or session expiry with no role="alert".
Fix: Default to role="status"; reserve role="alert" for urgent problems not tied to a control.
Grade: MAJOR. Sources: better-accessibility.

### AC-49 Live region mounted together with its message
Symptom: Repeated status or alert messages are announced inconsistently, or not at all on some screen readers.
Detect: role="status" element rendered conditionally together with its message, or a new role="alert" element created on each error, instead of a persistent empty region whose text changes.
Fix: Render a stable empty live region first and update its text.
Grade: MAJOR. Sources: better-accessibility.

### AC-50 Forced-colors mode colors overridden
Symptom: In Windows High Contrast the focus ring or control boundary disappears.
Detect: forced-color-adjust: none, or hard-coded colors with no @media (forced-colors: active) rule naming a system color such as Highlight.
Fix: Keep the default color adjustment, or name system colors under the forced-colors query.
Grade: MAJOR. Sources: better-accessibility.

### AC-51 Link text without standalone meaning
Symptom: Links read "Click here" or "here", so a screen reader's link list is useless.
Detect: Anchor text that does not describe the destination out of context (WCAG 2.4.4).
Fix: Give links standalone meaning, such as "View pricing plans".
Grade: MAJOR. Sources: impeccable.

### AC-52 aria-label on a generic element
Symptom: The label is silently ignored by most screen readers.
Detect: aria-label on a div or span with no role, which ARIA 1.2 prohibits naming.
Fix: Put the name on a role-bearing element or give the element a role first.
Grade: MAJOR. Sources: better-accessibility.

### AC-53 aria-labelledby or aria-describedby pointing at a missing id
Symptom: The control silently has no name or description.
Detect: aria-labelledby or aria-describedby values with no matching id in the DOM; an empty computed name in the accessibility tree.
Fix: Point the attribute at an existing id.
Grade: MAJOR. Sources: better-accessibility.

### AC-54 Multiple form errors without a summary
Symptom: A long form shows several inline errors scattered off-screen with no overview.
Detect: More than one invalid field and no top-of-form summary with anchor links to each field.
Fix: Add a summary at the top linking to each invalid field.
Grade: MAJOR. Sources: ui-ux-pro-max.

### AC-55 System or assistive-technology shortcuts overridden
Symptom: App shortcuts hijack combinations like Cmd+Q, Ctrl+F, or screen reader keys, so the OS stops responding.
Detect: Global keydown listeners calling preventDefault() on modifier combos; custom shortcuts colliding with platform or screen reader shortcuts.
Fix: Scope custom shortcuts to the focused component and leave system combinations alone.
Grade: MAJOR. Sources: ui-ux-pro-max.

### AC-56 Text selection suppressed across the interface
Symptom: Users cannot copy useful text because selection is disabled.
Detect: user-select: none or select-none on a layout root, text container, or button label with no verified drag or gesture conflict.
Fix: Keep user-select: none only on draggable or gesture-driven surfaces.
Grade: MAJOR. Sources: better-typography.

### AC-57 Missing lang attribute
Symptom: Browsers and screen readers pick the wrong pronunciation, quotes, and hyphenation.
Detect: html element or language-switching elements without lang (WCAG 3.1.1, 3.1.2).
Fix: Set lang on the document and on elements whose language differs.
Grade: MAJOR. Sources: better-typography.

### AC-58 Mixed-direction text without dir or bdi
Symptom: Names, numbers, URLs, or paragraphs beside RTL text render in the wrong order or alignment.
Detect: No dir on the document or on elements whose direction differs; mixed-direction values without bdi; paragraphs of three or more lines in another script without their own lang, dir, and text-align: start.
Fix: Set dir where direction changes, wrap mixed values in bdi, and align long paragraphs to their own script.
Grade: MAJOR. Sources: better-typography.

### AC-59 Decorative effect applied to readable text
Symptom: Body, form, or data text moves, glows, or splits into color fringes while being read.
Detect: Animated or kinetic text in long-form, form, or data contexts; neon glow, 1px hairline, or RGB-split and glitch filters on body text with no reduced-motion option.
Fix: Keep reading and data text static and unfiltered; confine effects to display moments.
Grade: MAJOR. Sources: ui-ux-pro-max.

### AC-60 Core functionality broken without JavaScript
Symptom: With scripts failed or disabled, the page shows an empty shell or dead controls.
Detect: Empty body before hydration; links and forms that only work through JS handlers.
Fix: Progressively enhance so links, forms, and core content work without JavaScript.
Grade: MAJOR. Sources: impeccable.

### AC-61 Decorative image or icon not hidden from assistive technology
Symptom: Screen readers announce filler descriptions, ornamental icons, or empty decorative layers.
Detect: Decorative img with non-empty alt; an icon beside text without aria-hidden="true", accessible={false}, or importantForAccessibility="no"; an svg inside a named button not hidden, so the name reads "trash icon Delete".
Fix: Give decorative images alt="" and hide ornamental icons and layers with aria-hidden="true".
Grade: POLISH. Sources: impeccable, ui-ux-pro-max, better-accessibility.

### AC-62 Redundant ARIA or tabindex on a native element
Symptom: Attributes restate what the element already exposes, adding noise and signaling hand-managed focus.
Detect: role="button" on button, aria-checked on a native checkbox, or tabindex="0" on button, a with href, or input.
Fix: Delete the redundant attribute.
Grade: POLISH. Sources: better-interface, better-accessibility.

### AC-63 Focus ring drawn inside the element
Symptom: The ring overlaps the control's label or border and is hard to distinguish.
Detect: outline-offset of 0 or negative; an inset box-shadow used as the ring.
Fix: Offset the ring from the element with outline-offset: 2px.
Grade: POLISH. Sources: impeccable.

### AC-64 aria-label used where visible text could name the element
Symptom: The invisible name drifts out of sync with the UI and translation tools handle it inconsistently.
Detect: aria-label on elements that already have visible text or a nearby heading that aria-labelledby could reference.
Fix: Prefer visible text or aria-labelledby over aria-label.
Grade: POLISH. Sources: better-accessibility.

### AC-65 Extra live announcement when focus already moves there
Symptom: An opened modal or the first invalid field is announced twice.
Detect: role="status" or role="alert" messages fired alongside a focus() into the same content.
Fix: When focus moves there, the focus move is the announcement; add nothing.
Grade: POLISH. Sources: better-accessibility.

### AC-66 Abrupt brightness jump on theme change
Symptom: Switching between dark and light flashes the whole screen.
Detect: Instant background swap from near-black to white with no transition.
Fix: Ease the theme change over a short transition.
Grade: POLISH. Sources: apple-design.


## Perceived performance (PE)

### PE-01 Layout shift as media, fonts or late content arrive
Symptom: Text and buttons jump down as images, embeds, fonts or banners arrive; users mis-click moving targets.
Detect: img or video without width, height or aspect-ratio; iframe, ad or embed slots without min-height or aspect-ratio; async blocks, cookie bars or alerts inserted above existing content; CLS over 0.1 (impeccable, design-taste-frontend).
Fix: Reserve space with explicit dimensions or aspect-ratio for every image, embed and async region; overlay late banners instead.
Grade: MAJOR. Sources: impeccable, design-taste-frontend, ui-ux-pro-max.

### PE-02 Spinner where a skeleton belongs
Symptom: A lone centered spinner replaces the content region, giving no preview of the incoming layout; the wait feels longer.
Detect: Spinner component swapped in for a list, card, table or chart region; full-screen spinner as the only state for fetches over 1s (ui-ux-pro-max); chart axes drawn before data with no placeholder.
Fix: Use skeleton or shimmer placeholders that mirror the final layout; keep spinners for small in-component actions.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max, redesign-existing-projects, claude-code-workflows.

### PE-03 Oversized media for its slot
Symptom: Images pop in late, mobile downloads the desktop hero, high-DPI screens get blurry images, video heroes stay blank for seconds.
Detect: Natural size far above rendered size (a 3000px image in a 300px slot); img with only src, no srcset width descriptors or sizes; PNG or JPEG at 100% quality; multi-megabyte video with no poster; 50MB textures or raw .obj models.
Fix: Serve WebP or AVIF at 80 to 85% quality via srcset and sizes; compress video and models; add a poster.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max.

### PE-04 Below-fold media loaded eagerly
Symptom: Visible content waits while dozens of off-screen images, videos or iframes download first.
Detect: img far below the fold without loading="lazy"; heavy video or iframes fetched on first paint; galleries and masonry grids fully eager.
Fix: Add loading="lazy" to below-fold images and heavy media; reveal grid images as they arrive.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max.

### PE-05 Heavy work on every keystroke or scroll event
Symptom: Search fires a request per key, scroll-linked effects jitter, and toggling a filter freezes the list.
Detect: onChange fetching on each keystroke with no debounce of about 300ms (impeccable); scroll or resize handlers doing layout or state work per event with no throttle of about 100ms (impeccable); non-urgent list updates not marked as transitions.
Fix: Debounce input, throttle scroll and resize handlers, and mark non-urgent updates as transitions.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max.

### PE-06 Input latency from long main-thread tasks
Symptom: Taps, keystrokes and scrolling respond late and the interface stutters or feels frozen.
Detect: Keystroke-to-render over 100ms (ui-ux-pro-max); INP over 200ms or FID over 100ms (impeccable, design-taste-frontend); frames longer than 16ms in a profile; heavy synchronous work or JSON parsing in handlers on the UI thread.
Fix: Break up long tasks, defer non-critical work and move heavy computation off the main thread.
Grade: MAJOR. Sources: impeccable, design-taste-frontend, ui-ux-pro-max.

### PE-07 Whole view held until the slowest fetch completes
Symptom: Nothing, or only a spinner, appears until all data or the full streamed response has arrived.
Detect: Render gated on one all-or-nothing loading flag; page-level await with no suspense boundary around the slow region; AI text held until 100% complete with no token streaming; no progressive images; 10s or more of spinner.
Fix: Render the shell first, stream slow regions and long responses progressively, use optimistic updates.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max.

### PE-08 Transition on every property
Symptom: Colors, padding and shadows drift on state change when only one property was meant to move.
Detect: transition: all, a transition-all class, or a bare transition duration class where a single property changes; the browser also loses optimizations watching every property.
Fix: Name the properties, for example transition-property: scale, opacity, or transition-transform for transforms only.
Grade: MAJOR. Sources: better-ui, make-interfaces-feel-better.

### PE-09 Animation driven by per-frame state updates
Symptom: Cursor-follow, parallax, scroll-progress and reveal effects stutter and collapse on mobile.
Detect: setState or useState updated inside onMouseMove, scroll or requestAnimationFrame callbacks; window.scrollY stored in state; window.addEventListener("scroll") driving reveals or progress bars; motion code inside wide layout components.
Fix: Drive continuous values outside the render cycle with motion values, IntersectionObserver or CSS animation-timeline: view().
Grade: MAJOR. Sources: design-taste-frontend, minimalist-ui.

### PE-10 Heavy decorative effects that drop frames
Symptom: Confetti, particles, blur, 3D scenes or stacked parallax stutter, worst on cheap phones and older desktops.
Detect: Frame drops while an effect plays; WebGL, realistic lighting, 3 to 5 parallax layers, dynamic blur, chromatic aberration or 400 to 600ms morphs around forms, tables or mobile-first screens; effects gated only on viewport width; no flat fallback.
Fix: Cut effects that cost frames; reserve 3D for showcase heroes with a flat fallback; keep forms and tables flat.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max.

### PE-11 First paint blocked by render-blocking resources
Symptom: A white screen or unstyled flash until a large stylesheet or synchronous script finishes downloading.
Detect: script in head without async or defer; one large render-blocking stylesheet and no inlined critical CSS; styled layout appears late in a filmstrip; LCP over 2.5s (impeccable) or load over 2s (ui-ux-pro-max).
Fix: Inline the above-the-fold CSS, defer the rest, and load non-critical scripts with async or defer.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max.

### PE-12 Layout thrashing
Symptom: Scroll, resize or list updates stutter because layout is recomputed many times in one frame.
Detect: offsetHeight, getBoundingClientRect or scrollTop reads interleaved with style writes in loops or scroll handlers; style set one property at a time; layout callbacks setting state synchronously; long Recalculate Style and Layout entries in a profile.
Fix: Batch all reads, then all writes; apply style changes through classes or cssText.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max.

### PE-13 Press or hover feedback that arrives late
Symptom: The pressed or hover state appears noticeably after the pointer lands, so the control feels laggy.
Detect: transition-delay on :active or :hover; pressed style driven by a network response, a delayed setState or a setTimeout; waiting on transitionend before responding; first feedback later than 80ms (impeccable) or 100ms, target 80 to 150ms (ui-ux-pro-max).
Fix: Render press and hover feedback synchronously within 80ms, independent of any async work.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max, apple-design, claude-code-workflows.

### PE-14 Chart or map with too many rendered marks
Symptom: Charts and maps stall while drawing; zoom, pan and live updates lag more as data accumulates.
Detect: 1000 or more points or regions as SVG; over 10,000 cells or points un-aggregated; calendar heatmap over 365 cells per SVG; over 500 visible candles; streaming SVG buffer beyond 60 to 300s; 3D scenes past 50,000 points without LOD.
Fix: Use Canvas or WebGL past 1000 marks, downsample or aggregate, cap the visible range, add level of detail.
Grade: MAJOR. Sources: ui-ux-pro-max.

### PE-15 Heavy feature initialized before it is visible
Symptom: The first screen waits for an editor, chart, map, WebGL scene or animation library the user cannot see yet.
Detect: GL context creation or WASM instantiation at module load instead of on viewport proximity; heavy components used only below the fold or on interaction imported statically; Lottie JSON, confetti or 3D libraries in the initial payload.
Fix: Initialize and load heavy features only when they approach the viewport or are requested.
Grade: MAJOR. Sources: impeccable, design-taste-frontend, ui-ux-pro-max.

### PE-16 Hero image lazy-loaded or not prioritized
Symptom: The largest above-fold visual paints late while smaller content is already visible.
Detect: loading="lazy" on the hero or any above-fold image; no fetch priority flag or link rel="preload" for the hero; the first-viewport component loaded through a dynamic import; LCP over 2.5s.
Fix: Load above-fold media eagerly and preload or prioritize the hero image.
Grade: MAJOR. Sources: impeccable, design-taste-frontend.

### PE-17 Grain or filter on a scrolling container
Symptom: Scrolling stutters on mobile under a noise, grain or filter overlay that repaints continuously.
Detect: SVG noise, CSS filter or grain overlay applied to a scrolling element or its children rather than to a fixed, inset-0, pointer-events-none overlay.
Fix: Apply grain only to a fixed, pointer-events-none overlay above the page.
Grade: MAJOR. Sources: design-taste-frontend.

### PE-18 Off-screen rendering left running
Symptom: An animated section keeps burning CPU and battery after it scrolls out of view, slowing the rest.
Detect: requestAnimationFrame loops with no IntersectionObserver pause; canvases or WebGL scenes still rendering while not visible; fans or thermal throttling after idle scrolling.
Fix: Pause rendering loops when the element leaves the viewport.
Grade: MAJOR. Sources: impeccable.

### PE-19 Flash of wrong theme or state on hydration
Symptom: The page renders in the default theme or without client data, then flips after hydration.
Detect: Client-only values such as theme or locale set in an effect after mount; a visible flicker on load; hydration mismatch warnings in the console.
Fix: Set client-only values with an inline script before hydration.
Grade: MAJOR. Sources: ui-ux-pro-max.

### PE-20 Console errors surfacing as visual glitches
Symptom: Views flicker, re-mount or show broken assets because runtime errors fire while they load.
Detect: Browser console shows errors or warnings on the changed views: hydration mismatches, missing list keys, failed asset loads.
Fix: Resolve every console error and warning before shipping.
Grade: MAJOR. Sources: claude-code-workflows.

### PE-21 Animation used to hide slow loading
Symptom: Elaborate entrance choreography masks a slow page; content stays blocked behind motion that cannot be skipped.
Detect: Decorative entrance sequences whose duration coincides with data fetch time; animation that cannot be skipped while the content behind it is still loading.
Fix: Fix the load time; use skeletons or progressive rendering instead of decorative motion as cover.
Grade: MAJOR. Sources: impeccable.

### PE-22 Misused will-change
Symptom: Extra compositor layers raise memory and can blur text, with no smoother motion in return.
Detect: will-change: all; will-change on background-color, padding, top, left, width, height, border or color; will-change on elements that never animate or added before any stutter was seen; will-change: clip-path relied on (unreliable per better-ui).
Fix: Limit will-change to transform, opacity or filter, on the animating element only, after stutter is seen.
Grade: POLISH. Sources: design-taste-frontend, better-ui, make-interfaces-feel-better, impeccable.

### PE-23 Font payload heavier than the page uses
Symptom: Text appears late or swaps late because the page fetches more font data than it renders.
Detect: Weights requested but unused in CSS; 3 or more static files for one family (variable would be smaller) or a variable file for 1 or 2 weights; .ttf, .otf or .woff instead of .woff2; a preload tag per weight.
Fix: Load only used weights as woff2, variable at 3 or more weights, and preload only the critical weight.
Grade: POLISH. Sources: impeccable, ui-ux-pro-max, better-typography.

### PE-24 First-frame animation stutter
Symptom: A transform animation hitches on its first frame as the browser promotes the layer mid-flight.
Detect: Visible micro-stutter at animation start, most often in Safari, on an element animating transform with no will-change and no prior layer promotion.
Fix: Add will-change: transform to that element only.
Grade: POLISH. Sources: impeccable, better-ui, make-interfaces-feel-better.

### PE-25 Same payload and effects on slow connections
Symptom: On 3G the page waits for full-resolution images and heavy animations before it becomes usable.
Detect: No low-resolution placeholder or progressive image strategy; no saveData or connection check; the same animation budget regardless of connection; throttle to 3G and observe.
Fix: Serve lower-resolution images and fewer animations when the connection is slow.
Grade: POLISH. Sources: impeccable, ui-ux-pro-max.

### PE-26 Code fetched only when the button is clicked
Symptom: Clicking a control pauses while its code downloads before anything responds.
Detect: Dynamic import triggered inside the click handler with no preload on hover, focus or viewport approach; a visible pause after click with no pressed state.
Fix: Preload the chunk on hover or focus and show pressed feedback immediately.
Grade: POLISH. Sources: ui-ux-pro-max.

### PE-27 Instant result for a heavy-sounding operation
Symptom: A search, analysis or generation returns in 0ms and users doubt that real work happened.
Detect: Operations framed as heavy (search, analysis, generation) that complete with no visible processing state at all.
Fix: Allow a brief, honest processing moment that signals real work.
Grade: POLISH. Sources: impeccable.

### PE-28 Tab activation mode mismatched to panel cost
Symptom: Arrowing across tabs triggers a slow panel load on every keystroke, or instant panels demand an extra Enter.
Detect: Automatic activation (panel switches on arrow focus) with panels that fetch or render slowly; manual activation with panels that render instantly.
Fix: Activate automatically when panels render instantly; require Enter or Space when switching is expensive.
Grade: POLISH. Sources: better-accessibility.


## Data display (DA)

### DA-01 Series distinguished by color alone
Symptom: Lines, bars, or positive and negative values differ only by hue, so colorblind readers see them merge.
Detect: Series colors limited to hue differences, often a red and green pair; no dash style, marker shape, pattern, texture, or direct label telling series apart.
Fix: Add a second cue such as shape, dash, pattern, or a direct label, and avoid red and green pairs.
Grade: BLOCKING. Sources: ui-ux-pro-max.

### DA-02 Information needed for a decision hidden or removed
Symptom: Users lack the price, status, consequence, or detail they need to decide.
Detect: Price, consequences, or status hidden or deleted to reduce clutter; an expert tool reduced to a few controls that hide needed detail.
Fix: Keep every piece of information a decision depends on and match complexity to the task.
Grade: BLOCKING. Sources: impeccable.

### DA-03 Gain and loss colors fixed across locales
Symptom: Gains show green and losses red everywhere, which reads reversed in markets where red means gain.
Detect: Gain, loss, status, or alert colors as fixed tokens with no per-locale variant in a product shipping to such markets.
Fix: Make gain and loss per-locale tokens and verify their meaning in every shipped locale.
Grade: BLOCKING. Sources: better-colors.

### DA-04 Proportional figures on aligned or changing numbers
Symptom: Numeric columns wobble out of alignment, and counters, prices, or timers jitter as digits change width.
Detect: Tables, stat columns, prices, timers, or counters without `font-variant-numeric: tabular-nums` (the `tabular-nums` class); digits of different widths visible in a stacked column of the capture.
Fix: Apply `tabular-nums` in the interface font; design-taste-frontend accepts a monospace face, better-typography says keep the interface font.
Grade: MAJOR. Sources: impeccable, design-taste-frontend, make-interfaces-feel-better, ui-ux-pro-max, design-review, redesign-existing-projects, better-typography.

### DA-05 Too many series or categories in one chart
Symptom: Overlapping lines, sliver bars, thin pie slices, or stacked annotations turn the chart into noise.
Detect: More than 6 line series; more than 15 vertical bars; more than 5 pie or waffle slices; more than 8 radar axes or 3 radar datasets; more than 12 waterfall bars or 8 funnel stages; dual y-axes.
Fix: Split into small multiples, horizontal bars, a stacked bar, or a table, and group minor items into "Other".
Grade: MAJOR. Sources: ui-ux-pro-max.

### DA-06 Numbers, dates, currency, or lists formatted by hand
Symptom: Values render in one locale's format for everyone: 1/15/2024, 1000000, "$" for a EUR audience, "1 days ago".
Detect: String concatenation, `toFixed`, `getMonth`, or `toLocaleDateString()` with no locale building numbers, dates, money, or units; custom "ago" helpers; `names.join(", ")` with a hand-appended "and".
Fix: Format through `Intl.NumberFormat`, `DateTimeFormat`, `RelativeTimeFormat`, and `ListFormat` with the user's locale.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max, better-writing.

### DA-07 Chart type mismatched to the data shape
Symptom: A trend shown as bars, categories joined by a line, or shares as plain bars hides the point.
Detect: Line chart with a categorical x-axis; bars across dates or for shares; scatter with a categorical axis; funnel whose stages are not sequential and decreasing; heatmap on under 20 cells or categorical data; trend data left as a raw table.
Fix: Use a line for time, bars for categories, stacked or waffle for proportion, scatter for two continuous variables.
Grade: MAJOR. Sources: ui-ux-pro-max.

### DA-08 Specialist chart or layout mismatched to audience or device
Symptom: Readers face a chart form or dashboard pattern they cannot read, or one that fails on their phone.
Detect: Candlesticks outside trading; sankey, network, sunburst, or word cloud on mobile; a dense analyst grid for consumers; funnel, cohort, or pipeline layouts on unrelated data; a streaming chart for data updating under once a minute.
Fix: Use the simpler form the audience knows, such as a line or table, and a layout matched to the data.
Grade: MAJOR. Sources: ui-ux-pro-max.

### DA-09 Encoding that hides the exact values the reader needs
Symptom: Users squint at angles, color intensity, or areas to estimate numbers they need precisely.
Detect: Pie used where exact reading matters or slices within 5 percent of each other; heatmap or treemap with no numeric values where precision matters; choropleth over regions of very different area; word cloud for precise values.
Fix: Use a bar chart or table, or overlay the numeric values.
Grade: MAJOR. Sources: ui-ux-pro-max.

### DA-10 Chart drawn from too few data points
Symptom: A line through three points or a handful of dots implies a pattern that does not exist.
Detect: Line series with fewer than 4 points; scatter with fewer than 20 points; box plot with fewer than 20 points per group; funnel with fewer than 3 stages; sankey with fewer than 3 pairs.
Fix: Show a stat card, table, or bar chart instead.
Grade: MAJOR. Sources: ui-ux-pro-max.

### DA-11 Full dataset rendered at once
Symptom: Long lists and tables freeze the page, scroll sluggishly, and wait for the whole collection before showing anything.
Detect: Thousands of DOM nodes in one list; no pagination, infinite scroll, `content-visibility: auto`, or virtualization for 1000 or more items; API calls returning full collections rendered at once.
Fix: Paginate, or virtualize so only visible rows render, and use `content-visibility: auto` on long lists.
Grade: MAJOR. Sources: impeccable, claude-code-workflows, ui-ux-pro-max.

### DA-12 Too many equal-weight headline metrics
Symptom: A row of identical big-number tiles or gauges gives every metric equal weight and exceeds what can be absorbed.
Detect: More than 4 KPI widgets above the fold (impeccable) or more than 4 to 6 KPI cards (ui-ux-pro-max); 3 or more gauges side by side; identical tiles with oversized numeral, muted caption, and delta chip regardless of importance.
Fix: Show at most 4 to 6 ranked metrics structured around the data, with a bullet chart grid for several targets.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max.

### DA-13 Hierarchical or network chart too deep or too large
Symptom: Nested rectangles, outer rings, or a hairball of nodes become unreadable.
Detect: Treemap or sunburst deeper than 3 levels; network graph over 500 nodes with no clustering, or over 100 nodes in SVG; process map over 100 nodes unfiltered; word cloud over 5000 terms.
Fix: Limit to 3 levels, cluster or filter to the top cases, or use a tree table.
Grade: MAJOR. Sources: ui-ux-pro-max.

### DA-14 Decorative effects obscuring data marks
Symptom: 3D bevels, glossy gradients, drop shadows, or heavy track bars make values harder to read than the decoration.
Detect: Gradient fills, shadow plugins, or 3D effects on bars and points; 3D chart where 2D conveys the same insight; status colors not driving hierarchy; full-width background tracks on inline comparison bars.
Fix: Use flat marks, a 2D projection, and let status colors carry the hierarchy.
Grade: MAJOR. Sources: ui-ux-pro-max, design-taste-frontend.

### DA-15 Long list as undifferentiated hairline rows
Symptom: Ten or more items rendered as bullets or identical rows with a hairline under each, and nothing grouped.
Detect: `<ul>` with more than 5 `<li>` or `divide-y` rows in a content section; 10 or more label and value rows each with `border-b`; both `border-t` and `border-b` on every row.
Fix: Group into 2 to 3 clusters, a card grid, tabs, or featured-versus-rest with a disclosure, using one divider at most.
Grade: MAJOR. Sources: design-taste-frontend.

### DA-16 Performance metric without target or benchmark
Symptom: A needle or delta points somewhere with nothing to compare it against.
Detect: Gauge with no target marker or threshold zones; bullet chart with no target range; period comparisons with no benchmark line, deltas not computed, and colors that carry no meaning.
Fix: Add a target line, threshold zones, and benchmarks, or show a plain number.
Grade: MAJOR. Sources: ui-ux-pro-max.

### DA-17 Wide table overflowing the page on small screens
Symptom: A wide table widens the whole page or shrinks to illegibility on phones.
Detect: `<table>`, map, or `<pre>` without an `overflow-x: auto` wrapper causing document-level horizontal scroll; no mobile `display: block` with `data-label` transformation.
Fix: Scroll the table inside its own container or transform rows to labeled cards on mobile.
Grade: MAJOR. Sources: impeccable, better-accessibility, ui-ux-pro-max.

### DA-18 Sortable columns without a visible or announced sort state
Symptom: Users cannot tell which columns sort or which direction is active, and assistive tech hears nothing.
Detect: `<table>` with static headers on sortable data; clickable headers with no arrow or indicator; sortable headers lacking `aria-sort`.
Fix: Support sorting, show an indicator on the active column, and set `aria-sort`.
Grade: MAJOR. Sources: ui-ux-pro-max, claude-code-workflows.

### DA-19 Numbers not end-aligned in tables
Symptom: Numeric columns are left or center aligned, so magnitudes cannot be compared down the column.
Detect: Numeric `<td>` without `text-align: end`; text columns without `text-align: start`; `text-align` not set per column type.
Fix: Use `text-align: end` for numbers and `text-align: start` for text.
Grade: MAJOR. Sources: claude-code-workflows, better-layout.

### DA-20 Empty chart frame instead of an empty, loading, or error state
Symptom: An empty axis frame with no bars suggests a bug rather than "no data yet" or a failed load.
Detect: Chart rendered with empty datasets or in the error branch; no empty-state message, loading state, error message, or retry action.
Fix: Show "No data yet" with guidance, a loading state, or an error with retry.
Grade: MAJOR. Sources: ui-ux-pro-max.

### DA-21 Layout designed only for the typical count
Symptom: The layout looks fine with 5 items and breaks at 0, 1, or 500.
Detect: No empty state; no truncation, pagination, or virtualization for the maximum range; fixed-height containers assuming one data shape; no spec for the 100-item case.
Fix: Design and specify behavior for the minimum, typical, and maximum content ranges.
Grade: MAJOR. Sources: impeccable, design-plugin/design-handoff.

### DA-22 Dense point cloud without aggregation or transparency
Symptom: A cloud of thousands of overlapping points hides density and renders slowly.
Detect: Datasets over 1000 points plotted directly with no aggregation, sampling, or drill-down; 500 to 5000 points at opacity 1; over 5000 points not hexbinned.
Fix: Aggregate or sample, use 0.6 to 0.8 opacity for 500 to 5000 points, hexbin above 5000.
Grade: MAJOR. Sources: ui-ux-pro-max.

### DA-23 Large numbers without separators or inconsistent decimals
Symptom: Values like 1234567 are hard to parse, and amounts mix decimal places.
Detect: Numbers rendered without thousand separators or abbreviations; currency unformatted; mixed decimal places in one column.
Fix: Format as 1,234 or 1.2K, format currency, and keep decimals consistent per column.
Grade: MAJOR. Sources: ui-ux-pro-max.

### DA-24 Legend missing or detached from the chart
Symptom: Series cannot be identified, or the legend sits far from the plot after a scroll.
Detect: `legend: { display: false }`; legend rendered outside the chart container or below the fold.
Fix: Show the legend adjacent to the chart.
Grade: MAJOR. Sources: ui-ux-pro-max.

### DA-25 No tooltips or data labels on marks
Symptom: Exact values cannot be read; users estimate from gridlines.
Detect: Tooltips disabled; no value shown on hover on web or tap on mobile; no data labels.
Fix: Show exact values through tooltips on hover or tap, or as data labels.
Grade: MAJOR. Sources: ui-ux-pro-max.

### DA-26 Axis without a title or units, or with unreadable labels
Symptom: Axes carry no units, and on mobile their labels are cut off or turned 90 degrees.
Detect: Missing axis titles or units; `maxRotation` producing vertical labels on small screens; ellipsized tick labels.
Fix: Title each axis with units and a readable scale; avoid truncation and rotation on mobile.
Grade: MAJOR. Sources: ui-ux-pro-max.

### DA-27 Large dataset without search or filter
Symptom: Users scroll through hundreds of rows to find one.
Detect: Long tables or lists with no search input or filter controls.
Fix: Add search and filter controls.
Grade: MAJOR. Sources: impeccable.

### DA-28 Full data table embedded in a marketing section
Symptom: A 20-row publication table, a 30-row award list, or a giant pricing matrix sits in a landing page.
Detect: `<table>` or list with more than 15 to 20 rows inside a marketing section.
Fix: Show the top 3 to 5 highlights with a "View full list" link, or give the data its own page.
Grade: MAJOR. Sources: design-taste-frontend.

### DA-29 Cramped table rows
Symptom: Rows are too short and tightly packed to scan.
Detect: Row height under about 36px; cell padding under about 8px.
Fix: Give rows adequate height and cell padding.
Grade: MAJOR. Sources: claude-code-workflows.

### DA-30 Row actions indistinguishable
Symptom: Edit, delete, and view icons on each row look alike.
Detect: Same icon style and color for destructive and non-destructive row actions.
Fix: Make per-row actions clearly distinguishable and style destructive ones differently.
Grade: MAJOR. Sources: claude-code-workflows.

### DA-31 Status buried in text instead of a badge
Symptom: Pending, approved, or rejected status is hidden in body text or absent from list items.
Detect: No color-coded status badge on list items or rows.
Fix: Show status as a color-coded badge with a text label.
Grade: MAJOR. Sources: claude-code-workflows.

### DA-32 Partial result without both counts
Symptom: "Some files failed" with no numbers and no retry.
Detect: Batch outcome messages lacking counts for both success and failure, or a retry action.
Fix: State both counts and offer retry: "9 of 12 files uploaded. Retry 3 failed files".
Grade: MAJOR. Sources: better-writing.

### DA-33 Chart faked with sized divs
Symptom: "Charts" are stacked colored blocks with no axes, scale, tooltips, or legend.
Detect: Width-percentage `div` elements standing in for data instead of a real chart with axes and a scale.
Fix: Render a real chart with axes, scale, legend, and tooltips.
Grade: MAJOR. Sources: ui-ux-pro-max.

### DA-34 Table header weak, not sticky, or rows hard to track
Symptom: The header row reads like data, scrolls away in long tables, and rows are hard to follow across columns.
Detect: `th` with the same weight and color as `td`; no `position: sticky` on `thead`; no frozen key column in wide tables; no row hover, alternating bands, or highlighted key column in comparison tables.
Fix: Distinguish headers, make them sticky, freeze the key column, and add row hover or banding.
Grade: POLISH. Sources: claude-code-workflows, ui-ux-pro-max.

### DA-35 Small datasets or pie slices without direct labels
Symptom: A chart with four bars still sends the eye to the axis, and pie slices show no percentages.
Detect: Few data points with no value labels on the marks; pie slices with no percent labels; largest slice not starting at 12 o'clock; more than 5 to 6 colors.
Fix: Label values directly on small datasets and every pie slice with its percent, largest slice at the top.
Grade: POLISH. Sources: ui-ux-pro-max.

### DA-36 Tick labels crowded or time granularity unstated
Symptom: Tick labels overlap on narrow screens, and a time series never says whether points are days, weeks, or months.
Detect: Tick spacing too tight to read; `autoSkip` disabled at small widths; time axis with no granularity label or toggle.
Fix: Auto-skip ticks on small screens, label the time granularity, and allow switching it.
Grade: POLISH. Sources: ui-ux-pro-max.

### DA-37 Forecast indistinguishable from actuals or without history
Symptom: A projection floats with no baseline, or forecast and actual lines look the same.
Detect: Forecast line styled like actuals; no confidence band; no historical series; forecast horizon over 30 percent of the x-axis; predictions undated.
Fix: Show 30 to 90 days of history, style the forecast distinctly, and show confidence bands and dates.
Grade: POLISH. Sources: ui-ux-pro-max.

### DA-38 Legend entries that do not toggle series
Symptom: Users cannot hide noisy series to focus on one.
Detect: Legend items not clickable to toggle series visibility.
Fix: Make legend entries toggle their series.
Grade: POLISH. Sources: ui-ux-pro-max.

### DA-39 Category bars not sorted by value
Symptom: The ranking, which is the point of the chart, has to be worked out by eye.
Detect: Category bars in arbitrary or alphabetical order.
Fix: Sort bars descending by value and offer a sort control.
Grade: POLISH. Sources: ui-ux-pro-max.

### DA-40 Gridlines as prominent as the data
Symptom: Dark or thick gridlines compete with the data lines.
Detect: Grid color darker than roughly gray-200; gridline width equal to the data stroke.
Fix: Keep gridlines thin and low-contrast.
Grade: POLISH. Sources: ui-ux-pro-max.

### DA-41 Chart redrawn from blank on data change
Symptom: Changing a filter redraws the whole chart from empty, and continuity between states is lost.
Detect: Chart components remounted on data change; no transition or View Transition between states.
Fix: Animate between data states so marks morph rather than reappear.
Grade: POLISH. Sources: impeccable.

### DA-42 No export from a data-heavy view
Symptom: Users take captures of charts because there is no CSV or image export.
Detect: Dashboards or reports with no export or download affordance.
Fix: Offer CSV or image export of the data.
Grade: POLISH. Sources: ui-ux-pro-max.

### DA-43 No bulk actions on lists
Symptom: Users must act on items one at a time.
Detect: Lists and tables without multi-select or batch operations.
Fix: Add bulk selection and batch actions.
Grade: POLISH. Sources: impeccable, ui-ux-pro-max.

### DA-44 Fake round numbers in sample data
Symptom: Stats like 99.99%, 50%, or $100.00 read as invented.
Detect: Round or repeating numbers in KPIs, pricing, or phone numbers.
Fix: Use organic values such as 47.2%, $99.00, or +1 (312) 847-1928.
Grade: POLISH. Sources: redesign-existing-projects.

### DA-45 Nested chart levels without tonal step or borders
Symptom: Sunburst rings or nested sectors merge into one another.
Detect: Levels not 15 to 20 percent lighter each step outward; no contrasting border between sectors.
Fix: Lighten each level 15 to 20 percent from the center outward and add contrasting borders.
Grade: POLISH. Sources: ui-ux-pro-max.


## Generic AI tells (GE)

### GE-01 Fabricated social proof shown as real
Symptom: Testimonials, logo walls, ratings, or stat counters present invented people, companies, or numbers as if they were real.
Detect: Quote cards attributed to "John Doe", "Jane Smith" or stock avatars; logo walls of "Acme", "Nexus", "Globex", "SmartFlow"; counters such as "10k+ users" or "99% uptime" with no data source behind them.
Fix: Use real quotes, logos, and figures, or remove the block; label sample data as sample.
Grade: BLOCKING. Sources: impeccable, gpt-taste, redesign-existing-projects.

### GE-02 Purple-to-blue gradient with no brand tie
Symptom: Heroes, buttons, or backgrounds wear the violet-to-blue gradient that every generated page defaults to.
Detect: `linear-gradient` between violet, indigo, or purple (#6366F1, #8B5CF6, #A855F7) and blue, cyan, or pink (#EC4899); `from-purple-500 to-blue-500`, `from-indigo-500 to-purple-500`, `from-purple-500 to-pink-500`; `bg-violet-600 shadow-violet-500/50`; gradient washes on surfaces with no brand reason.
Fix: Use a neutral base with one brand-derived accent; keep any gradient subtle and tied to the palette.
Grade: MAJOR. Sources: impeccable, design-taste-frontend, ui-ux-pro-max, redesign-existing-projects, frontend-design, minimalist-ui.

### GE-03 Three identical feature cards after a centered hero
Symptom: A centered hero, three equal icon-title-blurb cards, then testimonials, pricing, and an FAQ: the stock page assembly.
Detect: `grid-cols-3` or `repeat(3, 1fr)` of cards sharing one icon, title, and blurb structure; section order matches the usual template; every list on the page padded or trimmed to exactly three items.
Fix: Compose for the content: natural item count, asymmetric or zigzag layout, non-card sections, varied spans.
Grade: MAJOR. Sources: impeccable, design-taste-frontend, ui-ux-pro-max, redesign-existing-projects, frontend-design, unslop.

### GE-04 Stock default typeface on a brand surface
Symptom: Type carries no personality because the primary face is the default every generated page uses.
Detect: `font-family` is Inter, Roboto, Arial, Open Sans, or system-ui where brand matters; impeccable also flags Space Grotesk, DM Sans, Outfit, Plus Jakarta Sans, Syne, IBM Plex Sans, and Instrument Sans, while design-taste-frontend and gpt-taste still suggest Outfit and Geist.
Fix: Choose a face for this brand; defaults only where neutrality is the point, such as accessibility-first or public-sector surfaces.
Grade: MAJOR. Sources: impeccable, design-taste-frontend, minimalist-ui, gpt-taste, frontend-design.

### GE-05 Editorial serif styling on a brief that is not editorial
Symptom: A display serif, italics, and drop caps chosen because the brief "feels premium", the most-tested generated tell.
Detect: Fraunces, Instrument Serif, Playfair Display, Cormorant, Newsreader, Lora, Crimson, or DM Serif as the display face; italic serif headlines, drop caps, hairline rules between everything, `border-radius: 0`, dense columns, with no editorial, luxury, or heritage rationale.
Fix: Pick the display face and layout lane for this brand; editorial is one lane among many.
Grade: MAJOR. Sources: impeccable, design-taste-frontend, frontend-design.

### GE-06 Uppercase tracked eyebrow above every heading
Symptom: Every section opens with a small letter-spaced caps label that restates the heading, the templated section rhythm.
Detect: `text-transform: uppercase; letter-spacing: 0.1em` or more, or `text-[11px] uppercase tracking-[0.18em]`, before each h2; labels such as "FEATURES", "ABOUT US", "SECTION 01", or year ranges; more than one eyebrow per three sections (design-taste-frontend, hero counts as one).
Fix: Remove eyebrows that add no classification; keep at most one per three sections, in sentence case.
Grade: MAJOR. Sources: design-taste-frontend, gpt-taste, frontend-design.

### GE-07 Gradient-filled headline or metric text
Symptom: Headings or big numbers are filled with a color gradient as the main visual trick.
Detect: `background-clip: text` or `-webkit-background-clip: text` with a gradient background and `color: transparent`; `bg-clip-text text-transparent bg-gradient-to-r` on h1, h2, or stat numerals.
Fix: Fill text with one solid color; carry emphasis through weight and size.
Grade: MAJOR. Sources: impeccable, design-taste-frontend.

### GE-08 Glassmorphism as the default surface
Symptom: Cards, navbars, and modals are frosted translucent panels, the surface treatment generated pages reach for first.
Detect: `backdrop-filter: blur()` with low-alpha white or black backgrounds and 1px rgba borders on panels; glass stacked over gradients; anything beyond a subtle navbar blur (minimalist-ui).
Fix: Use opaque surfaces with depth from layering or texture; keep glass for one specific purpose.
Grade: MAJOR. Sources: impeccable, minimalist-ui.

### GE-09 Neon accent and glow on a near-black canvas
Symptom: A near-black page with one electric accent and colored halos, the default dark look of generated pages.
Detect: Backgrounds `#0a0a0a` to `#111`, `bg-zinc-950`, or `bg-black` with fully saturated accents (`#00ff..`, `#ff00..`, acid green, vermilion); glow via `shadow-[0_0_40px_rgba(...)]`, `shadow-violet-500/50`, saturated `drop-shadow`, or `text-shadow`.
Fix: Derive the dark palette and accent from the brand, vibrant but not neon, and drop the glow.
Grade: MAJOR. Sources: impeccable, design-taste-frontend, minimalist-ui, frontend-design.

### GE-10 Big-number stat tile row as the default header
Symptom: The hero or dashboard opens with three or four uniform tiles of oversized numerals and muted captions.
Detect: A row of equal stat tiles with giant figures, small labels, and gradient accents at the top of a hero or dashboard; "10k+ users" and "99% uptime" counters inside the hero.
Fix: Show a prominent metric only where real data earns it; shape the display around the actual metrics.
Grade: MAJOR. Sources: impeccable, gpt-taste, frontend-design.

### GE-11 Decorative labels and cues around the hero that carry no information
Symptom: Version pills, locale strips, word strips, tag rows, stamps, or scroll prompts decorate the hero or footer as filler.
Detect: "v0.6", "BETA", "EARLY ACCESS", or "last sync 4s ago" pills; "LIS 14:23 · 18°C" strips; "DESIGN · BUILD · SHIP" strips; `rounded-full` tag rows under the H1; stamp badges over it; "Scroll to explore" text or an animated mouse icon.
Fix: Remove unless the string is real live status or the brief is about a launch.
Grade: MAJOR. Sources: design-taste-frontend, gpt-taste, redesign-existing-projects.

### GE-12 Zero-padded numbering on content that is not a sequence
Symptom: Cards, sections, and tiles carry "01", "02", "03" counters although their order carries no meaning.
Detect: "01", "02", "03" prefixes on feature cards; eyebrows such as "00 / INDEX" or "001 · Capabilities"; "01 / 4" counters on grid tiles; serial lines such as "Brand · No. 01 · Product".
Fix: Number only real steps or timelines; otherwise name the topic or drop the label.
Grade: MAJOR. Sources: design-taste-frontend, gpt-taste, frontend-design.

### GE-13 Every content block boxed as the same rounded card
Symptom: Lists, tables, and flows alike are chopped into identical white cards with one radius and one shadow.
Detect: `.card { background: #fff; border: 1px solid; border-radius; box-shadow: rgba(0,0,0,.1) }` on every block; one radius regardless of hierarchy; card grids for content that is a list, table, form, or single flow.
Fix: Use cards only where elevation signals hierarchy; elsewhere use spacing or background alone, and vary surfaces.
Grade: MAJOR. Sources: impeccable, frontend-design, redesign-existing-projects.

### GE-14 Centered single-column stack for every section
Symptom: Every section is a centered column, neither asymmetric nor rigorously gridded, which reads as the default landing template.
Detect: `text-center items-center mx-auto` with a max-width wrapper on the hero and every following section; no left-aligned composition and no visible grid.
Fix: Commit to a left-aligned asymmetric composition or a strict visible grid.
Grade: MAJOR. Sources: impeccable, design-taste-frontend, ui-ux-pro-max.

### GE-15 Warm cream, serif, and terracotta as the default premium palette
Symptom: Premium, artisan, or wellness briefs all get cream backgrounds, a serif display, and brass, clay, or terracotta accents.
Detect: Backgrounds near `#F4F1EA`, `#f5f1ea`, `#f7f5f1`, `#fbf8f1`, `#efeae0`, `#ece6db`, `#faf7f1`, `#e8dfcb`; accents near `#D97757`, `#b08947`, `#b6553a`, `#9a2436`, `#9c6e2a`, `#bc7c3a`, `#7d5621`; text near `#1a1714`; serif display on top.
Fix: Derive the palette from this brand; use the warm-craft family only when the brief names it.
Grade: MAJOR. Sources: design-taste-frontend, frontend-design, impeccable.

### GE-16 Emoji used as icons or bullets
Symptom: Headings, list items, buttons, or alt text contain emoji glyphs standing in for icons.
Detect: Emoji code points in markup, visible text, button labels, or `alt` attributes; headings and bullets opening with an emoji.
Fix: Replace with a consistent icon set or plain text; remove decorative emoji.
Grade: MAJOR. Sources: minimalist-ui, gpt-taste, unslop, ui-ux-pro-max, design-taste-frontend.

### GE-17 AI vocabulary and frames in interface copy
Symptom: Headlines and blurbs lean on words and sentence shapes that mark the text as machine-written.
Detect: Visible copy contains "elevate", "seamless", "unleash", "next-gen", "game-changer", "delve", "tapestry", "crucial", "enhance", "landscape", "pivotal", "showcase", "testament", "underscore", "vibrant", "In the world of"; headlines opening "Not just a"; bold label plus colon restating its own sentence.
Fix: Write plain, specific language that states the point directly.
Grade: MAJOR. Sources: redesign-existing-projects, unslop.

### GE-18 Blurred gradient blobs standing in for a hero visual
Symptom: The hero is headline copy over blurred gradient blobs with no image, product, or demo: a placeholder.
Detect: Hero section with no `<img>`, video, or component preview; absolutely positioned `blur-3xl` divs, `radial-gradient` mesh layers, or `bg-gradient-to-*` on `bg-zinc-950` or `bg-black` as the only visual.
Fix: Open with a real asset: photography, a real screenshot, a live component, or a strong typographic move.
Grade: MAJOR. Sources: design-taste-frontend, frontend-design.

### GE-19 Fake product screenshot built from divs
Symptom: The "product preview" is nested rectangles imitating an app window, the single most recognized generated tell.
Detect: Nested divs with `rounded` and `bg-zinc-800`, fake window dots, fake rows, task lists, or terminals, with no `<img>`; strings such as "v0.6.2-rc.1" or "last sync 4s ago · main" inside the mock.
Fix: Use a real screenshot, a real mini component, or editorial photography; otherwise drop the preview.
Grade: MAJOR. Sources: design-taste-frontend.

### GE-20 Primary hue chosen by reflex instead of brand
Symptom: The accent is default blue or warm orange, or the whole palette is guessable from the product category alone.
Detect: `oklch(... 250)` or `oklch(... 60)` primaries, framework blue CTAs; theme predictable from the domain: observability dark blue, healthcare white and teal, finance navy and gold, crypto neon on black.
Fix: Treat hue and theme as decisions for this brand and audience; a category palette needs a stated trust reason (ui-ux-pro-max).
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max.

### GE-21 Component library shipped with untouched default tokens
Symptom: Default radii, colors, shadows, and type from the component kit make the page look like every site built on it.
Detect: Untouched generated UI component files, default `--radius` and theme variables, system fonts, default shadows, framework default blue; nothing in the token file traces to this brand.
Fix: Set radii, colors, shadows, and type for this product before shipping; never ship the default state.
Grade: MAJOR. Sources: design-taste-frontend, impeccable, ui-ux-pro-max.

### GE-22 Decorative accent repeated on every item
Symptom: Every card, heading, or label wears the same ornament: a left stripe, a rounded icon tile, or a colored dot.
Detect: `border-left: 4px solid <accent>` on cards, alerts, or rows; large rounded icon containers above each heading; `w-2 h-2 rounded-full bg-emerald-500` before text that carries no live state.
Fix: Remove the ornament; allow a dot only for real state, at most one per section.
Grade: MAJOR. Sources: impeccable, design-taste-frontend.

### GE-23 One section architecture repeated down the whole page
Symptom: Every section is the same text-left image-right split or the same card grid, one rhythm with no variance.
Detect: Repeated two-column split sections, or the same uniform card component in every section; no section breaks the grid or changes proportion.
Fix: Vary section architecture by content: full-bleed, asymmetric, single feature, or a grid break.
Grade: MAJOR. Sources: gpt-taste, impeccable.

### GE-24 Rotated edge text and hairline grid lines as decoration
Symptom: Vertical labels along the page edge and crosshair lines across the page are agency-portfolio cliches with no structural job.
Detect: `writing-mode: vertical-rl`, `rotate-90`, or `-rotate-90` on labels; absolutely positioned `border-l` or `border-t` lines or background grid patterns not tied to content columns.
Fix: Use lines only where they organize real content; rotate text only for a real compositional purpose.
Grade: MAJOR. Sources: design-taste-frontend.

### GE-25 Fade-and-slide-up entrance on every section
Symptom: Each section fades in and slides up as it scrolls into view, the stock reveal of generated pages.
Detect: `opacity: 0; transform: translateY(20px)` with an intersection observer or `whileInView` applied to every section.
Fix: Keep one orchestrated moment, such as a single load sequence, and drop per-section entrances.
Grade: MAJOR. Sources: frontend-design.

### GE-26 Hover lift on every static card
Symptom: Cards that are not clickable lift, scale, or gain shadow on hover, promising interaction that is not there.
Detect: `.card:hover { transform: translateY(-4px); box-shadow }` or `hover:scale-105` on elements with no link, button, or handler.
Fix: Reserve hover motion for interactive elements that answer the user's action.
Grade: MAJOR. Sources: frontend-design.

### GE-27 More than one marquee on a page
Symptom: Logos, a manifesto, and a word strip all scroll sideways on the same page, which reads as filler.
Detect: Two or more horizontally scrolling text or logo marquees in one page.
Fix: Keep at most one marquee, in the single section where it serves the content.
Grade: MAJOR. Sources: design-taste-frontend.

### GE-28 Single accented word in a headline
Symptom: One word of the headline is italic, colored, or a different weight for emphasis, a template flourish.
Detect: A `<span>` inside the h1 or h2 that changes color, style, or weight on a single word.
Fix: Remove the accent and let the whole headline carry the weight.
Grade: MAJOR. Sources: frontend-design.

### GE-29 Visual style that contradicts the product's audience
Symptom: The look fights what the product is: playful claymorphism on banking, agency motion on public-sector, cinematic effects on a utility.
Detect: Glass, neon, brutalist, pastel, generative art, or cinematic transitions on a trust-first, regulated, utilitarian, or conservative product; palette and type chosen without reference to industry or audience.
Fix: Choose the style from the product type and audience before styling anything.
Grade: MAJOR. Sources: ui-ux-pro-max, impeccable, design-taste-frontend.

### GE-30 Several generated tells stacked on one screen
Symptom: Gradient hero, glass cards, neon accents, gradient metrics, and piled effects together read as an "AI slop gallery".
Detect: Count catalog tells in one capture: 5 or more is a slop gallery, 3 to 4 heavy generated aesthetic, 1 to 2 some tells (impeccable); stacked effects, trend elements, or confetti with no change to type, scale, or composition.
Fix: Remove every tell; make boldness come from type, scale, color commitment, and composition.
Grade: MAJOR. Sources: impeccable, design-taste-frontend, frontend-design, apple-design.

### GE-31 Interface with no point of view specific to the product
Symptom: The page could be for any product; palette, type, imagery, and layout come from a template, not the subject.
Detect: Swap the product name and nothing else would change; the tone cannot be named in one phrase; pale accent, small type, cream and slate, standard layout, and no single element anyone would remember.
Fix: Pick one direction derived from the subject, audience, and brand, and make one deliberate distinctive move.
Grade: MAJOR. Sources: impeccable, frontend-design, design-taste-frontend, ui-ux-pro-max.

### GE-32 Stock SaaS component shapes used unchanged
Symptom: Nav, buttons, FAQ, testimonials, and pricing are the exact shapes every template ships, chosen by habit rather than content.
Detect: Logo-left links-right nav; filled plus outlined button pair in every section; accordion FAQ; three-card testimonial carousel with dots; three pricing towers with the middle one only taller.
Fix: Choose each component's shape for its content; highlight a recommended tier with color and emphasis.
Grade: POLISH. Sources: redesign-existing-projects, gpt-taste, frontend-design.

### GE-33 Sun and moon theme toggle in the header
Symptom: A sun or moon icon button in the nav flips light and dark, a default control nobody asked for.
Detect: Icon button toggling a `dark` class in the header, with no `prefers-color-scheme` handling.
Fix: Follow the system preference by default and move the override into settings.
Grade: POLISH. Sources: redesign-existing-projects.

### GE-34 Neutrals and dark surfaces tinted toward a stock hue
Symptom: Greys lean warm orange or cool blue and dark surfaces lean navy regardless of the brand's hue.
Detect: Neutral or dark-surface hue near 60 or 250 on a brand whose primary is elsewhere; `#0B0B0B` or `#111` as the universal black.
Fix: Tint neutrals and dark surfaces with the brand hue and chroma, varying only lightness.
Grade: POLISH. Sources: impeccable, frontend-design.

### GE-35 Generic thin-line icon library chosen by default
Symptom: The icons are the same Lucide, Feather, or Heroicons glyphs as every generated site.
Detect: Imports from `lucide-react`, `feather-icons`, or Heroicons in a project where the user did not ask for them and they were not already a dependency.
Fix: Pick an icon set for the brand (Phosphor, Radix, Tabler, HugeIcons) with one consistent stroke weight.
Grade: POLISH. Sources: design-taste-frontend, minimalist-ui.

### GE-36 Monospace as a style cue on non-code text
Symptom: Captions, timestamps, eyebrows, and stats are set in monospace to look "technical", usually the same stock mono.
Detect: `font-family: monospace`, JetBrains Mono, IBM Plex Mono, or Space Mono on labels that are neither code nor tabular data.
Fix: Use monospace only where code or tabular semantics justify it, and choose the face for the brand.
Grade: POLISH. Sources: impeccable, frontend-design.

### GE-37 Template punctuation flourishes in labels and links
Symptom: Every link ends in an arrow, meta rows are joined with middle dots, and labels follow a caps-word-dash-fragment pattern.
Detect: "→" or `&rarr;` appended to CTA strings; "·" between author, date, and read-time; labels made of an uppercase word, a spaced long dash, then a fragment.
Fix: Drop the arrow unless it conveys needed direction; set meta rows and labels as plain phrases.
Grade: POLISH. Sources: frontend-design, design-taste-frontend.


## Consistency (CS)

### CS-01 Logo, wordmark or legal copy changed silently
Symptom: The brand mark is redrawn, or consent, cookie or legal text is reworded, inside an unrelated change.
Detect: A changed logo asset, wordmark SVG or modified legal and consent strings in the diff of a UI change whose scope did not include them.
Fix: Restore the original logo, wordmark and legal copy; change them only with explicit approval.
Grade: BLOCKING. Sources: design-taste-frontend.

### CS-02 Hardcoded value where a token exists
Symptom: Colors, spacing, radii or type sizes drift from the system because components carry literal values beside the tokens.
Detect: Hex, `rgb()`, `hsl()`, `oklch()`, `#RRGGBBAA` or px literals, bracketed arbitrary utilities like `p-[13px]` or `text-[#1a1a2e]`, and ad hoc `border-radius` or `box-shadow` values in component styles, slides or specs while a token for that role exists.
Fix: Replace each literal with the existing token, or add a token for the missing role.
Grade: MAJOR. Sources: impeccable, better-interface, better-ui, better-colors, ui-ux-pro-max, design-review, claude-code-workflows, design-plugin/design-system, design-plugin/design-handoff.

### CS-03 Screens drift from one visual language
Symptom: Screens or sections differ in palette, type, radius, shadow or components, so the product reads as stitched together.
Detect: Count distinct font families, type scales, radii, shadow recipes, button styles and palettes across routes; per-page style overrides instead of shared tokens; each screen introducing a new visual treatment.
Fix: Apply one token set and one component vocabulary across every screen; reserve novelty for moments.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max, design-review, claude-code-workflows, design-plugin/design-critique.

### CS-04 Same control drawn two ways
Symptom: The same action or component, such as a save button or input, looks different in two places.
Detect: Compare identical actions across views for shape, height, radius, color and states; a local component that mirrors a shared one with different padding, radius or states; one-off copies, lookalikes of a system component, or `!important` overrides.
Fix: Use the shared component everywhere; add a missing variant or size to it instead of forking.
Grade: MAJOR. Sources: impeccable, design-taste-frontend, claude-code-workflows, design-plugin/design-system.

### CS-05 Mixed radii, shadows or borders on same-level surfaces
Symptom: Cards, buttons and inputs at the same level show different corner radii, shadow depths or border treatments.
Detect: Several `border-radius` values on same-level surfaces, such as `rounded-full`, `rounded-2xl` and `rounded-md` mixed with no documented rule; multiple `box-shadow` recipes for one elevation; border width or color varying across cards and dividers.
Fix: Define one radius per level, one shadow per elevation and one border recipe, and apply them everywhere.
Grade: MAJOR. Sources: design-taste-frontend, design-review, minimalist-ui, ui-ux-pro-max.

### CS-06 Identical-looking controls behave differently
Symptom: Controls that look the same act differently, so users cannot predict outcomes.
Detect: The same button label, icon or card opening a page here and a modal there; row click selecting in one list and opening detail in another; the same gesture deleting here and archiving there.
Fix: Give the same control, label and gesture the same behavior everywhere.
Grade: MAJOR. Sources: impeccable, apple-design, design-plugin/design-critique.

### CS-07 Primitive color token used directly in a component
Symptom: A component paints a raw palette step, so themes cannot repoint it and it keeps the light value.
Detect: `var(--blue-600)`, `var(--neutral-200)`, `bg-blue-600` or `text-gray-500` in component files; primitives redefined under a dark selector instead of semantic roles.
Fix: Point a semantic token at the primitive and reference only the semantic tier; retheme that layer.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max, better-colors.

### CS-08 Token used outside its role
Symptom: A token borrowed for another role looks right today and breaks when its own role is retuned.
Detect: A border or separator token inside `color:`; a text token inside `background:`; spacing tokens used for radius; a palette token and a semantic token for the same role side by side.
Fix: Use each token only in its role; add a token for the missing role.
Grade: MAJOR. Sources: impeccable, better-colors.

### CS-09 Rendering language mixed on one surface
Symptom: Some elements break the product's declared style, such as flat fills beside glossy bevels or shadows inside a flat system.
Detect: Gradients, inner shadows, blur or textures on sibling components that are flat elsewhere; `box-shadow` or `border-radius` above 0 in a declared sharp monochrome system; a minimal direction with effects on everything, or a maximal direction rendered flat and static.
Fix: Commit to one rendering language per surface and match every element's depth and effects to it.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max, frontend-design.

### CS-10 Visual register at odds with the brand or audience
Symptom: The interface's register does not fit its product: playful or raw on a trust product, sterile on a creative one.
Detect: Saturated color blocks, neon, glitch, chrome gloss, hand-drawn or puffy clay treatments on finance, health, legal or enterprise products; grey static grids on entertainment or creative brands; copy tone at odds with the stated brand.
Fix: Tune color, type, motion and copy to the intended register for the stated audience.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max.

### CS-11 Standard platform pattern reinvented
Symptom: A familiar control or convention is replaced with an invented one, so users' habits fail.
Detect: Custom scrollbars, close controls away from the expected corner, invented form controls, unconventional link styling; Material components on iOS or iOS switches on Android; components deviating from category conventions with no functional reason.
Fix: Follow the platform's and category's standard patterns unless a functional reason justifies the deviation.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max.

### CS-12 Accent hue drifts between sections or from the brand
Symptom: A second accent appears, such as a blue CTA on a warm-grey site or a teal badge in the footer.
Detect: Buttons, badges, links or icons whose hue differs from the hero accent in later sections; a redesign or asset whose accent or typeface does not match the extracted brand tokens.
Fix: Lock one accent from the brand tokens and audit every component and asset against it.
Grade: MAJOR. Sources: design-taste-frontend, ui-ux-pro-max.

### CS-13 Navigation or recurring control placement changes by page
Symptom: The nav is a top bar on some pages and a sidebar on others; close buttons move around.
Detect: Different navigation components or positions per route; the same recurring control, such as close or save, in varying positions across screens.
Fix: Keep navigation and recurring controls in the same place on every screen.
Grade: MAJOR. Sources: ui-ux-pro-max, apple-design.

### CS-14 Part of the interface left unstyled or dated beside polished parts
Symptom: A polished area sits next to a rough one, such as a refined hero beside an unstyled table.
Detect: Default browser form controls, bevelled buttons, table-based layout or tiny type next to styled components; refined primary states with crude edge states.
Fix: Bring every part, including edge states, to the same quality with the shared component set.
Grade: MAJOR. Sources: impeccable, ui-ux-pro-max.

### CS-15 Palette structure out of proportion
Symptom: Similar surfaces land on different hues, and backgrounds, borders and text cannot be told apart.
Detect: More hue families than one neutral, one accent and the shipped statuses; fewer neutral steps than accent steps; no primary, neutral, semantic and surface role structure behind the colors.
Fix: Collapse extra ramps, give the neutral at least as many steps as the accent, and assign every color a role.
Grade: MAJOR. Sources: impeccable, better-colors.

### CS-16 Mixed perspectives in one flow
Symptom: "My account" sits beside "Your settings" in the same flow.
Detect: Both "My" and "Your" prefixes within one screen, flow or navigation group.
Fix: Pick one perspective and use it throughout the flow.
Grade: MAJOR. Sources: better-writing.

### CS-17 Color carries different meanings across screens
Symptom: One hue means success on one screen and selected on another, or colors appear with no system behind them.
Detect: The same hue used for different semantics in different views; color choices that cannot be explained by state, hierarchy, category or brand.
Fix: Give every color one consistent meaning and apply it only for that purpose.
Grade: MAJOR. Sources: impeccable.

### CS-18 Section inverts the page theme
Symptom: A light section is sandwiched between dark ones, or the reverse, so the page feels like two sites.
Detect: A white or pale section inside a dark page or vice versa; more than one theme flip per page; a section wrapping its own theme provider instead of the root.
Fix: Set the theme once at the root; vary sections only with tints of the same family.
Grade: MAJOR. Sources: design-taste-frontend.

### CS-19 Two design systems in one tree
Symptom: Components from two systems sit side by side with mismatched radii, focus rings, type scales and motion.
Detect: Imports from more than one component system in the same tree; a system's token package imported beside a large override sheet for color, radius, type and spacing.
Fix: Use one system per project, honestly, or drop it for a coherent custom theme.
Grade: MAJOR. Sources: design-taste-frontend.

### CS-20 Systemic value corrected in one instance
Symptom: A spacing or color problem that exists everywhere is fixed in only one place.
Detect: A local override correcting a value that the token or scale gets wrong globally while other instances still show it.
Fix: Fix the token or scale, not the instance.
Grade: MAJOR. Sources: impeccable.

### CS-21 Typeface outside the established stack
Symptom: A font family that is not in the product's type stack appears on some text.
Detect: `font-family` declarations or classes outside the token set; sans-serif UI text inside a serif or mono system; several families within one app.
Fix: Set every text role in the families the stack defines.
Grade: MAJOR. Sources: ui-ux-pro-max.

### CS-22 Primary fill does not render the brand color
Symptom: Buttons and links show an approximation of the brand color instead of the brand color itself.
Detect: The brand hex missing from the solid-fill step of the ramp, replaced by a darker neighbour so white text passes contrast, or placed on a non-fill step.
Fix: Put the brand on the fill step if it passes contrast; otherwise keep it and fill one step darker.
Grade: MAJOR. Sources: better-colors.

### CS-23 Rendering breaks or differs in a supported browser
Symptom: The feature looks or behaves differently in one supported browser; older browsers show broken layouts or missing effects.
Detect: Compare captures across supported browsers; `:has`, container queries or `backdrop-filter` with no `@supports` fallback; browser detection instead of feature detection.
Fix: Provide fallbacks through feature detection so every supported browser renders the same result.
Grade: MAJOR. Sources: impeccable.

### CS-24 CSS color keyword replaced by a literal
Symptom: An element stops following its text color or parent and renders the wrong value in other contexts.
Detect: A diff replacing `currentColor`, `transparent`, `inherit`, `initial` or `unset` with a fixed color during a conversion or cleanup.
Fix: Leave CSS color keywords alone.
Grade: MAJOR. Sources: better-colors.

### CS-25 Token named by value or appearance instead of role
Symptom: Tokens encode a value, hue or location, so the same role uses different tokens and names lie after retuning.
Detect: Names like `--spacing-8`, `--font-size-16`, `--color-text-2`, `--color-blue-button`, `--color-sidebar-gray`, `--color-light-gray`, `--color-gray-hover`; `--color-primary` beside `--color-text-primary`; only default utility names such as `text-sm` with inconsistent role usage.
Fix: Name tokens by role, such as `--space-sm`, `--text-body`, `--color-accent-solid`, `--color-bg-surface`.
Grade: POLISH. Sources: impeccable, better-colors, better-typography.

### CS-26 Warm and cool neutrals mixed
Symptom: Some surfaces look yellowish and others bluish, so the page feels assembled from different sites.
Detect: Warm and cool gray families, such as stone or neutral beside slate or zinc, both used for backgrounds and text; warm neutrals with cool accents with no rationale.
Fix: Use one neutral family and keep the palette's temperature consistent.
Grade: POLISH. Sources: design-taste-frontend, impeccable.

### CS-27 Unused tokens, ramps or steps
Symptom: Tokens nothing references bloat the system, and components sample arbitrary steps so similar surfaces differ slightly.
Detect: A ramp or step with no reference; status ramps outnumbering rendered status states; a status ramp of 11 or 12 steps while components use four or fewer; steps outside the role mapping.
Fix: Generate only the ramps and steps roles consume, map each step to a role, and delete the rest.
Grade: POLISH. Sources: better-interface, better-colors.

### CS-28 Inconsistent naming vocabulary across tokens and variants
Symptom: Readers cannot guess a token or variant name, pick the wrong one, and produce a visible mismatch.
Detect: More than one word per concept in token names, such as `text` and `fg`, `bg` and `surface`, `accent` and `primary`; variant or size names differing across components, such as `sm`, `small` and `compact`.
Fix: Pick one word per concept and one variant and size vocabulary across every component.
Grade: POLISH. Sources: better-colors, design-plugin/design-system.

### CS-29 Token set shaped by components instead of roles
Symptom: The same role renders differently from component to component, and later screens find no token and improvise.
Detect: Many `--color-<component>-*` tokens instead of documented exceptions; a token file missing surface, text, border, accent or status roles while holding screen-specific names; one `--color-border` serving both control edges and content dividers.
Fix: Build the semantic tier against the full role inventory and keep component tokens to documented exceptions.
Grade: POLISH. Sources: better-colors.

### CS-30 Color notation mixed in one codebase
Symptom: A hex codebase holds a few `oklch()` values, or the reverse, so the palette reads as two systems.
Detect: `oklch(` in a hex project or `hsl(` and `rgb(` in an oklch project; a single converted literal, or a bulk conversion, inside an unrelated diff.
Fix: Write values in the established notation; convert only in an agreed migration.
Grade: POLISH. Sources: better-colors.

### CS-31 Near-duplicate colors side by side
Symptom: Two almost identical colors are both used, so matching surfaces look subtly off.
Detect: After sorting literals by perceived lightness within a hue family, neighbours within 0.02 OKLab delta E; a merged token whose value matches neither original.
Fix: Keep the most used original and retire the others; never average them.
Grade: POLISH. Sources: better-colors.

### CS-32 Inconsistent focus rings across elements
Symptom: Links, buttons and inputs each show a different focus treatment.
Detect: Multiple differing `:focus-visible` outline colors, widths or offsets across components.
Fix: Use one focus ring token on every interactive element.
Grade: POLISH. Sources: impeccable.

### CS-33 Progress and completion strings not parallel
Symptom: "Saving changes..." resolves to "Your update was successful".
Detect: Progress and completion strings for one action using different nouns or verbs.
Fix: Keep them parallel, so "Saving changes..." resolves to "Changes saved".
Grade: POLISH. Sources: better-writing.

### CS-34 Component with near-duplicate variants
Symptom: A component ships many variants that look nearly alike and get used interchangeably.
Detect: Variant props or classes beyond what most cases need; variants whose styles differ by a hair.
Fix: Reduce variants to the few that cover most cases.
Grade: POLISH. Sources: impeccable.

### CS-35 Derived color values in the token layer
Symptom: Token colors resolve only at render time and diverge from what the design specified.
Detect: `color-mix(` or relative color syntax inside `:root` token definitions, especially chained several deep.
Fix: Keep mixed and derived values out of the token layer; use them for states only.
Grade: POLISH. Sources: better-colors.
