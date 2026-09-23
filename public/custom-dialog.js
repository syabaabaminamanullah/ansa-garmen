// Modern Glassmorphism Alert & Modal for SEAM ANNSA
(function () {
  const isBrowser = typeof window !== 'undefined' && typeof document !== 'undefined';
  if (!isBrowser) return;

  // Inject styles
  const style = document.createElement('style');
  style.id = 'seam-dialog-styles';
  style.textContent = `
    .seam-alert-overlay {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(3, 7, 18, 0.75);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 999999;
      padding: 16px;
      opacity: 0;
      transition: opacity 0.25s cubic-bezier(0.16, 1, 0.3, 1);
      font-family: 'Outfit', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    .seam-alert-overlay.show {
      opacity: 1;
    }
    .seam-alert-card {
      position: relative;
      width: 100%;
      max-width: 420px;
      background: linear-gradient(180deg, rgba(15, 23, 42, 0.95) 0%, rgba(10, 18, 33, 0.98) 100%);
      border: 1px solid rgba(16, 185, 129, 0.25);
      box-shadow: 0 25px 60px -15px rgba(0, 0, 0, 0.8), 0 0 40px rgba(16, 185, 129, 0.15);
      border-radius: 28px;
      padding: 32px 28px 28px 28px;
      display: flex;
      flex-col;
      flex-direction: column;
      align-items: center;
      text-align: center;
      transform: scale(0.9) translateY(15px);
      transition: transform 0.28s cubic-bezier(0.34, 1.56, 0.64, 1);
      overflow: hidden;
    }
    .seam-alert-overlay.show .seam-alert-card {
      transform: scale(1) translateY(0);
    }
    .seam-alert-ambient-glow {
      position: absolute;
      top: -60px;
      left: 50%;
      transform: translateX(-50%);
      width: 180px;
      height: 180px;
      border-radius: 50%;
      background: radial-gradient(circle, rgba(16, 185, 129, 0.25) 0%, transparent 70%);
      pointer-events: none;
      filter: blur(20px);
    }
    .seam-alert-tag {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 4px 12px;
      border-radius: 999px;
      background: rgba(16, 185, 129, 0.08);
      border: 1px solid rgba(16, 185, 129, 0.2);
      font-size: 10px;
      font-weight: 800;
      color: #34d399;
      text-transform: uppercase;
      letter-spacing: 0.18em;
      margin-bottom: 20px;
    }
    .seam-alert-tag-dot {
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: #10b981;
      box-shadow: 0 0 8px #10b981;
    }
    .seam-alert-icon-wrap {
      width: 68px;
      height: 68px;
      border-radius: 22px;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-bottom: 18px;
      position: relative;
    }
    .seam-alert-icon-wrap.success {
      background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(5, 150, 105, 0.05));
      border: 1.5px solid rgba(16, 185, 129, 0.35);
      color: #10b981;
      box-shadow: 0 10px 25px rgba(16, 185, 129, 0.2);
    }
    .seam-alert-icon-wrap.error {
      background: linear-gradient(135deg, rgba(239, 68, 68, 0.2), rgba(185, 28, 28, 0.05));
      border: 1.5px solid rgba(239, 68, 68, 0.35);
      color: #ef4444;
      box-shadow: 0 10px 25px rgba(239, 68, 68, 0.2);
    }
    .seam-alert-icon-wrap.info {
      background: linear-gradient(135deg, rgba(59, 130, 246, 0.2), rgba(37, 99, 235, 0.05));
      border: 1.5px solid rgba(59, 130, 246, 0.35);
      color: #3b82f6;
      box-shadow: 0 10px 25px rgba(59, 130, 246, 0.2);
    }
    .seam-alert-title {
      font-size: 20px;
      font-weight: 800;
      color: #ffffff;
      letter-spacing: -0.02em;
      margin: 0 0 10px 0;
    }
    .seam-alert-msg {
      font-size: 14px;
      font-weight: 500;
      color: #94a3b8;
      line-height: 1.6;
      margin: 0 0 26px 0;
      word-break: break-word;
      max-height: 240px;
      overflow-y: auto;
    }
    .seam-alert-btn {
      width: 100%;
      padding: 14px 24px;
      border-radius: 16px;
      background: linear-gradient(135deg, #10b981 0%, #059669 100%);
      color: #ffffff;
      font-size: 13px;
      font-weight: 800;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      border: none;
      cursor: pointer;
      box-shadow: 0 8px 25px rgba(16, 185, 129, 0.35);
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
    }
    .seam-alert-btn:hover {
      transform: translateY(-2px);
      box-shadow: 0 12px 30px rgba(16, 185, 129, 0.5);
      filter: brightness(1.08);
    }
    .seam-alert-btn:active {
      transform: scale(0.98);
    }
    .seam-alert-btn.error-btn {
      background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
      box-shadow: 0 8px 25px rgba(239, 68, 68, 0.35);
    }
    .seam-alert-btn.error-btn:hover {
      box-shadow: 0 12px 30px rgba(239, 68, 68, 0.5);
    }
  `;
  document.head.appendChild(style);

  // SVG Icons
  const icons = {
    success: `<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6L9 17l-5-5"/></svg>`,
    error: `<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>`,
    info: `<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>`
  };

  function showCustomAlert(message) {
    const rawMsg = String(message || '');
    const isError = /gagal|error|gagal|salah|rusak|invalid|denied|ditolak/i.test(rawMsg);
    const isSuccess = /berhasil|sukses|success|tersimpan|diperbarui|selesai|updated|created/i.test(rawMsg) || !isError;
    
    const type = isError ? 'error' : (isSuccess ? 'success' : 'info');
    const titleText = isError ? 'Pemberitahuan' : (isSuccess ? 'Berhasil' : 'Informasi');

    const overlay = document.createElement('div');
    overlay.className = 'seam-alert-overlay';
    overlay.innerHTML = `
      <div class="seam-alert-card">
        <div class="seam-alert-ambient-glow"></div>
        <div class="seam-alert-tag">
          <span class="seam-alert-tag-dot"></span>
          SEAM ANNSA NOTIFICATION
        </div>
        <div class="seam-alert-icon-wrap ${type}">
          ${icons[type]}
        </div>
        <h3 class="seam-alert-title">${titleText}</h3>
        <p class="seam-alert-msg">${rawMsg.replace(/\\n/g, '<br/>')}</p>
        <button class="seam-alert-btn ${isError ? 'error-btn' : ''}" id="seam-alert-ok-btn">
          <span>MENGERTI</span>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
        </button>
      </div>
    `;

    document.body.appendChild(overlay);

    // Trigger animation
    requestAnimationFrame(() => {
      overlay.classList.add('show');
    });

    const btn = overlay.querySelector('#seam-alert-ok-btn');

    function close() {
      overlay.classList.remove('show');
      setTimeout(() => {
        if (overlay.parentNode) {
          overlay.parentNode.removeChild(overlay);
        }
      }, 280);
      document.removeEventListener('keydown', handleKey);
    }

    function handleKey(e) {
      if (e.key === 'Enter' || e.key === 'Escape' || e.key === ' ') {
        e.preventDefault();
        close();
      }
    }

    btn.addEventListener('click', close);
    overlay.addEventListener('click', (e) => {
      if (e.target === overlay) close();
    });
    document.addEventListener('keydown', handleKey);
    btn.focus();
  }

  // Override window.alert
  window.alert = function (msg) {
    try {
      showCustomAlert(msg);
    } catch (e) {
      console.error('Custom alert failed, falling back:', e);
      if (typeof window.origAlert === 'function') {
        window.origAlert(msg);
      }
    }
  };
})();
