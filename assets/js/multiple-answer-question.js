// Global variables for multiple-answer question functionality
// let multiUserAnswers = {}; // Will use global userAnswers
// let multiUserFeedback = {}; // Will use global userFeedback

function checkMultipleAnswerDynamic(btn) {
    const questionContainer = btn.closest('.question-container');
    const questionNumber = questionContainer.dataset.questionNumber;
    const correctAnswers = questionContainer.dataset.answer.split(',').map(a => a.trim());
    const checkboxes = questionContainer.querySelectorAll('input[type="checkbox"]');
    const selectedAnswers = Array.from(checkboxes)
        .filter(cb => cb.checked)
        .map(cb => cb.value);
    // Show warning if not enough selected
    let warning = questionContainer.querySelector('.check-warning');
    const buttonGroup = questionContainer.querySelector('.button-group');
    if (!warning) {
        warning = document.createElement('div');
        warning.className = 'check-warning';
        buttonGroup.insertAdjacentElement('afterend', warning);
    }
    if (selectedAnswers.length < correctAnswers.length) {
        warning.textContent = `Please select ${correctAnswers.length} choice${correctAnswers.length > 1 ? 's' : ''}.`;
        warning.style.display = 'block';
        return;
    } else {
        warning.textContent = '';
        warning.style.display = 'none';
    }
    userAnswers[questionNumber] = selectedAnswers;

    const feedback = questionContainer.querySelector('.feedback');
    const correctMsg = feedback.querySelector('.correct-message');
    const incorrectMsg = feedback.querySelector('.incorrect-message');

    feedback.style.display = 'block';
    correctMsg.style.display = 'none';
    incorrectMsg.style.display = 'none';

    // Compare arrays (order-insensitive)
    const isCorrect =
        selectedAnswers.length === correctAnswers.length &&
        selectedAnswers.every(ans => correctAnswers.includes(ans));

    if (isCorrect) {
        correctMsg.style.display = 'block';
        userFeedback[questionNumber] = 'correct';
    } else {
        incorrectMsg.querySelector('.correct-answer').textContent = correctAnswers.join(', ');
        incorrectMsg.style.display = 'block';
        userFeedback[questionNumber] = 'incorrect';
    }

    // Update question status if status indicator exists
    const statusIndicator = document.querySelector(`.question-status[data-question="${questionNumber}"]`);
    if (statusIndicator) {
        statusIndicator.classList.remove('correct', 'incorrect');
        statusIndicator.classList.add(isCorrect ? 'correct' : 'incorrect');
        // Only count as completed the first time
        if (!statusIndicator.dataset.answered) {
            statusIndicator.dataset.answered = 'true';
            if (typeof updateProgress === 'function') {
                updateProgress();
            }
        } else if (statusIndicator.dataset.wasCorrect === 'true' && !isCorrect) {
            if (typeof updateProgress === 'function') {
                updateProgress();
            }
        } else if (statusIndicator.dataset.wasCorrect === 'false' && isCorrect) {
            if (typeof updateProgress === 'function') {
                updateProgress();
            }
        }
        statusIndicator.dataset.wasCorrect = isCorrect;
    }

    // Trigger custom event for external listeners
    const event = new CustomEvent('questionAnswered', {
        detail: {
            questionNumber: parseInt(questionNumber),
            isCorrect: isCorrect,
            selectedAnswers: selectedAnswers,
            correctAnswers: correctAnswers
        }
    });
    document.dispatchEvent(event);
}

// Function to reset individual multiple-answer question
function resetMultipleAnswerDynamic(btn) {
    const questionContainer = btn.closest('.question-container');
    const questionNumber = questionContainer.dataset.questionNumber;
    
    // Clear user answer and feedback for this question
    delete userAnswers[questionNumber];
    delete userFeedback[questionNumber];
    
    // Uncheck all checkboxes
    const checkboxes = questionContainer.querySelectorAll('input[type="checkbox"]');
    checkboxes.forEach(checkbox => {
        checkbox.checked = false;
    });
    
    // Hide feedback
    const feedback = questionContainer.querySelector('.feedback');
    if (feedback) {
        feedback.style.display = 'none';
    }
    
    // Remove correct/incorrect styling
    questionContainer.classList.remove('correct', 'incorrect');
    
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

// Function to render a multiple-answer question dynamically
function renderMultipleAnswerQuestion(questionData, totalQuestions) {
    const questionArea = document.getElementById('question-area');
    if (!questionArea) return;

    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    const labelStyle = isDark ? ' style="color:#fff !important; opacity:1 !important; visibility:visible !important; filter:none !important;"' : '';
    const choiceStyle = isDark ? ' style="color:#fff !important; opacity:1 !important; visibility:visible !important; filter:none !important;"' : '';
    const choicesClass = 'choices';

    let html = '';
    let indicatorHtml = '';
    if (questionData.indicator === 'out of syllabus') {
        indicatorHtml = `<div class="out-of-syllabus-banner">⚠️ Note: This question is marked as out of syllabus.</div>`;
    }
    html += `<div class="question-container" data-page="${questionData.number}" data-answer="${questionData.answer.join(',')}" data-question-number="${questionData.number}">`;
    html += `<div class="button-group">`;
    html += `<button type="button" class="check-answer-btn" onclick="checkMultipleAnswerDynamic(this)" data-tooltip="Check Answer">`;
    html += `<span class="btn-icon check">✔</span>`;
    html += `</button>`;
    html += `<button type="button" class="reset-answer-btn" onclick="resetMultipleAnswerDynamic(this)" data-tooltip="Reset Answer">`;
    html += `<span class="btn-icon reset">↺</span>`;
    html += `</button>`;
    html += `</div>`;
    html += `<div class="question">`;
    html += `<p><strong>Question ${questionData.number} of ${totalQuestions}</strong></p>`;
    html += indicatorHtml;
    html += `<p>${escapeHTML(questionData.text)}</p>`;
    if (questionData.answer.length < questionData.choices.length) {
        html += `<div class="hint" style="color:var(--md-primary,#1976d2);font-weight:500;margin-bottom:8px;">Hint: Select ${questionData.answer.length} choices</div>`;
    }
    html += `<div class="${choicesClass}">`;

    questionData.choices.forEach(choice => {
        const checked = (userAnswers[questionData.number] || []).includes(choice.letter) ? 'checked' : '';
        html += `<div class="choice"${choiceStyle}>`;
        html += `<input type="checkbox" name="q_${questionData.number}" value="${choice.letter}" id="q${questionData.number}${choice.letter}" ${checked}>`;
        html += `<label for="q${questionData.number}${choice.letter}\"${labelStyle}>${choice.letter}) ${escapeHTML(choice.text)}</label>`;
        html += `</div>`;
    });

    html += `</div>`;
    html += `<div class="feedback" style="display: ${userFeedback[questionData.number] ? 'block' : 'none'};">`;
    html += `<p class="correct-message" style="display: ${userFeedback[questionData.number] === 'correct' ? 'block' : 'none'};">✓ Correct!<br><span class='explanation'>${escapeHTML(questionData.explanation || '')}</span></p>`;
    html += `<p class="incorrect-message" style="display: ${userFeedback[questionData.number] === 'incorrect' ? 'block' : 'none'};">✗ Incorrect. The correct answers are: <span class="correct-answer">${questionData.answer.join(', ')}</span><br><span class='explanation'>${escapeHTML(questionData.explanation || '')}</span></p>`;
    html += `</div>`;
    html += `</div>`;
    html += `</div>`;

    questionArea.innerHTML = html;
}

// Function to reset multiple-answer question state
/* function resetMultipleAnswerQuestionState() {
    multiUserAnswers = {};
    multiUserFeedback = {};
    const questions = document.querySelectorAll('.question-container');
    questions.forEach(q => {
        q.classList.remove('correct', 'incorrect');
        q.removeAttribute('data-answered');
        q.removeAttribute('data-was-correct');
        const feedback = q.querySelector('.feedback');
        if (feedback) {
            feedback.style.display = 'none';
        }
    });
    document.querySelectorAll('.question-status').forEach(q => {
        q.classList.remove('correct', 'incorrect');
        q.removeAttribute('data-answered');
        q.removeAttribute('data-was-correct');
    });
} */

// Helpers for state/score are no longer needed here as they would be duplicates
/* function getCurrentMultiAnswers() {
    return multiUserAnswers;
}
function getCurrentMultiFeedback() {
    return multiUserFeedback;
}
function areAllMultiQuestionsAnswered(totalQuestions) {
    return Object.keys(multiUserAnswers).length === totalQuestions;
}
function calculateMultiScore(totalQuestions) {
    let score = 0;
    for (let i = 1; i <= totalQuestions; i++) {
        if (multiUserFeedback[i] === 'correct') {
            score++;
        }
    }
    return score;
} */ 