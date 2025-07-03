// Global variables for question functionality
let userAnswers = {};
let userFeedback = {};

// Global variable to track current page
window.currentPage = 1;

function escapeHTML(str) {
    if (typeof str !== 'string') return '';
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#039;');
}

function checkAnswerDynamic(input) {
    const questionContainer = input.closest('.question-container');
    const questionNumber = questionContainer.dataset.questionNumber;
    const correctAnswer = questionContainer.dataset.answer;
    const selectedAnswer = input.value;
    
    userAnswers[questionNumber] = selectedAnswer;
    
    const feedback = questionContainer.querySelector('.feedback');
    const correctMsg = feedback.querySelector('.correct-message');
    const incorrectMsg = feedback.querySelector('.incorrect-message');
    
    feedback.style.display = 'block';
    correctMsg.style.display = 'none';
    incorrectMsg.style.display = 'none';
    
    const isCorrect = selectedAnswer === correctAnswer;
    
    if (isCorrect) {
        correctMsg.style.display = 'block';
        userFeedback[questionNumber] = 'correct';
    } else {
        incorrectMsg.querySelector('.correct-answer').textContent = correctAnswer;
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
            selectedAnswer: selectedAnswer,
            correctAnswer: correctAnswer
        }
    });
    document.dispatchEvent(event);
}

// Function to reset individual question answer
function resetAnswerDynamic(btn) {
    const questionContainer = btn.closest('.question-container');
    const questionNumber = questionContainer.dataset.questionNumber;
    
    // Clear user answer and feedback for this question
    delete userAnswers[questionNumber];
    delete userFeedback[questionNumber];
    
    // Uncheck all radio buttons
    const radioButtons = questionContainer.querySelectorAll('input[type="radio"]');
    radioButtons.forEach(radio => {
        radio.checked = false;
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
    
    // Trigger custom event for external listeners
    const event = new CustomEvent('questionReset', {
        detail: {
            questionNumber: parseInt(questionNumber)
        }
    });
    document.dispatchEvent(event);
}

// Function to render a question dynamically
function renderQuestion(questionData, totalQuestions) {
    const questionArea = document.getElementById('question-area');
    if (!questionArea) return;
    
    // Convert choices from object to array if needed
    if (questionData.choices && !Array.isArray(questionData.choices)) {
        questionData.choices = Object.keys(questionData.choices).map(key => ({
            letter: key,
            text: questionData.choices[key]
        }));
    }

    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    const labelStyle = isDark ? ' style="color:#fff !important; opacity:1 !important; visibility:visible !important; filter:none !important;"' : '';
    const choiceStyle = isDark ? ' style="color:#fff !important; opacity:1 !important; visibility:visible !important; filter:none !important;"' : '';
    const choicesClass = 'choices';

    let html = '';
    html += `<div class=\"question-container\" data-page=\"${questionData.number}\" data-answer=\"${questionData.answer}\" data-question-number=\"${questionData.number}\">`;
    html += `<div class=\"question\">`;
    html += `<p><strong>Question ${questionData.number} of ${totalQuestions}</strong></p>`;
    html += `<p>${escapeHTML(questionData.text)}</p>`;
    html += `<div class=\"${choicesClass}\">`;
    
    questionData.choices.forEach(choice => {
        const checked = userAnswers[questionData.number] === choice.letter ? 'checked' : '';
        html += `<div class=\"choice\"${choiceStyle}>`;
        html += `<input type=\"radio\" name=\"q_${questionData.number}\" value=\"${choice.letter}\" id=\"q${questionData.number}${choice.letter}\" ${checked} onchange=\"checkAnswerDynamic(this)\">`;
        html += `<label for=\"q${questionData.number}${choice.letter}\"${labelStyle}>${choice.letter}) ${escapeHTML(choice.text)}</label>`;
        html += `</div>`;
    });
    
    html += `</div>`;
    html += `<div class=\"button-group\">`;
    html += `<button type=\"button\" class=\"reset-answer-btn\" onclick=\"resetAnswerDynamic(this)\" data-tooltip=\"Reset Answer\">`;
    html += `<span class=\"btn-icon\">↺</span>`;
    html += `</button>`;
    html += `</div>`;
    html += `<div class=\"feedback\" style=\"display: ${userFeedback[questionData.number] ? 'block' : 'none'};\">`;
    html += `<p class=\"correct-message\" style=\"display: ${userFeedback[questionData.number] === 'correct' ? 'block' : 'none'};\">✓ Correct!<br><span class='explanation'>${escapeHTML(questionData.explanation || '')}</span></p>`;
    html += `<p class=\"incorrect-message\" style=\"display: ${userFeedback[questionData.number] === 'incorrect' ? 'block' : 'none'};\">✗ Incorrect. The correct answer is: <span class=\"correct-answer\">${questionData.answer}</span><br><span class='explanation'>${escapeHTML(questionData.explanation || '')}</span></p>`;
    html += `</div>`;
    html += `</div>`;
    html += `</div>`;
    
    let indicatorHtml = '';
    if (questionData.indicator === 'out of syllabus') {
        indicatorHtml = `<div class="out-of-syllabus-banner">⚠️ Note: This question is marked as out of syllabus.</div>`;
    }
    questionArea.innerHTML = `
        ${indicatorHtml}
        ${html}
    `;
}

// Function to reset question state
function resetQuestionState() {
    userAnswers = {};
    userFeedback = {};
    
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
    
    // Reset status indicators if they exist
    document.querySelectorAll('.question-status').forEach(q => {
        q.classList.remove('correct', 'incorrect');
        q.removeAttribute('data-answered');
        q.removeAttribute('data-was-correct');
    });
}

// Function to get current answers
function getCurrentAnswers() {
    return userAnswers;
}

// Function to get current feedback
function getCurrentFeedback() {
    return userFeedback;
}

// Function to check if all questions are answered
function areAllQuestionsAnswered(totalQuestions) {
    return Object.keys(userAnswers).length === totalQuestions;
}

// Function to calculate score
function calculateScore(totalQuestions) {
    let score = 0;
    for (let i = 1; i <= totalQuestions; i++) {
        if (userFeedback[i] === 'correct') {
            score++;
        }
    }
    return score;
}

// Function to render the current question page
window.renderCurrentPage = function() {
  if (typeof renderQuestionPage === 'function') {
    renderQuestionPage(window.currentPage);
  }
};

// Re-render when the theme changes
window.addEventListener('themeChanged', window.renderCurrentPage);

// Re-render after DOMContentLoaded to ensure everything is ready
// (Small delay to allow theme and data to be set)
document.addEventListener('DOMContentLoaded', function() {
  setTimeout(window.renderCurrentPage, 50);
}); 