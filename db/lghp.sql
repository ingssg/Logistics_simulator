-- --------------------------------------------------------
-- 호스트:                          127.0.0.1
-- 서버 버전:                        10.7.6-MariaDB - mariadb.org binary distribution
-- 서버 OS:                        Win64
-- HeidiSQL 버전:                  11.3.0.6295
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- lghpdb 데이터베이스 구조 내보내기
CREATE DATABASE IF NOT EXISTS `lghpdb` /*!40100 DEFAULT CHARACTER SET utf8mb3 */;
USE `lghpdb`;

-- 테이블 lghpdb.buffer 구조 내보내기
CREATE TABLE IF NOT EXISTS `buffer` (
  `Buffer_ID` char(50) NOT NULL,
  `Grid_ID` char(10) DEFAULT NULL,
  `Cell_ID` char(30) DEFAULT NULL,
  `LocationX` int(11) DEFAULT NULL,
  `LocationY` int(11) DEFAULT NULL,
  `Buffer_Status` int(11) DEFAULT 1,
  PRIMARY KEY (`Buffer_ID`),
  KEY `FK__buffer_Grid_ID` (`Grid_ID`) USING BTREE,
  KEY `FK__buffer_Cell_ID` (`Cell_ID`),
  CONSTRAINT `FK__buffer_Cell_ID` FOREIGN KEY (`Cell_ID`) REFERENCES `cell` (`Cell_ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK__buffer_Grid_ID` FOREIGN KEY (`Grid_ID`) REFERENCES `grid` (`Grid_ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- 테이블 데이터 lghpdb.buffer:~2 rows (대략적) 내보내기
/*!40000 ALTER TABLE `buffer` DISABLE KEYS */;
/*!40000 ALTER TABLE `buffer` ENABLE KEYS */;

-- 테이블 lghpdb.cell 구조 내보내기
CREATE TABLE IF NOT EXISTS `cell` (
  `Cell_ID` char(30) NOT NULL,
  `Grid_ID` char(10) DEFAULT NULL,
  `CellStatus` int(11) DEFAULT 7,
  `Color` int(10) DEFAULT 0,
  `LocationX` int(11) DEFAULT NULL,
  `LocationY` int(11) DEFAULT NULL,
  `NorthDirection` int(11) DEFAULT 0,
  `SouthDirection` int(11) DEFAULT 0,
  `WestDirection` int(11) DEFAULT 0,
  `EastDirection` int(11) DEFAULT 0,
  `Robot_ID` char(10) DEFAULT NULL,
  PRIMARY KEY (`Cell_ID`),
  KEY `FK_cell_Robot_ID` (`Robot_ID`),
  KEY `FK_cell_Grid_ID` (`Grid_ID`),
  CONSTRAINT `FK_cell_Grid_ID` FOREIGN KEY (`Grid_ID`) REFERENCES `grid` (`Grid_ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK_cell_Robot_ID` FOREIGN KEY (`Robot_ID`) REFERENCES `robot` (`Robot_ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- 테이블 데이터 lghpdb.cell:~26 rows (대략적) 내보내기
/*!40000 ALTER TABLE `cell` DISABLE KEYS */;
/*!40000 ALTER TABLE `cell` ENABLE KEYS */;

-- 테이블 lghpdb.chargingstation 구조 내보내기
CREATE TABLE IF NOT EXISTS `chargingstation` (
  `CS_ID` char(30) NOT NULL DEFAULT '',
  `Cell_ID` char(30) DEFAULT NULL,
  `Grid_ID` char(10) DEFAULT NULL,
  `LocationX` int(11) DEFAULT NULL,
  `LocationY` int(11) DEFAULT NULL,
  `CS_Status` int(11) DEFAULT 1,
  `RobotDirection` int(11) DEFAULT NULL,
  `Robot_ID` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`CS_ID`),
  KEY `FK_chargingstation_Grid_ID` (`Grid_ID`) USING BTREE,
  KEY `FK_chargingstation_Cell_ID` (`Cell_ID`),
  CONSTRAINT `FK_chargingstation_Cell_ID` FOREIGN KEY (`Cell_ID`) REFERENCES `cell` (`Cell_ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK_chargingstation_Grid_ID` FOREIGN KEY (`Grid_ID`) REFERENCES `grid` (`Grid_ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- 테이블 데이터 lghpdb.chargingstation:~1 rows (대략적) 내보내기
/*!40000 ALTER TABLE `chargingstation` DISABLE KEYS */;
/*!40000 ALTER TABLE `chargingstation` ENABLE KEYS */;

-- 테이블 lghpdb.chute 구조 내보내기
CREATE TABLE IF NOT EXISTS `chute` (
  `Chute_ID` char(30) NOT NULL DEFAULT '',
  `Cell_ID` char(30) DEFAULT NULL,
  `Grid_ID` char(10) DEFAULT NULL,
  `LocationX` int(11) DEFAULT NULL,
  `LocationY` int(11) DEFAULT NULL,
  `RobotDirection` int(11) DEFAULT NULL,
  `Chute_Status` int(11) DEFAULT 1,
  `CurrentCnt` int(11) DEFAULT 0,
  `MaxCnt` int(11) DEFAULT NULL,
  PRIMARY KEY (`Chute_ID`),
  KEY `FK_chute_Grid_ID` (`Grid_ID`),
  KEY `FK_chute_Cell_ID` (`Cell_ID`),
  CONSTRAINT `FK_chute_Cell_ID` FOREIGN KEY (`Cell_ID`) REFERENCES `cell` (`Cell_ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK_chute_Grid_ID` FOREIGN KEY (`Grid_ID`) REFERENCES `grid` (`Grid_ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- 테이블 데이터 lghpdb.chute:~4 rows (대략적) 내보내기
/*!40000 ALTER TABLE `chute` DISABLE KEYS */;
/*!40000 ALTER TABLE `chute` ENABLE KEYS */;

-- 프로시저 lghpdb.createBuffer 구조 내보내기
DELIMITER //
CREATE PROCEDURE `createBuffer`(
	IN `myGrid_ID` VARCHAR(50),
	IN `myCell_ID` VARCHAR(50),
	IN `myBuffer_ID` VARCHAR(50)
)
    COMMENT '버퍼셀 생성 프로시저'
BEGIN

DECLARE X INT;
DECLARE Y INT;
SELECT cell.LocationX INTO X
FROM cell
WHERE cell.Cell_ID = myCell_ID;
SELECT cell.LocationY INTO Y
FROM cell
WHERE cell.Cell_ID = myCell_ID;

INSERT INTO buffer(Grid_ID, Cell_ID, Buffer_ID, LocationX, LocationY)
VALUES(myGrid_ID, myCell_ID, myBuffer_ID, X, Y);

END//
DELIMITER ;

-- 프로시저 lghpdb.createCell 구조 내보내기
DELIMITER //
CREATE PROCEDURE `createCell`(
	IN `myGrid_ID` VARCHAR(50),
	IN `myCell_ID` VARCHAR(50),
	IN `myLocationX` INT,
	IN `myLocationY` INT
)
    COMMENT '1개의 셀 정보 생성 프로시저'
BEGIN
INSERT INTO cell(Grid_id, Cell_ID, LocationX, LocationY)
VALUES(myGrid_ID, myCell_ID, myLocationX, myLocationY);
END//
DELIMITER ;

-- 프로시저 lghpdb.createChute 구조 내보내기
DELIMITER //
CREATE PROCEDURE `createChute`(
	IN `myGrid_ID` VARCHAR(50),
	IN `myCell_ID` VARCHAR(50),
	IN `myChute_ID` VARCHAR(50),
	IN `myRobotDirection` INT,
	IN `MyMaxCnt` INT
)
    COMMENT '슈트생성 프로시저'
BEGIN

DECLARE X INT;
DECLARE Y INT;
SELECT cell.LocationX INTO X
FROM cell
WHERE cell.Cell_ID = myCell_ID;
SELECT cell.LocationY INTO Y
FROM cell
WHERE cell.Cell_ID = myCell_ID;

INSERT INTO Chute(Grid_ID, Cell_ID, Chute_ID, RobotDirection, LocationX, LocationY, MaxCnt)
VALUES(myGrid_ID, myCell_ID, myChute_ID, myRobotDirection, X, Y, myMaxCnt);

END//
DELIMITER ;

-- 프로시저 lghpdb.createCS 구조 내보내기
DELIMITER //
CREATE PROCEDURE `createCS`(
	IN `myGrid_ID` VARCHAR(50),
	IN `myCell_ID` VARCHAR(50),
	IN `myCS_ID` VARCHAR(50),
	IN `myRobotDirection` INT
)
    COMMENT 'CS 셀 생성 프로시저'
BEGIN

DECLARE X INT;
DECLARE Y INT;
SELECT cell.LocationX INTO X
FROM cell
WHERE cell.Cell_ID = myCell_ID;
SELECT cell.LocationY INTO Y
FROM cell
WHERE cell.Cell_ID = myCell_ID;

INSERT INTO chargingstation(Grid_ID, Cell_ID, CS_ID, RobotDirection, LocationX, LocationY)
VALUES(myGrid_ID, myCell_ID, myCS_ID, myRobotDirection, X, Y);

END//
DELIMITER ;

-- 프로시저 lghpdb.createGrid 구조 내보내기
DELIMITER //
CREATE PROCEDURE `createGrid`(
	IN `myGrid_ID` VARCHAR(50),
	IN `myGridSizeX` INT,
	IN `myGridSizeY` INT,
	IN `myCellWidth` INT,
	IN `myCellHeight` INT
)
BEGIN
INSERT INTO grid(Grid_ID, GridSizeX, GridSizeY, CellWidth, CellHeight)
VALUES(myGrid_ID, myGridSizeX, myGridSizeY, myCellWidth, myCellHeight);

UPDATE grid
SET TotalCellCnt = myGridSizeX * myGridSizeY
WHERE Grid_ID = myGrid_ID;
END//
DELIMITER ;

-- 프로시저 lghpdb.createProject 구조 내보내기
DELIMITER //
CREATE PROCEDURE `createProject`(
	IN `myProject_ID` VARCHAR(50),
	IN `myDistributor` VARCHAR(50),
	IN `myCustomer` VARCHAR(50),
	IN `myCenterName` VARCHAR(50)
)
    COMMENT '프로젝트 정보 삽입 프로시저'
BEGIN
INSERT INTO project(Project_ID, Distributor, Customer, CenterName)
VALUES(myProject_ID, myDistributor, myCustomer, myCenterName);
END//
DELIMITER ;

-- 프로시저 lghpdb.createResult 구조 내보내기
DELIMITER //
CREATE PROCEDURE `createResult`(
	IN `mySimul_ID` CHAR(50)
)
    COMMENT 'run페이지에서 확인버튼 누를 때'
BEGIN
INSERT INTO result(Simul_ID)
VALUES(mySimul_ID);
END//
DELIMITER ;

-- 프로시저 lghpdb.createRobot 구조 내보내기
DELIMITER //
CREATE PROCEDURE `createRobot`(
	IN `mySimul_ID` VARCHAR(50),
	IN `myWS_ID` VARCHAR(50),
	IN `myRobot_ID` VARCHAR(50),
	IN `myRobotType` INT
)
    COMMENT '로봇 생성 프로시저'
BEGIN

DECLARE X INT;
DECLARE Y INT;

SELECT workstation.LocationX INTO X
FROM workstation
WHERE workstation.WS_ID = myWS_ID && workstation.Simul_ID = mySimul_ID;

SELECT workstation.LocationY INTO Y
FROM workstation
WHERE workstation.WS_ID = myWS_ID && workstation.Simul_ID = mySimul_ID;

INSERT robot(Simul_ID, Robot_ID, RobotType, LocationX, LocationY, Robot_Status)
VALUES(mySimul_ID, myRobot_ID, myRobotType, X, Y, 1);

UPDATE cell
SET Robot_ID = myRobot_ID
WHERE Simul_ID = mySimul_ID && LocationX = X && LocationY = Y;

UPDATE workstation
SET Robot_ID = myRobot_ID
WHERE Simul_ID = mySimul_ID && LocationX = X && LocationY = Y;
END//
DELIMITER ;

-- 프로시저 lghpdb.createRun 구조 내보내기
DELIMITER //
CREATE PROCEDURE `createRun`(
	IN `mySimulID` VARCHAR(50),
	IN `myBeltCnt` INT,
	IN `myDumpCnt` INT,
	IN `mySimulSpeed` INT,
	IN `myTotalTask` INT
)
    COMMENT '시뮬레이션 설정 값 삽입 프로시저'
BEGIN
INSERT INTO run(Simul_ID, Belt_Robot_Cnt, Dump_Robot_Cnt, SimulSpeed, TotalTask)
VALUES(mySimulID, myBeltCnt, myDumpCnt, mySimulSpeed, myTotalTask);
END//
DELIMITER ;

-- 프로시저 lghpdb.createService 구조 내보내기
DELIMITER //
CREATE PROCEDURE `createService`(
	IN `myCell_ID` VARCHAR(50),
	IN `myService_ID` VARCHAR(50)
)
    COMMENT '서비스셀 생성 프로시저'
BEGIN

DECLARE X INT;
DECLARE Y INT;
SELECT cell.LocationX INTO X
FROM cell
WHERE cell.Cell_ID = myCell_ID;
SELECT cell.LocationY INTO Y
FROM cell
WHERE cell.Cell_ID = myCell_ID;

INSERT INTO service(Cell_ID, Service_ID, LocationX, LocationY)
VALUES(myCell_ID, myService_ID, X, Y);

END//
DELIMITER ;

-- 프로시저 lghpdb.createSimul 구조 내보내기
DELIMITER //
CREATE PROCEDURE `createSimul`(
	IN `myProject_ID` CHAR(50),
	IN `mySimul_ID` VARCHAR(50)
)
    COMMENT '시뮬레이션 생성 프로시저'
BEGIN
INSERT INTO simulation(Project_ID, Simul_ID, Simul_Status)
VALUES(myProject_ID, mySimul_ID, 1);
END//
DELIMITER ;

-- 프로시저 lghpdb.createWS 구조 내보내기
DELIMITER //
CREATE PROCEDURE `createWS`(
	IN `myGrid_ID` VARCHAR(50),
	IN `myCell_ID` VARCHAR(50),
	IN `myWS_ID` VARCHAR(50),
	IN `myRobotDirection` INT
)
    COMMENT '워크스테이션 생성 프로시저'
BEGIN

DECLARE X INT;
DECLARE Y INT;
SELECT cell.LocationX INTO X
FROM cell
WHERE cell.Cell_ID = myCell_ID;
SELECT cell.LocationY INTO Y
FROM cell
WHERE cell.Cell_ID = myCell_ID;

INSERT INTO workstation(Grid_ID, Cell_ID, WS_ID, RobotDirection, LocationX, LocationY)
VALUES(myGrid_ID, myCell_ID, myWS_ID, myRobotDirection, X, Y);

END//
DELIMITER ;

-- 프로시저 lghpdb.deleteCell 구조 내보내기
DELIMITER //
CREATE PROCEDURE `deleteCell`(
	IN `mySimul_ID` VARCHAR(50),
	IN `myCell_ID` VARCHAR(50)
)
    COMMENT '셀정보 삭제 프로시저'
BEGIN
DELETE FROM chargingstation
WHERE Simul_ID = mySimul_ID && Cell_ID = myCell_ID;

DELETE FROM workstation
WHERE Simul_ID = mySimul_ID && Cell_ID = myCell_ID;

DELETE FROM buffer
WHERE Simul_ID = mySimul_ID && Cell_ID = myCell_ID;

DELETE FROM chute
WHERE Simul_ID = mySimul_ID && Cell_ID = myCell_ID;

DELETE FROM service
WHERE Simul_ID = mySimul_ID && Cell_ID = myCell_ID;

DELETE FROM cell
WHERE Simul_ID = mySimul_ID && Cell_ID = myCell_ID;
END//
DELIMITER ;

-- 프로시저 lghpdb.deleteGrid 구조 내보내기
DELIMITER //
CREATE PROCEDURE `deleteGrid`(
	IN `myGrid_ID` VARCHAR(50)
)
    COMMENT '그리드 일괄삭제를 위한 프로시저'
BEGIN
DELETE FROM grid
WHERE Grid_ID = myGrid_ID;
END//
DELIMITER ;

-- 프로시저 lghpdb.deleteProject 구조 내보내기
DELIMITER //
CREATE PROCEDURE `deleteProject`(
	IN `myproject_ID` VARCHAR(50)
)
    COMMENT '프로젝트삭제 프로시저'
BEGIN
DELETE FROM project
WHERE project_ID = myproject_ID;
END//
DELIMITER ;

-- 프로시저 lghpdb.deleteSimulation 구조 내보내기
DELIMITER //
CREATE PROCEDURE `deleteSimulation`(
	IN `mySimul_ID` VARCHAR(50)
)
    COMMENT '시뮬레이션 삭제 프로시저'
BEGIN
DELETE FROM simulation
WHERE Simul_ID = mySimul_ID;
END//
DELIMITER ;

-- 테이블 lghpdb.grid 구조 내보내기
CREATE TABLE IF NOT EXISTS `grid` (
  `Grid_ID` char(10) NOT NULL,
  `GridSizeX` int(11) DEFAULT NULL,
  `GridSizeY` int(11) DEFAULT NULL,
  `CellWidth` int(11) DEFAULT NULL,
  `CellHeight` int(11) DEFAULT NULL,
  `TotalCellCnt` int(11) DEFAULT NULL,
  `CS_Cnt` int(11) DEFAULT NULL,
  `Chute_Cnt` int(11) DEFAULT NULL,
  `WS_Cnt` int(11) DEFAULT NULL,
  `Buffer_Cnt` int(11) DEFAULT NULL,
  `Block_Cnt` int(11) DEFAULT NULL,
  `Service_Cnt` int(11) DEFAULT NULL,
  `CS_Color` int(11) DEFAULT NULL,
  `Chute_Color` int(11) DEFAULT NULL,
  `WS_Color` int(11) DEFAULT NULL,
  `Buffer_Color` int(11) DEFAULT NULL,
  `Block_Color` int(11) DEFAULT NULL,
  `Service_Color` int(11) DEFAULT NULL,
  PRIMARY KEY (`Grid_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- 테이블 데이터 lghpdb.grid:~1 rows (대략적) 내보내기
/*!40000 ALTER TABLE `grid` DISABLE KEYS */;
/*!40000 ALTER TABLE `grid` ENABLE KEYS */;

-- 테이블 lghpdb.project 구조 내보내기
CREATE TABLE IF NOT EXISTS `project` (
  `Project_ID` char(10) NOT NULL DEFAULT '',
  `Distributor` varchar(50) DEFAULT NULL,
  `Customer` varchar(50) DEFAULT NULL,
  `CenterName` varchar(50) DEFAULT NULL,
  `running` int(11) DEFAULT 0,
  PRIMARY KEY (`Project_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='프로젝트 정보를 담은 테이블';

-- 테이블 데이터 lghpdb.project:~1 rows (대략적) 내보내기
/*!40000 ALTER TABLE `project` DISABLE KEYS */;
/*!40000 ALTER TABLE `project` ENABLE KEYS */;

-- 테이블 lghpdb.result 구조 내보내기
CREATE TABLE IF NOT EXISTS `result` (
  `Simul_ID` char(10) NOT NULL,
  `TotalTime` time DEFAULT NULL,
  `BeltResult` int(11) DEFAULT NULL,
  `DumpResult` int(11) DEFAULT NULL,
  `TotalResult` int(11) DEFAULT NULL,
  `ErrorCnt` int(11) DEFAULT NULL,
  PRIMARY KEY (`Simul_ID`),
  CONSTRAINT `FK_result_Simul_ID` FOREIGN KEY (`Simul_ID`) REFERENCES `simulation` (`Simul_ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- 테이블 데이터 lghpdb.result:~0 rows (대략적) 내보내기
/*!40000 ALTER TABLE `result` DISABLE KEYS */;
/*!40000 ALTER TABLE `result` ENABLE KEYS */;

-- 테이블 lghpdb.robot 구조 내보내기
CREATE TABLE IF NOT EXISTS `robot` (
  `Robot_ID` char(10) NOT NULL,
  `Simul_ID` char(10) DEFAULT NULL,
  `RobotType` int(11) DEFAULT NULL,
  `LocationX` int(11) DEFAULT NULL,
  `LocationY` int(11) DEFAULT NULL,
  `Robot_Status` int(11) DEFAULT NULL,
  `Logistics_Result` int(11) DEFAULT NULL,
  `Direction` int(11) DEFAULT NULL,
  `RobotSpeed` int(11) DEFAULT NULL,
  `Battery` int(11) DEFAULT NULL,
  PRIMARY KEY (`Robot_ID`),
  KEY `FK_robot_Simul_ID` (`Simul_ID`),
  CONSTRAINT `FK_robot_Simul_ID` FOREIGN KEY (`Simul_ID`) REFERENCES `simulation` (`Simul_ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- 테이블 데이터 lghpdb.robot:~0 rows (대략적) 내보내기
/*!40000 ALTER TABLE `robot` DISABLE KEYS */;
/*!40000 ALTER TABLE `robot` ENABLE KEYS */;

-- 테이블 lghpdb.run 구조 내보내기
CREATE TABLE IF NOT EXISTS `run` (
  `Simul_ID` char(10) NOT NULL,
  `Belt_Robot_Cnt` int(11) DEFAULT NULL,
  `Dump_Robot_Cnt` int(11) DEFAULT NULL,
  `SimulSpeed` int(11) DEFAULT NULL,
  `TotalTask` int(11) DEFAULT NULL,
  PRIMARY KEY (`Simul_ID`),
  CONSTRAINT `FK_run_Simul_ID` FOREIGN KEY (`Simul_ID`) REFERENCES `simulation` (`Simul_ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='시뮬레이션 설정';

-- 테이블 데이터 lghpdb.run:~0 rows (대략적) 내보내기
/*!40000 ALTER TABLE `run` DISABLE KEYS */;
/*!40000 ALTER TABLE `run` ENABLE KEYS */;

-- 테이블 lghpdb.service 구조 내보내기
CREATE TABLE IF NOT EXISTS `service` (
  `Service_ID` char(30) NOT NULL DEFAULT '',
  `Cell_ID` char(30) DEFAULT NULL,
  `LocationX` int(11) DEFAULT NULL,
  `LocationY` int(11) DEFAULT NULL,
  `Service_Status` int(11) DEFAULT 0,
  PRIMARY KEY (`Service_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- 테이블 데이터 lghpdb.service:~0 rows (대략적) 내보내기
/*!40000 ALTER TABLE `service` DISABLE KEYS */;
/*!40000 ALTER TABLE `service` ENABLE KEYS */;

-- 테이블 lghpdb.simulation 구조 내보내기
CREATE TABLE IF NOT EXISTS `simulation` (
  `Simul_ID` char(10) NOT NULL DEFAULT '',
  `Grid_ID` char(30) DEFAULT NULL,
  `Simul_Status` int(1) DEFAULT NULL,
  `Duration` time DEFAULT NULL,
  `Remaining` time DEFAULT NULL,
  `Progress` char(50) DEFAULT NULL,
  `Project_ID` char(10) DEFAULT NULL,
  PRIMARY KEY (`Simul_ID`),
  KEY `FK_simulation_Project_ID` (`Project_ID`),
  KEY `FK_simulation_Grid_ID` (`Grid_ID`),
  CONSTRAINT `FK_simulation_Grid_ID` FOREIGN KEY (`Grid_ID`) REFERENCES `grid` (`Grid_ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK_simulation_Project_ID` FOREIGN KEY (`Project_ID`) REFERENCES `project` (`Project_ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='시뮬레이션 정보를 담은 테이블';

-- 테이블 데이터 lghpdb.simulation:~1 rows (대략적) 내보내기
/*!40000 ALTER TABLE `simulation` DISABLE KEYS */;
/*!40000 ALTER TABLE `simulation` ENABLE KEYS */;

-- 프로시저 lghpdb.updateBufferName 구조 내보내기
DELIMITER //
CREATE PROCEDURE `updateBufferName`(
	IN `myOldBuffer_ID` VARCHAR(50),
	IN `myNewBuffer_ID` VARCHAR(50)
)
    COMMENT '버터이름 업데이트 프로시저'
BEGIN
UPDATE buffer
SET Buffer_ID = myNewBuffer_ID
WHERE Buffer_ID = myOldBuffer_ID;
END//
DELIMITER ;

-- 프로시저 lghpdb.updateCellCnt 구조 내보내기
DELIMITER //
CREATE PROCEDURE `updateCellCnt`(
	IN `myGrid_ID` VARCHAR(50),
	IN `myCS_Cnt` INT,
	IN `myChute_Cnt` INT,
	IN `myWS_Cnt` INT,
	IN `myBuffer_Cnt` INT,
	IN `myBlock_Cnt` INT
)
    COMMENT '그리드 테이블의 셀 개수 업데이트 프로시저'
BEGIN
UPDATE grid
SET CS_Cnt = myCS_Cnt,
WS_Cnt = myWS_Cnt,
Chute_Cnt = myChute_Cnt,
Block_Cnt = myBlock_Cnt,
Buffer_Cnt = myBuffer_Cnt,
Service_Cnt = 0
WHERE Grid_ID = myGrid_ID;
END//
DELIMITER ;

-- 프로시저 lghpdb.updateCellDirection 구조 내보내기
DELIMITER //
CREATE PROCEDURE `updateCellDirection`(
	IN `myCell_ID` VARCHAR(50),
	IN `myND` INT,
	IN `mySD` INT,
	IN `myWD` INT,
	IN `myED` INT
)
    COMMENT '셀의 이동방향 업데이트 프로시저'
BEGIN
UPDATE cell
SET NorthDirection = myND,
SouthDirection = mySD,
WestDirection = myWD,
EastDirection = myED
WHERE Cell_ID = myCell_ID;
END//
DELIMITER ;

-- 프로시저 lghpdb.updateCellName 구조 내보내기
DELIMITER //
CREATE PROCEDURE `updateCellName`(
	IN `myOldCell_ID` CHAR(50),
	IN `myNewCell_ID` CHAR(50)
)
    COMMENT '셀이름 업데이트 프로시저'
BEGIN
UPDATE cell
SET Cell_ID = myNewCell_ID
WHERE Cell_ID = myOldCell_ID;
END//
DELIMITER ;

-- 프로시저 lghpdb.updateCellStatus 구조 내보내기
DELIMITER //
CREATE PROCEDURE `updateCellStatus`(
	IN `myGrid_ID` VARCHAR(50),
	IN `myCell_ID` VARCHAR(50),
	IN `myStatus` INT
)
    COMMENT '셀의 상태, 색상 업데이트'
BEGIN
DECLARE cell_color INT;
SET cell_color = 0;

SET cell_color =
case  
	when (myStatus = 1) then (SELECT G.CS_Color 
										FROM grid as G
										WHERE G.Grid_ID = myGrid_ID)
	when (myStatus = 2) then (SELECT G.Chute_Color 
										FROM grid as G
										WHERE G.Grid_ID = myGrid_ID)
	when (myStatus = 3) then (SELECT G.WS_Color 
										FROM grid AS G
										WHERE G.Grid_ID = myGrid_ID)
	when (myStatus = 4) then (SELECT G.Buffer_Color 
										FROM grid as G
										WHERE G.Grid_ID = myGrid_ID)
	when (myStatus = 5) then (SELECT G.Block_Color 
										FROM grid as G
										WHERE G.Grid_ID = myGrid_ID)	
	when (myStatus = 7) then (SELECT G.Service_Color 
										FROM grid as G
										WHERE G.Grid_ID = myGrid_ID)	
END; 

UPDATE cell
SET Color = cell_color,
CellStatus = myStatus
WHERE Cell_ID = myCell_ID;
END//
DELIMITER ;

-- 프로시저 lghpdb.updateCHName 구조 내보내기
DELIMITER //
CREATE PROCEDURE `updateCHName`(
	IN `myOldChute_ID` CHAR(50),
	IN `myNewChute_ID` CHAR(50)
)
    COMMENT '슈트이름 업데이트 프로시저'
BEGIN
UPDATE chute
SET Chute_ID = myNewChute_ID
WHERE Chute_ID = myOldChute_ID;
END//
DELIMITER ;

-- 프로시저 lghpdb.updateCSName 구조 내보내기
DELIMITER //
CREATE PROCEDURE `updateCSName`(
	IN `myOldCS_ID` VARCHAR(50),
	IN `myNewCS_ID` VARCHAR(50)
)
    COMMENT 'CS이름 업데이트 프로시저'
BEGIN
UPDATE chargingstation
SET CS_ID = myNewCS_ID
WHERE CS_ID = myOldCS_ID;
END//
DELIMITER ;

-- 프로시저 lghpdb.updateGridColor 구조 내보내기
DELIMITER //
CREATE PROCEDURE `updateGridColor`(
	IN `myGrid_ID` VARCHAR(50),
	IN `myCS_Color` INT,
	IN `myChute_Color` INT,
	IN `myWS_Color` INT,
	IN `myBuffer_Color` INT,
	IN `myBlock_Color` INT
)
    COMMENT '그리드 테이블 안의 셀 색상 업데이트 프로시저'
BEGIN
UPDATE grid
SET CS_Color = myCS_Color,
WS_Color = myWS_Color,
Chute_Color = myChute_Color,
Block_Color = myBlock_Color,
Buffer_Color = myBuffer_Color,
Service_Color = 9
WHERE Grid_ID = myGrid_ID;
END//
DELIMITER ;

-- 프로시저 lghpdb.updateGridName 구조 내보내기
DELIMITER //
CREATE PROCEDURE `updateGridName`(
	IN `mySimul_ID` CHAR(50),
	IN `myGrid_ID` CHAR(50)
)
    COMMENT '그리드 이름 업데이트 프로시저'
BEGIN
UPDATE grid
SET Grid_ID = myGrid_ID,
Simul_ID = mySimul_ID
WHERE Simul_ID = mySimul_ID;
END//
DELIMITER ;

-- 프로시저 lghpdb.updateGridSize 구조 내보내기
DELIMITER //
CREATE PROCEDURE `updateGridSize`(
	IN `mySimul_ID` VARCHAR(50),
	IN `myGrid_ID` VARCHAR(50),
	IN `myGridSizeX` INT,
	IN `myGridSizeY` INT
)
    COMMENT '그리드사이즈 업데이트 프로시저'
BEGIN
UPDATE grid
SET GridSizeX = myGridSizeX,
GridSizeY = myGridSizeY,
TotalCellCnt = myGridSizeX * myGridSizeY
WHERE Simul_iD = mySimul_ID && Grid_ID = myGrid_ID;
END//
DELIMITER ;

-- 프로시저 lghpdb.updateGridtoSimul 구조 내보내기
DELIMITER //
CREATE PROCEDURE `updateGridtoSimul`(
	IN `mySimul_ID` VARCHAR(50),
	IN `myGrid_ID` VARCHAR(50)
)
    COMMENT '시뮬레이션 테이블에 그리드id 연결하는 프로시저'
BEGIN
UPDATE simulation
SET Grid_ID = myGrid_ID
WHERE Simul_ID = mySimul_ID;
END//
DELIMITER ;

-- 프로시저 lghpdb.updateProject 구조 내보내기
DELIMITER //
CREATE PROCEDURE `updateProject`(
	IN `OldProject_ID` VARCHAR(50),
	IN `NewProject_ID` VARCHAR(50),
	IN `myDistributor` VARCHAR(50),
	IN `myCustomer` VARCHAR(50),
	IN `myCenterName` VARCHAR(50)
)
    COMMENT '프로젝트 정보 입력 프로시저'
BEGIN
UPDATE project
SET Project_ID = NewProject_ID,
Distributor = myDistributor,
Customer = myCustomer,
CenterName = myCenterName
WHERE Project_ID = OldProject_ID;
END//
DELIMITER ;

-- 프로시저 lghpdb.updateProjectRunning 구조 내보내기
DELIMITER //
CREATE PROCEDURE `updateProjectRunning`(
	IN `myrunning` INT,
	IN `myProject_ID` VARCHAR(50)
)
    COMMENT '현재 사용중인 프로젝트 상태 업데이트 프로시저'
BEGIN
UPDATE project
SET running = myrunning
WHERE Project_ID = myProject_ID;
END//
DELIMITER ;

-- 프로시저 lghpdb.updateResult 구조 내보내기
DELIMITER //
CREATE PROCEDURE `updateResult`(
	IN `mySimul_ID` CHAR(50),
	IN `myTotalTime` TIME,
	IN `myBeltResult` INT,
	IN `myDumpResult` INT,
	IN `myErrorCnt` INT
)
    COMMENT '시뮬레이션 끝난 후 그 결과 값 업데이트'
BEGIN
UPDATE result
SET TotalTime = myTotalTime,
BeltResult = myBeltResult,
DumpResult = myDumpResult,
TotalResult = BeltResult + DumpResult,
ErrorCnt = myErrorCnt
WHERE Simul_ID = mySimul_ID;
END//
DELIMITER ;

-- 프로시저 lghpdb.updateRobot 구조 내보내기
DELIMITER //
CREATE PROCEDURE `updateRobot`(
	IN `mySimul_ID` VARCHAR(50),
	IN `myRobot_ID` VARCHAR(50),
	IN `X` INT,
	IN `Y` INT
)
    COMMENT '로봇 좌표, 방향수정, 상태 프로시저'
BEGIN
DECLARE RD INT;
DECLARE RS INT;
DECLARE Cell_Status INT;
DECLARE myLocationX INT;
DECLARE myLocationY INT;
SET myLocationX = 0;
SET myLocationY = 0;
SET myLocationX = (SELECT R.LocationX
								FROM robot AS R
								WHERE R.Simul_ID = mySimul_ID && R.Robot_ID = myRobot_ID) + (X);
SET myLocationY = (SELECT R.LocationY
								FROM robot AS R
								WHERE R.Simul_ID = mySimul_ID && R.Robot_ID = myRobot_ID) + (Y);
SET RD = 0;
SET RS = 2;
SET Cell_Status = (SELECT C.CellStatus
							FROM cell AS C
							WHERE C.Simul_ID = mySimul_ID && LocationX = myLocationX - X && LocationY = myLocationY - Y);

SET RD =
case  
	when (myLocationY > (SELECT R.LocationY
								FROM robot AS R
								WHERE R.Simul_ID = mySimul_ID && R.Robot_ID = myRobot_ID)) then 0 -- NORTH
	when (myLocationX > (SELECT R.LocationX
								FROM robot AS R
								WHERE R.Simul_ID = mySimul_ID && R.Robot_ID = myRobot_ID)) then 1 -- EAST
	when (myLocationY < (SELECT R.LocationY
								FROM robot AS R
								WHERE R.Simul_ID = mySimul_ID && R.Robot_ID = myRobot_ID)) then 2 -- SOUTH
	when (myLocationX < (SELECT R.LocationX
								FROM robot AS R
								WHERE R.Simul_ID = mySimul_ID && R.Robot_ID = myRobot_ID)) then 3	-- WEST
END;

SET RS = 
case  
	when (myLocationX = (SELECT CS.LocationX
								FROM chargingstation AS CS
								WHERE CS.Simul_ID = mySimul_ID) &&
			myLocationY = (SELECT CS.LocationY
								FROM chargingstation AS CS
								WHERE CS.Simul_ID = mySimul_ID)) then 3
	ELSE 2
END;

UPDATE cell
SET CellStatus = 
case
	when (LocationX = (SELECT CS.LocationX
								FROM chargingstation AS CS
								WHERE CS.Simul_ID = mySimul_ID && Robot_ID = myRobot_ID) &&
			LocationY = (SELECT CS.LocationY
								FROM chargingstation AS CS
								WHERE CS.Simul_ID = mySimul_ID && Robot_ID = myRobot_ID)) then 1
	when (LocationX = (SELECT WS.LocationX
								FROM workstation AS WS
								WHERE WS.Simul_ID = mySimul_ID && Robot_ID = myRobot_ID) &&
			LocationY = (SELECT WS.LocationY
								FROM workstation AS WS
								WHERE WS.Simul_ID = mySimul_ID && Robot_ID = myRobot_ID)) then 3
	ELSE 7
END,
Robot_ID = NULL
WHERE Simul_ID = mySimul_ID && Robot_ID = myRobot_ID;

UPDATE cell
SET Robot_ID = myRobot_ID,
CellStatus = 6
WHERE Simul_ID = mySimul_ID && LocationX = myLocationX && LocationY = myLocationY;

UPDATE chargingstation
SET Robot_ID = NULL,
CS_Status = 1
WHERE Simul_ID = mySimul_ID && Robot_ID = myRobot_ID;

UPDATE chargingstation
SET Robot_ID = myRobot_ID,
CS_Status = 0
WHERE Simul_ID = mySimul_ID && LocationX = myLocationX && LocationY = myLocationY;

UPDATE workstation
SET Robot_ID = NULL,
WS_Status = 1
WHERE Simul_ID = mySimul_ID && Robot_ID = myRobot_ID;

UPDATE workstation
SET Robot_ID = myRobot_ID,
WS_Status = 0
WHERE Simul_ID = mySimul_ID && LocationX = myLocationX && LocationY = myLocationY;


UPDATE robot
SET LocationX = myLocationX,
LocationY = myLocationY,
Direction = RD,
Robot_Status = RS
WHERE Simul_ID = mySimul_ID && Robot_ID = myRobot_ID;
END//
DELIMITER ;

-- 프로시저 lghpdb.updateSimul 구조 내보내기
DELIMITER //
CREATE PROCEDURE `updateSimul`(
	IN `mySimul_ID` VARCHAR(50)
)
    COMMENT '시뮬레이션 상태 업데이트'
BEGIN
UPDATE simulation
SET Simul_Status = -1 * Simul_Status
WHERE Simul_ID = mySimul_ID;
END//
DELIMITER ;

-- 프로시저 lghpdb.updateSimulName 구조 내보내기
DELIMITER //
CREATE PROCEDURE `updateSimulName`(
	IN `OldSimul_ID` VARCHAR(50),
	IN `NewSimul_ID` VARCHAR(50)
)
    COMMENT '시뮬 이름 업데이트 프로시저'
BEGIN
UPDATE simulation
SET Simul_ID = NewSimul_ID
WHERE Simul_ID = OldSimul_ID;
END//
DELIMITER ;

-- 프로시저 lghpdb.updateSimultoGrid 구조 내보내기
DELIMITER //
CREATE PROCEDURE `updateSimultoGrid`(
	IN `myGrid_ID` VARCHAR(50),
	IN `mySimul_ID` VARCHAR(50)
)
    COMMENT '파일가져오기 시 그리드 테이블에 시뮬id 업데이트 프로시저'
BEGIN
UPDATE grid
SET Grid_ID = myGrid_ID,
Simul_ID = mySimul_ID
WHERE Grid_ID = myGrid_ID;
END//
DELIMITER ;

-- 프로시저 lghpdb.updateWSName 구조 내보내기
DELIMITER //
CREATE PROCEDURE `updateWSName`(
	IN `myOldWS_ID` VARCHAR(50),
	IN `myNewWS_ID` VARCHAR(50)
)
    COMMENT 'WS이름 업데이트 프로시저'
BEGIN
UPDATE Workstation
SET WS_ID = myNewWS_ID
WHERE WS_ID = myOldWS_ID;
END//
DELIMITER ;

-- 테이블 lghpdb.workstation 구조 내보내기
CREATE TABLE IF NOT EXISTS `workstation` (
  `WS_ID` char(30) NOT NULL DEFAULT '',
  `Cell_ID` char(30) DEFAULT NULL,
  `Grid_ID` char(10) DEFAULT NULL,
  `LocationX` int(11) DEFAULT NULL,
  `LocationY` int(11) DEFAULT NULL,
  `WS_Status` int(11) DEFAULT 1,
  `RobotDirection` int(11) DEFAULT NULL,
  `Robot_ID` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`WS_ID`),
  KEY `FK_workstation_Grid_ID` (`Grid_ID`),
  KEY `FK_workstation_Cell_ID` (`Cell_ID`),
  CONSTRAINT `FK_workstation_Cell_ID` FOREIGN KEY (`Cell_ID`) REFERENCES `cell` (`Cell_ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK_workstation_Grid_ID` FOREIGN KEY (`Grid_ID`) REFERENCES `grid` (`Grid_ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- 테이블 데이터 lghpdb.workstation:~2 rows (대략적) 내보내기
/*!40000 ALTER TABLE `workstation` DISABLE KEYS */;
/*!40000 ALTER TABLE `workstation` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
