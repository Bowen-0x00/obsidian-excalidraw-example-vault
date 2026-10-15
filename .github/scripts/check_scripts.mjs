// Non-executing syntax check for Excalidraw scripts in the vault.
import fs from 'node:fs';
import path from 'node:path';

const root = process.argv[2] || '.';
const AsyncFunction = Object.getPrototypeOf(async function () {}).constructor;

function scanDir(dir, fileList = []) {
  if (!fs.existsSync(dir)) return fileList;
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    if (['.git', '.obsidian', 'node_modules', '.upstream-scripts', '.upstream-plugin'].includes(entry.name)) {
      continue;
    }
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      scanDir(fullPath, fileList);
    } else if (entry.isFile() && entry.name.endsWith('.md')) {
      const rel = path.relative(root, fullPath).replace(/\\/g, '/');
      if (rel.toLowerCase().includes('/scripts/')) {
        fileList.push(fullPath);
      }
    }
  }
  return fileList;
}

const scripts = scanDir(root);
let checked = 0;
let errors = 0;

for (const scriptPath of scripts) {
  const rel = path.relative(root, scriptPath).replace(/\\/g, '/');
  const content = fs.readFileSync(scriptPath, 'utf8');
  // Strip frontmatter
  const body = content.replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n/, '');
  if (!body.trim()) continue;
  try {
    new AsyncFunction('ea', 'utils', body);
    checked++;
  } catch (error) {
    console.error(`Syntax error in ${rel}: ${error.message}`);
    errors++;
  }
}

console.log(`Syntax checked ${checked} Excalidraw scripts without execution.`);
if (errors > 0) {
  console.error(`Total errors: ${errors}`);
  process.exit(1);
}
