/** @odoo-module **/
/*
 * Badge scanner front end (design decisions D2, D3, D4, D6).
 *
 * Reads QR codes with the browser's BarcodeDetector where available, falls
 * back to manual entry, and queues scans locally when the network is down.
 */

import { ScanQueue } from './scan_queue';

const root = document.getElementById('scan_root');
if (root) {
    const sessionToken = root.dataset.sessionToken;
    const video = document.getElementById('scan_video');
    const startBtn = document.getElementById('scan_start_camera');
    const manualInput = document.getElementById('scan_manual_input');
    const manualBtn = document.getElementById('scan_manual_submit');
    const confirmBox = document.getElementById('scan_confirm');
    const nameEl = document.getElementById('scan_attendee_name');
    const companyEl = document.getElementById('scan_attendee_company');
    const dupWarn = document.getElementById('scan_duplicate_warning');
    const consentWarn = document.getElementById('scan_consent_warning');
    const noteEl = document.getElementById('scan_note');
    const saveBtn = document.getElementById('scan_save');
    const cancelBtn = document.getElementById('scan_cancel');
    const counterEl = document.getElementById('scan_counter');
    const syncStatus = document.getElementById('scan_sync_status');
    const pendingCount = document.getElementById('scan_pending_count');
    const messageEl = document.getElementById('scan_message');

    let pendingScan = null;
    let stream = null;
    let detector = null;
    let scanLoopHandle = null;

    function message(text, kind) {
        messageEl.innerHTML = text
            ? `<div class="alert alert-${kind || 'info'}">${text}</div>`
            : '';
    }

    function selectedScore() {
        const checked = document.querySelector('input[name="scan_score"]:checked');
        return checked ? checked.value : null;
    }

    function resetConfirm() {
        pendingScan = null;
        confirmBox.classList.add('d-none');
        dupWarn.classList.add('d-none');
        consentWarn.classList.add('d-none');
        noteEl.value = '';
        document
            .querySelectorAll('input[name="scan_score"]')
            .forEach((el) => { el.checked = false; });
    }

    function updateCounter(count) {
        if (typeof count === 'number') {
            counterEl.textContent = count;
        }
    }

    function updateSyncStatus() {
        const n = ScanQueue.count();
        if (n > 0) {
            syncStatus.classList.remove('d-none');
            pendingCount.textContent = n;
        } else {
            syncStatus.classList.add('d-none');
        }
    }

    async function flushQueue() {
        if (!navigator.onLine || ScanQueue.count() === 0) {
            updateSyncStatus();
            return;
        }
        try {
            const result = await ScanQueue.flush(sessionToken);
            updateCounter(result.leadCount);
            updateSyncStatus();
        } catch (err) {
            console.warn('[scan_app] sync failed, will retry', err);
            updateSyncStatus();
        }
    }

    function showConfirm(registration, alreadyScanned) {
        pendingScan = registration;
        nameEl.textContent = registration.name || '—';
        companyEl.textContent = registration.company || '—';
        dupWarn.classList.toggle('d-none', !alreadyScanned);
        consentWarn.classList.toggle('d-none', registration.consent !== false);
        confirmBox.classList.remove('d-none');
        confirmBox.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    async function submitScan(registrationToken) {
        message('');
        const body = {
            session_token: sessionToken,
            registration_token: registrationToken,
            client_scan_uuid: ScanQueue.newUuid(),
        };

        if (!navigator.onLine) {
            // Offline: queue it and confirm locally (D4).
            const item = ScanQueue.enqueue({
                registration_token: registrationToken,
            });
            updateSyncStatus();
            message(
                'Saved offline. It will sync when you are back online.',
                'warning'
            );
            return;
        }

        try {
            const response = await fetch('/event_lead_scan/api/scan', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body),
            });
            const data = await response.json();
            if (!response.ok) {
                message(data.message || 'Could not read that badge.', 'danger');
                return;
            }
            const registration = data.registration || {};
            showConfirm(registration, data.already_scanned);
            updateCounter(data.lead_count);
        } catch (err) {
            // Network died mid-request: queue it rather than losing the scan.
            ScanQueue.enqueue({ registration_token: registrationToken });
            updateSyncStatus();
            message('Network problem — the scan is queued.', 'warning');
        }
    }

    async function saveAnnotation() {
        if (!pendingScan) {
            return;
        }
        // The scan itself is already recorded; this only adds the annotation.
        // Re-submitting with the same client reference is idempotent.
        const body = {
            session_token: sessionToken,
            registration_token: pendingScan.scan_token,
            client_scan_uuid: ScanQueue.newUuid(),
            note: noteEl.value || null,
            score: selectedScore(),
        };
        try {
            const response = await fetch('/event_lead_scan/api/scan', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body),
            });
            const data = await response.json();
            if (response.ok) {
                updateCounter(data.lead_count);
                resetConfirm();
                message('Lead saved.', 'success');
                setTimeout(() => message(''), 1500);
            } else {
                message(data.message || 'Could not save the note.', 'danger');
            }
        } catch (err) {
            message('Network problem — try again.', 'warning');
        }
    }

    // ---------------------------------------------------------------- camera
    async function startCamera() {
        if (!('BarcodeDetector' in window)) {
            message(
                'This browser cannot read QR codes. Use the badge code field below.',
                'info'
            );
            return;
        }
        try {
            stream = await navigator.mediaDevices.getUserMedia({
                video: { facingMode: 'environment' },
            });
            video.srcObject = stream;
            await video.play();
            detector = new window.BarcodeDetector({ formats: ['qr_code'] });
            startBtn.classList.add('d-none');
            scanLoop();
        } catch (err) {
            message('Could not start the camera. Use the badge code field below.', 'warning');
        }
    }

    async function scanLoop() {
        if (!detector || !video) {
            return;
        }
        try {
            const codes = await detector.detect(video);
            if (codes && codes.length) {
                const value = codes[0].rawValue;
                if (value) {
                    stopCamera();
                    await submitScan(value);
                    return;
                }
            }
        } catch (err) {
            // Detection errors are normal while the frame is blurry.
        }
        scanLoopHandle = window.setTimeout(scanLoop, 400);
    }

    function stopCamera() {
        if (scanLoopHandle) {
            window.clearTimeout(scanLoopHandle);
            scanLoopHandle = null;
        }
        if (stream) {
            stream.getTracks().forEach((t) => t.stop());
            stream = null;
        }
        startBtn.classList.remove('d-none');
    }

    // ---------------------------------------------------------------- wiring
    startBtn.addEventListener('click', startCamera);
    manualBtn.addEventListener('click', () => {
        const value = (manualInput.value || '').trim();
        if (value) {
            manualInput.value = '';
            submitScan(value);
        }
    });
    manualInput.addEventListener('keydown', (ev) => {
        if (ev.key === 'Enter') {
            ev.preventDefault();
            manualBtn.click();
        }
    });
    saveBtn.addEventListener('click', saveAnnotation);
    cancelBtn.addEventListener('click', resetConfirm);
    window.addEventListener('online', flushQueue);
    window.addEventListener('offline', updateSyncStatus);

    updateSyncStatus();
    flushQueue();
    // Retry the queue periodically while the page is open.
    window.setInterval(flushQueue, 15000);
}
