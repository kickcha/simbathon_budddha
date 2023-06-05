const lotusElement = document.querySelector('.lotus');

// top 위치를 120px로 이동시키는 함수
function moveLotus() {
  lotusElement.style.transition = 'top 0.5s ease';
  lotusElement.style.top = '120px';
}

// 0.5초 후에 moveLotus 함수를 호출
setTimeout(moveLotus, 500);