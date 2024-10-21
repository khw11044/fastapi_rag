// 질문 제출 함수
function sendQuestion(questionBox) {
    const questionText = questionBox.value.trim();
    if (questionText) {
        // 질문을 서버로 보내는 fetch 요청
        fetch('/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: questionText })
        })
        .then(response => response.json())
        .then(data => {
            // 기존 검색 결과 초기화
            const resultsContainer = document.getElementById('resultsContainer');
            resultsContainer.innerHTML = ''; // 기존 결과를 비웁니다.

            // 각 검색 결과마다 새로운 텍스트박스를 생성하여 결과 표시
            data.results.forEach((result, index) => {
                // 텍스트박스 생성
                const resultBox = document.createElement('textarea');
                resultBox.classList.add('result-box'); // 스타일링을 위한 클래스 추가
                resultBox.rows = 6; // 기본적으로 6줄로 설정
                resultBox.readOnly = true; // 수정 불가능

                // 검색 결과 내용을 텍스트박스에 넣음
                resultBox.value = `질문: ${result.metadata.question}\n\n` +
                                  `답변: ${result.content}\n\n` +
                                  `기업 이름: ${result.metadata.기업이름}\n` +
                                  `인재상: ${result.metadata.인재상}\n` +
                                  `지원시기: ${result.metadata.지원시기}\n` +
                                  `지원직무: ${result.metadata.지원직무}`;

                // 검색 결과 텍스트박스를 컨테이너에 추가
                resultsContainer.appendChild(resultBox);
            });
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
}

// + 버튼 클릭 시 질문 및 생성 텍스트박스를 추가하는 함수
document.getElementById('addButton').addEventListener('click', function() {
    const container = document.getElementById('questionsContainer');

    // 구분선 추가
    const separator = document.createElement('div');
    separator.classList.add('separator');
    container.appendChild(separator);

    // 질문 텍스트박스와 버튼을 같은 줄에 배치
    const questionWrapper = document.createElement('div');
    questionWrapper.classList.add('question-wrapper');

    const questionLabel = document.createElement('label');
    questionLabel.textContent = '질문:';

    const questionBox = document.createElement('textarea');
    questionBox.classList.add('question-box');
    questionBox.rows = 2;

    const sendButton = document.createElement('button');
    sendButton.innerHTML = '📤';  // 'send' 아이콘
    sendButton.classList.add('send-button');

    // 엔터 키 이벤트 처리
    questionBox.addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            sendQuestion(questionBox);
        }
    });

    sendButton.addEventListener('click', function() {
        sendQuestion(questionBox);
    });

    questionWrapper.appendChild(questionLabel);
    questionWrapper.appendChild(questionBox);
    questionWrapper.appendChild(sendButton);
    container.appendChild(questionWrapper);

    const contentLabel = document.createElement('label');
    contentLabel.textContent = '생성:';
    const contentBox = document.createElement('textarea');
    contentBox.classList.add('content-box');
    contentBox.rows = 6;

    container.appendChild(contentLabel);
    container.appendChild(contentBox);
});
