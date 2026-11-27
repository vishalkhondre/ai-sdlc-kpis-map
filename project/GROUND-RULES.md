# Ground rules

Version 1.0 · adapted from the AI SDLC Map ground rules v1.2 · changes only with Vishal's approval.
Every check and reviewer finding cites a rule number, for example `GR-2.6`. *(check)* means a script
enforces it; *(review)* means a reviewer does, until a check exists (GR-5.3).

## §1 Independence and confidentiality
- **GR-1.1** Nothing may identify the author's employer or its internal work: company, product,
  project, team or people names, internal codes, customers or internal figures. *(review: confidentiality; check: deny-list, to port)*
- **GR-1.2** Any deny-list is stored as hashes or a CI secret, never as plain names. *(check, to port)*

## §2 Evidence
- **GR-2.1** Every claim beyond common knowledge has a public source, preferring standards and
  research (DORA, SPACE, peer-reviewed studies), then recognised practitioners, then official tool
  documentation for facts about that tool only. *(review: accuracy)*
- **GR-2.2** Borrowed terms and metric names are credited to their originator; terms this site
  introduces are marked *coined*. *(review; check once the glossary exists)*
- **GR-2.3** No invented statistics, benchmarks, case studies or quotes. *(review: accuracy)*
- **GR-2.4** A cited source must say what the page claims. *(review: accuracy)*
- **GR-2.5** Every reference records title, organisation or author, URL and date accessed. *(check, to add)*
- **GR-2.6** Every metric page gives a definition, a formula with unit and aggregation, and the
  source of the definition. Where sources define a metric differently, the page says so. *(check: template · review)*
- **GR-2.7** A benchmark or threshold appears only with its source, year and population, and is
  presented as that source's finding, never as a target. *(review: accuracy)*
- **GR-2.8** Research from chat assistants (ChatGPT Deep Research or similar) is a lead, not a
  source: each claim is traced to the primary source before use. *(review: accuracy)*

## §3 Voice
- **GR-3.1** Reference register: present tense, plain practitioner English, no first person.
- **GR-3.2** No provisional language on the public site: "coming soon", "work in progress", "TBD",
  "placeholder". Map boxes without a page are plain labels. The release build refuses a provisional
  inventory or a layout-sample page. *(check)*
- **GR-3.3** Vendor-neutral by default. *(review)*
- **GR-3.4** One running example at most, chosen with Vishal's approval. *(review)*

## §4 Completeness
- **GR-4.1** A page is published only when every required section of its template is present and
  substantive. *(check: template, to add · review: editorial)*
- **GR-4.2** Every page stands alone for a reader arriving from search. *(review: editorial)*
- **GR-4.3** Every internal link and anchor resolves. *(check)*
- **GR-4.4** Every diagram is diagram-as-code with a text alternative; the overview map has a full
  text route on the home page. *(check)*
- **GR-4.5** The landing page shows the full overview map, never a reduced one (design system v1.0). *(review)*

## §5 Process
- **GR-5.1** Every page follows the pipeline in `APPROACH.md`.
- **GR-5.2** Every released page has a review record in `content/reviews/` naming each reviewer, its
  independence (independent human, fresh-context agent, or self-check) and verdict. *(review; check to add)*
- **GR-5.3** Recurring findings become checks where possible; changes go in `DECISIONS.md`.
- **GR-5.4** `main` always builds and passes validation. Work lands through pull requests.

## §6 Authority
- **GR-6.1** Single final review (D-002): the maintainer decides routine milestones, then brings
  Vishal one complete preview with the review record and limitations. "Ready for review" is not
  "authorised to publish". Only Vishal triggers publication.
- **GR-6.2** Where a rule conflicts with a session request, the rule wins until Vishal changes it here.
- **GR-6.3** Visual design follows the locked AI SDLC design system v1.0; changes need Vishal's approval.
