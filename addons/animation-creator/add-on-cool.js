// FrameForge Animated Transitions Add-on
FrameForge.addPanel('Animated Transitions', `
  <div class="stack">
    <div class="row">
      <label for="trans-effect">Transition Effect</label>
      <select id="trans-effect">
        <option value="pageflip">Page Flip (Curl)</option>
        <option value="crossfade">Crossfade</option>
        <option value="wipe">Slide / Wipe Left</option>
      </select>
    </div>
    <div class="row">
      <label for="trans-steps">In-between Frames</label>
      <input id="trans-steps" type="number" min="1" max="10" value="3">
    </div>
    <div class="grid2">
      <button id="trans-bake-one" class="primary">Bake to Next Frame</button>
      <button id="trans-bake-all">Bake Between All Frames</button>
    </div>
    <div class="control-note">
      Generates smooth transition frames directly into your timeline so they display during playback and export seamlessly to MP4.
    </div>
  </div>
`);

FrameForge.addStyle(`
  .stack { display: grid; gap: 10px; }
  .row { display: flex; align-items: center; justify-content: space-between; gap: 8px; }
  .grid2 { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
  .control-note { color: var(--muted); font-size: 0.78rem; line-height: 1.35; }
`);

function drawTransition(type, ctxA, imgA, imgB, t, W, H) {
  ctxA.clearRect(0, 0, W, H);

  if (type === 'crossfade') {
    ctxA.save();
    ctxA.globalAlpha = 1 - t;
    ctxA.drawImage(imgA, 0, 0, W, H);
    ctxA.globalAlpha = t;
    ctxA.drawImage(imgB, 0, 0, W, H);
    ctxA.restore();
  } else if (type === 'wipe') {
    const shift = W * t;
    ctxA.drawImage(imgA, -shift, 0, W, H);
    ctxA.drawImage(imgB, W - shift, 0, W, H);
  } else {
    // Page Flip with realistic paper curl, underside reflect, and drop shadow
    ctxA.drawImage(imgB, 0, 0, W, H);

    const flipX = W * (1 - t);
    if (flipX > 0) {
      // Draw remaining un-flipped portion of Frame A
      ctxA.save();
      ctxA.beginPath();
      ctxA.rect(0, 0, flipX, H);
      ctxA.clip();
      ctxA.drawImage(imgA, 0, 0, W, H);
      ctxA.restore();

      // Drop shadow on revealed Frame B
      ctxA.save();
      const shadowW = Math.min(35, W * 0.06);
      const gradB = ctxA.createLinearGradient(flipX, 0, flipX + shadowW, 0);
      gradB.addColorStop(0, 'rgba(0,0,0,0.4)');
      gradB.addColorStop(1, 'rgba(0,0,0,0)');
      ctxA.fillStyle = gradB;
      ctxA.fillRect(flipX, 0, shadowW, H);
      ctxA.restore();

      // Curl underside (mirrored peel)
      const curlW = Math.min(W * 0.25, (W - flipX) * 0.5);
      if (curlW > 0) {
        ctxA.save();
        ctxA.beginPath();
        ctxA.rect(flipX - curlW, 0, curlW, H);
        ctxA.clip();

        ctxA.translate(flipX, 0);
        ctxA.scale(-1, 1);
        ctxA.drawImage(imgA, -flipX, 0, W, H);

        ctxA.fillStyle = 'rgba(240, 240, 255, 0.35)';
        ctxA.fillRect(-W, 0, W * 2, H);

        const gradCurl = ctxA.createLinearGradient(flipX, 0, flipX - curlW, 0);
        gradCurl.addColorStop(0, 'rgba(0,0,0,0.3)');
        gradCurl.addColorStop(1, 'rgba(0,0,0,0)');
        ctxA.fillStyle = gradCurl;
        ctxA.fillRect(flipX - curlW, 0, curlW, H);

        ctxA.restore();
      }
    }
  }
}

function captureFrame(index) {
  const framesList = document.querySelectorAll('#frames .frame');
  if (index < 0 || index >= framesList.length) return null;
  framesList[index].click();
  const canvas = FrameForge.getCanvas();
  const snap = document.createElement('canvas');
  snap.width = FrameForge.getWidth();
  snap.height = FrameForge.getHeight();
  const sCtx = snap.getContext('2d');
  sCtx.drawImage(canvas, 0, 0);
  return snap;
}

function bakeTransitionBetween(indexA, steps, effect) {
  const imgA = captureFrame(indexA);
  const imgB = captureFrame(indexA + 1);
  if (!imgA || !imgB) return false;

  document.querySelectorAll('#frames .frame')[indexA].click();

  const W = FrameForge.getWidth();
  const H = FrameForge.getHeight();
  const ctx = FrameForge.getContext();

  for (let k = 1; k <= steps; k++) {
    const t = k / (steps + 1);
    FrameForge.addFrame();
    drawTransition(effect, ctx, imgA, imgB, t, W, H);
    FrameForge.saveFrame();
  }
  return true;
}

FrameForge.getElement('trans-bake-one').addEventListener('click', () => {
  const steps = parseInt(FrameForge.getElement('trans-steps').value, 10) || 3;
  const effect = FrameForge.getElement('trans-effect').value;
  const curr = FrameForge.getCurrentFrame();
  const total = FrameForge.getFrameCount();

  if (curr >= total - 1) {
    FrameForge.notify('Select a frame that has a next frame to transition into!');
    return;
  }

  if (bakeTransitionBetween(curr, steps, effect)) {
    FrameForge.notify(`Inserted ${steps} ${effect} transition frames!`);
  }
});

FrameForge.getElement('trans-bake-all').addEventListener('click', () => {
  const steps = parseInt(FrameForge.getElement('trans-steps').value, 10) || 3;
  const effect = FrameForge.getElement('trans-effect').value;
  let total = FrameForge.getFrameCount();

  if (total < 2) {
    FrameForge.notify('Need at least 2 keyframes to create transitions!');
    return;
  }

  let currIndex = 0;
  while (currIndex < total - 1) {
    bakeTransitionBetween(currIndex, steps, effect);
    currIndex += steps + 1;
    total = FrameForge.getFrameCount();
  }

  FrameForge.notify(`Successfully baked ${effect} transitions across all keyframes!`);
});
