// Captura PNG das páginas geradas e mede textos cortados/overflow.
// Uso: node shot.js jobs.json   (jobs: [{html, png, w, h, metrics}])
const { chromium } = require('playwright-core');
const fs = require('fs');

(async () => {
  const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell' });
  const out = {};
  for (const j of jobs) {
    const page = await browser.newPage({ viewport: { width: j.w, height: j.h } });
    await page.goto('file://' + j.html);
    await page.waitForTimeout(150);
    if (j.png) await page.screenshot({ path: j.png });
    out[j.id] = await page.evaluate(() => {
      const res = { truncated: [], hscroll: document.documentElement.scrollWidth > window.innerWidth };
      document.querySelectorAll('.hv[data-name]').forEach(el => {
        // conteúdo HTML que ultrapassa a caixa do próprio controle (cortado pelo controle)
        const r = el.getBoundingClientRect();
        el.querySelectorAll('*').forEach(d => {
          if (d.children.length || !d.textContent.trim()) return;
          const q = d.getBoundingClientRect();
          if (q.height > 0 && (q.bottom > r.bottom + 1 || q.right > r.right + 1))
            res.truncated.push({ name: el.getAttribute('data-name'), text: '[fora da caixa] ' + d.textContent.trim().slice(0, 70) });
        });
      });
      document.querySelectorAll('[data-name]').forEach(el => {
        const name = el.getAttribute('data-name');
        el.querySelectorAll('*').forEach(d => {
          const cs = getComputedStyle(d);
          if (d.children.length === 0 && d.textContent.trim() && (d.scrollWidth > d.clientWidth + 1 || d.scrollHeight > d.clientHeight + 2) &&
              (cs.overflow !== 'visible')) res.truncated.push({ name, text: d.textContent.trim().slice(0, 80) });
        });
      });
      return res;
    });
    await page.close();
  }
  await browser.close();
  fs.writeFileSync(process.argv[2] + '.out.json', JSON.stringify(out, null, 1));
})();
