import { createHighlighterCore } from "shiki/core";
import getWasm from "shiki/wasm";

export const highlighter = await createHighlighterCore({
    themes: [
      import('shiki/themes/material-theme-ocean.mjs')
    ],
    langs: [
      import('shiki/langs/sql.mjs'),
    ],
    loadWasm: getWasm
  })
