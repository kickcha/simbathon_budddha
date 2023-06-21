var errorMessage = document.getElementById('error-message');

function showErrorMessage() {
  errorMessage.classList.add('show');

  setTimeout(function() {
    errorMessage.classList.remove('show');
  }, 3000); // 3초 후에 오류 메시지 숨김
}

document.getElementById('errortext').addEventListener('invalid', showErrorMessage);
