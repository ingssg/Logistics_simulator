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

> Run simulation using map files created by previous map design program
>
> Use Dijkstra algorithm for simulation
>
> Compare simulation results in multiple data formats
</br>

> + pyqt5, pycharm
> + MariaDB, HediSQL

## RUN
**환경 설정**

DB 연결

pycharm 패키지 설치

## Result

## Process
***[1단계] 기본 기능 구현***

노션 구현-시뮬레이터-기본기능_설명.pdf 설명 올려두었습니다.

**사용법 (주의)**

> + 삭제할 시뮬레이션 탭 반드시 클릭후, x표시 클릭해야 정확한 정보가 삭제됨
>
> + 시뮬레이션 정보 입력 후 시뮬레이션 보기 버튼 반드시 클릭해야 db 저장 가능
>
> + 현재코드는 시뮬레이션 총 5개까지 가능
</br>

**to-do-list**

DB

+ line 88: DB-1) self.map에 db에서 맵파일 불러오기

+ line 125:  DB-2)속성별 색상 정보 db에서 가져와서 보여주기

+ line 178: DB-3) 입력된 프로젝트정보 db에 저장

+ line 334: DB-4) simul id가 simulname인 데이터 DB에서 삭제

+ line 342: DB-5) simul id가 'simulid'["simul"+str(move)]인 데이터의 simul id를 simulid-1["simul"+str(move-1)]로 변경

+ line 371,391,410,429,448: DB-6) 시뮬레이션 보기 클릭시, 시뮬 정보를 simulid인 db에 저장하기


시뮬레이션(알고리즘)

+ line 376, 396,415,434,453: 시뮬레이션-1) 시뮬레이션 화면 띄우기

+ line 462: 시뮬레이션-2) 시뮬레이션 화면 클래스 추가



기능

+ line 198:기능-1)시뮬레이션 탭(우선 5번 추가 단순 반복으로 구현, 문자열+숫자를 객체이름으로 사용하는 법 다시 시도)

+ line 329: 기능-2) (시뮬레이션보기 버튼 클릭 없이 삭제하기 위해->시뮬레이션 만들때 임의값 넣어줄지 말지)

+ result tab에 마침 버튼 추가
