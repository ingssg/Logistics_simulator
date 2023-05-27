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

만약 버퍼에 로봇이 가장 적은 워크스테이션으로 가야한다?
워크스테이션의 마지막 버퍼 찾기 함수를 dict[워크스테이션,버퍼리스트,로봇수] 이렇게 구성해야한다.
그리고 각각 워크스테이션에서 물건을 쥐어줄때마다 로봇수 -1 하고
마지막 버퍼에 로봇이 들어올때 로봇수 +1 해준다

메인 루프 
    123456
    클럭 맞춰야함
    3칸 booking 이동 -> 재설정/매클럭 마다 재설정
    대기 회전 이동이 전부 같음

    1클럭마다 한칸씩만 이동으로

맵 구성
    tomkins map 일단 비슷하게

escape 로직은 왔던 길 되돌아가기 후퇴함
123456 순서를 바꿔서 다시계산

---
할일
에러상황 처리 구현
    에러라고 판단된 그 로봇을 리스트 앞으로 옮김
    히스토리에서 하나씩 빼면서 움직일 수 있는지 확인

waitcount

simulationfinish 일때 버퍼에 로봇 모인거 에러상황으로 오인 해결
trackbuffers
workbufferdict

할수도있는일
버퍼 슈트 끼어들기 -> 이거왜됨??
길이 1도없을때 생으로 evaluateroute -> tempblocked[바로앞에막힌곳]
박스 분포도

멘토님 질문
예전 회의때 박스 목적지...?

지금 문제
waitcount가 계속 오르는데 에러가 안남
되감기 하다가 로봇이 겹침


에러 판단 조건
되감기?