# Hospital Objects Project Page

This repository contains the Astro project page for the research paper
"Hospital Objects: An Object Library for Robotic Nursing Assistance." The page
summarizes a field study of nursing supplies and the perception, grasping, and
control challenges they introduce for robots.

## Content

The page is authored in [src/paper.mdx](./src/paper.mdx). This file contains:

- The browser metadata and page title in its frontmatter.
- The header, conference information, and cover image.
- The abstract, copied verbatim from the paper.
- A concise summary of the field study and its findings.
- Figures and captions describing the nursing-supply object library.

Keep research claims and numerical results synchronized with the paper source.
The abstract should remain verbatim unless the paper itself changes.

## Assets

Paper images are stored in [src/assets/Figures](./src/assets/Figures). The
labeled object-kit overview is [kit_square.png](./src/assets/kit_square.png).
Import images from `src/paper.mdx` and display them with the local `Picture`
component so Astro can optimize their formats and sizes.

The [Dataset.xlsx](./src/assets/Dataset.xlsx) file contains the associated
study data. It is kept as a source asset and is not currently rendered on the
page.

## Local development

Install dependencies and start the development server from the repository root:

```bash
npm install
npm run dev
```

The site is available at `http://localhost:4321`. Astro reloads the page when
`src/paper.mdx` or a component changes.

## Production build

Run the type checks and static build with:

```bash
npm run build
```

The generated site is written to `dist/`. Images imported through Astro are
converted into responsive optimized assets during this build.

## Future extensions

Useful additions for the project page include:

- An object browser filtered by deformability, transparency, packaging layers,
  and manipulation failure modes.
- A task-to-object matrix connecting nursing workflows to object properties.
- Short videos showing retrieval, opening, sorting, and handover actions.
- Downloadable annotations for benchmarking perception and manipulation systems.
