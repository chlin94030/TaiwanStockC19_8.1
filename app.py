"""Alpha Radar V19.8.1 safe Cloud entrypoint.

A small, dependency-isolated landing page makes it possible to distinguish
Streamlit server/health-check failure from application-import failure. Full
V19.8 functionality loads only after an explicit click. No numerical module is
modified or imported for the first display.
"""
from __future__ import annotations

import importlib.metadata
import importlib.util
import os
from pathlib import Path
import platform
import sys
import traceback
from datetime import datetime, timezone

BASE = Path(__file__).resolve().parent
PREFIX = '[ALPHARADAR_BOOT]'


def log(stage, **values):
    value_text = ' '.join(f'{k}={v}' for k, v in values.items())
    print(f'{PREFIX} stage={stage} {value_text}', file=sys.stderr, flush=True)


def _error(stage, exc):
    ident = 'AR1981-' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '-' + stage
    print(f'[ALPHARADAR_BOOT_ERROR] id={ident} error={type(exc).__name__}',
          file=sys.stderr, flush=True)
    traceback.print_exception(type(exc), exc, exc.__traceback__, file=sys.stderr)
    return ident


def _version(name):
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return 'NOT_INSTALLED'


def _safe_page(st):
    st.set_page_config(page_title='Alpha Radar V19.8.1 | Safe start', page_icon='🛠️',
                       layout='centered', initial_sidebar_state='collapsed')
    st.title('Alpha Radar V19.8.1')
    st.success('Safe startup completed. The Streamlit frontend is responding.')
    st.caption('This page has not imported the stock model or downloaded historical data.')
    st.info('Choose "Open complete dashboard" to check the main app. If it fails, this page will show an error ID and preserve the full traceback in Cloud logs.')
    if st.button('Open complete dashboard', type='primary', key='ar1981_launch'):
        st.session_state['ar1981_mode'] = 'full'
        log('full_dashboard_requested')
        st.rerun()
    with st.expander('Environment details / Diagnostic'):
        st.write({'Python': platform.python_version(),
                  'Streamlit': _version('streamlit'),
                  'Runtime': sys.version.split()[0],
                  'Root sources': 'OK' if (BASE/'v19_ui.py').exists() else 'MISSING',
                  'Ranking core': 'OK' if (BASE/'v19_backtest.py').exists() else 'MISSING',
                  'Research CLI': 'OK' if (BASE/'research_lab.py').exists() else 'MISSING'})
        st.caption('For errors, open Manage app > Logs and search ALPHARADAR_BOOT_ERROR.')
    st.caption('Historical optimisation runs separately using research_lab.py; it is intentionally not an endless task on the free Cloud web worker.')
    log('safe_page_render_ok', python=platform.python_version(), st_version=_version('streamlit'))


def run():
    log('entry', python=platform.python_version())
    try:
        import streamlit as st
    except Exception as exc:
        _error('streamlit_import', exc)
        raise
    mode = st.session_state.get('ar1981_mode',
                                'safe' if os.getenv('ALPHARADAR_SAFE_START', '1') != '0'
                                else 'full')
    if mode != 'full':
        try:
            _safe_page(st)
        except Exception as exc:
            _error('safe_page', exc)
            raise
        return
    try:
        log('full_import_start')
        from v19_ui import main
        log('full_import_ok')
        main()
        log('full_render_ok')
    except Exception as exc:
        ident = _error('full_dashboard', exc)
        # Error display MUST NOT reveal cached market data or the user's Secrets.
        try:
            st.error('The full dashboard failed. The lightweight startup page is still available.')
            st.warning(f'Error ID: {ident} | Exception: {type(exc).__name__}')
            st.caption('Manage app > Logs > search ALPHARADAR_BOOT_ERROR for the traceback.')
            if st.button('Return to safe startup', key='ar1981_back'):
                st.session_state['ar1981_mode'] = 'safe'
                st.rerun()
        except Exception as diagnostic_exc:
            _error('error_renderer', diagnostic_exc)


if __name__ == '__main__':
    run()
