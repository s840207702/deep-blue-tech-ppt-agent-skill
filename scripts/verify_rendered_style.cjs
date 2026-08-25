#!/usr/bin/env node
"use strict";

const fs = require("node:fs");
const path = require("node:path");
const { pathToFileURL } = require("node:url");
const { chromium } = require("playwright");

const PROFILE_VIEWPORTS = {
  "terminal-studio-16x9-v1": { width: 1920, height: 1080 },
  "terminal-studio-1x1-v1": { width: 1920, height: 1920 },
};

function parseArgs(argv) {
  const result = { html: argv[2], timeout: 30, browser: null, slides: null };
  for (let index = 3; index < argv.length; index += 1) {
    const value = argv[index];
    if (value === "--timeout") result.timeout = Number(argv[++index]);
    else if (value === "--browser") result.browser = argv[++index];
    else if (value === "--slides") result.slides = argv[++index];
    else throw new Error(`unknown argument: ${value}`);
  }
  return result;
}

function detectBrowser(explicit) {
  const candidates = [
    explicit,
    process.env.CHROME_PATH,
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
  ];
  return candidates.find((candidate) => candidate && fs.existsSync(candidate)) || null;
}

function parseDeck(source) {
  const profile = source.match(/<meta\s+name=["']terminal-studio-profile["']\s+content=["']([^"']+)["']/i)?.[1];
  const slides = [...source.matchAll(/<section\b[^>]*class=["'][^"']*\bslide\b[^"']*["']/gi)].length;
  return { profile, slides };
}

async function main() {
  const args = parseArgs(process.argv);
  if (!args.html) throw new Error("missing HTML path");
  const htmlPath = path.resolve(args.html);
  const source = fs.readFileSync(htmlPath, "utf8");
  const deck = parseDeck(source);
  const viewport = PROFILE_VIEWPORTS[deck.profile];
  if (!viewport) throw new Error(`unsupported or missing profile: ${deck.profile}`);
  if (deck.slides < 1) throw new Error("no .slide sections found");

  const selected = args.slides
    ? args.slides.split(",").map((value) => Number(value.trim()))
    : Array.from({ length: deck.slides }, (_, index) => index + 1);
  if (selected.some((slide) => !Number.isInteger(slide) || slide < 1 || slide > deck.slides)) {
    throw new Error(`--slides must stay within 1..${deck.slides}`);
  }

  const executablePath = detectBrowser(args.browser);
  const browser = await chromium.launch({ headless: true, ...(executablePath ? { executablePath } : {}) });
  const context = await browser.newContext({ viewport });
  const page = await context.newPage();
  const failures = [];

  try {
    for (const slide of selected) {
      const url = `${pathToFileURL(htmlPath).href}?slide=${slide}`;
      try {
        await page.goto(url, { waitUntil: "networkidle", timeout: args.timeout * 1000 });
        await page.waitForFunction(
          () => document.documentElement.dataset.renderReady !== "pending",
          null,
          { timeout: args.timeout * 1000 },
        );
        const state = await page.evaluate(() => ({
          fontsReady: document.documentElement.dataset.fontsReady,
          imagesReady: document.documentElement.dataset.imagesReady,
          styleReady: document.documentElement.dataset.styleReady,
          renderReady: document.documentElement.dataset.renderReady,
          report: document.documentElement.dataset.renderReport || "no render report",
        }));
        if (state.fontsReady !== "true" || state.imagesReady !== "true" || state.styleReady !== "true" || state.renderReady !== "true") {
          failures.push(`slide ${slide}: ${JSON.stringify(state)}`);
        }
      } catch (error) {
        failures.push(`slide ${slide}: ${error.message}`);
      }
    }
  } finally {
    await browser.close();
  }

  if (failures.length) {
    process.stderr.write(`FAIL: rendered verification failed for ${htmlPath}\n`);
    failures.forEach((failure) => process.stderr.write(`- ${failure}\n`));
    process.exitCode = 1;
    return;
  }
  process.stdout.write(`PASS: ${selected.length} slides rendered at ${viewport.width}x${viewport.height} with locked styles, fonts, and images\n`);
}

main().catch((error) => {
  process.stderr.write(`ERROR: ${error.message}\n`);
  process.exitCode = 2;
});
