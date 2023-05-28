# Capstone Project Sorting Simulator

## project

> Run simulation using map files created by previous map design program
>
> Use Dijkstra algorithm for simulation
>
> Compare simulation results in multiple data formats
</br>

> + PySide6, python
> + MariaDB, HediSQL

## RUN
**환경 설정**

DB 연결

pycharm 패키지 설치

## Result

## Process
***[1단계] 기본 기능 구현***

***[2단계] pyqt5를 PySide6로 수정***
</br>
-코드, ui파일 수정되었습니다.

**to-do-list**
</br>
-시뮬레이션 자체를 해당 코드에 합치기 </br>
-값 받아와서 시뮬레이션 실행 후, 실행 결과(시간) DB에 저장 </br>
-결과 페이지(결과표, 그래프) 구현 </br>
-UI </br>

**사용법 (주의)**

> + 삭제할 시뮬레이션 탭 반드시 클릭후, x표시 클릭해야 정확한 정보가 삭제됨
>
> + 시뮬레이션 정보 입력 후 시뮬레이션 보기 버튼 반드시 클릭해야 db 저장 가능
>
> + 현재코드는 시뮬레이션 총 5개까지 가능
</br>

#### ui

- 시뮬레이션 삭제시 차트 삭제 버그

#### simulator

맵 구성
    tomkins map 일단 비슷하게

escape 로직은 왔던 길 되돌아가기 후퇴함
123456 순서를 바꿔서 다시계산

---
할일
에러상황 처리 구현
    에러라고 판단된 그 로봇을 리스트 앞으로 옮김
    히스토리에서 하나씩 빼면서 움직일 수 있는지 확인


할수도있는일
버퍼 슈트 끼어들기
길이 1도없을때 생으로 evaluateroute -> tempblocked[바로앞에막힌곳]
박스 분포도
맵 캐싱 콜마다 tempblocked 빼는법

푸시해보고 컬러라벨이나 이런거 안맞는거 수정좀