from flask import Blueprint, render_template, redirect, url_for, g, request, flash, session, jsonify
from routes.auth import login_required
from database import get_db
import json

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@bp.route('/')
@login_required
def index():
    db = get_db()
    
    # Fetch recent searches
    recent_searches = db.execute('''
        SELECT s.id, s.topic, s.created_at, r.summary
        FROM searches s
        LEFT JOIN reports r ON s.id = r.search_id
        WHERE s.user_id = ?
        ORDER BY s.created_at DESC
        LIMIT 10
    ''', (g.user['id'],)).fetchall()

    # Calculate statistics
    total_searches = db.execute(
        'SELECT COUNT(*) FROM searches WHERE user_id = ?', (g.user['id'],)
    ).fetchone()[0]

    # Active Roadmaps count (represented by completed searches with roadmap generated)
    active_roadmaps = db.execute('''
        SELECT COUNT(r.id) 
        FROM reports r
        JOIN searches s ON r.search_id = s.id
        WHERE s.user_id = ? AND r.roadmap IS NOT NULL
    ''', (g.user['id'],)).fetchone()[0]

    # Fetch daily search metrics for chart (last 7 days)
    daily_searches = db.execute('''
        SELECT DATE(created_at) as search_date, COUNT(*) as count
        FROM searches
        WHERE user_id = ? AND created_at >= date('now', '-7 days')
        GROUP BY search_date
        ORDER BY search_date ASC
    ''', (g.user['id'],)).fetchall()

    chart_labels = []
    chart_data = []
    
    # Format database results for Chart.js
    import datetime
    today = datetime.date.today()
    last_7_days = [today - datetime.timedelta(days=i) for i in range(6, -1, -1)]
    
    search_counts = {row['search_date']: row['count'] for row in daily_searches}
    
    for d in last_7_days:
        date_str = d.strftime('%Y-%m-%d')
        chart_labels.append(d.strftime('%b %d'))
        chart_data.append(search_counts.get(date_str, 0))

    return render_template(
        'dashboard.html', 
        recent_searches=recent_searches,
        total_searches=total_searches,
        active_roadmaps=active_roadmaps,
        chart_labels=json.dumps(chart_labels),
        chart_data=json.dumps(chart_data)
    )

@bp.route('/settings/theme', methods=['POST'])
@login_required
def toggle_theme():
    data = request.get_json() or {}
    new_theme = data.get('theme', 'dark')
    if new_theme in ['light', 'dark']:
        session['theme'] = new_theme
        return jsonify({'status': 'success', 'theme': new_theme})
    return jsonify({'status': 'error', 'message': 'Invalid theme'}), 400

@bp.route('/settings/clear-history', methods=['POST'])
@login_required
def clear_history():
    db = get_db()
    db.execute('DELETE FROM searches WHERE user_id = ?', (g.user['id'],))
    db.commit()
    return jsonify({'status': 'success', 'message': 'Search history cleared successfully.'})
