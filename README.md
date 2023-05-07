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

### note park

할일

- 방향대로 맵 제너레이트
- simulator missionfinishhandler
    - 모든 도착지 - 배터리가 10미만이면 충전셀로 이동 미션 부여
    - 슈트 - 상위 클래스에서 큐가 제일 짧은 스테이션으로 이동 미션 부여
        - 만약 물건 놓고 돌아올때 어디를 목적지로 돌아와야함? 이게제일문제
    - 워크스테이션 - 다음 물건 올려주고 목적지 슈트로 이동 미션 부여
    - 큐 - 다음 큐로 이동 미션 부여
        - 다음 큐가 어디인지 알려줘야 하나?
- 결과테이블
    - 로봇
    - 에러수

일단 단방향 이거 고려해서 맵 만드는데 에러 시에는 어떻게 처리하는지?

맵 셀에 하나하나 방향 넣는게 맞는건지