let currentFilename = '';  // 현재 선택된 파일 이름 저장

// 파일 선택 시 자동으로 업로드
document.getElementById('wordFile').addEventListener('change', async function(event) {
    const fileInput = event.target;
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    // 파일 업로드 경로를 '/files/upload'로 변경
    const response = await fetch('/files/upload', {
        method: 'POST',
        body: formData
    });

    if (response.ok) {
        alert('File uploaded successfully');
        loadUploadedFiles();  // 파일 목록 다시 로드
    } else {
        alert('Failed to upload file');
    }
});

// 업로드된 파일 목록을 불러오는 함수
async function loadUploadedFiles() {
    const response = await fetch('/files/uploaded_files');
    const data = await response.json();
    const fileList = document.getElementById('fileList');
    fileList.innerHTML = '';  // 기존 목록 초기화

    data.files.forEach(file => {
        const listItem = document.createElement('li');
        listItem.innerHTML = `
            <span onclick="loadFileContent('${file.filename}')" class="file-item">${file.filename} (Uploaded on: ${file.upload_time})</span>
            <button onclick="renameFilePrompt('${file.filename}')">Rename</button>
            <button onclick="deleteFile('${file.filename}')">Delete</button>
        `;
        fileList.appendChild(listItem);
    });
}

// 선택한 파일의 내용을 불러와서 각 단락을 텍스트박스에 표시하는 함수
async function loadFileContent(filename) {
    const encodedFilename = encodeURIComponent(filename);
    const response = await fetch(`/files/${encodedFilename}`);
    const data = await response.json();
    if (data.error) {
        alert('Error loading file content');
    } else {
        currentFilename = filename;
        const questionsContainer = document.getElementById('questionsContainer');
        questionsContainer.innerHTML = '';
        const saveButton = document.getElementById('saveButton');

        // 기업 이름 입력 부분 추가
        const companyLabel = document.createElement('label');
        companyLabel.textContent = '해당 기업 이름을 작성해주세요';
        const companyBox = document.createElement('input');
        companyBox.type = 'text';
        companyBox.id = '기업이름';
        companyBox.classList.add('company-box');
        companyBox.value = data.content.기업이름 || '';
        questionsContainer.appendChild(companyLabel);
        questionsContainer.appendChild(companyBox);

        // 지원 직무 입력 부분 추가
        const jobLabel = document.createElement('label');
        jobLabel.textContent = '지원 직무(업무,요구사항등 모두 포함)를 작성해주세요';
        const jobBox = document.createElement('textarea');
        jobBox.id = '지원직무';
        jobBox.classList.add('job-box');
        jobBox.value = data.content.지원직무 || '';
        questionsContainer.appendChild(jobLabel);
        questionsContainer.appendChild(jobBox);

        // 인재상 입력 부분 추가
        const talentLabel = document.createElement('label');
        talentLabel.textContent = '인재상을 작성해주세요';
        const talentBox = document.createElement('textarea');
        talentBox.id = '인재상';
        talentBox.classList.add('talent-box');
        talentBox.value = data.content.인재상 || '';
        questionsContainer.appendChild(talentLabel);
        questionsContainer.appendChild(talentBox);

        // 지원 시기 입력 부분 추가
        const periodLabel = document.createElement('label');
        periodLabel.textContent = '지원 시기를 작성해주세요';
        const periodBox = document.createElement('input');
        periodBox.type = 'text';
        periodBox.id = '지원시기';
        periodBox.classList.add('period-box');
        periodBox.value = data.content.지원시기 || '';
        questionsContainer.appendChild(periodLabel);

        // 각 질문에 대한 텍스트박스 추가
        Object.keys(data.content.에세이 || {}).forEach(key => {
            const label = document.createElement('label');
            label.textContent = key;
            const questionBox = document.createElement('textarea');
            questionBox.id = key;
            questionBox.value = data.content.에세이[key];
            questionBox.classList.add('question-box');
            questionsContainer.appendChild(label);
            questionsContainer.appendChild(questionBox);
        });

        saveButton.style.display = "block";
    }
}

// 파일 내용 저장 요청 함수
document.getElementById('saveButton').addEventListener('click', async function() {
    if (!currentFilename) {
        alert('No file selected to save.');
        return;
    }

    const content = {};
    document.querySelectorAll('#questionsContainer textarea, #questionsContainer input').forEach(input => {
        content[input.id] = input.value;
    });

    const response = await fetch('/files/save', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            filename: currentFilename,
            content: content
        })
    });

    if (response.ok) {
        alert('File saved successfully');
    } else {
        alert('Failed to save file');
    }
});

// 파일 삭제 요청 함수
async function deleteFile(filename) {
    if (confirm(`Are you sure you want to delete ${filename}?`)) {
        const formData = new FormData();
        formData.append('filename', filename);

        const response = await fetch('/files/delete', {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            alert('File deleted successfully');
            loadUploadedFiles();
            clearFileContent();
        } else {
            alert('Failed to delete file');
        }
    }
}

// 파일 이름 변경을 위한 프롬프트
function renameFilePrompt(oldFilename) {
    const newFilename = prompt("Enter new filename:", oldFilename);
    if (newFilename && newFilename !== oldFilename) {
        renameFile(oldFilename, newFilename);
    }
}

// 파일 이름 변경 요청
async function renameFile(oldFilename, newFilename) {
    const formData = new FormData();
    formData.append('old_filename', oldFilename);
    formData.append('new_filename', newFilename);

    const response = await fetch('/files/rename', {
        method: 'POST',
        body: formData
    });

    if (response.ok) {
        alert('File renamed successfully');
        loadUploadedFiles();
        clearFileContent();
    } else {
        alert('Failed to rename file');
    }
}

// Show File Content 영역의 내용을 모두 지우는 함수
function clearFileContent() {
    const questionsContainer = document.getElementById('questionsContainer');
    questionsContainer.innerHTML = '';
    const saveButton = document.getElementById('saveButton');
    saveButton.style.display = "none";
}

// 페이지 로드 시 업로드된 파일 목록 불러오기
window.onload = loadUploadedFiles;
