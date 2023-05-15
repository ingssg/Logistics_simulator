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

### todo park

#### ui

- 시뮬레이션 삭제시 차트 삭제 버그

#### simulator

멘토님 질문

셀에 하나하나 방향 넣는게 맞는건지
맵 구성은 어떻게 하는지

tempblocked 해결방법 (로봇이 다른 로봇과 충돌회피시 돌아가야 할 때)
충전셀 슈트셀 방향 맞워야 하나?

현재 상태
충전중인 로봇을 비켜가지 않는다. 이거는 충전셀가는길을 단방향으로 해야할듯
또는 charging프로퍼티를 넣는다 stopped와 비슷함
로봇이 앞에 있으면 계속 기다린다.

- traffic handle
    - 로봇 마주치면 한칸 물러나기? 직선구간에서는 애초에 에러가 없다
- pathfinding
    - map cache
    - if tempblocked appears
        - wait...?
- 시뮬레이션 두개 이상 시작할때 로봇 인스턴스 관리 문제
- 맵 캐싱
    - 캐싱은 가능한데, tempblocked는 어떻게 처리하는가?
- 로그 저장

만약 버퍼에 로봇이 가장 적은 워크스테이션으로 가야한다?

워크스테이션의 마지막 버퍼 찾기 함수를 dict[워크스테이션,버퍼리스트,로봇수] 이렇게 구성해야한다.

그리고 각각 워크스테이션에서 물건을 쥐어줄때마다 로봇수 -1 하고

마지막 버퍼에 로봇이 들어올때 로봇수 +1 해준다