# simulation program

simul.ui 파일 업데이트 하고 실행해주세요
</br>
</br>
**교체할 값(*)**
</br>
-line 513,521,531,541,551: **소요시간**
</br>
-line 514,523,533,543,553: **소요시간(시간당작업량)**
</br>
-line 515,525,535,545,555: **벨트로봇당 작업량**
</br>
-line 516,526,536,546,556: **덤프로봇당 작업량**
</br>
-line 574: **벨트로봇당 작업량**
</br>
-line 575: **덤프로봇당 작업량**
</br>
-line 595: **소요시간(시간당 작업량)**
</br>

</br>

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


