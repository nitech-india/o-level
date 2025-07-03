function escapeHTML(str) {
    if (typeof str !== 'string') return '';
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#039;');
}

// Render a match-together question in the #question-area
function renderMatchTogetherQuestion(question, totalQuestions) {
    const questionArea = document.getElementById('question-area');
    if (!questionArea) return;

    let indicatorHtml = '';
    if (question.indicator === 'out of syllabus') {
        indicatorHtml = `<div class=\"out-of-syllabus-banner\">⚠️ Note: This question is marked as out of syllabus.</div>`;
    }

    // Build the HTML for the match question dynamically
    let html = `
    <div class="question-container match-question-container" data-page="${question.number}" data-question-number="${question.number}">
        <div class="button-group">
            <button type="button" class="check-match-btn" data-tooltip="Check Answer">
                <span class="btn-icon check">✔</span>
            </button>
            <button type="button" class="reset-answer-btn" onclick="resetMatchAnswerDynamic(this)" data-tooltip="Reset Answer">
                <span class="btn-icon reset">↺</span>
            </button>
        </div>
        <div class="question">
            ${indicatorHtml}
            <p><strong>Question ${question.number} of ${totalQuestions}</strong></p>
            <p>${escapeHTML(question.text)}</p>
            <div class="match-choices-dnd">
                <div class="match-left-dnd" id="match-left-dnd"></div>
                <div class="match-right-dnd" id="match-right-dnd"></div>
            </div>
            <div class="feedback" style="display: none;">
                <p class="correct-message" style="display: none;">✓ Correct! <span class="explanation">${escapeHTML(question.explanation || '')}</span></p>
                <p class="incorrect-message" style="display: none;">✗ Incorrect. The correct matches are shown above.<br><span class="explanation">${escapeHTML(question.explanation || '')}</span></p>
            </div>
        </div>
    </div>
    <style>
        .match-question-container { 
            margin-bottom: 20px; 
            padding: 20px; 
            border: 1px solid var(--md-outline, #ddd); 
            border-radius: 5px; 
            background: var(--md-surface, #fff);
            color: var(--md-on-surface, #212121);
            transition: border-color 0.3s, background-color 0.3s, color 0.3s;
        }
        body[data-theme="dark"] .match-question-container {
            background: var(--md-surface, #121212);
            color: var(--md-on-surface, #ffffff);
            border-color: var(--md-outline, #424242);
        }
        .match-choices-dnd { display: flex; gap: 40px; margin-bottom: 15px; }
        .match-left-dnd { display: flex; flex-direction: column; gap: 18px; }
        .match-item-dnd { display: flex; align-items: center; gap: 16px; margin-bottom: 8px; }
        .match-label { 
            font-size: 15px; 
            padding: 8px 12px; 
            background: var(--md-surface-container, #f8f9fa); 
            color: var(--md-on-surface, #212121); 
            border-radius: 4px; 
            min-width: 120px; 
            transition: background-color 0.3s, color 0.3s;
        }
        body[data-theme="dark"] .match-label {
            background: var(--md-surface-container, #1e1e1e);
            color: var(--md-on-surface, #ffffff);
        }
        .drop-zone { 
            min-width: 140px; 
            min-height: 32px; 
            border: 2px dashed var(--md-outline, #bbb); 
            border-radius: 4px; 
            background: var(--md-surface-container-high, #f4f4f4); 
            color: var(--md-on-surface, #212121);
            display: flex; 
            align-items: center; 
            padding: 4px 8px; 
            transition: border-color 0.2s, background-color 0.3s, color 0.3s; 
        }
        body[data-theme="dark"] .drop-zone {
            background: var(--md-surface-container-high, #2d2d2d);
            border-color: var(--md-outline, #555);
            color: var(--md-on-surface, #ffffff);
        }
        .drop-zone.over { 
            border-color: var(--md-primary, #007bff); 
            background: var(--md-primary-container, #e3f0ff); 
        }
        body[data-theme="dark"] .drop-zone.over {
            background: var(--md-primary-container, #1a237e);
        }
        .match-right-dnd { display: flex; flex-direction: column; gap: 12px; }
        .draggable-option { 
            padding: 8px 12px; 
            background: var(--md-surface-container, #e9ecef); 
            color: var(--md-on-surface, #212121);
            border-radius: 4px; 
            border: 1px solid var(--md-outline, #ccc); 
            cursor: grab; 
            user-select: none; 
            font-size: 15px; 
            margin-bottom: 4px; 
            transition: background 0.2s, border 0.2s, color 0.3s; 
        }
        body[data-theme="dark"] .draggable-option {
            background: var(--md-surface-container, #1e1e1e);
            color: var(--md-on-surface, #ffffff);
            border-color: var(--md-outline, #444);
        }
        .draggable-option.dragging { 
            opacity: 0.5; 
            border: 2px solid var(--md-primary, #007bff); 
        }
        .feedback { 
            margin-top: 15px; 
            padding: 12px; 
            border-radius: 4px; 
            background-color: var(--md-primary-container, #f0f4ff);
            color: var(--md-on-primary-container, #000000);
            transition: background-color 0.3s, color 0.3s;
        }
        body[data-theme="dark"] .feedback {
            background-color: var(--md-primary-container, #1a237e);
            color: var(--md-on-primary-container, #ffffff);
        }
        .correct-message { 
            color: var(--md-success, #155724); 
            font-weight: 500; 
            transition: color 0.3s;
        }
        body[data-theme="dark"] .correct-message {
            color: var(--md-success, #81c784);
        }
        .incorrect-message { 
            color: var(--md-error, #721c24); 
            font-weight: 500; 
            transition: color 0.3s;
        }
        body[data-theme="dark"] .incorrect-message {
            color: var(--md-error, #e57373);
        }
        .correct { 
            background-color: var(--md-success-container, #d4edda) !important; 
            transition: background-color 0.3s;
        }
        body[data-theme="dark"] .correct {
            background-color: var(--md-success-container, #1b5e20) !important;
        }
        .incorrect { 
            background-color: var(--md-error-container, #f8d7da) !important; 
            transition: background-color 0.3s;
        }
        body[data-theme="dark"] .incorrect {
            background-color: var(--md-error-container, #b71c1c) !important;
        }
    </style>
    `;

    questionArea.innerHTML = html;
    
    // Populate the left and right columns and set up drag-and-drop
    renderMatchOptions(question);
    setupDragAndDrop(question);

    // Restore feedback if it exists and disable check button
    const feedback = document.querySelector('.feedback');
    const qContainer = document.querySelector('.question-container');
    const checkBtn = document.querySelector('.check-match-btn');

    if (userFeedback[question.number]) {
        if (userFeedback[question.number] === 'correct') {
            feedback.style.display = 'block';
            feedback.querySelector('.correct-message').style.display = 'block';
            qContainer.classList.add('correct');
        } else if (userFeedback[question.number] === 'incorrect') {
            feedback.style.display = 'block';
            feedback.querySelector('.incorrect-message').style.display = 'block';
            qContainer.classList.add('incorrect');
        }
        checkBtn.disabled = true;
    }
}

function renderMatchOptions(question) {
    const leftCol = document.getElementById('match-left-dnd');
    const rightCol = document.getElementById('match-right-dnd');
    leftCol.innerHTML = '';
    rightCol.innerHTML = '';

    const savedAnswers = userAnswers[question.number];
    const allRightOptions = question.choices.map(pair => pair.right);
    let usedRightOptions = [];

    // Render left column and populate drop zones if state is saved
    question.choices.forEach((pair, idx) => {
        const item = document.createElement('div');
        item.className = 'match-item-dnd';
        item.setAttribute('data-index', idx);
        
        let dropZoneHtml = `<div class="drop-zone" data-index="${idx}">`;
        if (savedAnswers && savedAnswers[idx]) {
            const savedValue = savedAnswers[idx];
            dropZoneHtml += `<div class="draggable-option" draggable="true" data-value="${escapeHTML(savedValue)}">${escapeHTML(savedValue)}</div>`;
            usedRightOptions.push(savedValue);
        }
        dropZoneHtml += '</div>';
        
        item.innerHTML = `<span class="match-label">${escapeHTML(pair.left)}</span>${dropZoneHtml}`;
        leftCol.appendChild(item);
    });

    // Render right column with remaining/shuffled options
    let rightOptionsToShow;
    if (savedAnswers) {
        rightOptionsToShow = allRightOptions.filter(opt => !usedRightOptions.includes(opt));
    } else {
        rightOptionsToShow = [...allRightOptions];
        shuffleArray(rightOptionsToShow);
    }
    
    rightOptionsToShow.forEach(right => {
        const opt = document.createElement('div');
        opt.className = 'draggable-option';
        opt.setAttribute('draggable', 'true');
        opt.setAttribute('data-value', escapeHTML(right));
        opt.textContent = escapeHTML(right);
        rightCol.appendChild(opt);
    });
}

function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
}

function setupDragAndDrop(question) {
    const options = document.querySelectorAll('.draggable-option');
    const dropZones = document.querySelectorAll('.drop-zone');
    let dragged = null;

    options.forEach(option => {
        option.addEventListener('dragstart', (e) => {
            dragged = option;
            option.classList.add('dragging');
            setTimeout(() => option.style.display = 'none', 0);
        });
        option.addEventListener('dragend', (e) => {
            option.classList.remove('dragging');
            option.style.display = '';
        });
    });

    dropZones.forEach(zone => {
        zone.addEventListener('dragover', (e) => {
            e.preventDefault();
            zone.classList.add('over');
        });
        zone.addEventListener('dragleave', (e) => {
            zone.classList.remove('over');
        });
        zone.addEventListener('drop', (e) => {
            e.preventDefault();
            zone.classList.remove('over');
            if (dragged) {
                // Remove any existing option in this drop zone
                if (zone.firstChild) {
                    document.querySelector('.match-right-dnd').appendChild(zone.firstChild);
                }
                zone.appendChild(dragged);
                dragged = null;
            }
        });
    });

    // Allow returning option to the right column
    const rightCol = document.querySelector('.match-right-dnd');
    rightCol.addEventListener('dragover', (e) => {
        e.preventDefault();
    });
    rightCol.addEventListener('drop', (e) => {
        e.preventDefault();
        if (dragged) {
            rightCol.appendChild(dragged);
            dragged = null;
        }
    });

    // Check answer button
    document.querySelector('.check-match-btn').addEventListener('click', () => {
        checkMatchAnswerDnd(question);
    });
}

function checkMatchAnswerDnd(question) {
    const dropZones = document.querySelectorAll('.drop-zone');
    let userAnswersForQuestion = [];
    let allFilled = true;
    dropZones.forEach(zone => {
        if (zone.firstChild && zone.firstChild.classList.contains('draggable-option')) {
            userAnswersForQuestion.push(zone.firstChild.getAttribute('data-value'));
        } else {
            allFilled = false;
            userAnswersForQuestion.push(null);
        }
    });

    // Show warning if not all filled
    const questionContainer = document.querySelector('.question-container');
    const buttonGroup = questionContainer.querySelector('.button-group');
    let warning = questionContainer.querySelector('.check-warning');
    if (!warning) {
        warning = document.createElement('div');
        warning.className = 'check-warning';
        buttonGroup.insertAdjacentElement('afterend', warning);
    }
    if (!allFilled) {
        warning.textContent = 'Please match all items before checking your answer.';
        warning.style.display = 'block';
        return;
    } else {
        warning.textContent = '';
        warning.style.display = 'none';
    }

    // Save user's answers
    userAnswers[question.number] = userAnswersForQuestion;

    let isCorrect = true;
    for (let i = 0; i < question.answer.length; i++) {
        if (userAnswersForQuestion[i] !== question.answer[i]) {
            isCorrect = false;
            break;
        }
    }

    // Save feedback state
    userFeedback[question.number] = isCorrect ? 'correct' : 'incorrect';

    const feedback = document.querySelector('.feedback');
    const qContainer = document.querySelector('.question-container');
    
    qContainer.classList.remove('correct', 'incorrect');

    if (isCorrect) {
        feedback.style.display = 'block';
        feedback.querySelector('.correct-message').style.display = 'block';
        feedback.querySelector('.incorrect-message').style.display = 'none';
        qContainer.classList.add('correct');
    } else {
        feedback.style.display = 'block';
        feedback.querySelector('.correct-message').style.display = 'none';
        feedback.querySelector('.incorrect-message').style.display = 'block';
        qContainer.classList.add('incorrect');
    }

    // Disable button after checking
    document.querySelector('.check-match-btn').disabled = true;

    // Dispatch event for progress sidebar
    const event = new CustomEvent('questionAnswered', {
        detail: {
            questionNumber: question.number,
            isCorrect: isCorrect
        }
    });
    document.dispatchEvent(event);
}

// Function to reset individual match-together question
function resetMatchAnswerDynamic(btn) {
    const questionContainer = btn.closest('.question-container');
    const questionNumber = questionContainer.dataset.questionNumber;
    
    // Clear user answer and feedback for this question
    delete userAnswers[questionNumber];
    delete userFeedback[questionNumber];
    
    // Clear all drop zones
    const dropZones = questionContainer.querySelectorAll('.drop-zone');
    dropZones.forEach(zone => {
        if (zone.firstChild && zone.firstChild.classList.contains('draggable-option')) {
            document.querySelector('.match-right-dnd').appendChild(zone.firstChild);
        }
    });
    
    // Hide feedback
    const feedback = questionContainer.querySelector('.feedback');
    if (feedback) {
        feedback.style.display = 'none';
    }
    
    // Remove correct/incorrect styling
    questionContainer.classList.remove('correct', 'incorrect');
    
    // Re-enable check button
    const checkBtn = questionContainer.querySelector('.check-match-btn');
    if (checkBtn) {
        checkBtn.disabled = false;
    }
    
    // Reset status indicator if it exists
    const statusIndicator = document.querySelector(`.question-status[data-question="${questionNumber}"]`);
    if (statusIndicator) {
        statusIndicator.classList.remove('correct', 'incorrect');
        statusIndicator.removeAttribute('data-answered');
        statusIndicator.removeAttribute('data-was-correct');
        if (typeof updateProgress === 'function') {
            updateProgress();
        }
    }
    
    // Hide warning if present
    const warning = questionContainer.querySelector('.check-warning');
    if (warning) {
        warning.textContent = '';
        warning.style.display = 'none';
    }
    
    // Trigger custom event for external listeners
    const event = new CustomEvent('questionReset', {
        detail: {
            questionNumber: parseInt(questionNumber)
        }
    });
    document.dispatchEvent(event);
}

// Renamed to avoid conflicts. This function might be needed to reset view-specific things on a quiz reset.
function resetMatchQuestionView() {
    // The global reset clears userAnswers/userFeedback. Re-rendering the question
    // will now correctly display it in its initial state.
    // Specific view-only logic could be added here if needed in the future.
} 