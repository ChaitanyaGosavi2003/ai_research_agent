from flask import Blueprint, render_template, redirect, url_for, g, request, flash, session, Response, jsonify, current_app
from routes.auth import login_required
from database import get_db
import services.ai_service as ai_service
import services.pdf_service as pdf_service
import sqlite3
import json
import time

bp = Blueprint('agent', __name__, url_prefix='/agent')

@bp.route('/')
@login_required
def index():
    search_id = request.args.get('id')
    db = get_db()
    
    report = None
    chat_history = []
    
    if search_id:
        # Load existing search and report
        search = db.execute(
            'SELECT * FROM searches WHERE id = ? AND user_id = ?',
            (search_id, g.user['id'])
        ).fetchone()
        
        if search:
            report = db.execute(
                'SELECT * FROM reports WHERE search_id = ?',
                (search_id,)
            ).fetchone()
            
            chat_history = db.execute(
                'SELECT role, content FROM chat_messages WHERE search_id = ? ORDER BY created_at ASC',
                (search_id,)
            ).fetchall()
            
            chat_history = [dict(row) for row in chat_history]
            
            if report:
                report = dict(report)
        else:
            flash("Report not found or access denied.", "error")
            return redirect(url_for('dashboard.index'))
            
    return render_template(
        'agent.html',
        search_id=search_id,
        search=search if search_id else None,
        report=report,
        chat_history=chat_history
    )

@bp.route('/run')
@login_required
def run_agent():
    topic = request.args.get('topic', '').strip()
    if not topic:
        return jsonify({"status": "error", "message": "Topic is required"}), 400

    api_key = current_app.config['GEMINI_API_KEY']
    db_path = current_app.config['DATABASE']
    user_id = session['user_id']

    def event_stream():
        # Establish individual DB connection for streaming generator
        db = sqlite3.connect(db_path)
        db.row_factory = sqlite3.Row
        
        # Save initial search record
        cursor = db.cursor()
        cursor.execute(
            'INSERT INTO searches (user_id, topic) VALUES (?, ?)',
            (user_id, topic)
        )
        search_id = cursor.lastrowid
        db.commit()

        # Step helper function to stream status
        def yield_status(step, status, message, data=None):
            payload = {
                "step": step,
                "status": status,
                "message": message,
                "search_id": search_id
            }
            if data:
                payload["data"] = data
            return f"data: {json.dumps(payload)}\n\n"

        try:
            # Step 1: Understand query
            yield time.sleep(0.5) or yield_status(1, "started", "Analyzing and clarifying query parameters...")
            time.sleep(0.8) # Simulate processing
            yield yield_status(1, "completed", f"Topic understood: {topic}")

            # Step 2: Generate detailed explanation
            yield yield_status(2, "started", "Generating comprehensive technical explanation...")
            explanation = ai_service.generate_explanation(topic, api_key)
            yield yield_status(2, "completed", "Explanation generation complete.", {"explanation": explanation})

            # Step 3: Generate key points
            yield yield_status(3, "started", "Extracting primary takeaways and key concepts...")
            key_points = ai_service.generate_key_points(topic, explanation, api_key)
            yield yield_status(3, "completed", "Key takeaways extracted.", {"key_points": key_points})

            # Step 4: Generate interview questions
            yield yield_status(4, "started", "Crafting interview preparation questions and answers...")
            interview_questions = ai_service.generate_interview_questions(topic, explanation, api_key)
            yield yield_status(4, "completed", "Interview preparation module created.", {"interview_questions": interview_questions})

            # Step 5: Generate MCQ quiz
            yield yield_status(5, "started", "Building custom multiple-choice assessment...")
            quiz = ai_service.generate_quiz(topic, explanation, api_key)
            yield yield_status(5, "completed", "Assessment quiz compiled.", {"quiz": quiz})

            # Step 6: Generate summary
            yield yield_status(6, "started", "Drafting executive summary...")
            summary = ai_service.generate_summary(topic, explanation, api_key)
            yield yield_status(6, "completed", "Executive summary created.", {"summary": summary})

            # Step 7: Generate learning roadmap
            yield yield_status(7, "started", "Designing strategic learning roadmap...")
            roadmap = ai_service.generate_roadmap(topic, explanation, api_key)
            yield yield_status(7, "completed", "Learning roadmap finalized.", {"roadmap": roadmap})

            # Step 8: Suggest useful references
            yield yield_status(8, "started", "Collecting external reference links and books...")
            references_data = ai_service.generate_references(topic, explanation, api_key)
            yield yield_status(8, "completed", "References compiled successfully.", {"references_data": references_data})

            # Save full report
            cursor.execute('''
                INSERT INTO reports (search_id, explanation, key_points, interview_questions, quiz, summary, roadmap, references_data)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (search_id, explanation, key_points, interview_questions, quiz, summary, roadmap, references_data))
            db.commit()

            yield yield_status(8, "finished", "All steps completed! Rendering report now.")

        except Exception as e:
            # Yield error event
            error_msg = f"Agent failed during execution: {str(e)}"
            yield f"data: {json.dumps({'step': 0, 'status': 'error', 'message': error_msg})}\n\n"
        finally:
            db.close()

    return Response(event_stream(), mimetype='text/event-stream')

@bp.route('/chat', methods=['POST'])
@login_required
def chat():
    data = request.get_json() or {}
    search_id = data.get('search_id')
    message = data.get('message', '').strip()
    
    if not search_id or not message:
        return jsonify({"status": "error", "message": "Missing search ID or message"}), 400
        
    db = get_db()
    
    # Verify search ownership
    search = db.execute(
        'SELECT * FROM searches WHERE id = ? AND user_id = ?',
        (search_id, g.user['id'])
    ).fetchone()
    
    if not search:
        return jsonify({"status": "error", "message": "Search context not found"}), 404
        
    # Get report details as context
    report = db.execute(
        'SELECT explanation, summary FROM reports WHERE search_id = ?',
        (search_id,)
    ).fetchone()
    
    context = ""
    if report:
        context = f"Explanation: {report['explanation']}\nSummary: {report['summary']}"
        
    # Get previous chat history
    raw_history = db.execute(
        'SELECT role, content FROM chat_messages WHERE search_id = ? ORDER BY created_at ASC',
        (search_id,)
    ).fetchall()
    
    chat_history = [{"role": row["role"], "content": row["content"]} for row in raw_history]
    
    # Save user message
    db.execute(
        'INSERT INTO chat_messages (search_id, role, content) VALUES (?, ?, ?)',
        (search_id, 'user', message)
    )
    db.commit()
    
    # Get Gemini response
    api_key = current_app.config['GEMINI_API_KEY']
    reply = ai_service.answer_chat_followup(search['topic'], context, chat_history, message, api_key)
    
    # Save assistant response
    db.execute(
        'INSERT INTO chat_messages (search_id, role, content) VALUES (?, ?, ?)',
        (search_id, 'assistant', reply)
    )
    db.commit()
    
    return jsonify({
        "status": "success",
        "reply": reply
    })

@bp.route('/pdf/<int:search_id>')
@login_required
def download_pdf(search_id):
    db = get_db()
    
    # Verify search ownership
    search = db.execute(
        'SELECT * FROM searches WHERE id = ? AND user_id = ?',
        (search_id, g.user['id'])
    ).fetchone()
    
    if not search:
        flash("Search report not found.", "error")
        return redirect(url_for('dashboard.index'))
        
    report = db.execute(
        'SELECT * FROM reports WHERE search_id = ?',
        (search_id,)
    ).fetchone()
    
    if not report:
        flash("Report details are not generated yet.", "error")
        return redirect(url_for('dashboard.index'))
        
    # Generate PDF bytes
    report_dict = dict(report)
    pdf_bytes = pdf_service.generate_report_pdf(search['topic'], report_dict)
    
    # Create file response
    import io
    from flask import send_file
    
    # Safe filename
    safe_topic = "".join([c if c.isalnum() else "_" for c in search['topic']])
    filename = f"AI_Research_Report_{safe_topic}.pdf"
    
    return send_file(
        io.BytesIO(pdf_bytes),
        mimetype='application/pdf',
        as_attachment=True,
        download_name=filename
    )
