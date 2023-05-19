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

로봇 경로 설정할때 에러 체크
막혔을때 에러
blocked=[]
if temp in blocked:
error

멘토님 질문

지금은 일단 무한대기

에러가 났다는 것은 어떤 상황인지?
-> 길이 막혀서 못가는 상황
에러가 나면 어떻게 처리해야 하는가?
-> 에러난 주변 로봇들 전부 경로재설정

슈트셀과 충전셀에서 나올때 어떻게?
그러니까 슈트셀과 충전셀 길을 어떻게 짜야함?

일직선 상에서 마주보는경우? 어떻게? 피해야하나?
wait 타임아웃 설정? 
일직선이면 경로재설정하면 뒤돌아서 다시 갈길가긴함

priority 낮은 로봇이 경로재설정 코드 실행

경로 재설정 시
길 못찾을때 donextoperation assignmission 무한루프걸림

차지 중인 로봇 상대로는 무조건 비켜가고
마주보고 있는 경우
    우선도 체크
        물건 있는애가 우선
        물건 없으면 차지하는 애가 우선
        아니면 그냥 번호 높은 애가 우선
그러다 루트 못찾은 경우
    에러+1
    에러 핸들링? 어떤거를 해야 풀리지? 로봇들 멈췄을텐데

경로재설정은 멈춰있는 로봇에 대해서만? 충전셀에 멈춰있는거는 못기다리니까

셀에 하나하나 방향 넣는게 맞는건지
맵 구성은 어떻게 하는지

tempblocked 해결방법 (로봇이 다른 로봇과 충돌회피시 돌아가야 할 때)
충전셀 슈트셀 방향

엑셀로 데이터 저장하는거 어떻게 하면 좋을까요?

현재 상태
충전중인 로봇을 비켜가지 않는다. 이거는 충전셀가는길을 단방향으로 해야할듯
또는 charging프로퍼티를 넣는다 stopped와 비슷함
로봇이 앞에 있으면 계속 기다린다.

만약 버퍼에 로봇이 가장 적은 워크스테이션으로 가야한다?
워크스테이션의 마지막 버퍼 찾기 함수를 dict[워크스테이션,버퍼리스트,로봇수] 이렇게 구성해야한다.
그리고 각각 워크스테이션에서 물건을 쥐어줄때마다 로봇수 -1 하고
마지막 버퍼에 로봇이 들어올때 로봇수 +1 해준다

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
