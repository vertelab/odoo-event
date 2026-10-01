# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo SA, Open Source Management Solution, third party addon
#    Copyright (C) 2022- Vertel AB (<https://vertel.se>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import json
import logging
import time

from odoo import http, fields, _
from odoo.http import request

_logger = logging.getLogger(__name__)

# Simple in-process rate limit per session token, to make guessing the
# attendee list impractical. Design decision D2/D3.
RATE_LIMIT_WINDOW = 60          # seconds
RATE_LIMIT_MAX_REQUESTS = 120   # requests per window per session

_rate_buckets = {}


def _rate_limited(token):
    """Return True when this token has exceeded its request budget."""
    now = time.time()
    bucket = _rate_buckets.setdefault(token, [])
    # drop timestamps outside the window
    bucket[:] = [t for t in bucket if now - t < RATE_LIMIT_WINDOW]
    if len(bucket) >= RATE_LIMIT_MAX_REQUESTS:
        return True
    bucket.append(now)
    return False


class EventLeadScanController(http.Controller):
    """Scan API and the mobile scanner pages."""

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _json(self, payload, status=200):
        return request.make_json_response(payload, status=status)

    def _get_session(self, token, require_open=True):
        """Resolve a session token to a session, or return an error tuple."""
        if not token:
            return None, ('missing_token', _('No session token supplied.'))
        if _rate_limited(token):
            return None, ('rate_limited',
                          _('Too many requests. Please wait a moment.'))
        session = request.env['event.lead.scan.session'].sudo().search(
            [('session_token', '=', token)], limit=1
        )
        if not session:
            return None, ('invalid_token', _('Unknown session.'))
        if require_open and not session._is_scannable():
            return None, ('session_closed', _('This session is closed.'))
        return session, None

    def _resolve_registration(self, session, registration_token=None,
                              registration_id=None):
        """Resolve the scanned badge to a registration of this event."""
        Registration = request.env['event.registration'].sudo()
        if registration_token:
            registration = Registration.search(
                [('scan_token', '=', registration_token)], limit=1
            )
        elif registration_id:
            registration = Registration.browse(int(registration_id)).exists()
        else:
            return None, ('missing_badge', _('No badge code supplied.'))
        if not registration:
            return None, ('invalid_badge', _('Unknown badge.'))
        # A badge from another event must not be capturable here.
        if registration.event_id != session.event_id:
            return None, ('wrong_event',
                          _('This badge belongs to another event.'))
        return registration, None

    def _registration_payload(self, registration):
        partner = registration.partner_id
        return {
            'id': registration.id,
            'name': partner.name or registration.name or '',
            'company': partner.parent_name or '',
            'email': partner.email or '',
            'phone': partner.phone or '',
            'consent': registration.scan_consent,
        }

    # ------------------------------------------------------------------
    # Session metadata
    # ------------------------------------------------------------------
    @http.route('/event_lead_scan/api/session/<string:token>',
                type='http', auth='public', methods=['GET'], csrf=False)
    def session_info(self, token, **kw):
        """Return the session header. Never exposes leads."""
        session, error = self._get_session(token, require_open=False)
        if error:
            code, message = error
            return self._json({'error': code, 'message': str(message)}, 403)
        return self._json({
            'session': {
                'name': session.name,
                'event': session.event_id.name,
                'responsible': session.responsible_id.name,
                'state': session.state,
                'scannable': session._is_scannable(),
                'lead_count': session.lead_count,
            }
        })

    # ------------------------------------------------------------------
    # Scanning
    # ------------------------------------------------------------------
    @http.route('/event_lead_scan/api/scan',
                type='http', auth='public', methods=['POST'],
                csrf=False)
    def scan(self, **kw):
        """Capture one scan and return the resulting lead.

        Idempotent on ``client_scan_uuid`` (D4) and duplicate-safe on
        (session, registration) (D5).
        """
        payload = self._payload(kw)
        session, error = self._get_session(payload.get('session_token'))
        if error:
            code, message = error
            return self._json({'error': code, 'message': str(message)}, 403)

        registration, error = self._resolve_registration(
            session,
            registration_token=payload.get('registration_token'),
            registration_id=payload.get('registration_id'),
        )
        if error:
            code, message = error
            return self._json({'error': code, 'message': str(message)}, 404)

        result = self._capture(
            session,
            registration,
            client_scan_uuid=payload.get('client_scan_uuid'),
            note=payload.get('note'),
            score=payload.get('score'),
        )
        return self._json(result)

    @http.route('/event_lead_scan/api/bulk',
                type='http', auth='public', methods=['POST'],
                csrf=False)
    def bulk(self, **kw):
        """Accept a queued batch of scans from the offline mode (D4)."""
        payload = self._payload(kw)
        session, error = self._get_session(payload.get('session_token'))
        if error:
            code, message = error
            return self._json({'error': code, 'message': str(message)}, 403)

        results = []
        for item in payload.get('scans', []):
            registration, err = self._resolve_registration(
                session,
                registration_token=item.get('registration_token'),
                registration_id=item.get('registration_id'),
            )
            if err:
                code, message = err
                results.append({
                    'client_scan_uuid': item.get('client_scan_uuid'),
                    'ok': False,
                    'error': code,
                    'message': str(message),
                })
                continue
            try:
                outcome = self._capture(
                    session,
                    registration,
                    client_scan_uuid=item.get('client_scan_uuid'),
                    note=item.get('note'),
                    score=item.get('score'),
                )
                outcome['ok'] = True
                results.append(outcome)
            except Exception as exc:  # noqa: BLE001 - report, do not crash
                _logger.exception('Bulk scan failed for %s', item)
                results.append({
                    'client_scan_uuid': item.get('client_scan_uuid'),
                    'ok': False,
                    'error': 'server_error',
                    'message': str(exc),
                })
        return self._json({'results': results,
                           'lead_count': session.lead_count})

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------
    def _payload(self, kw):
        """Accept both JSON bodies and form-encoded posts."""
        if request.httprequest.data:
            try:
                return json.loads(request.httprequest.data.decode('utf-8'))
            except (ValueError, UnicodeDecodeError):
                pass
        return kw

    def _capture(self, session, registration, client_scan_uuid=None,
                 note=None, score=None):
        """Create or update the lead for one scan. Returns a result dict."""
        Lead = request.env['crm.lead'].sudo()

        # D4 - idempotency: the same client reference is the same scan.
        if client_scan_uuid:
            existing = Lead.search(
                [('client_scan_uuid', '=', client_scan_uuid)], limit=1
            )
            if existing:
                return {
                    'lead_id': existing.id,
                    'already_scanned': True,
                    'idempotent_replay': True,
                    'lead_count': session.lead_count,
                }

        # D5 - duplicate rule: one lead per session and registration.
        existing = Lead.search([
            ('scan_session_id', '=', session.id),
            ('event_registration_id', '=', registration.id),
        ], limit=1)

        now = fields.Datetime.now()
        if existing:
            vals = {}
            if note is not None:
                vals['scan_note'] = note
            if score:
                vals['scan_score'] = score
            if vals:
                existing.write(vals)
            return {
                'lead_id': existing.id,
                'already_scanned': True,
                'idempotent_replay': False,
                'lead_count': session.lead_count,
            }

        partner = registration.partner_id
        lead_vals = {
            'name': _('%(event)s — %(attendee)s') % {
                'event': session.event_id.name,
                'attendee': partner.name or registration.name or _('Attendee'),
            },
            'partner_id': partner.id or False,
            'contact_name': partner.name or False,
            'email_from': partner.email or False,
            'phone': partner.phone or False,
            'scan_session_id': session.id,
            'event_registration_id': registration.id,
            'scan_note': note or False,
            'scan_score': score or False,
            'scan_time': now,
            'scanned_by_id': session.responsible_id.id,
            'client_scan_uuid': client_scan_uuid or False,
        }
        # Tag the lead with the event so it is findable in CRM.
        if session.event_id.name:
            lead_vals['description'] = _(
                'Captured by scanning the attendee badge at %(event)s.'
            ) % {'event': session.event_id.name}

        lead = Lead.create(lead_vals)
        return {
            'lead_id': lead.id,
            'already_scanned': False,
            'idempotent_replay': False,
            'lead_count': session.lead_count,
        }

    # ------------------------------------------------------------------
    # Pages
    # ------------------------------------------------------------------
    @http.route('/event_lead_scan/scan/<string:token>',
                type='http', auth='public', website=True, csrf=False)
    def scan_app(self, token, **kw):
        """The mobile scanner. No Odoo login required (D3)."""
        session, error = self._get_session(token, require_open=False)
        if error:
            code, message = error
            return request.render(
                'event_lead_scan.scan_error',
                {'error_code': code, 'error_message': str(message)},
            )
        return request.render('event_lead_scan.scan_app', {
            'session': session,
            'session_token': token,
        })

    @http.route('/event_lead_scan/badge/<string:token>',
                type='http', auth='public', website=True, csrf=False)
    def badge_qr(self, token, **kw):
        """Portal fallback: display the badge QR for a registration (D2)."""
        registration = request.env['event.registration'].sudo().search(
            [('scan_token', '=', token)], limit=1
        )
        if not registration:
            return request.not_found()
        return request.render('event_lead_scan.badge_qr', {
            'registration': registration,
            'scan_token': token,
        })
