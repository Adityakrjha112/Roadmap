LESSONS = []

def add(title, part, summary, why, code, output, use, mistakes, takeaway, quiz, practice, source, diagram='', added=False, focus=False, notes=()):
    LESSONS.append(dict(id=f'chapter-{len(LESSONS)+1:02}', title=title, part=part,
        summary=summary, why=why, code=code.strip(), output=output, use=use,
        mistakes=mistakes, takeaway=takeaway, quiz=quiz, practice=practice,
        source=source, diagram=diagram, added=added, focus=focus, notes=notes))

add('Your first HTML page', 1,
    'HTML gives content a job: a heading introduces, a paragraph explains, and a link leads somewhere. Tags mark these roles; attributes add details. Think of HTML as a set of meaningful labels attached to your content.',
    'An element usually has an opening tag, content, and a closing tag. Close an inner element before its parent. The head describes the document; the body holds its visible content. The title in the head names the browser tab, while h1 introduces the page itself.',
    '''<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Sunday Cycle Club</title>
  </head>
  <body>
    <!-- Meaning comes before appearance. -->
    <h1>A better way to see the city</h1>
    <p>Bring your <strong>helmet</strong> and your curiosity.</p>
  </body>
</html>''',
    'A large heading sits above a paragraph. “helmet” is usually bold. The browser tab has a different title from the visible heading; the preview below shows only the body.',
    'Every article, booking page, and portfolio starts with a document structure like this.',
    ['Do not cross closing tags: <p><strong>Hi</strong></p> is correctly nested.', 'Save as .html, not .html.txt. Save the file before refreshing.', 'Void elements such as meta, img, and input have no closing tag or child content.'],
    'HTML describes what the content is, before CSS decides how it looks.',
    [('Where does the browser-tab title belong?', 'Inside <title> in the <head>. The visible page heading belongs in the body.'), ('What does lang="en" do?', 'It identifies English as the document language, helping tools such as screen readers choose pronunciation.')],
    'Change the tab title to “My first page” and the visible heading to your name. Add a second paragraph. Explain which changes you expect before refreshing.',
    ['https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content/Basic_HTML_syntax','https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content/Webpage_metadata'], 'document', True,
    notes=[('Attributes are little settings', 'In <a href="https://example.com">Visit</a>, href supplies the destination and Visit supplies the label. Quote attribute values and keep them inside the opening tag.'), ('Why the extra lines?', 'The doctype requests standards rendering. UTF-8 supports a wide range of characters. The viewport setting helps mobile browsers use the device width; it does not make a fixed-width layout responsive on its own.')])

add('Everyday content', 1,
    'Headings create an outline, paragraphs group ideas, and lists collect related items. Links connect pages. Images need useful alternative text when their content matters.',
    'Choose a heading level by its place in the outline, not its default size. Use an ordered list when the sequence matters and an unordered list when it does not. A relative path starts from the current file location; a full URL includes its destination host.',
    '''<h1>Your first city ride</h1>
<p>A slow route with <em>plenty</em> of stops.</p>
<h2>Bring these essentials</h2>
<ul>
  <li>A fitted helmet</li>
  <li>A bottle of water</li>
</ul>
<!-- The link describes its destination. -->
<a href="https://example.com">Read the route guide</a>''',
    'One main heading, a short introduction, a smaller section heading, a bulleted list, and a descriptive link.',
    'Recipe pages, product descriptions, trip guides, and help articles all use this small set of elements.',
    ['Do not use repeated br elements to create page spacing; spacing belongs in CSS.', 'Avoid “click here” when a descriptive link label would explain the destination.', 'Do not put an image filename in alt text. Describe its purpose; use alt="" for purely decorative images.'],
    'A good page remains understandable when you read its headings and links alone.',
    [('When would ol be better than ul?', 'For a sequence such as booking steps or assembly instructions.'), ('How would you show a literal < character in text?', 'Use the character reference &lt;. Use &amp; for an ampersand when it needs escaping.')],
    'Write a route guide with one main heading, two sections, a packing list, and three ordered steps. Add a meaningful link.',
    ['https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content/Headings_and_paragraphs','https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content/HTML_images'], added=True,
    notes=[('A small image example', '<img src="images/bike.jpg" alt="A blue step-through bicycle beside a rack" width="800" height="600"> expects an images folder next to the HTML file. The dimensions describe the image’s aspect ratio; CSS can still scale it.'), ('Meaning, not decoration', 'strong marks importance; em marks stress. Browsers commonly show them as bold and italic, but their meaning matters beyond appearance. Use CSS when you only want a visual change.')])

add('Meaningful page structure', 1,
    'Semantic elements tell people and browsers what a region is for. A navigation area is different from an article, even if both happen to look like rectangles. Good HTML gives the page a useful map.',
    'Use main for the central content, nav for significant navigation, and article for a self-contained piece. A section is a themed group, normally with a heading. A div is fine when you only need a styling wrapper.',
    '''<header>
  <p>Sunday Cycle Club</p>
  <nav aria-label="Main">
    <a href="#rides">Rides</a>
    <a href="#contact">Contact</a>
  </nav>
</header>
<main>
  <h1>Find your next ride</h1>
  <section id="rides">
    <h2>This weekend</h2>
    <article>
      <h3>Riverside loop</h3>
      <p>A gentle 12 km ride.</p>
    </article>
  </section>
</main>
<footer id="contact">Meet us at the town square.</footer>''',
    'The content is stacked vertically by default. The navigation links jump to their matching page regions; semantic elements do not automatically create a complex layout.',
    'News articles, dashboards, shop pages, and documentation navigation become easier to understand and navigate.',
    ['Do not replace every div with section; use a section for a meaningful topic.', 'Use links to navigate and buttons for actions. Styling a div to look clickable does not give it button behavior.', 'Keep a single visible main region for the page’s central content.'],
    'Choose the element by its purpose, then style it.',
    [('Which element should take someone to a booking page?', 'An anchor with an href, because it navigates.'), ('Should a data table be used to place the sidebar?', 'No. Tables describe tabular data; CSS layout handles page arrangement.')],
    'Give your route guide a header, labeled navigation, main region, two headed sections, and footer. Check that every internal link has a matching id.',
    ['https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content/Structuring_documents','https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content/HTML_table_accessibility'], 'document',
    notes=[('➕ Added · Tables that explain data', 'Use table with caption for its subject, th scope="col" for column headings, th scope="row" for row headings, and td for values. A rental-price table is appropriate. A layout made from table cells is not.'), ('Headings form the outline', 'Use a clear h1, then h2 sections and h3 subsections. A section element does not automatically fix skipped heading levels. aside is for related secondary material.')])

add('Forms people can use', 1,
    'A form is a conversation: each label asks a question and each control accepts an answer. Good labels stay visible, suitable input types help users enter data, and related controls are grouped together.',
    'A label’s for value must match the control’s id. The id identifies an element; the name is the key used when that control’s data is submitted. fieldset and legend give a group of controls a shared description.',
    '''<form>
  <fieldset>
    <legend>Your rental</legend>
    <p>
      <label for="rider">Full name</label>
      <input id="rider" name="rider" autocomplete="name" required>
    </p>
    <p>
      <label for="email">Email</label>
      <input id="email" name="email" type="email"
        autocomplete="email" required>
    </p>
    <label for="bike">Bike style</label>
    <select id="bike" name="bike">
      <option value="city">City bike</option>
      <option value="touring">Touring bike</option>
    </select>
  </fieldset>
  <button type="submit">Request a bike</button>
</form>''',
    'A grouped rental form with two labeled fields and a dropdown. Clicking “Full name” focuses its input. In the isolated preview, submission is intentionally disabled.',
    'Contact forms, checkout, account settings, and booking flows.',
    ['A placeholder is not a replacement for a persistent label.', 'An id alone does not include a value in submitted form data: give the control a name.', 'Specify type="button" for a button that should not submit its containing form.'],
    'Labels explain controls; names identify the values you submit.',
    [('What happens when label for and input id differ?', 'The explicit label-control association fails.'), ('Does inputmode="numeric" validate a number?', 'No. It suggests a keyboard; it is not a validation rule.')],
    'Add a pickup-date field and a radio group for rental duration. Give the radio buttons one shared name and unique ids. Click every label.',
    ['https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/label','https://web.dev/learn/forms/form-fields'], focus=True,
    notes=[('Choose the control for the task', 'Use textarea for multiple lines, select for a compact fixed list, checkboxes for independent choices, and radio buttons for one choice in a group. A postal code often belongs in a text field, even if numeric.'), ('Autofill is a feature', 'autocomplete="name" and autocomplete="email" help browsers fill known information. inputmode can suggest a keyboard for a text field without changing how its value is interpreted.')])

add('Validation without guesswork', 1,
    'Native validation checks simple rules before the browser submits a form. required means a value is needed; type="email" checks email syntax. These checks help people correct mistakes, but do not replace validation by the receiving service.',
    'The browser checks eligible controls when a normal submission is attempted. A disabled control is not editable and is omitted from submission. A readonly text control cannot be edited but is normally included. Unchecked checkboxes are omitted, rather than sent as false.',
    '''<style>
  input:user-invalid { border: 2px solid #a12424; }
  input { padding: .65rem; }
</style>
<form>
  <label for="booking">Booking code (3 uppercase letters)</label>
  <p id="format">For example: ABC. All three letters are required.</p>
  <input id="booking" name="booking" required pattern="[A-Z]{3}"
    aria-describedby="format">
  <button type="submit">Check booking</button>
</form>''',
    'A field with visible format guidance. In a standalone page, an empty or malformed value blocks submission. :user-invalid lets the browser delay invalid styling until relevant interaction; exact timing can vary.',
    'Email entry, quantities, date bounds, and codes with a simple documented format.',
    ['Do not rely on color alone to explain an error. Keep instructions visible.', 'type="email" cannot prove an address exists or belongs to the person.', 'novalidate skips interactive form validation; do not add it accidentally.'],
    'Use browser validation for helpful feedback, not as a security boundary.',
    [('Will a disabled named input be submitted?', 'No. A supported readonly control normally will be.'), ('Does an optional empty input fail pattern?', 'Not just because of pattern. Add required when emptiness must be rejected.')],
    'Open the Part 1 project. Submit it empty, then with an invalid email, then valid demo values. Observe the browser’s message and focus behavior.',
    ['https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Forms/Form_validation','https://developer.mozilla.org/en-US/docs/Web/HTML/Guides/Constraint_validation'],
    notes=[('More built-in rules', 'min and max constrain supported number or date types; step controls allowed increments. minlength and maxlength constrain text length. A pattern matches the whole value and should be paired with readable instructions.'), ('Submission is a separate step', 'action chooses a destination and method chooses how data is sent. The receiving service must validate again. This guide’s project uses local demonstration values and sends nothing to an external service.')])

add('Accessibility from the start', 1,
    'Accessibility means people can use the page with different bodies, devices, and settings. HTML supplies much of the behavior for ordinary controls. An accessible name tells assistive technology what a control is called.',
    'Start with native controls, visible labels, meaningful headings, and sensible document order. ARIA can add meaning, but does not create keyboard behavior. The accessibility tree is a browser representation of useful roles, names, and states—not just a copy of every HTML node.',
    '''<style>
  a:focus-visible, summary:focus-visible {
    outline: 3px solid #17634a;
    outline-offset: 4px;
  }
</style>
<a href="#main-content">Skip to main content</a>
<nav aria-label="Main"><a href="#faq">Rental questions</a></nav>
<main id="main-content" tabindex="-1">
  <h1>Plan your ride</h1>
  <details id="faq">
    <summary>Is a helmet included?</summary>
    <p>Yes. We help you find the right fit.</p>
  </details>
</main>''',
    'A skip link, navigation, and an expandable answer. Tab highlights links and the summary; the native disclosure can be opened with the keyboard.',
    'Every public interface benefits: keyboard users, screen-reader users, and people who zoom or need larger targets.',
    ['Never remove focus outlines without a visible replacement.', 'Positive tabindex values create a separate focus order that is hard to maintain.', 'opacity: 0 does not by itself remove a control from keyboard navigation.'],
    'Native meaning and predictable keyboard behavior are the best starting point.',
    [('Does role="button" make a div keyboard-operable?', 'No. Use a real button for the built-in behavior.'), ('What does tabindex="-1" do here?', 'It makes the main region focusable without adding it to normal sequential Tab navigation.')],
    'Use only Tab, Shift+Tab, Enter, and Space to explore this example. Then zoom the page. Can you still find the current focus and read everything?',
    ['https://www.w3.org/WAI/tutorials/page-structure/','https://www.w3.org/WAI/ARIA/apg/practices/read-me-first/'], focus=True,
    notes=[('Contrast and comfortable targets', 'WCAG AA generally requires 4.5:1 contrast for ordinary text and 3:1 for large text. Large means at least 18pt, or 14pt bold. Provide roomy controls and do not communicate state through color alone.'), ('Dialog and inert: understand the boundary', 'A dialog with the open attribute is non-modal. A true modal needs the browser’s modal-opening behavior; merely styling an overlay is insufficient. inert removes a subtree from interaction and focus. Complex dynamic focus management is outside this HTML/CSS-only course.'), ('A small manual audit', 'Check meaningful page titles, image alternatives, labels, focus visibility, reading order, and reflow. WCAG A and AA contain multiple criteria; one automated score cannot establish that a page is accessible.')])

add('Your first stylesheet', 2,
    'CSS is a set of rules about appearance. Each rule selects elements and gives them property-value pairs. A class is a reusable label that lets several elements share a style.',
    'The selector .note matches elements whose class list includes note. Properties such as color and font-family commonly inherit from a parent; padding and borders do not. A stylesheet linked from the head lets multiple pages share rules.',
    '''<style>
  body { font-family: system-ui, sans-serif; }
  .note {
    color: #18543e;
    background: #e5f1e8;
    padding: 1rem;
    border-radius: .5rem;
  }
</style>
<p class="note">Your helmet is included.</p>
<p>This paragraph keeps its normal background.</p>''',
    'The first paragraph has a pale green background and breathing room. Both paragraphs inherit the body font.',
    'A shared note class can style rental notices, checkout hints, and friendly reminders.',
    ['Use a dot for a class selector: .note. The HTML class attribute itself has no dot.', 'Properties and values are separated with a colon; declarations end with semicolons.', 'Check the stylesheet path before trying stronger selectors when nothing changes.'],
    'A CSS rule says which elements to style and which properties to change.',
    [('Does padding automatically pass from a parent to a child?', 'No. Padding is not an inherited property.'), ('How do you connect a separate stylesheet?', 'Put <link rel="stylesheet" href="styles.css"> in the document head.')],
    'Create styles.css, move the rules into it, and link it from your HTML. Add the note class to a second paragraph.',
    ['https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Getting_started','https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Cascade/Inheritance'], added=True,
    notes=[('Read the rule aloud', '“.note: use this text color, this background, this inner spacing.” Reading rules this way helps separate selecting the right element from choosing the right value.'), ('Keep reusable styles together', 'A style element is handy for learning. An external stylesheet is easier to share. Inline style attributes affect individual elements and can make later overrides harder to follow.')])

add('Block, inline, inline-block', 2,
    'Display controls how a box participates in layout. In ordinary horizontal flow, a block starts on a new line; inline content shares a text line. Inline-block behaves like an inline item whose box can have dimensions.',
    'A normal block with auto width usually fills the available inline space. A non-replaced inline element such as span does not use width and height the same way a block does. Inline-block accepts those dimensions while still sitting among text.',
    '''<style>
  .sample { background: #dbece2; margin: .3rem; padding: .4rem; }
  .block { display: block; }
  .inline { display: inline; }
  .inline-block { display: inline-block; width: 6rem; }
</style>
<span class="sample block">Block A</span>
<span class="sample block">Block B</span>
<p><span class="sample inline">Inline A</span>
  <span class="sample inline">Inline B</span></p>
<span class="sample inline-block">Box A</span>
<span class="sample inline-block">Box B</span>''',
    'Two full-row blocks appear first. Inline labels share a text line. Inline-block labels have a set width and can wrap as whole boxes.',
    'Paragraph flow, badges, labels, and small controls inside text.',
    ['Do not expect width: 200px to size an ordinary inline span.', 'Vertical padding on inline text can paint beyond the line without separating lines as a block would.', 'display changes layout, not an element’s HTML meaning. A block-styled link remains a link.'],
    'Ask whether the element should behave like a line, a word, or an inline box.',
    [('Which option accepts width while sharing a text line?', 'Inline-block.'), ('Does display: none reserve its former space?', 'No. visibility: hidden normally preserves the box’s layout space.')],
    'Change the widths and compare all three rows. Then hide one box with display: none and another with visibility: hidden.',
    ['https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Box_model','https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/display'], 'display',
    notes=[('Three ways to hide are different', 'display: none removes layout participation. visibility: hidden normally keeps space while hiding the content. opacity: 0 makes it transparent but can leave it clickable and keyboard-focusable.'), ('Outer and inner behavior', 'display: flex makes a flex formatting context for children; its outer box is block-level by default. Changing the child layout does not mean the container is inline.')])

add('The box model', 2,
    'Every visible element occupies a box. Content sits in the middle, padding cushions it, a border surrounds it, and margin separates it from neighboring boxes. Think of a parcel: item, wrapping, box edge, then the gap on the shelf.',
    'With content-box, width describes only the content. Padding and border add to the outer size. With border-box, the declared width includes content, padding, and border. Margin stays outside either calculation.',
    '''<style>
  .card {
    box-sizing: border-box;
    width: 240px;
    max-width: 100%;
    padding: 20px;
    border: 4px solid #21664d;
    margin: 16px 0;
    background: #e7f2e8;
  }
</style>
<div class="card">This box is 240px wide, including its border.</div>''',
    'A green card is 240px wide when space permits. Its content width is 192px: 240 minus 40px padding and 8px border.',
    'Cards, buttons, form inputs, and any layout where several pieces must fit a known width.',
    ['Margin is never included by border-box.', 'A fixed height can clip longer text; prefer padding and natural content height.', 'Padding grows the inside of a box; margin separates it from neighbors.'],
    'Use border-box when you want declared widths to include padding and borders.',
    [('What is the outer width with content-box, width 240px, padding 20px, and border 4px?', '288px, before margins: 240 + 40 + 8.'), ('Does border-box prevent every overflow?', 'No. Long content and minimum sizes can still cause overflow.')],
    'Switch the example to content-box and compare the box width. Then add a long sentence and remove any fixed height.',
    ['https://web.dev/learn/css/box-model','https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/box-sizing'], 'box-model',
    notes=[('A useful starting rule', 'Apply box-sizing: border-box to *, *::before, and *::after for predictable sizing across components. It changes the width calculation; it does not remove spacing.'), ('Vertical margins have another rule', 'Some block margins collapse rather than add. We will isolate that behavior in the normal-flow chapter; padding does not collapse.')])

add('Why one style wins', 2,
    'The cascade is the browser’s decision process when several declarations target the same property. Specificity is only one step in that process. Imagine a queue with different priority lanes, not a shouting contest.',
    'First check whether a rule applies. Origin, importance, and layer precedence come before selector specificity. For otherwise tied declarations, scoping proximity may matter, then source order decides. In normal author CSS, unlayered rules outrank named-layer rules.',
    '''<style>
  @layer base, components;
  @layer base {
    #welcome { color: firebrick; }
  }
  @layer components {
    .message { color: #17634a; }
  }
</style>
<p id="welcome" class="message">The later normal layer wins.</p>''',
    'The message is green. The later components layer wins before the browser compares the class selector with the ID selector.',
    'A component library, reset, theme, and page stylesheet can coexist without endless !important overrides.',
    ['Do not compare specificity before checking layer precedence.', 'A later rule only wins on source order after earlier cascade criteria tie.', 'Important declarations reverse named-layer precedence; adding !important can make a layering problem worse.'],
    'Find the winning priority group first, then compare selectors inside it.',
    [('Does an ID always beat a class?', 'No. Layer, origin, and importance can decide first.'), ('What specificity does :where(.card #title) contribute?', 'Zero. :where() and its arguments add no specificity.')],
    'Move both rules into one layer. Predict the new color before testing. Then remove the ID selector and create a true source-order tie.',
    ['https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Cascade/Introduction','https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Cascade/Specificity'], 'cascade',
    notes=[('Specificity is a tuple', 'Compare ID counts, then class/attribute/pseudo-class counts, then type/pseudo-element counts. It is not a decimal score. :is(), :not(), and :has() use the specificity of their most specific argument.'), ('The wider picture', 'Browser styles, user styles, author styles, animations, and transitions occupy defined cascade positions. Inline styles also have special author precedence. The simple “last rule wins” slogan hides those rules.')])

add('Units and readable text', 2,
    'A size can follow a fixed CSS unit, the root font, the current font, or a containing box. Choosing the relationship is more useful than memorizing a list of units. Text should remain readable when users change their settings.',
    'For font-size, rem relates to the root font and em relates to the parent’s font. On padding, em uses the element’s own font size. Percentage sizing depends on the property and its reference size. A CSS pixel is not necessarily a physical display pixel.',
    '''<style>
  .reading {
    font: 1rem/1.65 system-ui, sans-serif;
    max-width: 60ch;
    padding: 1.5rem;
  }
  .reading h2 { font-size: 1.6rem; line-height: 1.2; }
</style>
<article class="reading">
  <h2>A slower Sunday</h2>
  <p>Take the riverside path. Leave enough time to stop,
    look around, and enjoy the part of the city you usually pass by.</p>
</article>''',
    'Comfortable text spacing and a restrained line length. ch approximates the width of the font’s zero character; it is not an exact character count.',
    'Articles, documentation, form controls, and interfaces that must handle zoom and user font preferences.',
    ['Nested em font sizes can multiply; rem is often easier for a shared type scale.', 'Do not set a tiny root font just to make rem arithmetic feel easier.', 'A line-height without a unit scales cleanly with descendant font sizes.'],
    'Pick the relationship you want: root-relative, font-relative, or container-relative.',
    [('If the root font is 20px, how large is 1.5rem?', '30 CSS pixels.'), ('Does px prevent browser zoom?', 'No. Browser zoom also scales CSS-pixel-based content; respecting font preferences is a separate consideration.')],
    'Increase the browser’s default font setting. Compare a rem-based paragraph with one fixed at 12px. Check both at 200% zoom.',
    ['https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Values_and_units','https://web.dev/learn/css/typography'],
    notes=[('➕ Added · Text that feels easy', 'Use a readable font stack, enough line height, and a moderate text width. Align longer paragraphs to the start edge. Avoid all-caps paragraphs and fully justified narrow text.'), ('Relative does not always mean flexible', 'A percentage height needs an appropriate reference height. height: 100% often does not fill a parent whose height is auto. We revisit this in the sizing chapter.')])

add('Style a useful card', 2,
    'Color, border, background, and shadow help communicate grouping and hierarchy. They work best when each has a job: a border separates, a background groups, and a strong text color preserves readability.',
    'Start with spacing and typography, then add decoration. border-radius rounds corners but does not automatically crop overflowing children. object-fit controls how a replaced image fills a box when that box has a defined size.',
    '''<style>
  .rental {
    max-width: 22rem;
    padding: 1.5rem;
    color: #20392d;
    background: #f0f6ec;
    border: 1px solid #c5d8bf;
    border-radius: 1rem;
    box-shadow: 0 .3rem 1rem rgb(25 50 35 / .08);
    font-family: system-ui, sans-serif;
  }
  .rental p { line-height: 1.6; }
</style>
<article class="rental">
  <p>WEEKEND FAVORITE</p>
  <h2>The city cruiser</h2>
  <p>Comfortable, upright, and ready for the scenic route.</p>
  <a href="https://example.com">View rental details</a>
</article>''',
    'A calm green card with a subtle edge and rounded corners. The text remains the strongest visual element.',
    'Product cards, account panels, pricing options, and helpful notices.',
    ['Low-contrast muted text can become unreadable; check the actual color pair.', 'Do not use a decorative background image for essential information without a text equivalent.', 'object-fit: cover can crop important image content; choose an appropriate focal point.'],
    'Good styling makes the content’s structure easier to see.',
    [('Does border-radius alone clip a child image?', 'Not necessarily. Set appropriate overflow behavior or round the image itself.'), ('When is object-fit: contain useful?', 'When the entire image must remain visible inside a sized box, even if empty space remains.')],
    'Create two card variants using the same markup. Change only color and border treatments. Keep the spacing and readability consistent.',
    ['https://web.dev/learn/css/backgrounds','https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/object-fit'], added=True,
    notes=[('Images in cards', 'For a fixed-ratio image box, use width: 100%, aspect-ratio: 4 / 3, and object-fit: cover. For a naturally scaled photo, use max-width: 100% and height: auto.'), ('A restrained palette', 'Choose one strong text color, one page background, one surface, and one accent. Check hover, focus, disabled, and error appearances as well as the default state.')])

add('States and smart selectors', 2,
    'Selectors can express relationships and states. A hover state means a pointer is over something; a focus state means it has input focus. Pseudo-elements let you style a generated part of an element.',
    'A space selects descendants, > selects direct children, + selects the next sibling, and ~ selects later siblings. :focus-visible follows browser heuristics for when a focus indicator is useful. :has() can select a parent based on matching descendants.',
    '''<style>
  .choice {
    display: block;
    padding: 1rem;
    border: 2px solid #c6cec5;
    border-radius: .6rem;
  }
  .choice:has(input:checked) { background: #e5f1e8; border-color: #17634a; }
  input:focus-visible { outline: 3px solid #17634a; outline-offset: 3px; }
</style>
<label class="choice">
  <input type="checkbox" name="helmet"> Include a helmet
</label>''',
    'Check the box to give its whole label a green background and border. Tab to it to see a focus indicator.',
    'Selected cards, focused controls, alternating table rows, and lightweight decoration.',
    ['Hover alone is not enough: touch and keyboard users need usable states too.', 'Do not put essential instructions only in ::before or ::after generated content.', 'A selector can match correctly and still lose in the cascade.'],
    'Use selectors to express real relationships and user states.',
    [('What is the difference between .card p and .card > p?', 'The first matches any descendant paragraph; the second only direct children.'), ('Does :where() increase specificity?', 'No. It is useful for easy-to-override defaults.')],
    'Add a focus-visible treatment to the Part 2 project. Add a checked option style that is still understandable without color.',
    ['https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Selectors/:has','https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Selectors/:focus-visible'],
    notes=[('➕ Added · Group and filter', ':is() groups alternatives. :not() excludes matches. :nth-child() selects by sibling position. ::before and ::after create generated boxes when content is supplied; they are not extra HTML elements.'), ('Validation states', ':invalid can match before the user has had a chance to edit. :user-invalid allows interaction-sensitive feedback. Pair it with real text guidance, not just a red border.')])

add('Normal flow and spacing surprises', 3,
    'Normal flow is the browser’s default way of placing content. Before reaching for positioning, understand how ordinary blocks stack. Some neighboring vertical margins collapse into one margin instead of adding together.',
    'Two positive adjoining block margins commonly collapse to the larger value. Parent-child margins can also collapse under specific conditions. Flex and grid item margins do not collapse with each other. flow-root creates a new block formatting context and can contain internal floats.',
    '''<style>
  .group {
    display: flow-root;
    background: #edf4e8;
    padding-inline: 1rem;
  }
  .group p { margin-block: 2rem; }
</style>
<section class="group">
  <p>First stop: the riverside.</p>
  <p>Second stop: the old market.</p>
</section>''',
    'The paragraphs’ adjoining positive margins collapse to 2rem, rather than 4rem. flow-root keeps their outer margins from collapsing through the parent; it does not stop sibling margin collapse inside it.',
    'Article spacing, floating illustrations, and debugging unexplained gaps at the top of a section.',
    ['Do not assume all vertical margins always add.', 'overflow: hidden may fix one containment issue while clipping useful content.', 'flow-root is not a universal switch that disables every margin collapse.'],
    'Understand ordinary flow before forcing elements out of it.',
    [('Do margins between flex items collapse?', 'No.'), ('What gap do adjoining positive margins of 16px and 24px usually produce?', '24px, when the conditions for margin collapse apply.')],
    'Create two paragraphs with different vertical margins. Then make the parent a flex column and compare. Replace the margins with gap.',
    ['https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Box_model/Margin_collapsing','https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Display/Block_formatting_context'],
    notes=[('Float still has a useful job', 'float is useful when text should wrap around an image. clear moves following content past relevant floats. For page columns and component alignment, learn Flexbox and Grid.'), ('Overflow has side effects', 'overflow: auto creates scrolling when needed. overflow: hidden clips and creates a scroll container even without visible scrollbars. overflow: clip clips without creating a scroll container.')])

add('Positioning and stacking', 3,
    'Positioning controls whether a box stays in normal flow and what its offsets refer to. Stacking controls which overlapping boxes appear in front. They are related, but a bigger z-index does not always solve an overlap.',
    'Static follows normal flow. Relative keeps its original space while allowing a visual offset. Absolute leaves normal flow and uses a containing block, often the nearest positioned ancestor. Fixed commonly uses the viewport; certain ancestors, including transformed ones, can change that reference. Sticky remains in flow and is constrained by its scroll container and containing block.',
    '''<style>
  .photo {
    position: relative;
    min-height: 10rem;
    padding: 1rem;
    background: #e4ecde;
  }
  .badge {
    position: absolute;
    top: 1rem;
    right: 1rem;
    padding: .4rem .7rem;
    background: #ffd4a9;
  }
</style>
<div class="photo">
  <p>City cruiser</p>
  <span class="badge">Available</span>
</div>''',
    'The badge sits in the top-right corner of the green photo placeholder. It does not reserve a separate row in normal flow.',
    'Card badges, anchored controls, sticky navigation, and carefully designed overlays.',
    ['Absolute positioning needs a deliberate containing block.', 'Sticky usually needs an inset such as top: 0 and enough scrolling room.', 'A child cannot use z-index to escape its parent’s lower stacking context.'],
    'First identify the containing block; then identify the stacking context.',
    [('Does relative positioning remove the original space?', 'No. Its original layout space remains.'), ('Why can z-index: 9999 lose to z-index: 1?', 'They may belong to different stacking contexts, with the entire first context below the second.')],
    'Add a relative offset to the card title. Compare it with absolute positioning. Build a sticky header in a page tall enough to scroll.',
    ['https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/position','https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Positioned_layout/Stacking_context'], 'position',
    notes=[('Debug a sticky element', 'Check its inset, ancestor overflow, height, containing block, and whether it has room to travel. A short parent can end its sticky movement quickly.'), ('Contexts are local groups', 'Positioned elements with a non-auto z-index, transforms, opacity below 1, and other properties can establish contexts. Flex/grid items can also use z-index without being positioned. Browser top-layer content sits outside ordinary stacking contexts.')])

add('Flexbox: one direction at a time', 3,
    'Flexbox arranges items along a main axis and helps distribute available space. The cross axis runs perpendicular to it. Imagine arranging books on one shelf, then deciding their spacing and alignment.',
    'flex-direction chooses the main axis. justify-content distributes main-axis space; align-items aligns items on the cross axis. With row in a horizontal writing mode, main is horizontal. With column, those roles switch. gap separates items without needing edge margins.',
    '''<style>
  .ride {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1rem;
    background: #e8f1e3;
  }
  .description { flex: 1 1 0; min-width: 0; }
  .description p { overflow-wrap: anywhere; }
  .price { flex-shrink: 0; }
</style>
<article class="ride">
  <div class="description">
    <h2>Riverside tour</h2>
    <p>A beautifully-long-route-name-that-still-needs-to-fit</p>
  </div>
  <strong class="price">₹250</strong>
</article>''',
    'The text takes the flexible space; the price keeps its width. The description can shrink, and the long text can wrap rather than pushing the price outside.',
    'Navigation bars, button groups, media objects, and rows with a flexible description and fixed action.',
    ['Do not memorize “justify is horizontal”: it follows the main axis.', 'flex-shrink: 1 does not automatically defeat an item’s automatic minimum size.', 'Visual reordering does not reliably change keyboard or reading order. Keep the HTML order meaningful.'],
    'Flexbox negotiates space along an axis; minimum sizes still set boundaries.',
    [('What often lets a row flex item shrink below its content-based minimum?', 'min-width: 0 on the relevant item, plus a deliberate strategy for overflowing content.'), ('What does align-content affect?', 'The distribution of flex lines when a wrapping flex container has extra cross-axis space—not alignment within a single line.')],
    'Remove min-width: 0 and overflow-wrap. Narrow the preview and observe the failure. Restore one rule at a time and explain each job.',
    ['https://web.dev/learn/css/flexbox','https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/flex'], 'flex', focus=True,
    notes=[('Grow, shrink, basis', 'flex: 1 1 12rem means grow factor 1, shrink factor 1, starting basis 12rem. Positive space is distributed using grow factors; shrinking also depends on base sizes. Min/max constraints can stop that negotiation.'), ('Wrapping is optional', 'The default is nowrap. Set flex-wrap: wrap when items should move onto new lines. Each line distributes its own space, so wrapped Flexbox does not promise aligned columns across rows.')])

add('Grid: rows and columns together', 3,
    'Grid arranges content across rows and columns at the same time. You define tracks, then place items or let the browser place them. It is a helpful way to draw a page’s layout before filling in details.',
    'A track is a row or column; a cell is one intersection. fr distributes a share of remaining space. Grid items have minimum-size behavior too, so minmax(0, 1fr) can be more shrinkable than a bare 1fr track.',
    '''<style>
  .cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(min(100%, 12rem), 1fr));
    gap: 1rem;
  }
  .cards article { padding: 1.5rem; background: #e8f1e3; min-width: 0; }
</style>
<div class="cards">
  <article>City cruiser</article>
  <article>Touring bike</article>
  <article>Weekend tandem</article>
</div>''',
    'Cards form as many columns as fit. Each tries to be at least 12rem, but can become narrower when the container itself is smaller.',
    'Product listings, dashboards, galleries, and aligned page regions.',
    ['Three 33.33% tracks plus gaps can overflow; use fractions or account for gaps.', 'Making a track shrinkable does not automatically wrap a long unbreakable string inside it.', 'Named grid areas must form rectangles.'],
    'Use Grid when relationships between rows and columns matter.',
    [('How do auto-fit and auto-fill differ with unused columns?', 'auto-fill retains empty repeated tracks; auto-fit collapses the empty tracks so occupied ones can expand.'), ('Does subgrid create an independent set of parent-aligned track sizes?', 'It adopts the parent grid’s tracks in the chosen axis, allowing descendants to align with them.')],
    'Create a page with named header, sidebar, main, and footer areas. Then change the card example from auto-fit to auto-fill and compare a wide view with only two items.',
    ['https://web.dev/learn/css/grid','https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Grid_layout/Subgrid'], 'grid',
    notes=[('Named areas sketch the page', 'grid-template-areas: "header header" "sidebar main" "footer footer" pairs naturally with grid-area on each child. Start with a single-column version for a narrow viewport.'), ('Use both layout systems', 'A dashboard can use Grid for the shell and Flexbox inside each card. Choose the system for the relationship you need, not as a permanent preference.')])

add('Let content help choose the size', 3,
    'Intrinsic sizing starts with the content’s own size needs. min-content asks how narrow content can become at its available breaks; max-content asks how wide it wants to be without soft wrapping. fit-content balances those limits with available space.',
    'A long unbreakable word raises the minimum content size. An automatic flex or grid minimum can therefore prevent a box from shrinking. Logical properties describe start/end and inline/block directions so layouts can adapt to different writing modes.',
    '''<style>
  .panel {
    inline-size: fit-content;
    max-inline-size: 100%;
    padding-inline: 1rem;
    padding-block: .8rem;
    border: 1px solid #9db59c;
    overflow-wrap: anywhere;
    box-sizing: border-box;
  }
</style>
<div class="panel">Pickup: Old Town Market</div>''',
    'The panel hugs the short label when there is room and is constrained by its container when space becomes tight.',
    'Badges, shrinkable sidebar content, variable labels, and multilingual interfaces.',
    ['width: 100% plus padding can overflow under content-box.', 'height: 100% needs an appropriate reference size; an auto-height parent is not a promise to fill the viewport.', 'min-width: 0 removes a lower bound but does not decide whether content should wrap, scroll, or clip.'],
    'Separate the box’s allowed size from the content’s overflow behavior.',
    [('Why does a very long URL break an otherwise flexible layout?', 'It can establish a large unbreakable minimum width.'), ('What replaces margin-left for the inline start edge?', 'margin-inline-start. Its physical side depends on writing direction and writing mode.')],
    'Put a long URL in a narrow card. Compare overflow-wrap: anywhere, a scrollable wrapper, and clipping. Explain which preserves the information best for that UI.',
    ['https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/min-content','https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Logical_properties_and_values'], focus=True,
    notes=[('The height question', 'In ordinary flow, percentage height often acts like auto when the containing block’s height is content-dependent. Flex and grid have additional definite-size rules. Give the layout a clear sizing relationship instead of stacking height: 100% guesses.'), ('Direction-aware spacing', 'inline-size and block-size describe the writing axes. padding-inline, margin-block, and border-inline-start work with those axes. Direction-aware properties are especially useful for right-to-left content.')])

add('Responsive pages', 3,
    'A responsive page adapts to available space and user settings. Start with a layout that works when space is limited, then add roomier arrangements where the content benefits. Breakpoints are decisions about the design, not a list of device names.',
    'A media query checks the viewport or another media feature. Fluid values vary continuously between bounds. clamp(minimum, preferred, maximum) is useful for headings and spacing when both small and large extremes need limits.',
    '''<style>
  .intro { padding: clamp(1rem, 4vw, 3rem); }
  .intro h1 { font-size: clamp(1.8rem, 1.1rem + 3vw, 3rem); }
  .layout { display: grid; gap: 1rem; }
  .layout > div { padding: 1rem; background: #e8f1e3; }
  @media (min-width: 40rem) {
    .layout { grid-template-columns: 2fr 1fr; }
  }
</style>
<section class="intro">
  <h1>Make space for the scenic route.</h1>
  <div class="layout"><div>Ride details</div><div>Booking summary</div></div>
</section>''',
    'The sections stack in a narrow viewport and sit side by side above 40rem. The heading changes gradually within its bounds.',
    'Every page that needs to work on phones, large monitors, and zoomed browsers.',
    ['Do not disable zoom in the viewport metadata.', 'A media query should solve a visible layout need, not match a phone brand.', 'Using only viewport units for font size can undermine user text-size preferences.'],
    'Let the content tell you when the layout needs to change.',
    [('Does a narrow desktop window need a mobile-friendly layout?', 'Yes. Available space matters more than the device label.'), ('What does dvh follow?', 'The dynamic viewport height; svh uses the small viewport height and is more stable as browser controls change.')],
    'Drag the browser from wide to narrow slowly. Fix the first point where the content becomes uncomfortable. Check text zoom and a narrow viewport, not only preset device sizes.',
    ['https://web.dev/learn/design/media-queries','https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/clamp'], 'responsive',
    notes=[('Reflow matters', 'At high zoom, ordinary content should reflow without page-wide two-dimensional scrolling. Some content such as genuinely two-dimensional data tables has exceptions; contain its scroll area rather than widening the whole page.'), ('Touch and viewport units', 'Give interactive controls generous targets and spacing. min-height: 100svh can avoid an oversized initial screen under mobile browser controls; 100dvh tracks changing usable height and may resize during scrolling.')])

add('Responsive components', 3,
    'A container query responds to a component’s available space rather than the whole viewport. The same card can be narrow in a sidebar and wide in the main content. It should adapt to the place it actually occupies.',
    'Declare an ancestor as a query container with container-type: inline-size. Descendant styles inside a size query depend on a matching ancestor container. A component does not query its own size to style itself through that same size query.',
    '''<style>
  .slot { container-type: inline-size; }
  .card { display: grid; gap: 1rem; padding: 1rem; background: #e8f1e3; }
  .art { min-height: 5rem; background: #c2d9b7; }
  @container (min-width: 24rem) {
    .card { grid-template-columns: 1fr 2fr; align-items: center; }
  }
</style>
<div class="slot">
  <article class="card">
    <div class="art" aria-hidden="true"></div>
    <div><h2>City cruiser</h2><p>Built for the slow lane.</p></div>
  </article>
</div>''',
    'The card stacks until its containing slot is at least 24rem wide. A wide page alone does not guarantee a side-by-side card.',
    'Reusable product cards, search results, dashboard widgets, and sidebar callouts.',
    ['Put containment on an ancestor of the element you want to restyle.', 'Containment changes sizing behavior; do not add it to every element indiscriminately.', 'Use viewport media queries for page-wide decisions and container queries for local ones.'],
    'A component should respond to the space its parent gives it.',
    [('Can two identical cards look different in one viewport?', 'Yes. They can have containers with different sizes.'), ('What is 1cqi?', 'One percent of the relevant query container’s inline size. Make the intended container explicit.')],
    'Place the same card in a narrow sidebar and a wide content area. Keep their markup and CSS identical and compare their layouts.',
    ['https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Containment/Container_queries','https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Containment/Container_size_and_style_queries'], 'container',
    notes=[('Named containers', 'container-name can identify a particular ancestor when nested containers make the default choice unclear. A named @container query asks for that matching ancestor.'), ('Container units', 'cqi follows inline size and cqb follows block size. Use clamp() when fluid type needs bounds. A suitable container is part of the component’s layout contract.')])

add('Images that fit and load well', 3,
    'Responsive images have two jobs: fit their layout box and let the browser choose an appropriate file. CSS handles the visible size. HTML can provide candidate files and describe how much space the image will occupy.',
    'With width-descriptor srcset, each candidate names its real intrinsic pixel width. sizes estimates the rendered slot width in CSS pixels. The browser combines that hint with device pixel density and other conditions. picture selects sources for art direction or format support.',
    '''<style>
  img { display: block; max-width: 100%; height: auto; }
</style>
<!-- This local SVG scales without losing sharpness. -->
<img src="assets/bicycle.svg" width="800" height="480"
  alt="A green city bicycle beside a warm sun">''',
    'A local bicycle illustration fits inside the preview while preserving its aspect ratio. The width and height also let the browser reserve the right shape before the image loads.',
    'Hero photos, product thumbnails, galleries, and editorial images.',
    ['A false sizes value can make the browser choose an unnecessarily large or small file.', 'width and height attributes do not prevent CSS from resizing the image.', 'Do not lazy-load the main above-the-fold image when it is important to initial rendering.'],
    'Describe the image’s space honestly and let the browser choose the file.',
    [('Does a 400px-wide slot always need a 400-pixel file?', 'No. A high-density display may benefit from more image pixels.'), ('What is picture useful for beyond resolution?', 'Different crops or compositions at different widths, and supported-format alternatives.')],
    'Use your own photo exported at 480 and 960 pixels wide. Supply both candidates and an accurate sizes value, then inspect which file loads at different viewport sizes and densities.',
    ['https://web.dev/learn/design/responsive-images','https://developer.mozilla.org/en-US/docs/Web/HTML/Guides/Responsive_images'],
    notes=[('A raster-image recipe', '<img src="ride-480.jpg" srcset="ride-480.jpg 480w, ride-960.jpg 960w" sizes="(min-width: 48rem) 40rem, calc(100vw - 2rem)" width="960" height="640" alt="Riders on the riverside path"> assumes those files exist and that the stated slot widths match the layout.'), ('Formats and cropping', 'Inside picture, list AVIF and WebP sources with their types before the fallback img. The img still carries alt and dimensions. Provide the actual files; changing a filename extension does not convert an image.')])

add('Themes that stay consistent', 3,
    'Custom properties store reusable CSS values. A semantic name such as --surface describes a purpose, so you can change a theme without rewriting every component. The same idea keeps spacing and typography consistent.',
    'Define defaults at the root, then override tokens in a theme scope or preference query. var() reads the value and can provide a fallback. Custom properties normally inherit, so a themed section can supply values to its descendants.',
    '''<style>
  :root { --surface: #edf4e7; --ink: #233f2e; --space: 1.5rem; }
  .panel { background: var(--surface); color: var(--ink); padding: var(--space); }
  @media (prefers-color-scheme: dark) {
    :root { --surface: #21392d; --ink: #edf4e7; }
  }
</style>
<section class="panel">
  <h2>Your ride, your pace.</h2>
  <p>This panel follows the device’s color-scheme preference.</p>
</section>''',
    'A light green panel in a light system theme, or a dark green panel with light text in a dark system theme.',
    'Design systems, dark mode, branded sections, and consistent component families.',
    ['Changing only the background can leave text or controls unreadable.', 'A custom property is still subject to the cascade.', 'Do not assume a palette is accessible in every state; check actual combinations.'],
    'Name values by their job so the design can change coherently.',
    [('Will a child normally inherit --surface?', 'Yes, ordinary custom properties inherit unless their registration changes that behavior.'), ('Does a CSS custom property escape cascade rules?', 'No. Its declarations participate in the cascade.')],
    'Replace hardcoded card colors with --surface, --text, and --border. Create a nested alternate-theme section and verify its links and focus styles.',
    ['https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Cascading_variables/Using_custom_properties','https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-color-scheme'],
    notes=[('Organize without a fight', 'A layer order such as reset, base, components, utilities makes normal overrides predictable. Keep the unlayered escape hatch deliberate. Important declarations reverse layer ordering.'), ('A useful token ladder', 'A primitive might name a green shade, a semantic token might call it --action, and a component token might use it for a button. Avoid creating three layers of names before the project actually needs them.')])

add('Motion with a purpose', 3,
    'A transition softens a change between states. A keyframe animation describes a sequence. Good motion helps a user follow what changed and respects people who prefer less movement.',
    'Animating size or position through layout properties can require repeated layout work. Transform and opacity often avoid layout, but they are not a guarantee of free rendering. Use modest effects and honor prefers-reduced-motion.',
    '''<style>
  .ride-link {
    display: inline-block;
    padding: 1rem;
    color: white;
    background: #1d6148;
    transition: transform 180ms ease;
  }
  .ride-link:hover { transform: translateY(-3px); }
  .ride-link:focus-visible { outline: 3px solid #b65b1b; outline-offset: 4px; }
  @media (prefers-reduced-motion: reduce) {
    .ride-link { transition: none; }
    .ride-link:hover { transform: none; }
  }
</style>
<a class="ride-link" href="https://example.com">Explore a ride</a>''',
    'The link lifts gently on hover, unless reduced motion is preferred. Keyboard focus remains visible without requiring the hover effect.',
    'State changes, expanding panels, and lightweight feedback that supports rather than distracts from a task.',
    ['Do not use transition: all when only one property should animate.', 'Avoid endless motion and important information that appears only during an animation.', 'Do not scatter will-change everywhere; extra compositing resources have a cost.'],
    'Animate a useful change, keep it small, and respect reduced motion.',
    [('Does transform change the box’s normal-flow footprint?', 'No. It changes its visual rendering without moving surrounding flow content in the same way.'), ('What is a keyframe animation?', 'A named sequence of property values assigned through animation; unlike a transition, it can define multiple stages.')],
    'Test the example with reduced motion enabled. Add a short keyframe effect only if it improves feedback, and give it the same reduced-motion treatment.',
    ['https://web.dev/learn/css/transitions','https://web.dev/learn/css/animations','https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion'], added=True,
    notes=[('A browser’s visual pipeline', 'Style chooses the rules, layout calculates geometry, paint draws visual content, and compositing combines layers. A change may invalidate more than one stage. Avoid blanket claims that every transform is automatically GPU-accelerated.'), ('Long pages', 'content-visibility: auto can let the browser skip some offscreen rendering. Pair it with appropriate intrinsic size estimates when using it; test scrolling, find-in-page, and accessibility behavior. It is an optimization, not a substitute for sound layout.')])

add('Become your own layout detective', 3,
    'Debugging CSS is asking which rule explains the result you see. Reduce the problem to one box, inspect its computed styles, and test one hypothesis at a time. A small reproducible example teaches more than a pile of overrides.',
    'Start with the HTML relationship, then the cascade, then layout constraints. Identify the container, available space, minimum sizes, and overflow strategy. A fix should explain why the original behavior occurred.',
    '''<style>
  .dashboard { display: grid; grid-template-columns: minmax(0, 1fr); }
  .table-wrap { overflow-x: auto; }
  table { border-collapse: collapse; min-width: 28rem; width: 100%; }
  th, td { padding: .8rem; border: 1px solid #a7bda4; text-align: start; }
</style>
<div class="dashboard">
  <div class="table-wrap" tabindex="0" role="region" aria-label="Rental prices">
    <table>
      <caption>Daily rental prices</caption>
      <thead><tr><th scope="col">Bike</th><th scope="col">Price</th></tr></thead>
      <tbody><tr><th scope="row">City cruiser</th><td>₹250</td></tr></tbody>
    </table>
  </div>
</div>''',
    'On a narrow viewport, the table scrolls inside its own named region instead of forcing the entire page wider. The table keeps its row and column meaning.',
    'Production bug reports: narrow screens, translated labels, longer data, and unexpected zoom levels.',
    ['Do not hide page-wide overflow just to conceal the symptom.', 'Do not change five properties at once and lose track of the cause.', 'A screenshot at one width does not prove the layout is responsive.'],
    'Find the smallest example that explains the bug, then fix the cause.',
    [('A rule is crossed out in the style inspector. What should you inspect?', 'The winning declaration and why it wins: relevance, cascade priority, specificity, and order.'), ('What should a good layout bug report include?', 'The viewport and settings, expected versus actual behavior, minimal markup/styles, and the rule causing the result.')],
    'Reproduce five bugs: a long word overflow, a stubborn flex item, a grid blowout, a trapped z-index, and a collapsed margin. Write one sentence explaining each before fixing it.',
    ['https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Debugging_CSS','https://www.w3.org/WAI/WCAG22/Understanding/reflow.html'],
    notes=[('Your investigation order', '1. Does the selector match? 2. Which declaration wins? 3. Which formatting context applies? 4. What limits the size? 5. Where should excess content go? 6. Does the fix survive another viewport and longer text?'), ('A final accessibility pass', 'Check heading order, labels, keyboard focus, contrast, reduced motion, image alternatives, and reflow. Keep tabular data scrollable when its two-dimensional relationship is essential. Test the complete interaction, not only the screenshot.')])
