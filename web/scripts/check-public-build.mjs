import { readdir, readFile } from 'node:fs/promises';
import { join } from 'node:path';

// The public bundle must not contain the harness's private UI controls or endpoints.
const assets = join(process.cwd(), 'dist', 'assets');
const scripts = (await readdir(assets)).filter(file => file.endsWith('.js'));
if (!scripts.length) throw new Error('no bundle in dist/assets; run the build first');
const bundle = (await Promise.all(scripts.map(file => readFile(join(assets, file), 'utf8')))).join('\n');
for (const forbidden of ['/benchmark', '/corpus/papers', '/settings', '/promote', '/rating', 'Gold candidates']) {
  if (bundle.includes(forbidden)) throw new Error(`Private UI control or endpoint found in public bundle: ${forbidden}`);
}
console.log('Public build contains no checked private controls or endpoints.');
