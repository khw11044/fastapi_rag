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
                resultBox.value = `질문: \n${result.metadata.question}\n\n` +
                                  `답변: \n${result.content}\n\n` +
                                  `기업 이름: ${result.metadata.기업이름}\n` +
                                  `지원시기: ${result.metadata.지원시기}\n` +
                                  `지원직무: ${result.metadata.지원직무}\n` + 
                                  `인재상: \n${result.metadata.인재상}`;

                // 검색 결과 텍스트박스를 컨테이너에 추가
                resultsContainer.appendChild(resultBox);
            });
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
}

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

    const sendButton = document.createElement('button');
    sendButton.textContent = '보내기';  // '보내기' 텍스트로 변경
    sendButton.classList.add('send-button');

    const questionBox = document.createElement('textarea');
    questionBox.classList.add('question-box');
    questionBox.rows = 2;

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

    // '질문:' 라벨과 질문 텍스트박스, 보내기 버튼을 같은 줄에 추가
    questionWrapper.appendChild(questionLabel);
    questionWrapper.appendChild(sendButton);   // 보내기 버튼 추가
    questionWrapper.appendChild(questionBox);  // 질문 텍스트박스 추가
    container.appendChild(questionWrapper);  // questionWrapper를 container에 추가

    const wordlimitLabel = document.createElement('label');
    wordlimitLabel.textContent = '글자수 제한:';
    const limitBox = document.createElement('textarea');
    limitBox.classList.add('limit-box');

    container.appendChild(wordlimitLabel);
    container.appendChild(limitBox);

    const contentLabel = document.createElement('label');
    contentLabel.textContent = '답변:';

    const genButton = document.createElement('button');
    genButton.textContent = '생성하기';  // '생성하기' 텍스트로 변경
    genButton.classList.add('gen-button');
    
    const contentBox = document.createElement('textarea');
    contentBox.classList.add('content-box');
    contentBox.rows = 6;

    genButton.addEventListener('click', function() {
        const companyName = document.getElementById('companyName').value;
        const talent = document.getElementById('talent').value;
        const job = document.getElementById('job').value;
        const limit = limitBox.value;
        const question = questionBox.value;  // 질문 텍스트 박스의 값
        
        // FastAPI에 POST 요청을 보내기
        fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                companyName: companyName, // 수정된 부분
                talent: talent,
                job: job,
                question: question,
                limit: limit,
            }),
        })
        .then(response => response.json())
        .then(data => {
            // '답변:' 텍스트 박스에 결과 표시
            contentBox.value = data.answer;
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

    container.appendChild(contentLabel);
    container.appendChild(genButton);
    container.appendChild(contentBox);
});
