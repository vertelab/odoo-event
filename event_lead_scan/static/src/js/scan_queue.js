/** @odoo-module **/
/*
 * Offline queue for the badge scanner (design decision D4).
 *
 * Scans are appended to localStorage with a client-generated UUID. The
 * server is idempotent on that UUID, so a retried or replayed scan never
 * creates a second lead. The queue survives a page reload, which matters
 * because trade-fair WiFi drops constantly.
 */

const STORAGE_KEY = 'event_lead_scan_queue_v1';

function readQueue() {
    try {
        const raw = window.localStorage.getItem(STORAGE_KEY);
        return raw ? JSON.parse(raw) : [];
    } catch (err) {
        console.warn('[scan_queue] could not read queue', err);
        return [];
    }
}

function writeQueue(items) {
    try {
        window.localStorage.setItem(STORAGE_KEY, JSON.stringify(items));
    } catch (err) {
        console.warn('[scan_queue] could not write queue', err);
    }
}

function newUuid() {
    if (window.crypto && window.crypto.randomUUID) {
        return window.crypto.randomUUID();
    }
    // Fallback for older browsers.
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
        const r = (Math.random() * 16) | 0;
        const v = c === 'x' ? r : (r & 0x3) | 0x8;
        return v.toString(16);
    });
}

export const ScanQueue = {
    newUuid,

    /** Add a scan to the local queue. Returns the stored item. */
    enqueue(scan) {
        const item = Object.assign({ client_scan_uuid: newUuid() }, scan);
        const items = readQueue();
        items.push(item);
        writeQueue(items);
        return item;
    },

    all() {
        return readQueue();
    },

    count() {
        return readQueue().length;
    },

    /** Remove one item by its client reference. */
    remove(clientScanUuid) {
        writeQueue(readQueue().filter((i) => i.client_scan_uuid !== clientScanUuid));
    },

    clear() {
        writeQueue([]);
    },

    /**
     * Submit everything that is queued. Items the server accepts (or
     * recognises as already recorded) are dropped; the rest stay queued.
     */
    async flush(sessionToken) {
        const items = readQueue();
        if (!items.length) {
            return { synced: 0, remaining: 0 };
        }
        const response = await fetch('/event_lead_scan/api/bulk', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ session_token: sessionToken, scans: items }),
        });
        if (!response.ok) {
            return { synced: 0, remaining: items.length };
        }
        const data = await response.json();
        const done = new Set(
            (data.results || [])
                .filter((r) => r.ok || r.error === 'idempotent_replay')
                .map((r) => r.client_scan_uuid)
        );
        writeQueue(items.filter((i) => !done.has(i.client_scan_uuid)));
        return { synced: done.size, remaining: this.count(), leadCount: data.lead_count };
    },
};
